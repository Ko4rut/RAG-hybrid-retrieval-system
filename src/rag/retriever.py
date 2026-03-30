from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

from indexing.embedding import build_embeddings
from indexing.chunk_store import load_chunks
from core.config import VECTOR_STORE_PATH, CHUNKS_PATH


def load_vectorstore():
    embeddings = build_embeddings()
    return FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def load_all_chunks():
    return load_chunks(CHUNKS_PATH)


def build_retriever(semantic_k: int = 20):
    vectorstore = load_vectorstore()
    faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": semantic_k})

    all_chunks = load_all_chunks()
    bm25_retriever = BM25Retriever.from_documents(all_chunks)
    bm25_retriever.k = semantic_k

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.6, 0.4],
        # id_key="chunk_id",  # bật nếu metadata của chunk có id riêng
    )
    return ensemble_retriever


def retrieve_docs(query: str, k: int = 3):
    retriever = build_retriever(semantic_k=15)
    docs = retriever.invoke(query)
    return docs[:k]