import os
from elasticsearch import AsyncElasticsearch

ES_HOST    = os.getenv("ES_HOST", "http://localhost:9200")
es         = AsyncElasticsearch(ES_HOST)
INDEX_NAME = "tech_news"
