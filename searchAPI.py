from flask import Flask, request, jsonify, abort
import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

indexName = "all-documents"
model = SentenceTransformer("all-mpnet-base-v2")

# ---- CHECK THE CONNECTION TO ELASTICSEARCH
try:
    es = Elasticsearch('http://localhost:9200/')
except ConnectionError as e:
    abort(500, f"Connection Error: {e}")

if es.ping():
    print('Yupiee  Connected ')
else:
    print('Awww it could not connect to Elasticsearch!')


def search(prompt):

    vector_input = model.encode(prompt)

    query = {
        "field": "description_vector",
        "query_vector": vector_input,
        "k": 5,  # next work: make the user choose !
        "num_candidates": 100,
    }

    res = es.knn_search(index="all_documents",
                        knn=query,
                        source=["_id","Title", "Field", "Image"])

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
                     "Title": result['_source']['Title'],
                     "Field": result['_source']['Field'],
                     "ImageURL": result['_source']['Image'],
                     "Score": result['_score']
                     } for result in results]
        return jsonify(response)
    else:
        return jsonify({"error": "Missing 'prompt' parameter"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=8080)
