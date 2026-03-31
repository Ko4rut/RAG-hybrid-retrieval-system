from src.rag.retriever import Retriever
from src.rag.prompt import template_prompt
from langchain_ollama import ChatOllama
from src.core.config import MODEL_LLM, OLLAMA_BASE_URL
import time

class RAG_Ko4rut:
    def __init__(self, model=MODEL_LLM, temperature=0, semantic_k=15, top_k = 5):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url= OLLAMA_BASE_URL
        )
        self.retriever =Retriever(semantic_k=semantic_k)
        self.top_k = top_k

    def filter_docs(self, docs, query: str):
        filtered = []
        q = query.lower()

        for doc in docs:
            text = doc.page_content.strip().lower()

            # Drop short chunk
            if len(text) < 50:
                continue
            
            # Searching by word
            if any(word in text for word in q):
                filtered.append(doc)

        return filtered

    def ask(self, question: str):
        t0 = time.time()

        docs_related = self.retriever.retrieve(question)
        t1 = time.time()

        docs_related = self.filter_docs(docs_related, question)[:self.top_k]
        print(f"docS: {docs_related}" )
        t2 = time.time()

        if not docs_related:
            t3 = time.time()
            return {
                "question": question,
                "answer": "I don't know based on the provided context.",
                "sources": [],
                "timings": {
                    "retrieve_s": round(t1 - t0, 4),
                    "filter_s": round(t2 - t1, 4),
                    "llm_s": 0.0,
                    "total_s": round(t3 - t0, 4),
                }
            }

        context = "\n\n".join(doc.page_content for doc in docs_related)

        prompt = template_prompt.format(
            context=context,
            question=question
        )

        response = self.llm.invoke(prompt)
        t3 = time.time()

        sources = []
        for doc in docs_related:
            sources.append({
                "filename": doc.metadata.get("filename"),
                "source": doc.metadata.get("source"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "start_index": doc.metadata.get("start_index"),
            })

        return {
            "question": question,
            "answer": response.content,
            "sources": sources,
            "timings": {
                "retrieve_s": round(t1 - t0, 4),
                "filter_s": round(t2 - t1, 4),
                "llm_s": round(t3 - t2, 4),
                "total_s": round(t3 - t0, 4),
            }
        }