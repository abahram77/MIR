from typing import List, Dict
import numpy as np
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw
from math import log

lemmatizer = WordNetLemmatizer()
stopwords = sw.words('english')

def get_doc_terms(doc_info):
    '''concatenate all terms (title + body) of the passed doc'''
    body_terms = doc_info['body'].split()
    title_terms = doc_info['title'].split()
    all_terms = body_terms + title_terms
    return all_terms

def get_document_frequency(json_data):
    vectors = {}
    
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    
    for doc_id, doc in enumerate(json_data):
        terms = get_doc_terms(doc)
        for term in terms:
            if term not in stopwords:
                term = lemmatizer.lemmatize(term)
                if term not in vectors:
                    vectors[term] = []
                if doc_id not in vectors[term]:
                    vectors[term].append(doc_id)
    
    vectors_list = list(vectors.items())
    term_map_index = {}
    
    for i in range(len(vectors_list)):
        term = vectors_list[i][0]
        term_map_index[term] = i
    
    frequencies = []
    for word, freq_list in vectors_list:
        frequencies.append(len(freq_list))
    
    return term_map_index, frequencies

def train(training_docs: List[Dict]):
    global term_map_index
    global frequencies
    global N
    global n_c
    global t_c
    global category_no
    category_no = 4
    term_map_index, frequencies = get_document_frequency(training_docs)
    N = len(training_docs)
    term_no = len(term_map_index)
    
    n_c = []
    for i in range(category_no):
        n_c.append(0)
    
    t_c = np.zeros((category_no, term_no))
    
    for doc_id, doc in enumerate(training_docs):
        terms = get_doc_terms(doc)
        category = doc['category']

        for term in terms:
            index = category - 1
            if term not in stopwords:
                term = lemmatizer.lemmatize(term)
                t_c[index, term_map_index[term]] += 1
            n_c[index] += 1

def classify(doc: Dict) -> int:
    global term_map_index
    global frequencies
    global N
    global n_c
    global t_c
    alpha = 1
    term_no = len(term_map_index)
    scores = []
    
    for i in range(category_no):
        score = log(n_c[i]/N)
        scores.append(score)
    
    sigma = np.sum(t_c, axis=1)
    
    for i in range(category_no):
        terms = get_doc_terms(doc)
        for term in terms:
            if term not in stopwords:
                term = lemmatizer.lemmatize(term)
                if term in term_map_index:
                    fraction = log((t_c[i, term_map_index[term]] + alpha) / (sigma[i] + term_no))
                    scores[i] += fraction
    predicted = np.argmax(scores) + 1

    return predicted


