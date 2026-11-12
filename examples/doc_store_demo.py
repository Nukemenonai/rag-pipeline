#!/usr/bin/env python3
"""Demo of rag_pipeline.doc_store: run with python -m examples.doc_store_demo"""
from rag_pipeline.doc_store import DocStore

DOCS = [
    "Gradient descent steps the weights against the gradient of the loss.",
    "The learning rate sets the size of each step.",
    "The vanishing gradient problem makes gradients tiny in deep networks.",
    "Dropout randomly switches off neurons to reduce overfitting.",
    "Batch normalisation rescales layer inputs and steadies training.",
    "Regularisation penalises large weights so the model generalises.",
    "Transformers use attention to weigh every token against the others.",
    "Embeddings map text to vectors; similar meanings land close together.",
    "Paris is the capital of France.",
    "Sourdough bread needs a long, slow fermentation.",
]

store = DocStore()
print("empty store: {} documents, query gives {}".format(
    store.count(), store.query("anything")))
store.add_documents(DOCS)
print("stored: {} documents".format(store.count()))

results = store.query("What reduces overfitting?", n_results=3)
print("results returned: {}".format(len(results)))
for rank, item in enumerate(results, 1):
    print('result {}: "{}"'.format(rank, item["text"][:48]))
distances = [item["distance"] for item in results]
print("closest first: {}".format(distances == sorted(distances)))
print("n_results above the count: {} results".format(
    len(store.query("training", n_results=50))))
