#!/usr/bin/env python3
"""Doc store class"""
import uuid 
import chromadb


class DocStore:
    def __init__(self) -> None:
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name=f"collection_{uuid.uuid4().hex}"
        )

    def add_documents(self, documents: list[str], metadatas: list[dict] | None = None) -> None:
        if not documents: 
            raise ValueError("documents must not be empty")
        if metadatas and len(metadatas ) != len(documents):
            raise ValueError("metadatas must have one dict per document")
        ids = [f"id_{uuid.uuid4().hex}" for doc in documents] 
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, text: str, n_results: int = 4) -> list[dict]:
        r = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        docs = r["documents"][0]
        metas = r["metadatas"][0] if r["metadatas"] else [None] * len(docs)
        dists = r["distances"][0]
        return [
            {"text": d, "metadata": m, "distance": dist}
            for d, m, dist in zip(docs, metas, dists)
        ]

        
    def count(self) -> int:
        return int(self.collection.count())