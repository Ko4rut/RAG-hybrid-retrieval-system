from langchain_ollama import OllamaEmbeddings
def build_embeddings(model_name: str ) -> OllamaEmbeddings:
    return OllamaEmbeddings(model=model_name)

