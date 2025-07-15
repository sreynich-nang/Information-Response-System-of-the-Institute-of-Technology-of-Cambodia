from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from app.config import API_TITLE, API_DESCRIPTION, API_VERSION, DATA_DIR, CHROMA_DIR
from app.api.endpoints import router as api_router

# Create required directories
os.makedirs(DATA_DIR / "uploaded", exist_ok=True)
os.makedirs(DATA_DIR / "processed", exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Initialize FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint that returns API information"""
    return {
        "title": API_TITLE,
        "description": API_DESCRIPTION,
        "version": API_VERSION,
        "status": "running",
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)