from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

from src.indexing.embedding import build_embeddings
from src.indexing.chunk_store import load_chunks
from src.core.config import VECTOR_STORE_PATH, CHUNKS_PATH, MODEL_NAME


class Retriever:
    def __init__(self, semantic_k: int = 15):
        self.semantic_k = semantic_k

        # load tài nguyên 1 lần duy nhất
        self.embeddings = build_embeddings(MODEL_NAME)
        self.vectorstore = self._load_vectorstore()
        self.all_chunks = self._load_all_chunks()

        # build retrievers
        self.retriever = self._build_retriever()

    def _load_vectorstore(self):
        return FAISS.load_local(
            VECTOR_STORE_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def _load_all_chunks(self):
        return load_chunks(CHUNKS_PATH)

    def _build_retriever(self):
        # FAISS retriever
        faiss_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.semantic_k}
        )

        # BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(self.all_chunks)
        bm25_retriever.k = self.semantic_k

        # Ensemble
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever],
            weights=[0.6, 0.4],
        )

        return ensemble_retriever

    def retrieve(self, query: str, k: int = 3):
        docs = self.retriever.invoke(query)
        return docs[:k]