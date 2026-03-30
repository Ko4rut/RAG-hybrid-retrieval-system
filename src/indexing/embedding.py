from langchain_ollama import OllamaEmbeddings
from core.config import MODEL_NAME
def build_embeddings(model_name: str = MODEL_NAME) -> OllamaEmbeddings:
    return OllamaEmbeddings(model=model_name)

