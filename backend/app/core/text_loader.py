from pathlib import Path
from typing import List
import json


def load_processed_text(file_path: Path) -> List[str]:
    """
    Load cleaned text content from a processed file.

    Supports JSON (list of chunks) or plain text (split by paragraphs).
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Processed file does not exist: {file_path}")
    
    if file_path.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Expected JSON file to contain a list of text chunks")
            return data
    
    elif file_path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            # Split text into chunks using double newlines as paragraph delimiter
            return text.split("\n\n")
    
    raise ValueError(f"Unsupported file format for processed file: {file_path.suffix}")
