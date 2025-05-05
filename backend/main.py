from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # Temporary placeholder logic
    return jsonify({'query_received': query, 'results': []})

if __name__ == '__main__':
    app.run(debug=True)
