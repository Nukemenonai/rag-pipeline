#!/usr/bin/env python3
"""ingestion pipeline"""
import os

from .chunking import chunk_text
from .doc_store import DocStore


def ingest_file(path: str, store: DocStore, chunk_size: int = 500, overlap: int = 50) -> int:
    """
    Reads a text file, cuts it with chunk_text
        and stores the chunks in a DocStore, each with its source and position
    returns: 
        int: the number of chunks added to the store. It is 0 when nothing was added.
    """

    filename = os.path.basename(path)
    with open(path) as f:
        text = f.read()
        if not text:
            return 0
        chunks = chunk_text(text, chunk_size, overlap)
    metadatas = [
        {"source": filename, "chunk": i}
        for i in range(len(chunks))
    ] 

    store.add_documents(chunks, metadatas)
    return len(chunks)