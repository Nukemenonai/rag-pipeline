# 0x06. RAG Pipeline — Retrieval-Augmented Generation

## Resources

**Read or watch:**

* [What is RAG? — IBM](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)
* [ChromaDB documentation](https://docs.trychroma.com/)
* [LangChain text splitters](https://python.langchain.com/docs/concepts/text_splitters/)
* [Anthropic — Building effective RAG systems](https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation)
* [RAG vs fine-tuning — when to use each](https://www.pinecone.io/learn/rag-vs-fine-tuning/)

## Learning Objectives

At the end of this project, you are expected to be able to explain to anyone,
**without the help of Google:**

* What RAG is and why it beats relying on a model's parametric memory
* What chunking is, why chunk size matters, and what overlap does
* What a vector store is and how it differs from a SQL database
* What the retrieve-then-read pattern is
* How to reduce hallucinations with source citations
* What a context window budget is and how retrieved chunks consume it
* When RAG fails (low-quality chunks, retrieval misses, context overflow)

## Requirements

* Python 3.11+
* `pip install anthropic chromadb sentence-transformers`
* `ANTHROPIC_API_KEY` must be set
* All functions must have a docstring

---

## Tasks

### 0. Text chunking

Write a function `chunk_text(text, chunk_size=500, overlap=50)` that splits
`text` into overlapping chunks of at most `chunk_size` characters. Adjacent
chunks share `overlap` characters at their boundary. Returns a `list[str]`.

* Split on sentence boundaries when possible (split on `. ` before
  hard-cutting on character count).
* The last chunk may be shorter than `chunk_size`.

**Prototype:** `def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:`

```
$ ./0-main.py
original length : 2048 chars
chunk count     : 5
chunk 0 length  : 498
chunk 1 length  : 502
overlap check   : True  (chunk[1][:50] in chunk[0])
```

* **File:** `0-chunking.py`

---

### 1. ChromaDB document store

Write a class `DocStore` backed by an in-memory ChromaDB collection:

* `DocStore(collection_name="docs")` — creates the collection.
* `add_documents(texts: list[str], metadatas: list[dict] | None = None)` —
  embeds and stores each text; auto-generates IDs.
* `query(text: str, n_results: int = 3) -> list[dict]` — returns top-n
  results as `[{"text": ..., "distance": ..., "metadata": ...}]`.
* `count() -> int` — number of stored documents.

**Prototype:** `class DocStore:`

```
$ ./1-main.py
stored: 10 documents
query: "how does gradient descent work?"
result 1 (dist 0.18): "Gradient descent updates weights by..."
result 2 (dist 0.31): "The learning rate controls the step size..."
result 3 (dist 0.45): "Momentum accumulates past gradients..."
```

* **File:** `1-doc_store.py`

---

### 2. Ingestion pipeline

Write a function `ingest_file(path, store, chunk_size=500, overlap=50)` that:

* Reads a plain-text file at `path`.
* Chunks it using `chunk_text()` from task 0.
* Stores chunks in a `DocStore` with metadata `{"source": path, "chunk_index": i}`.
* Returns the number of chunks stored.

**Prototype:** `def ingest_file(path: str, store: DocStore, chunk_size: int = 500, overlap: int = 50) -> int:`

```
$ ./2-main.py
ingested "sample_doc.txt" → 12 chunks
total documents in store: 12
```

A sample `sample_doc.txt` is provided in this directory.

* **File:** `2-ingestion.py`

---

### 3. RAG query function

Write a function `rag_query(question, store, n_chunks=4)` that:

* Retrieves the top `n_chunks` from `store` for `question`.
* Builds a prompt that includes the retrieved context (with source metadata)
  and the user's question.
* Calls `claude-haiku-4-5-20251001` and returns the answer.
* The system prompt must instruct Claude to answer **only** from the
  provided context and cite sources.

**Prototype:** `def rag_query(question: str, store: DocStore, n_chunks: int = 4) -> str:`

```
$ ./3-main.py
Q: "What is the vanishing gradient problem?"
A: "The vanishing gradient problem occurs when gradients become
    exponentially small during backpropagation [source: sample_doc.txt,
    chunk 3]. This makes training deep networks difficult..."
```

* **File:** `3-rag_query.py`

---

### 4. Full RAG pipeline

Write a class `RAGPipeline` that wires everything together:

* `RAGPipeline(collection_name="rag")` — constructor.
* `ingest(path)` — calls `ingest_file` internally.
* `ask(question, n_chunks=4) -> str` — calls `rag_query` internally.
* `sources(question, n_chunks=4) -> list[str]` — returns only the source
  file names retrieved (no LLM call).

**Prototype:** `class RAGPipeline:`

```
$ ./4-main.py
Ingested 2 files (24 chunks total).
Q: "Explain dropout regularisation."
A: "Dropout randomly zeroes activations during training..."
Sources: ['dl_notes.txt', 'dl_notes.txt', 'ml_intro.txt', 'dl_notes.txt']
```

* **File:** `4-rag_pipeline.py`

---

## Files

| File | Description |
|---|---|
| `0-chunking.py` | Sentence-aware overlapping text splitter |
| `1-doc_store.py` | ChromaDB-backed document store |
| `2-ingestion.py` | File → chunks → vector store |
| `3-rag_query.py` | Retrieve context → call LLM → answer |
| `4-rag_pipeline.py` | End-to-end `RAGPipeline` class |
| `0-main.py` … `4-main.py` | Drivers |
| `sample_doc.txt` | Sample knowledge-base document |
