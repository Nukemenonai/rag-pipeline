# rag-pipeline

A small retrieval-augmented generation (RAG) library in Python. It splits text files into chunks, stores them in an in-memory ChromaDB collection, retrieves the chunks closest to a question and asks Claude to answer from them, citing each source as `[source: file, chunk N]`. When nothing is retrieved it answers `I don't know.` without calling the API.

## Setup

Python 3.11 or newer.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

The first run downloads ChromaDB's default embedding model (about 79 MB) once. Chunking and retrieval run locally; only answering calls the API.

## Use

```python
from rag_pipeline.pipeline import RAGPipeline

pipeline = RAGPipeline(n_chunks=4, chunk_size=500, overlap=50)
pipeline.ingest("notes.txt")                      # -> number of chunks stored
print(pipeline.ask("What does the note say?"))    # answer with citations
print(pipeline.sources("What does the note say?"))  # files of the retrieved chunks
```

## Layout

| Path | Description |
|---|---|
| `rag_pipeline/chunking.py` | `chunk_text(text, chunk_size=500, overlap=50)`: sentence-aware overlapping chunks |
| `rag_pipeline/doc_store.py` | `DocStore`: a document store backed by an in-memory ChromaDB collection |
| `rag_pipeline/ingestion.py` | `ingest_file(path, store, ...)`: reads a file, chunks it and stores the chunks |
| `rag_pipeline/rag_query.py` | `rag_query(question, store, n_chunks=4)`: retrieves context and asks the model |
| `rag_pipeline/pipeline.py` | `RAGPipeline`: ingestion and querying behind one class |
| `examples/` | Small programs that call each module and print the result |

## Examples

Run from the repository root:

```
python -m examples.chunking_demo
python -m examples.doc_store_demo
python -m examples.ingestion_demo
python -m examples.rag_query_demo    # needs ANTHROPIC_API_KEY
python -m examples.pipeline_demo     # needs ANTHROPIC_API_KEY
```

## Notes

* The store lives in memory only; nothing is written to disk.
* Every document gets a unique id, so ingesting the same file twice stores its chunks twice.
* Chunk metadata is `{"source": <file name>, "chunk": <index from 0>}`.
