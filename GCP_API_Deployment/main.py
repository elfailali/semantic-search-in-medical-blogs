from flask import Flask, request, jsonify, abort
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ELASTIC_PASSWORD = "ysP1ylGF4F9UCzbD3RXLzCVW"
CLOUD_ID="8fc609e4e1a947fab7f3ab52e7e1c3d7:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGFmZDgyZGYyNzFlNjRiYjRhNTcwNjg2Yzk4ZWFmOTI0JDljYmQ0NDhhMWM3MjRjNjE5YTk4NTAyOWE3NmFkM2E0"
indexName = "medical_documents"
model = SentenceTransformer("all-mpnet-base-v2")

# ---- CHECK THE CONNECTION TO ELASTICSEARCH CLOUD
try:
    # es = Elasticsearch('http://localhost:9200/')
    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
except ConnectionError as e:
    abort(500, f"Connection Error: {e}")

if es.ping():
    print('Yupiee  Connected ')
else:
    print('Ops, it could not connect to Elasticsearch!')


def search(prompt):
    vector_input = model.encode(prompt)

    query = {
        "field": "description_vector",
        "query_vector": vector_input,
        "k": 5,  # next work: make the user choose !
        "num_candidates": 200,
    }

    res = es.knn_search(index=indexName,
                        knn=query,
                        source=['title', 'imageURL', 'articleURL', 'category', 'publishedDate', 'content'])

    result = res["hits"]["hits"]

    return result


@app.route('/')
def welcome():
    return "Welcome to the Medical Blog Search API!"


@app.route('/search', methods=['POST'])
def search_api():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print("prompt = ", prompt)

    if prompt:
        results = search(prompt)
        response = [{
            "Id": result["_id"],
            "Title": result['_source']['title'],
            "Content": result['_source']['content'],
            "ImageURL": result['_source']['imageURL'],
            "PublishedDate": result['_source']['publishedDate'],
            "articleURL": result['_source']['articleURL'],
            "Score": result['_score']
        } for result in results]
        return jsonify(response)
    else:
        return jsonify({"error": "Missing 'prompt' parameter"}), 400


if __name__ == "__main__":
    app.run(debug=True)
