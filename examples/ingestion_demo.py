#!/usr/bin/env python3
"""Demo of rag_pipeline.ingestion: run with python -m examples.ingestion_demo"""
import os
import tempfile

from rag_pipeline.doc_store import DocStore
from rag_pipeline.ingestion import ingest_file

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
    stored = ingest_file(path, store)
    print('ingested "sample_doc.txt": more than one chunk: {}'.format(
        stored > 1))
    print("returned count matches the store: {}".format(
        stored == store.count()))

    items = store.query("dropout", n_results=store.count())
    sources = {os.path.basename(i["metadata"]["source"]) for i in items}
    print("every chunk has its source: {}".format(
        len(items) == stored and sources == {"sample_doc.txt"}))

    try:
        ingest_file(os.path.join(folder, "missing.txt"), store)
    except FileNotFoundError:
        print("FileNotFoundError")
