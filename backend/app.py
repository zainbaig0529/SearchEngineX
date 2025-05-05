from flask import Flask, request, jsonify
from search_engine import InvertedIndex

app = Flask(__name__)
engine = InvertedIndex()

# Sample documents to preload (you can replace this)
documents = {
    "doc1": "The quick brown fox jumps over the lazy dog.",
    "doc2": "Fast foxes leap over lazy dogs in summer.",
    "doc3": "The dog is not lazy; it is simply energy-efficient."
}

for doc_id, text in documents.items():
    engine.add_document(doc_id, text)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    results = engine.search(query)
    return jsonify(results)

@app.route("/add", methods=["POST"])
def add_document():
    data = request.get_json()
    doc_id = data.get("id")
    content = data.get("content")
    if not doc_id or not content:
        return jsonify({"error": "Missing id or content"}), 400
    engine.index_documents({doc_id: content})
    return jsonify({"message": "Document added", "id": doc_id})

if __name__ == "__main__":
    app.run(debug=True)
