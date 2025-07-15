import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from app.config import DATA_DIR
from app.api.schemas import DocumentMetadata, DocumentStatus, DocumentType
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Paths for storing data
UPLOADED_DIR = DATA_DIR / "uploaded"
PROCESSED_DIR = DATA_DIR / "processed"
METADATA_FILE = DATA_DIR / "document_metadata.json"

# Ensure directories exist
UPLOADED_DIR.mkdir(exist_ok=True, parents=True)
PROCESSED_DIR.mkdir(exist_ok=True, parents=True)

# In document_loader.py
def process_document(document_id: str):
    metadata = get_document_metadata(document_id)
    if metadata.document_type == DocumentType.TXT:
        return process_txt_file(document_id)
    # Add other types (PDF, DOCX, etc.)
    else:
        raise ValueError(f"Unsupported type: {metadata.document_type}")

def calculate_file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of a file to detect changes"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_metadata() -> Dict[str, Any]:
    """Load document metadata from JSON file"""
    if not METADATA_FILE.exists():
        with open(METADATA_FILE, "w") as f:
            json.dump({"documents": {}}, f)
        return {"documents": {}}
    
    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def save_metadata(metadata: Dict[str, Any]) -> None:
    """Save document metadata to JSON file"""
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)


def get_document_metadata(document_id: str) -> Optional[DocumentMetadata]:
    """Get metadata for a specific document"""
    metadata_store = load_metadata()
    if document_id in metadata_store["documents"]:
        return DocumentMetadata(**metadata_store["documents"][document_id])
    return None


def save_document_metadata(doc_metadata: DocumentMetadata) -> None:
    """Save metadata for a document"""
    metadata_store = load_metadata()
    metadata_store["documents"][doc_metadata.document_id] = doc_metadata.dict()
    save_metadata(metadata_store)


def save_uploaded_file(file_content: bytes, filename: str) -> Path:
    """Save uploaded file to the uploads directory"""
    file_path = UPLOADED_DIR / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path


def get_document_type(filename: str) -> DocumentType:
    """Determine document type from filename"""
    extension = filename.lower().split(".")[-1]
    if extension == "pdf":
        return DocumentType.PDF
    elif extension == "txt":
        return DocumentType.TXT
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def create_document_record(filename: str, file_path: Path) -> DocumentMetadata:
    """Create a new document record with metadata"""
    document_id = str(uuid.uuid4())
    file_hash = calculate_file_hash(file_path)
    doc_type = get_document_type(filename)
    
    # Create metadata
    metadata = DocumentMetadata(
        filename=filename,
        document_id=document_id,
        original_path=str(file_path),
        processed_path="",  # Will be updated after processing
        file_hash=file_hash,
        document_type=doc_type,
        last_modified=datetime.now().timestamp(),
        embedding_status=DocumentStatus.RECEIVED
    )
    
    # Save metadata
    save_document_metadata(metadata)
    return metadata

def check_document_exists(file_path: Path, filename: str) -> Optional[DocumentMetadata]:
    """Check if document already exists with the same hash"""
    current_hash = calculate_file_hash(file_path)
    metadata_store = load_metadata()
    
    for doc_id, doc in metadata_store["documents"].items():
        if doc["filename"] == filename and doc["file_hash"] == current_hash:
            return DocumentMetadata(**doc)
    
    return None


def update_document_status(document_id: str, status: DocumentStatus, processed_path: Optional[str] = None, chunks: Optional[int] = None) -> None:
    """Update the status of a document in the metadata store"""
    metadata = get_document_metadata(document_id)
    if metadata:
        metadata.embedding_status = status
        metadata.last_modified = datetime.now().timestamp()
        
        if processed_path:
            metadata.processed_path = processed_path
            
        if chunks is not None:
            metadata.chunks = chunks
            
        save_document_metadata(metadata)


def get_documents_for_embedding() -> List[DocumentMetadata]:
    """Get all documents that need to be embedded (processed but not embedded)"""
    metadata_store = load_metadata()
    documents_to_embed = []
    
    for doc_id, doc in metadata_store["documents"].items():
        if doc["embedding_status"] == DocumentStatus.PROCESSED:
            documents_to_embed.append(DocumentMetadata(**doc))
            
    return documents_to_embed


def get_all_documents() -> List[DocumentMetadata]:
    """Get all documents in the metadata store"""
    metadata_store = load_metadata()
    return [DocumentMetadata(**doc) for doc in metadata_store["documents"].values()]

def process_txt_file(document_id: str) -> int:
    """
    Process a .txt document by splitting it into chunks using RecursiveCharacterTextSplitter.
    Returns the number of chunks.
    """
    metadata = get_document_metadata(document_id)
    if not metadata or metadata.document_type != DocumentType.TXT:
        raise ValueError("Invalid document or not a .txt file.")

    original_path = Path(metadata.original_path)

    with open(original_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Use RecursiveCharacterTextSplitter to chunk based on newline patterns
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = splitter.split_text(text)

    # Save processed file as one chunk per line (or however your vectorstore reads it)
    processed_dir = PROCESSED_DIR / document_id
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_path = processed_dir / "chunks.txt"

    with open(processed_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.strip() + "\n---\n")  # separate chunks with delimiter for debugging

    update_document_status(
        document_id=document_id,
        status=DocumentStatus.PROCESSED,
        processed_path=str(processed_path),
        chunks=len(chunks)
    )

    return len(chunks)