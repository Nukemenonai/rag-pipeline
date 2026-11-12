#!/usr/bin/env python3
"""ingestion pipeline"""
import os

chunk_text = __import__('0-chunking').chunk_text
DocStore = __import__('1-doc_store').DocStore


def ingest_file(path: str, store: DocStore, chunk_size: int = 500, overlap: int = 50) -> int:
    """
    Reads a text file, cuts it with chunk_text
        and stores the chunks in a DocStore (task 1), each with its source and position
    returns: 
        int: the number of chunks added to the store. It is 0 when nothing was added.
    """

    filename = os.path.basename(path)
    with open(path) as f:
        text = f.read()
        chunks = chunk_text(text, chunk_size, overlap)
    metadatas = [
        {"source": filename, "chunk": i}
        for i in range(len(chunks))
    ] 

    store.add_documents(chunks, metadatas)
    return len(chunks)