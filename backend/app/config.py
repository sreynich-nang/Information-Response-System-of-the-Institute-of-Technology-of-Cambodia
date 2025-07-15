import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
MODEL_DIR = APP_DIR / "models"

# Model settings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
LLM_MODEL_PATH = str(MODEL_DIR / "openchat-3.5-0106.Q4_K_M.gguf")

# Vector store settings
COLLECTION_NAME = "document_collection"

# Text processing configuration
CHUNK_SIZE = 512  # In characters
CHUNK_OVERLAP = 100
TEXT_SPLITTER = "recursive_character"

# LLM settings
TEMPERATURE = 0.1
MAX_TOKENS = 1024
TOP_P = 0.95
N_GPU_LAYERS = 35  # -1 means use all available GPU memory
N_BATCH = 512  # Batch size for prompt processing

# RAG settings
NUM_DOCUMENTS = 3  # Number of documents to retrieve for RAG

# API settings
API_TITLE = "Chatbot API with RAG"
API_DESCRIPTION = "FastAPI application for RAG-powered chatbot using LangChain"
API_VERSION = "0.1.0"