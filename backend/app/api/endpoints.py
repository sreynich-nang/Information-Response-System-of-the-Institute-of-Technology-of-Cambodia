from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List, Optional
import traceback
import time

from app.core.document_loader import (
    save_uploaded_file,
    create_document_record,
    check_document_exists
)
from app.api.schemas import (
    DocumentResponse, 
    DocumentStatus, 
    MessageRequest, 
    MessageResponse,
    DocumentType,
    DocumentMetadata
)
from app.core.document_loader import (
    save_uploaded_file,
    create_document_record,
    check_document_exists,
    get_document_metadata,
    get_all_documents
)
from app.core.pdf_upload_handle import process_pdf
from app.core.txt_upload_handle import process_txt
from app.core.vectorstore import embed_document
from app.core.rag_chain import query_rag_chain

router = APIRouter()

def process_document_task(doc_metadata: DocumentMetadata):
    """Background task to process and embed a document"""
    # Process document based on type
    if doc_metadata.document_type == DocumentType.PDF:
        process_pdf(doc_metadata)
    elif doc_metadata.document_type == DocumentType.TXT:
        process_txt(doc_metadata)
    else:
        print(f"Unsupported document type: {doc_metadata.document_type}")
        return
    
    # Embed the document
    embed_document(doc_metadata.document_id)

@router.post("/upload", response_model=List[DocumentResponse])  # Return list of responses
async def upload_document(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)  # Accept multiple files
):
    """
    Upload multiple documents (.pdf or .txt) to be processed and embedded
    """
    responses = []
    
    for file in files:
        filename = file.filename
        file_extension = filename.split(".")[-1].lower()
        
        if file_extension not in ["pdf", "txt"]:
            responses.append(DocumentResponse(
                filename=filename,
                status=DocumentStatus.ERROR,
                message=f"Unsupported file type: {file_extension}",
                document_id=None
            ))
            continue
        
        try:
            file_content = await file.read()
            file_path = save_uploaded_file(file_content, filename)
            
            existing_doc = check_document_exists(file_path, filename)
            if existing_doc:
                responses.append(DocumentResponse(
                    filename=filename,
                    status=DocumentStatus.SKIPPED,
                    message="Document already exists",
                    document_id=existing_doc.document_id
                ))
                continue
            
            doc_metadata = create_document_record(filename, file_path)
            background_tasks.add_task(process_document_task, doc_metadata)
            
            responses.append(DocumentResponse(
                filename=filename,
                status=DocumentStatus.RECEIVED,
                message="Document received for processing",
                document_id=doc_metadata.document_id
            ))
            
        except Exception as e:
            responses.append(DocumentResponse(
                filename=filename,
                status=DocumentStatus.ERROR,
                message=f"Error processing document: {str(e)}",
                document_id=None
            ))
    
    return responses
# @router.post("/upload", response_model=DocumentResponse)
# async def upload_document(
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...)
# ):
#     """
#     Upload a document (.pdf or .txt) to be processed and embedded
#     """
#     # Check file type
#     filename = file.filename
#     file_extension = filename.split(".")[-1].lower()
    
#     if file_extension not in ["pdf", "txt"]:
#         raise HTTPException(
#             status_code=400, 
#             detail=f"Unsupported file type: {file_extension}. Only PDF and TXT files are supported."
#         )
    
#     try:
#         # Read file content
#         file_content = await file.read()
        
#         # Save file to uploads directory
#         file_path = save_uploaded_file(file_content, filename)
        
#         # Check if file already exists with the same hash
#         existing_doc = check_document_exists(file_path, filename)
#         if existing_doc:
#             return DocumentResponse(
#                 filename=filename,
#                 status=DocumentStatus.SKIPPED,
#                 message="Document already exists and has not changed.",
#                 document_id=existing_doc.document_id
#             )
        
#         # Create document record
#         doc_metadata = create_document_record(filename, file_path)
        
#         # Process document in background
#         background_tasks.add_task(process_document_task, doc_metadata)
        
#         return DocumentResponse(
#             filename=filename,
#             status=DocumentStatus.RECEIVED,
#             message="Document received and is being processed.",
#             document_id=doc_metadata.document_id
#         )
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/documents", response_model=List[DocumentMetadata])
async def get_documents():
    """
    Get all documents in the system
    """
    try:
        documents = get_all_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


@router.get("/document/{document_id}", response_model=Optional[DocumentMetadata])
async def get_document(document_id: str):
    """
    Get information about a specific document
    """
    try:
        document = get_document_metadata(document_id)
        if not document:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")


@router.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    Chat with the RAG system
    """
    try:
        start_time = time.time()
        
        answer, sources = query_rag_chain(request.query)
        
        response_time = time.time() - start_time
        
        return MessageResponse(
            answer=answer,
            response_time=response_time,
            sources=sources
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/reprocess/{document_id}", response_model=DocumentResponse)
async def reprocess_document(
    document_id: str,
    background_tasks: BackgroundTasks
):
    """
    Force reprocessing of a document
    """
    try:
        # Get document metadata
        doc_metadata = get_document_metadata(document_id)
        if not doc_metadata:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")
        
        # Process document in background
        background_tasks.add_task(process_document_task, doc_metadata)
        
        return DocumentResponse(
            filename=doc_metadata.filename,
            status=DocumentStatus.RECEIVED,
            message="Document is being reprocessed.",
            document_id=doc_metadata.document_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reprocessing document: {str(e)}")


@router.delete("/document/{document_id}", response_model=DocumentResponse)
async def delete_document(document_id: str):
    """
    Delete a document from the system
    """
    try:
        # Get document metadata
        doc_metadata = get_document_metadata(document_id)
        if not doc_metadata:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")
        
        # Delete the document from the vector store
        # Note: This requires implementation in vectorstore.py
        from app.core.vectorstore import delete_document
        delete_success = delete_document(document_id)
        
        if delete_success:
            return DocumentResponse(
                filename=doc_metadata.filename,
                status=DocumentStatus.EMBEDDED,  # Using EMBEDDED as a general status
                message="Document deleted successfully.",
                document_id=document_id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete document from vector store")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")