import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName = "all-documents"

# ---- CHECK THE CONNECTION TO ELASTICSEARCH
try:
    es = Elasticsearch('http://localhost:9200/')
except ConnectionError as e:
    print("Connection Error: ", e)

if es.ping():
        print('Yupiee  Connected ')
else:
        print('Awww it could not connect to Elasticsearch!')


def search(prompt):
    model = SentenceTransformer("all-mpnet-base-v2")
    vector_input = model.encode(prompt)

    query = {
        "field": "description_vector",
        "query_vector": vector_input,
        "k": 5, # next work: make the user choose !
        "num_candidates": 100,
    }

    res = es.knn_search(index="all_documents",
                        knn=query,
                        source=["_id","Title","Field", "Image"])

    result = res["hits"]["hits"]

    return result


def main():
    st.title("Search into our Medical Blog.")

    prompt = st.chat_input("Search something...")
    if prompt:
        st.write(f"You searched about: {prompt}")

        results = search(prompt)

        st.subheader("Search Results: ")
        for result in results:
            with st.container():
                if "_source" in result:
                    try:
                        st.subheader(f"Score: {result['_score']}")
                        st.header(f"Title: {result['_source']['Title']}")
                        st.write(f"{result['_source']['Field']}")
                    except Exception as e:
                        print(e)


if __name__ == "__main__":
    main()