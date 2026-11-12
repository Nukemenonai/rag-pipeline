#!/usr/bin/env python3
"""text chunking"""
import re


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be at least 1 and overlap must be between 0 and chunk_size - 1")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be at least 1 and overlap must be between 0 and chunk_size - 1")
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        remaining = text_length - start

        if remaining <= chunk_size:
            chunks.append(text[start:])
            break

        window = text[start : start + chunk_size]

        cut = -1
        for i in range(len(window) - 1, 0, -1):
            if window[i - 1] in ".!?" and window[i].isspace():
                cut = i
                break

        if cut <= overlap:
            cut = chunk_size

        chunks.append(window[:cut])

        start += cut - overlap

    return chunks