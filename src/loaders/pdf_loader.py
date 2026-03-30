from pathlib import Path
from typing import List

import pymupdf4llm
from langchain_core.documents import Document


def load_pdf(pdf_path: str | Path) -> List[Document]:
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    md_text = pymupdf4llm.to_markdown(str(pdf_path))

    doc = Document(
        page_content=md_text,
        metadata={
            "source": str(pdf_path),
            "filename": pdf_path.name,
        }
    )

    return [doc]


def load_pdfs_from_folder(folder_path: str | Path) -> List[Document]:
    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    all_docs: List[Document] = []

    for pdf_file in folder_path.glob("*.pdf"):
        docs = load_pdf(pdf_file)
        all_docs.extend(docs)

    return all_docs