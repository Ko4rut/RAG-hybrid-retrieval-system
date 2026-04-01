<!-- ===================== HEADER ===================== -->
# RAG Chatbot System (Ko4rut)
**`Retrieval-Augmented Generation · Backend AI System · Production-Oriented Design`**

---

## Overview

This project implements a **Retrieval-Augmented Generation (RAG) system** designed to answer questions strictly based on provided document context.

The system focuses on transitioning from experimental pipelines to a more **production-oriented backend architecture**, emphasizing:

- Modular design  
- Retrieval quality  
- Deterministic outputs (no hallucination)  
- Scalability considerations  

---

## System Objective

The goal of this project is not just to “make a chatbot”, but to explore:

- How **LLMs interact with structured knowledge sources**  
- How to design a **reliable and controllable retrieval pipeline**  
- How to move from **toy AI demos → real backend systems**  

---

## Architecture

```text
User Query
   ↓
Hybrid Retriever (FAISS + BM25)
   ↓
Top-k Relevant Chunks
   ↓
Prompt Construction
   ↓
LLM (Ollama / Groq)
   ↓
Final Answer (Context-Constrained)
```

## Pipeline 
### Indexing:
```PDF Loader -> Text Cleaner -> Table Parser -> Normalizer -> Chunker -> Embedding Model -> FAISS Vector Store```

### Query / Runtime Flow
```User Query -> Hybrid Retriever (FAISS + BM25) -> Top-k Chunks -> Prompt Builder -> LLM -> Final Answer```

## How to Run

### 1. Clone repository

git clone <your-repo-url>
cd RAG_Chatbot

---

### 2. Create environment

python -m venv rag_env
source rag_env/bin/activate   # Linux / Mac
rag_env\Scripts\activate      # Windows

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Install Ollama

Download and install Ollama from:

* https://ollama.com

Verify installation:

ollama --version

---

### 5. Pull required models

Embedding model:

ollama pull nomic-embed-text

LLM (based on your source code):

ollama pull qwen3:4b

You can change the model in your code:

model="qwen3:4b"

---

### 6. Build Vector Store (Embedding Phase)

python -m src.indexing.build_vectorstore

This step will:

* Load PDF documents
* Preprocess & normalize text
* Chunk documents
* Generate embeddings
* Store into FAISS vector database

---

### 7. Run the RAG pipeline

python src/main.py

Then input your question:

Enter your question: What is Under-Earth?

---

## Why Local Models? (Privacy & System Design Perspective)

One of the key design decisions in this project is using local LLMs via Ollama instead of external APIs.

### Data Privacy

* No data is sent to third-party providers
* All documents remain fully on-premise
* Suitable for:

  * Internal company knowledge bases
  * Sensitive documents
  * Proprietary data

---

### Full System Control

* Control over:

  * Model selection
  * Inference parameters
  * Latency vs quality trade-offs

* No dependency on:

  * API rate limits
  * External service downtime

---

### Cost Efficiency

* No token-based pricing
* One-time compute cost (local or server)
* Scales better for heavy internal usage

---

### Production-Oriented Thinking

Using local models helps simulate real-world backend AI systems, where:

* Data security is critical
* Systems must run independently
* Infrastructure is part of the solution

---

## Summary

This project is not just about RAG — it is about:

* Building controllable AI systems
* Designing backend pipelines for LLMs
* Understanding trade-offs between cloud vs local AI

