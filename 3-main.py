#!/usr/bin/env python3
"""Driver for task 3: run with .venv/bin/python 3-main.py

Needs ANTHROPIC_API_KEY in the environment.
"""
import os
import re
import tempfile

DocStore = __import__('1-doc_store').DocStore
ingest_file = __import__('2-ingestion').ingest_file
rag_query = __import__('3-rag_query').rag_query

SENTENCES = [
    "Gradient descent steps the weights against the gradient of the loss.",
    "The learning rate sets the size of each step.",
    "A rate that is too large can overshoot the minimum.",
    "The vanishing gradient problem makes gradients tiny in deep networks.",
    "Early layers then learn very slowly because updates are almost zero.",
    "Dropout randomly switches off neurons to reduce overfitting.",
    "Batch normalisation rescales layer inputs and steadies training.",
    "Regularisation penalises large weights so the model generalises.",
]

with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "sample_doc.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(" ".join(SENTENCES * 3))
    store = DocStore()
    ingest_file(path, store)

question = "What is the vanishing gradient problem?"
answer = rag_query(question, store, n_chunks=4)
print('Q: "{}"'.format(question))
print("A: {}".format(answer))
print("cites a source: {}".format(
    re.search(r"\[source: [^\]]+\]", answer) is not None))
