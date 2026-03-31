from src.core.config import DATA_PATH
from src.loaders.pdf_loader import load_pdfs_from_folder
from src.preprocess.preprocessor import DocumentPreprocessor
from src.indexing.indexer import Indexer
from src.rag.service import RAG_Ko4rut
from fastapi import FastAPI
from src.api.routes import router

# app = FastAPI()

# app.include_router(router)


def Built_Base_Knowledge():
    docs = load_pdfs_from_folder(DATA_PATH)

    preprocessor = DocumentPreprocessor()
    docs_processed = preprocessor.run(docs)

    indexer = Indexer()
    indexer.run(docs_processed)
    print("Succses")

if __name__ == "__main__":
    # Built_Base_Knowledge()
    rag = RAG_Ko4rut()  

    question = input("Enter your question: ")
    answer = rag.ask(question) 

    print("\nAnswer: ")
    print(answer)