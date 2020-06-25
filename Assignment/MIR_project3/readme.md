# MIR Project Phase 3

## Section1: Crawler

For running the crawler execute `scrapy crawl semanticscholar` in the current directory.

> **WARNING:** make sure to have scrapy installed on your computer. If you have docker installed, you can easily run elasticsearch by running `docker-compose up` command in `elasticsearch` directory.

**PS:** The data is saved in `elasticsearch` directory as `data.json` file.


## Section2: Elasticsearch Indexing

For indexing the documents run the `bulk_indexing.py` file which is located in `elasticsearch` directory. 

```
python3 ./elasticsearch/bulk_indexing.py
```

## Section3: Calculate PageRank
For calculating the page-rank and add them to the elasticsearch use the following command:

```
python3 ./elasticsearch/page_rank.py
```

## Section4: Elasticsearch Query

For giving some parameters to search in the database.

```
python3 ./elasticsearch/query.py
```