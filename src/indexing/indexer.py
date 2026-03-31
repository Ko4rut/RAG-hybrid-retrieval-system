from langchain_core.documents import Document
from src.indexing.embedding import build_embeddings
from src.indexing.build_vectorstore import build_and_save_vectorstore
from src.indexing.chunking import chunk_documents
from src.indexing.chunk_store import save_chunks
from src.core.config import VECTOR_STORE_PATH, MODEL_NAME, CHUNKS_PATH, CHUNK_OVERLAP, CHUNK_SIZE 


class Indexer:
    def __init__(self):
        self.embeddings = build_embeddings(MODEL_NAME)

    def run(self, docs: list[Document]):
        chunks = chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
        save_chunks(chunks, CHUNKS_PATH)
        build_and_save_vectorstore(chunks,VECTOR_STORE_PATH,self.embeddings)