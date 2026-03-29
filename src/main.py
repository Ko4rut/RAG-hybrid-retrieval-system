from loaders.pdf_loader import load_pdfs_from_folder
from core.config import DATA_PATH
from preprocess.clean_text import clean_documents

docs = load_pdfs_from_folder(DATA_PATH)

cleaned_docs = clean_documents(docs)

for doc in cleaned_docs:
    print(doc.page_content)