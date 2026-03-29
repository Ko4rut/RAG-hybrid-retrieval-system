from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

def load_pdf(pdf_path: str| Path) -> List[Document]:
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    loader = PyMuPDFLoader(str(pdf_path))
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = str(pdf_path)
        doc.metadata["filename"] = pdf_path.name
    
    return docs

def load_pdfs_from_folder(folder_path: str | Path) -> List[Document]:
    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    all_docs: List[Document] = []

    for pdf_file in folder_path.glob("*.pdf"):
        docs = load_pdf(pdf_file)
        all_docs.extend(docs)

    return all_docs