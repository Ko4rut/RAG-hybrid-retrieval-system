from rag.retriever import build_retriever
from rag.prompt import template_prompt
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

def filter_docs(docs, query: str):
    filtered = []
    q = query.lower()

    for doc in docs:
        text = doc.page_content.strip().lower()

        # bỏ chunk quá ngắn
        if len(text) < 80:
            continue

        # bỏ chunk chỉ mang tính tiêu đề / kết thúc file
        if "end of volume" in text:
            continue
        if text.startswith("under-earth survival guide"):
            continue

        filtered.append(doc)

    return filtered


def ask_rag(question: str) -> str:
    retriever = build_retriever(semantic_k=15)
    docs_related = retriever.invoke(question)
    docs_related = filter_docs(docs_related,question)[:4]
    # retriever = build_retriever(semantic_k=15)
    # docs = retriever.invoke(query)
    # results = filter_docs(docs, query)[:4]
    print("\n=== RETRIEVED DOCS ===")
    print(f"Number of docs: {len(docs_related)}")

    # for i, doc in enumerate(docs_related, 1):
    #     print(f"\n--- Doc {i} ---")
    #     print(doc.page_content[:1000])
    #     print(doc.metadata)

    if not docs_related:
        return "I don't know based on the provided context."

    context = "\n\n".join(doc.page_content for doc in docs_related)

    prompt = template_prompt.format(
        context=context,
        question=question
    )
    print(prompt)
    response = llm.invoke(prompt)
    return response.content