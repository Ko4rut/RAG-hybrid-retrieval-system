from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

MARKDOWN_SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    " ",
    ""
]


def build_text_splitter(CHUNK_SIZE: int, CHUNK_OVERLAP: int) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
        strip_whitespace=True,
        separators=MARKDOWN_SEPARATORS
    )


def chunk_documents(docs: list[Document], CHUNK_SIZE: int, CHUNK_OVERLAP: int) -> list[Document]:
    splitter = build_text_splitter(CHUNK_SIZE, CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata = dict(chunk.metadata) if chunk.metadata else {}
        chunk.metadata["chunk_id"] = i

    return chunks