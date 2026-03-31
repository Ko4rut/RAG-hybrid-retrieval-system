from rag.retriever import build_retriever

query = "What is the Ash Ladder"
k = 10

def filter_docs(docs, query: str):
    filtered = []
    q = query.lower()

    for doc in docs:
        text = doc.page_content.strip().lower()

        # bỏ chunk quá ngắn
        if len(text) < 80:
            continue
        if any(word in text for word in q):
            filtered.append(doc)
        
    return filtered

retriever = build_retriever(semantic_k=15)
docs = retriever.invoke(query)
results = filter_docs(docs, query)[:4]

print(f"\n=== QUERY: {query} ===")
found = False

for i, doc in enumerate(results, 1):
    chunk_id = doc.metadata.get("chunk_id")
    print(f"\n--- Doc {i} | chunk_id={chunk_id} ---")
    print(doc.page_content[:300])
    print(doc.metadata)

    if chunk_id in [51, 63]:
        found = True
        print(">>> THIS IS AN ASH LADDER CHUNK <<<")

if not found:
    print(f"\nNo Ash Ladder chunk found in top {k}.")