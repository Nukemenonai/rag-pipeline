#!/usr/bin/env python3
"""
chunk retrieval module
"""
import os
from anthropic import Anthropic

from .doc_store import DocStore


def rag_query(question: str, store: DocStore, n_chunks: int = 4) -> str:
    """
    Retrieves the chunks closest to a question, 
    builds a prompt that labels each chunk with its source, 
    asks Claude once, and returns the answer text.
    """
    if n_chunks < 1:
        raise ValueError('n_chunks must be at least 1')
    client = Anthropic(
        api_key=os.environ.get(
            "ANTHROPIC_API_KEY"
        ),
    )

    chunks = store.query(question, n_chunks)
    context = "\n\n".join(
    "[source: {}, chunk {}]\n{}".format(
        c["metadata"]["source"], c["metadata"]["chunk"], c["text"])
    for c in chunks)
    if not chunks:
        return "I don't know."

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        system=f"""
            answer the user's question.

            answer using only the context provided in context: {context}. 
            cite every claim in the same form: 
            [source: file, chunk N]

            if the context does not contain the answer, say you don't know. 
        """,
        messages=[
            {
                "role": "user", "content": f"{question}"
            }
        ]
    )
    message = ""
    for block in response.content:
        if block.type == "text":
            message += block.text
    return message
    