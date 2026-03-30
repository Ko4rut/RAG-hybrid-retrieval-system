from core.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_STORE_PATH, MODEL_NAME, CHUNKS_PATH
from loaders.pdf_loader import load_pdfs_from_folder
from preprocess.clean_text import clean_documents
from preprocess.parse_tables import TableParser
from preprocess.normalize_docs import normalize_documents
from indexing.chunking import chunk_documents
from indexing.chunk_store import save_chunks
from indexing.build_vectorstore import build_and_save_vectorstore
from rag.service import ask_rag

# docs = load_pdfs_from_folder(DATA_PATH)

# docs = clean_documents(docs)
# parser = TableParser()
# docs = [parser.parse_document(doc) for doc in docs]
# docs = normalize_documents(docs)


# chunks = chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
# save_chunks(chunks, CHUNKS_PATH)
# print("Save Chunk succesfull")

# # for chunk in chunks:
# #     text = chunk.page_content

# #     text = text.replace(" | ", ". ")
# #     text = text.replace("Row 1:", "")
# #     text = text.replace("Row 2:", "")
# #     text = text.replace("Columns:", "Fields:")
    
# #     chunk.page_content = text

# # for i, chunk in enumerate(chunks):
# #     if "Ash Ladder" in chunk.page_content:
# #         print(f"\n=== CHUNK CONTAINS ASH LADDER | index={i} ===")
# #         print(chunk.page_content)
# #         print(chunk.metadata)

# vectorstore = build_and_save_vectorstore(chunks, VECTOR_STORE_PATH, MODEL_NAME)

# print("Vectorstore built successfully!")



if __name__ == "__main__":
    question = input("Enter your question: ")
    answer = ask_rag(question)
    print("\nAnswer:")
    print(answer)