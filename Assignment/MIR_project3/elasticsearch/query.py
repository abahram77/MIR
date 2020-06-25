from elasticsearch import Elasticsearch


def search(es_url, abstract_weight, abstract_search, title_weight, title_search, date_weight, date_search):
    es = Elasticsearch(es_url)
    tie_breaker = input('Enter a number between 0 to 1 for tiebreaker, or leave it empty for the default value')
    if not tie_breaker:
        tie_breaker = 0.5
    else:
        tie_breaker = float(tie_breaker)
    search_params = {
        'query': {
            'size': 10,
            'from': 0,
            'nested': {
                'path': 'paper',
                'query': {
                    'dis_max': {
                        'queries': [
                            {
                                'paper.abstract': {
                                    'query': abstract_search,
                                    'boost': abstract_weight
                                }
                            },
                            {
                                'paper.title': {
                                    'query': title_search,
                                    'boost': title_weight
                                }
                            },
                            {
                                'paper.date': {
                                    'query': date_search,
                                    'boost': date_weight
                                }
                            },
                        ],
                        'tie-breaker': tie_breaker
                    }
                }
            }
        }
    }


    result = es.search(index='paper', body=search_params)
    return result



# Variables 
ES_URL = 'localhost:9200'

abstract_weight = input("please enter the abstract weight:\n")
abstract_search = input("please enter the keywords from abstract:\n")

title_weight = input("please enter the title weight:\n")
title_search = input("please enter the keywords from title:\n")

date_weight = input("please enter the date weight:\n")
date_search = input("please enter the paper date:\n")

search(ES_URL, abstract_weight, abstract_search, title_weight, title_search, date_weight, date_search)