# src/preprocess/pipeline.py
from langchain_core.documents import Document
from src.preprocess.clean_text import clean_documents
from src.preprocess.normalize_docs import normalize_documents
from src.preprocess.parse_tables import TableParser

class DocumentPreprocessor:
    def __init__(self):
        self.table_parser = TableParser()

    def run(self, docs: list[Document]) -> list[Document]:
        docs = clean_documents(docs)
        docs = [self.table_parser.parse_document(doc) for doc in docs]
        docs = normalize_documents(docs)
        return docs