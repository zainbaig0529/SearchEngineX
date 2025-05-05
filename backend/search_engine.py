import math
import re
from collections import defaultdict, Counter

# -----------------------------
# Define the InvertedIndex class FIRST
# -----------------------------
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)
        self.doc_lengths = {}
        self.documents = {}
        self.avg_doc_length = 0.0
        self.total_docs = 0

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def add_document(self, doc_id, text):
        tokens = self.tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        self.documents[doc_id] = text
        self.total_docs += 1

        term_counts = Counter(tokens)
        for term, count in term_counts.items():
            self.index[term][doc_id] = count

        self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def bm25_score(self, term, doc_id, k1=1.5, b=0.75):
        N = self.total_docs
        df = len(self.index[term])
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

        f = self.index[term][doc_id]
        dl = self.doc_lengths[doc_id]
        avg_dl = self.avg_doc_length

        return idf * ((f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / avg_dl)))

    def search(self, query):
        tokens = self.tokenize(query)
        scores = defaultdict(float)

        for term in tokens:
            if term in self.index:
                for doc_id in self.index[term]:
                    scores[doc_id] += self.bm25_score(term, doc_id)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, self.documents[doc_id], score) for doc_id, score in ranked]

# -----------------------------
# Test block LAST
# -----------------------------
if __name__ == "__main__":
    engine = InvertedIndex()

    engine.add_document("doc1", "The quick brown fox jumps over the lazy dog.")
    engine.add_document("doc2", "Fast foxes leap over lazy dogs in summer.")
    engine.add_document("doc3", "The dog is not lazy; it is simply energy-efficient.")

    query = "lazy dog"
    results = engine.search(query)

    print(f"Search results for: '{query}'\n")
    for doc_id, content, score in results:
        print(f"Doc ID: {doc_id} | Score: {score:.4f}\nContent: {content}\n")
