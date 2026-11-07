# 0x06. RAG Pipeline

## Description

A model only knows what it was trained on. Retrieval-augmented generation (RAG) fixes that by looking up relevant passages first and giving them to the model along with the question. In this project you split documents into chunks, store them in a vector database, ingest files, answer questions from the retrieved passages, and combine everything into one pipeline class.

## Learning Objectives

By the end of this project you should be able to explain, without looking anything up:

* What RAG is and why it beats relying on a model's memory alone
* What chunking is, why chunk size matters, and what overlap does
* What a vector store is and how it differs from a SQL database
* What the retrieve-then-read pattern is
* How source citations reduce hallucinations
* What a context-window budget is and how retrieved chunks use it up
* When RAG fails: poor chunks, retrieval misses and context overflow

## Requirements

* Python 3.11 or newer
* Every file starts with `#!/usr/bin/env python3` and a module docstring
* Code follows `pycodestyle`, and every function and class has a docstring
* Your `ANTHROPIC_API_KEY` set as an environment variable (never written into a file)

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic chromadb sentence-transformers
export ANTHROPIC_API_KEY="your-key-here"
```

## Files

| File | Description |
|---|---|
| `0-chunking.py` | `chunk_text(text, chunk_size=500, overlap=50)`: sentence-aware overlapping chunks |
| `1-doc_store.py` | `DocStore`: a document store backed by an in-memory ChromaDB collection |
| `2-ingestion.py` | `ingest_file(path, store, ...)`: reads a file, chunks it and stores the chunks |
| `3-rag_query.py` | `rag_query(question, store, n_chunks=4)`: retrieves context and asks the model |
| `4-rag_pipeline.py` | `RAGPipeline`: ingestion and querying behind one class |
| `0-main.py` … `4-main.py` | Small programs that call each function and print the result |
| `sample_doc.txt` | A short document to ingest and ask questions about |

## Usage

```
$ python3 4-main.py
```

## Resources

* [What is RAG? (IBM Research)](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)
* [ChromaDB documentation](https://docs.trychroma.com/)
* [LangChain text splitters](https://python.langchain.com/docs/concepts/text_splitters/)
* [RAG vs fine-tuning](https://www.pinecone.io/learn/rag-vs-fine-tuning/)
