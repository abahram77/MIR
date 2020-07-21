from elasticsearch import Elasticsearch


def search(es_url, abstract_weight, abstract_search, title_weight, title_search, date_weight, date_search):
    es = Elasticsearch(es_url)
    tie_breaker = 0.5
    search_params = {
            "query": {
            "nested": {
                "path": "paper",
                "query": {
                    "dis_max": {
                        "queries": 
                        [
                            {
                                "match": {
                                    "paper.title": {
                                        "query": title_search, 
                                        "boost": title_weight
                                    }
                                }
                            },
                            {
                                "match": {
                                    "paper.abstract": {
                                        "query": abstract_search, 
                                        "boost": abstract_weight
                                    }
                                }
                            },
                            {
                                "range": {
                                    "paper.date": {
                                        "gte": date_search, 
                                        "boost": date_weight
                                    }
                                }
                            }
                        ],
                        "tie_breaker": 0.5
                    }
                }
            }
        }
    }

    result = es.search(index='paper', body=search_params)
    return result



# Variables 
ES_URL = 'localhost:9200'

abstract_weight = float(input("please enter the abstract weight:\n"))
abstract_search = input("please enter the keywords from abstract:\n")

title_weight = float(input("please enter the title weight:\n"))
title_search = input("please enter the keywords from title:\n")

date_weight = float(input("please enter the date weight:\n"))
date_search = input("please enter the paper date:\n")

result = search(ES_URL, abstract_weight, abstract_search, title_weight, title_search, date_weight, date_search)

for doc in result['hits']['hits']:
    paper = doc['_source']['paper']
    print('title:',paper['title'], 'date:', paper['date'])