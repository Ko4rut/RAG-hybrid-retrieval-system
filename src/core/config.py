from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR/"data"

STORAGE_DIR = BASE_DIR/"storage"
VECTOR_STORE_PATH = STORAGE_DIR / "faiss_index"
CHUNKS_PATH = STORAGE_DIR / "chunks.pkl"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 4
MODEL_NAME = "nomic-embed-text-v2-moe:latest"