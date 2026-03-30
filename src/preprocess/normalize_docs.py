from langchain_core.documents import Document
import re


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def normalize_document(doc: Document) -> Document:
    metadata = dict(doc.metadata) if doc.metadata else {}

    return Document(
        page_content=normalize_text(doc.page_content),
        metadata=metadata
    )


def normalize_documents(docs: list[Document]) -> list[Document]:
    return [normalize_document(doc) for doc in docs]