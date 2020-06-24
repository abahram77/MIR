from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch("localhost:9200")

def delete_index():
    es.indices.delete(index='paper')


def index_data():
    indexed_docs = list()
    with open('./data.json', 'r') as json_file:
        docs = json.load(json_file)
    
    for index, doc in enumerate(docs):
        doc_str = json.dumps(doc)
        es.index(index='paper', id=index, body=doc)


index_data()
# delete_index()
