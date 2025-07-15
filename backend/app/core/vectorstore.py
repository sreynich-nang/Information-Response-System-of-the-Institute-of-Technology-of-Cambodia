import os
from pathlib import Path
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from app.core.text_loader import load_processed_text 

from app.config import CHROMA_DIR, COLLECTION_NAME
from app.models.embedding import get_embedding_model
from app.core.document_loader import update_document_status, get_document_metadata
from app.api.schemas import DocumentStatus

def get_vector_store():
    os.makedirs(CHROMA_DIR, exist_ok=True)
    embeddings = get_embedding_model()
    
    # Always return a fresh instance
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

def chunk_document(file_path: str, document_id: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Chunk a document into smaller pieces for embedding.

    Args:
        file_path: Path to the processed document
        document_id: Unique ID of the document
        chunk_size: Size of each chunk in characters
        chunk_overlap: Overlap between chunks in characters

    Returns:
        List of Document objects with text and metadata
    """
    # Load content from processed file
    raw_chunks = load_processed_text(Path(file_path))  # 👈 use loader

    # Join all content to a single string for splitting
    full_text = "\n\n".join(raw_chunks)  # optional depending on strategy

    # Get metadata
    doc_metadata = get_document_metadata(document_id)
    if not doc_metadata:
        raise ValueError(f"Document metadata not found for ID: {document_id}")

    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    # Split text into chunks
    split_chunks = text_splitter.split_text(full_text)

    # Wrap each chunk in a Document
    documents = []
    for i, chunk_text in enumerate(split_chunks):
        metadata = {
            "source": doc_metadata.filename,
            "document_id": document_id,
            "chunk_id": i,
            "chunk_index": i,
            "total_chunks": len(split_chunks)
        }
        documents.append(Document(page_content=chunk_text, metadata=metadata))

    return documents


def embed_document(document_id: str) -> bool:
    """
    Embed a document and store in ChromaDB
    
    Args:
        document_id: ID of the document to embed
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get document metadata
        doc_metadata = get_document_metadata(document_id)
        if not doc_metadata:
            raise ValueError(f"Document metadata not found for ID: {document_id}")
        
        # Check if document has been processed
        if doc_metadata.embedding_status != DocumentStatus.PROCESSED:
            print(f"Document {document_id} is not ready for embedding (status: {doc_metadata.embedding_status})")
            return False
        
        # Chunk the document
        documents = chunk_document(doc_metadata.processed_path, document_id)
        
        # Get vector store
        vectorstore = get_vector_store()
        
        # Add documents to vector store
        vectorstore.add_documents(documents)
        vectorstore.persist()
        
        # Update document status
        update_document_status(
            document_id=document_id,
            status=DocumentStatus.EMBEDDED,
            chunks=len(documents)
        )
        
        print(f"Successfully embedded document {doc_metadata.filename} with {len(documents)} chunks")
        return True
    
    except Exception as e:
        print(f"Error embedding document {document_id}: {str(e)}")
        update_document_status(document_id=document_id, status=DocumentStatus.FAILED)
        return False



def search_documents(query: str, k: int = 4) -> List[Document]:
    """
    Search for relevant documents based on a query
    
    Args:
        query: The search query
        k: Number of documents to retrieve
        
    Returns:
        List of relevant Document objects
    """
    vectorstore = get_vector_store()
    documents = vectorstore.similarity_search(query, k=k)
    return documents