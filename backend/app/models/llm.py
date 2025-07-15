import torch
from llama_cpp import Llama
from langchain_community.llms import LlamaCpp
from langchain.prompts import ChatPromptTemplate
from ..config import (
    LLM_MODEL_PATH, 
    TEMPERATURE, 
    MAX_TOKENS, 
    TOP_P, 
    N_GPU_LAYERS,
    N_BATCH
)

def get_llm_model():
    """
    Initialize and return the LLM model with GPU acceleration.
    
    Returns:
        LlamaCpp: The initialized LLM model.
    """
    # Check if CUDA is available
    # if not torch.cuda.is_available():
    #   print("⚠️ GPU not available. Using CPU for LLM.")
    #   gpu_message = "GPU acceleration disabled"
    # else:
    #   print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
    #   gpu_message = f"Using {N_GPU_LAYERS} GPU layers"
    
    # print(f"Loading model from: {LLM_MODEL_PATH}")
    # print(f"Model configuration: {gpu_message}, temp={TEMPERATURE}, max_tokens={MAX_TOKENS}")

    # Initialize the LLM using llama-cpp-python
    llm = LlamaCpp(
        model_path=LLM_MODEL_PATH,  # Updated model path
        n_ctx=4096,                 # Same context window size
        n_gpu_layers=35,           # Set explicitly for RTX 4070's VRAM
        gpu_id=0,                  # Explicitly select GPU (if supported by your wrapper)
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        n_batch=N_BATCH,
        verbose=True,              # Keep for debugging; set to False in production
        f16_kv=True                # Use half-precision for memory savings
    )


    # llm = LlamaCpp(
    #     model_path=LLM_MODEL_PATH,
    #     temperature=TEMPERATURE,
    #     max_tokens=MAX_TOKENS,
    #     top_p=TOP_P,
    #     n_gpu_layers=N_GPU_LAYERS if torch.cuda.is_available() else 0,
    #     n_batch=N_BATCH,
    #     verbose=True,  # Set to False in production
    #     n_ctx=4096,  # Context window size
    #     f16_kv=True  # To use half precision for key/value cache
    # )
    
    return llm

# Singleton pattern for reusing the LLM model
_LLM_MODEL = None

def get_llm_singleton():
    """
    Get or create the LLM model using singleton pattern.
    
    Returns:
        LlamaCpp: The LLM model instance.
    """
    global _LLM_MODEL
    if _LLM_MODEL is None:
        _LLM_MODEL = get_llm_model()
    return _LLM_MODEL