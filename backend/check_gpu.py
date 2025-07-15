# Add this to your get_llm_model() function:
from llama_cpp import Llama
print(f"llama.cpp GPU support: {Llama.llama_has_gpu_support()}")
# Should output "True" if CUDA version installed correctly