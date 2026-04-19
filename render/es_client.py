import os
from elasticsearch import AsyncElasticsearch

ES_HOST    = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es         = AsyncElasticsearch(ES_HOST)
INDEX_NAME = "tech_news"
