from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Tuple


class DocumentStatus(str, Enum):
    """Status of document processing"""
    RECEIVED = "received"
    PROCESSED = "processed"
    EMBEDDED = "embedded"
    FAILED = "failed"
    SKIPPED = "skipped"  # For documents that were already embedded


class DocumentType(str, Enum):
    """Types of documents supported"""
    PDF = "pdf"
    TXT = "txt"

class DocumentResponse(BaseModel):
    """Response for document upload"""
    filename: str
    status: DocumentStatus
    message: str
    document_id: Optional[str] = None

class MessageRequest(BaseModel):
    """Request for chat messages"""
    query: str = Field(..., description="The user's query")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for contextual chat")

class MessageResponse(BaseModel):
    """Response for chat messages"""
    answer: str
    response_time: float = Field(..., description="Response time in seconds")
    sources: List[str] = Field(default_factory=list, description="Source documents used for the answer")


class DocumentMetadata(BaseModel):
    """Metadata for a document"""
    filename: str
    document_id: str
    original_path: str
    processed_path: str
    file_hash: str
    document_type: DocumentType
    last_modified: float
    embedding_status: DocumentStatus
    chunks: int = 0