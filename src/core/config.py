import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = Path(os.getenv("DATA_PATH", BASE_DIR / "data"))
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", BASE_DIR / "storage"))
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", STORAGE_DIR / "faiss_index"))
CHUNKS_PATH = Path(os.getenv("CHUNKS_PATH", STORAGE_DIR / "chunks.pkl"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 400))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 80))
TOP_K = int(os.getenv("TOP_K", 4))

MODEL_NAME = os.getenv("MODEL_NAME", "nomic-embed-text-v2-moe:latest")
MODEL_LLM = os.getenv("MODEL_LLM", "qwen3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")