from elasticsearch import Elasticsearch


def search(es_url, abstract_weight, abstract_search, title_weight, title_search, date_weight, date_search):
    es = Elasticsearch(es_url)
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
                                'paper.abstract': abstract_search
                            },
                        ],
                        'tie-breaker': abstract_weight,
                    },
                    'dis_max': {
                        'queries': [
                            {
                                'paper.title': title_search
                            }
                        ],
                        'tie-breaker': title_weight
                    },
                    'dis_max': {
                        'queries': [
                            {
                                'paper.date': date_search
                            },
                        ],
                        'tie-breaker': date_weight
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