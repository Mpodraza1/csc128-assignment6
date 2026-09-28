"""
CSC-128 Assignment 6 starter: retrieval
Matthew Podraza
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge import DOCUMENTS

STOP_WORDS = set()

# This will be adjusted after examining test scores.
DEFAULT_THRESHOLD = 0.30
DEFAULT_TOP_K = 3


def stem(word):
    """
    Strip common suffixes so reserve, reserved, and reservation
    collapse to the same token.
    """
    word = word.lower()

    if word.startswith("reserv"):
        return "reserve"

    for suffix in ("ation", "ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]

    return word


def analyze(text):
    """Normalize, tokenize, stem, and add bigrams."""
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    tokens = [stem(token) for token in tokens if token not in STOP_WORDS]

    bigrams = [
        tokens[i] + "_" + tokens[i + 1]
        for i in range(len(tokens) - 1)
    ]

    return tokens + bigrams


class Retriever:
    def __init__(self, documents=None, threshold=DEFAULT_THRESHOLD):
        """Fit a TF-IDF vectorizer using the analyze function."""
        self.documents = documents if documents is not None else DOCUMENTS
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(analyzer=analyze)

        texts = [document["text"] for document in self.documents]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, question, top_k=DEFAULT_TOP_K):
        """
        Return (document, score) pairs in best-first order.
        Results below the threshold are removed.
        """
        question_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(
            self.matrix,
            question_vector
        ).flatten()

        results = [
            (document, float(score))
            for document, score in zip(self.documents, scores)
            if score >= self.threshold
        ]

        results.sort(key=lambda hit: hit[1], reverse=True)
        return results[:top_k]

    def build_context(self, hits):
        """Format retrieved chunks with their IDs and sources."""
        return "\n\n".join(
            f"[{document['id']}] Source: {document['source']}\n"
            f"{document['text']}"
            for document, score in hits
        )
