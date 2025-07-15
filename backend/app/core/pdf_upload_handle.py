## This is just a sample code, not the code for processing, extracting and cleaning with the complex table i have uploaded (be responsible with your inputted data) :D

from pathlib import Path
from typing import Optional
import fitz 

from app.config import DATA_DIR
from app.core.document_loader import update_document_status
from app.api.schemas import DocumentMetadata, DocumentStatus

# Path for processed documents
PROCESSED_DIR = DATA_DIR / "processed"


def process_pdf(doc_metadata: DocumentMetadata) -> Optional[Path]:
    """
    Process a PDF file:
    1. Extract text from PDF
    2. Clean the extracted text
    3. Save to processed directory
    """
    try:
        # Open the PDF file
        pdf_path = Path(doc_metadata.original_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Extract text from PDF
        extracted_text = ""
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                extracted_text += page.get_text()
                # Add page separator
                extracted_text += f"\n\n[PAGE {page_num + 1}]\n\n"

        # Clean the text
        cleaned_text = clean_pdf_text(extracted_text)
        
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
        print(f"Error processing PDF {doc_metadata.filename}: {str(e)}")
        update_document_status(
            document_id=doc_metadata.document_id,
            status=DocumentStatus.FAILED
        )
        return None


def clean_pdf_text(text: str) -> str:
    """Clean text extracted from PDF"""
    # Remove excessive whitespace
    cleaned = " ".join(text.split())
    
    # Replace multiple newlines with double newlines
    import re
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Fix common OCR errors and PDF artifacts
    cleaned = cleaned.replace("fi", "fi")  # Common ligature issue
    cleaned = cleaned.replace("fl", "fl")  # Common ligature issue
    
    # Remove headers/footers - this is a simplified approach
    # For production, you'd want more sophisticated header/footer detection
    lines = cleaned.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip page numbers and common headers/footers
        if re.match(r'^\d+$', line.strip()) or len(line.strip()) < 3:
            continue
        filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)