# GPU-Accelerated RAG Chatbot with FastAPI, LangChain, and HuggingFace

This project implements a comprehensive end-to-end Retrieval-Augmented Generation (RAG) chatbot system that runs locally on GPU hardware. The system uses LangChain for orchestration, HuggingFace models for embeddings and text generation, ChromaDB for vector storage, and FastAPI for the API interface.

## Features

- **GPU-Accelerated**: Optimized for both embedding and LLM models
- **RAG Architecture**: Combines retrieval and generation for more accurate, factual responses
- **Local Deployment**: No external API calls, all processing happens locally
- **Vector Database**: ChromaDB for efficient document storage and retrieval
- **REST API**: FastAPI interface with Pydantic schemas
- **Self-contained**: Ready to use out of the box

## System Requirements

- Python 3.9
- CUDA-compatible GPU with at least 8GB VRAM (for optimal performance)
- ~20GB disk space for models and dependencies

## Quick Start

### Install Dependencies

consider to set up the environment by following the step guidance in my report.

### Download the Quantized LLM Model

Download a 4-bit quantized GGUF model file or any pre-trained you want. For this project, we've configured for Mistral 7B Instruct, MPNet for embedding and OpenChat for generating.

### Run the API

```bash
python -m app.main
```

The API will start on `http://localhost:8000`.

### Use the API

#### Index Documents

Before querying, you should index your documents. A sample document is created automatically, but you can add your own documents to the `data/sample_docs/` directory.

## Project Structure

```
chatbot_project/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI entry point
│   ├── config.py              # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── embedding.py       # Embedding model setup
│   │   └── llm.py             # LLM model setup
│   ├── core/
│   │   ├── __init__.py
│   │   ├── document_loader.py # Document loading utilities
│   │   ├── vectorstore.py     # ChromaDB setup
│   │   ├── pdf_upload_handle.py 
│   │   ├── txt_upload_handle.py    
│   │   ├── text_loader.py    
│   │   └── rag_chain.py       # LangChain ReAct + RAG setup
│   └── api/
│       ├── __init__.py
│       ├── endpoints.py        # API endpoints
│       └── schemas.py          # Pydantic schemas
├── data/                       # Store your documents here
│       ├── processed/       
│       └── uploaded/         
├── chroma_db/                  # ChromaDB will store embeddings here
├── requirements.txt
└── README.md
```

## Adding Your Own Documents

Place your documents in the `data/sample_docs/` directory. Supported formats:
- PDF (`.pdf`)
- Plain text (`.txt`)

## GPU Optimization

The system is configured to use GPU acceleration for both embedding generation and text generation. You can modify the GPU settings in `app/config.py`:

- `USE_GPU`: Enable/disable GPU usage
- `GPU_LAYERS`: Number of layers to offload to GPU (-1 for all)

## Troubleshooting

### CUDA Out of Memory

If you encounter CUDA out of memory errors:
1. Reduce `GPU_LAYERS` in the config
2. Use a more aggressively quantized model (e.g., Q3_K_M instead of Q4_K_M)
3. Reduce batch size settings

### Model Loading Failures

Ensure you've downloaded the correct GGUF model and placed it in the `models/` directory. Update the `GGUF_MODEL_PATH` in `app/config.py` to match your model filename.

## Performance Optimization

- The embedding model uses normalized embeddings for better performance
- The LLM uses 4-bit quantization to reduce VRAM usage
- Document chunking parameters can be adjusted for memory/performance trade-offs
- MD5 Hash to prevent pre-embedding

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
- [Mistral AI](https://mistral.ai/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## License

This project is licensed under the MIT License.