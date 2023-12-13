import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName = "all-documents"

# ---- CHECK THE CONNECTION TO ELASTICSEARCH
try:
    es = Elasticsearch('http://localhost:9200/')
except ConnectionError as e:
    print("Connection Error: ",e)

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
        "k": 5, # make the user choose !
        "num_candidates": 100,
    }

    res = es.knn_search(index="all_documents",
                        knn=query,
                        source=["medical_abstract"])

    result = res["hits"]["hits"]

    return result


def main():
    st.title("Search into our Medical Blog.")

    prompt = st.chat_input("Search something...")
    if prompt:
        st.write(f"You searched about the following prompt: {prompt}")

        results = search(prompt)

        st.subheader("Search Results")
        for result in results:
            with st.container():
                if "_source" in result:
                    try:
                        st.header(f"Document: {result['_source']['medical_abstract']}")
                    except Exception as e:
                        print(e)


if __name__ == "__main__":
    main()