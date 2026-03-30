import pickle
from pathlib import Path
from langchain_core.documents import Document


def save_chunks(chunks: list[Document], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(chunks, f)


def load_chunks(path: str | Path) -> list[Document]:
    path = Path(path)

    with open(path, "rb") as f:
        chunks = pickle.load(f)

    return chunks