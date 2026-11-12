#!/usr/bin/env python3
"""complete RAG pipeline"""
chunk_text = __import__('0-chunking').chunk_text
DocStore = __import__('1-doc_store').DocStore
ingest_file = __import__('2-ingestion').ingest_file
rag_query = __import__('3-rag_query').rag_query


class RAGPipeline:
    def __init__(self, n_chunks: int = 4, chunk_size: int = 500, overlap: int = 50) -> None:
        self.store = DocStore()
        if n_chunks < 1:
            raise ValueError("n_chunks must be at least 1")
        self.n_chunks = n_chunks
        self.chunk_size = chunk_size
        self.overlap = overlap
 
    def ingest(self, path: str) -> int:
        return ingest_file(path, self.store, self.chunk_size, self.overlap)

    def ask(self, question: str) -> str:
        return rag_query(question, self.store, self.n_chunks)
    
    def sources(self, question: str) -> list[str]:
        r = self.store.query(question, self.n_chunks)
        return [c["metadata"]["source"] for c in r]