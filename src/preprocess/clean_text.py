import re
from langchain_core.documents import Document

BULLET_CHARS = ["•", "", "◦", "▪", "■", "‣"]

def clean_text(text: str | None) -> str:
    """Safe text cleanup only. Do not infer document structure."""
    if not text:
        return ""

    # Normalize newline
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Normalize common invisible / special spaces
    text = text.replace("\xa0", " ")   # non-breaking space
    text = text.replace("\u200b", "")  # zero-width space
    text = text.replace("\ufeff", "")  # BOM

    # Normalize bullet characters
    for ch in BULLET_CHARS:
        text = text.replace(ch, "•")

    # Clean trailing spaces per line, but keep line structure
    lines = [line.rstrip() for line in text.split("\n")]

    # Collapse multiple blank lines
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if not line.strip():
            if not prev_blank:
                cleaned_lines.append("")
            prev_blank = True
        else:
            cleaned_lines.append(re.sub(r"[ \t]+", " ", line).strip())
            prev_blank = False

    return "\n".join(cleaned_lines).strip()


def clean_documents(docs: list[Document]) -> list[Document]:
    return [
        Document(
            page_content=clean_text(doc.page_content),
            metadata=doc.metadata.copy()
        )
        for doc in docs
    ]