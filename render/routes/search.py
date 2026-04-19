from fastapi import APIRouter, Query
from typing import Optional
from es_client import es, INDEX_NAME
from datetime import datetime, timedelta, timezone

router = APIRouter()

TIME_FILTERS = {
    "hour":  timedelta(hours=1),
    "today": timedelta(hours=24),
    "week":  timedelta(weeks=1),
    "month": timedelta(days=30),
}

@router.get("/search")
async def search(
    q:      str            = Query(default=""),
    source: Optional[str]  = None,
    time:   Optional[str]  = None,
    sort:   Optional[str]  = "relevant",
    page:   int            = 1,
    size:   int            = 10
):
    must          = []
    filter_clause = []

    if q.strip():
        must.append({
            "multi_match": {
                "query":     q,
                "fields":    ["title^3", "summary", "tags^2"],
                "fuzziness": "AUTO",
                "operator":  "or"
            }
        })
    else:
        must.append({"match_all": {}})

    if source and source != "all":
        filter_clause.append({"term": {"source": source}})

    if time and time in TIME_FILTERS:
        since = datetime.now(timezone.utc) - TIME_FILTERS[time]
        filter_clause.append({"range": {"published_at": {"gte": since.isoformat()}}})

    sort_clause = (
        [{"published_at": {"order": "desc"}}]
        if sort == "latest"
        else [{"_score": {"order": "desc"}}]
    )

    body = {
        "from":  (page - 1) * size,
        "size":  size,
        "query": {"bool": {"must": must, "filter": filter_clause}},
        "sort":  sort_clause,
        "highlight": {
            "fields": {
                "title":   {"number_of_fragments": 0},
                "summary": {"fragment_size": 200, "number_of_fragments": 1}
            },
            "pre_tags":  ["<mark>"],
            "post_tags": ["</mark>"]
        }
    }

    response = await es.search(index=INDEX_NAME, body=body)
    hits     = response["hits"]["hits"]
    total    = response["hits"]["total"]["value"]

    results = []
    for h in hits:
        src       = h["_source"]
        highlight = h.get("highlight", {})
        results.append({
            "title":        highlight.get("title",   [src.get("title", "")])[0],
            "summary":      highlight.get("summary", [src.get("summary", "")])[0],
            "author":       src.get("author", ""),
            "source":       src.get("source", ""),
            "url":          src.get("url", ""),
            "tags":         src.get("tags", []),
            "image_url":    src.get("image_url"),
            "published_at": src.get("published_at"),
            "score":        h["_score"]
        })

    return {"total": total, "page": page, "size": size, "results": results}
