#!/usr/bin/env python3
"""Driver for task 0: run with .venv/bin/python 0-main.py"""
chunk_text = __import__('0-chunking').chunk_text

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
text = " ".join(SENTENCES * 3)


def report(chunks, size, overlap):
    """Print the properties every correct chunker has."""
    print("  more than one chunk: {}".format(len(chunks) > 1))
    print("  every chunk <= {} chars: {}".format(
        size, all(len(c) <= size for c in chunks)))
    print("  overlap check: {}".format(
        all(a[-overlap:] == b[:overlap] for a, b in zip(chunks, chunks[1:]))))


print("original length: {} chars".format(len(text)))
print("defaults (500, 50):")
report(chunk_text(text), 500, 50)
print("chunk_size=200, overlap=20:")
report(chunk_text(text, chunk_size=200, overlap=20), 200, 20)
print("short text is one chunk: {}".format(
    chunk_text("Short text.") == ["Short text."]))
