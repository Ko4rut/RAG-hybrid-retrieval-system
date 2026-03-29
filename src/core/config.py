from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
VECTOR_STORE_PATH = BASE_DIR/"storage"
DATA_PATH = BASE_DIR/"data"
TOP_K = 4
