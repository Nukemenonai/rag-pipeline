#!/usr/bin/env python3
"""Driver for task 4: run with .venv/bin/python 4-main.py

Needs ANTHROPIC_API_KEY in the environment.
"""
import os
import tempfile

RAGPipeline = __import__('4-rag_pipeline').RAGPipeline

NOTES = {
    "dl_notes.txt": [
        "Gradient descent steps the weights against the gradient of the loss.",
        "Vanishing gradients make learning slow in deep networks.",
        "Dropout randomly switches off neurons to reduce overfitting.",
        "Batch normalisation rescales layer inputs and steadies training.",
    ],
    "ml_intro.txt": [
        "Supervised learning fits a model to labelled examples.",
        "Overfitting happens when a model memorises the training set.",
        "A validation set measures how well a model generalises.",
        "Regularisation and dropout are common remedies for overfitting.",
    ],
}

pipeline = RAGPipeline()
with tempfile.TemporaryDirectory() as folder:
    for name, sentences in NOTES.items():
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(" ".join(sentences * 3))
        pipeline.ingest(path)
print("Ingested {} files.".format(len(NOTES)))

question = "Explain dropout regularisation."
print('Q: "{}"'.format(question))
print("A: {}".format(pipeline.ask(question)))
print("Sources: {}".format(pipeline.sources(question)))
