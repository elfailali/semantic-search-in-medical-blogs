# semantic-search-in-medical-blogs

## Prerequisites

Before you start, make sure you have the following installed on your machine:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/elfailali/semantic-search-in-medical-blogs.git
   cd semantic-search-in-medical-blogs

2. **Up the docker-compose:**

   docker-compose up

   - or only **Run Elasticsearch Container:**

        docker run --rm --name elasticsearch_container -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -v ./shared_data/:/usr/share/elasticsearch/data/ elasticsearch:8.11.0

3. **Install Dependencies:**
   pip install -r requirements.txt

4. **Execute App:**

   4.1 *Index Documents:*
        For the first time you have to index your documents, after that the index will be saved into docker volume
      Go to notebook folder, then open the indexData.ipynb and execute all the cells (this code will index your documents)

   4.2 *Execute Api:*

      - Execute the searchAPI.py to start your API.
      Now you can test it using Postman for example.

      ![alt text](Postman_screenshot.png?raw=true)



