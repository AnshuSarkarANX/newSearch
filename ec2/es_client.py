import os
from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
es = Elasticsearch(ES_HOST)
INDEX_NAME = "tech_news"

MAPPING = {
    "mappings": {
        "properties": {
            "title":        {"type": "text", "analyzer": "english"},
            "summary":      {"type": "text", "analyzer": "english"},
            "author":       {"type": "keyword"},
            "source":       {"type": "keyword"},
            "url":          {"type": "keyword"},
            "tags":         {"type": "keyword"},
            "image_url":    {"type": "keyword"},
            "published_at": {"type": "date"},
            "indexed_at":   {"type": "date"}
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=MAPPING)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

def index_article(article: dict):
    # URL as unique doc ID — prevents duplicates on re-crawl
    doc_id = article["url"].replace("https://", "").replace("/", "_")[:200]
    es.index(index=INDEX_NAME, id=doc_id, document=article)
