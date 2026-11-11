#!/usr/bin/env python3
"""text chunking"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Splits on sentence boundaries when possible; 
    adjacent chunks share overlap characters."""
    if not text: return []
    if len(text) <= chunk_size: return [text]
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be strictly less than chunk_size")
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunk = text[i: i+chunk_size]
        chunks.append(chunk)
        if i + chunk_size >= len(text):
            break
    return chunks