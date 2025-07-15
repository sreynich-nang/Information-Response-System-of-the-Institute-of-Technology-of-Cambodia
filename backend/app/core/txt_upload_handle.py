import os
from pathlib import Path
from typing import Optional
import re

from app.config import DATA_DIR
from app.core.document_loader import update_document_status
from app.api.schemas import DocumentMetadata, DocumentStatus

# Path for processed documents
PROCESSED_DIR = DATA_DIR / "processed"


def process_txt(doc_metadata: DocumentMetadata) -> Optional[Path]:
    """
    Process a text file:
    1. Read the text file
    2. Clean the text
    3. Save to processed directory
    """
    try:
        # Open the text file
        txt_path = Path(doc_metadata.original_path)
        if not txt_path.exists():
            raise FileNotFoundError(f"Text file not found: {txt_path}")

        # Read text file
        with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
            text_content = f.read()

        # Clean the text
        cleaned_text = clean_txt_text(text_content)
        
        # Save processed text
        processed_path = PROCESSED_DIR / f"{doc_metadata.document_id}.txt"
        with open(processed_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        
        # Update document status
        update_document_status(
            document_id=doc_metadata.document_id,
            status=DocumentStatus.PROCESSED,
            processed_path=str(processed_path)
        )
        
        return processed_path
    
    except Exception as e:
        print(f"Error processing text file {doc_metadata.filename}: {str(e)}")
        update_document_status(
            document_id=doc_metadata.document_id,
            status=DocumentStatus.FAILED
        )
        return None


def clean_txt_text(text: str) -> str:
    """Clean text from a text file"""
    # Replace non-breaking spaces with regular spaces
    cleaned = text.replace("\xa0", " ")
    
    # Remove control characters
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
    
    # Remove excessive whitespace
    cleaned = re.sub(r' {2,}', ' ', cleaned)
    
    # Replace multiple newlines with double newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Remove very short lines (potentially headers or page numbers)
    lines = cleaned.split('\n')
    filtered_lines = [line for line in lines if len(line.strip()) > 3 or not line.strip()]
    
    return '\n'.join(filtered_lines)