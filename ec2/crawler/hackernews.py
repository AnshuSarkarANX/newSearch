import requests
from datetime import datetime, timezone
from es_client import index_article

HN_TOP_URL  = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def crawl_hackernews():
    print("Fetching Hacker News...")
    try:
        ids   = requests.get(HN_TOP_URL, timeout=10).json()[:30]
        count = 0

        for story_id in ids:
            try:
                item = requests.get(HN_ITEM_URL.format(story_id), timeout=5).json()
                if not item or item.get("type") != "story" or not item.get("url"):
                    continue

                index_article({
                    "title":        item.get("title", ""),
                    "summary":      item.get("text") or f"{item.get('score', 0)} points | {item.get('descendants', 0)} comments",
                    "author":       item.get("by", "HN User"),
                    "source":       "hackernews",
                    "url":          item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "tags":         ["hackernews"],
                    "image_url":    None,
                    "published_at": datetime.fromtimestamp(item["time"], tz=timezone.utc).isoformat(),
                    "indexed_at":   datetime.now(timezone.utc).isoformat()
                })
                count += 1
            except Exception as e:
                print(f"  HN item error: {e}")
                continue

        print(f"  Hacker News: indexed {count} stories")
    except Exception as e:
        print(f"  Hacker News fetch failed: {e}")
