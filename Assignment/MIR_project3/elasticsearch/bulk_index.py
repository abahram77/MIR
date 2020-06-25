from elasticsearch import Elasticsearch, helpers
import json


def delete_index(es_url):
    es = Elasticsearch(es_url)
    es.indices.delete(index='paper')


def index_data(es_url, data_address):
    es = Elasticsearch(es_url)
    mappings = {
        "mappings": {
            "properties": {
                "page-rank": {
                    "type": "float"
                },
                "paper": {
                    "type": "nested",
                    "properties": {
                        "abstract": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "authors": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "date": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "references": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "title": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                }
            }
        },
    }
    es.indices.create('paper', body=mappings)

    indexed_docs = list()
    with open(data_address, 'r') as json_file:
        docs = json.load(json_file)
    
    for index, doc in enumerate(docs):
        doc_str = json.dumps(doc)
        es.index(index='paper', id=index, body=doc)

ES_URL = 'localhost:9200'
data_address = './data.json'

while True:
    user_preference = input("1. Create index from data.\n2. Delete all indexes.\n3. Exit\n")
    if user_preference == '1':
        index_data(ES_URL, data_address)
        print('\ndata indexed\n')
    elif user_preference == '2':
        delete_index(ES_URL)
        print('\nindices deleted\n')
    elif user_preference == '3':
        print('\nexiting...\n')
        exit()
    else:
        print('\ninput is invalid\n')