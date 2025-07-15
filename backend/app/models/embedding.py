import torch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from ..config import EMBEDDING_MODEL_NAME
from typing import List

def get_embedding_model():
    """
    Initialize and return the embedding model with GPU acceleration if available.
    
    Returns:
        HuggingFaceEmbeddings: The embedding model.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}
    
    # Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    return embeddings

# Singleton pattern for reusing the embedding model
_EMBEDDING_MODEL = None

def get_embeddings_singleton():
    """
    Get or create the embedding model using singleton pattern.
    
    Returns:
        HuggingFaceEmbeddings: The embedding model instance.
    """
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        _EMBEDDING_MODEL = get_embedding_model()
    return _EMBEDDING_MODEL

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed multiple texts at once"""
    embeddings = get_embedding_model()
    return embeddings.embed_documents(texts)


def embed_query(query: str) -> List[float]:
    """Embed a single query text"""
    embeddings = get_embedding_model()
    return embeddings.embed_query(query)