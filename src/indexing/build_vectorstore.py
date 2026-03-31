from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

def build_and_save_vectorstore(
    chunks: list[Document],
    save_path: str,
    embeddings
):
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
        # distance_strategy=DistanceStrategy.COSINE
    )
    vectorstore.save_local(save_path)
    return vectorstore