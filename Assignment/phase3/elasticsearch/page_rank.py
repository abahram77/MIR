import numpy as np
import json
from elasticsearch import Elasticsearch

es = Elasticsearch('localhost:9200')

# Reading data from file
with open('./elasticsearch/data.json', 'r') as json_file:
    data = json.load(json_file)


N = len(data)
a = np.zeros(shape=(N, N))
v = np.ones(shape=(1, N))
x = np.zeros(shape=(1, N))
x[0][0] = 1
alpha = 0.1
papers = set()

# Creating a list of IDs
for paper_info in data:
    paper_id = paper_info['paper']['id']
    papers.add(paper_id)

# Map each ID to index
paper_id_map = dict()
for index, paper in enumerate(papers):
    paper_id_map[paper] = index
    index += 1

    
# calculate adjacency matrix
def len_calc(refs):
    valid_len = len(refs)
    for ref in refs:
        ref_id = ref.split('/')[-1]
        if ref_id not in papers:
            valid_len -= 1
    return valid_len

dead_ends = list()

for paper_info in data:
    paper_id = paper_info['paper']['id']
    paper_index = paper_id_map[paper_id]
    paper_refs = paper_info['paper']['references']
    refs_no = len_calc(paper_refs)
    
    is_deadend = True
    for paper_ref in paper_refs:
        reference = paper_ref.split('/')[-1]
        reference_no = len(paper)
        if reference in papers:
            is_deadend = False
            ref_index = paper_id_map[reference]
            a[paper_index][ref_index] = 1/refs_no
            a[paper_index][ref_index] = (1 - alpha) * a[paper_index][ref_index] + (alpha * 1 / N)
    
    if is_deadend:
        a[paper_index] = np.array([1/N] * N)
p = a[:]

# calculate pi = (1  - alpha) * pi + alpha * v/N
for i, row in enumerate(p):
    if i not in dead_ends:
        p[i][:] = (1 - alpha) * row + (alpha * (v / N))
    
#page ranks
page_ranks = np.dot(x, p)
for _ in range(10):
    page_ranks = np.dot(page_ranks, p)

for i in range(N):
    es.update(index='paper', id=i, body={'doc': {'page-rank': page_ranks[0][i]}})