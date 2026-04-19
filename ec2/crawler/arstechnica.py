import requests
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime
from es_client import index_article


RSS_FEEDS = [
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://feeds.arstechnica.com/arstechnica/gadgets",
    "https://feeds.arstechnica.com/arstechnica/science",
    "https://feeds.arstechnica.com/arstechnica/gaming",
    "https://feeds.arstechnica.com/arstechnica/security",
]

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc":      "http://purl.org/dc/elements/1.1/"
}


def crawl_arstechnica():
    print("Crawling Ars Technica via RSS...")
    count = 0
    seen_urls = set()

    for rss_url in RSS_FEEDS:
        try:
            res  = requests.get(rss_url, timeout=10)
            root = ET.fromstring(res.content)

            for item in root.findall(".//item"):
                try:
                    url = item.findtext("link", "").strip()
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    title   = item.findtext("title", "").strip()
                    summary = item.findtext("description", "").strip()[:600]
                    author  = item.findtext("dc:creator", "Ars Technica", NS).strip()

                    image_url = None
                    enclosure = item.find("enclosure")
                    if enclosure is not None:
                        image_url = enclosure.get("url")

                    pub_date = item.findtext("pubDate", "")
                    try:
                        published_at = parsedate_to_datetime(pub_date).isoformat()
                    except:
                        published_at = datetime.now(timezone.utc).isoformat()

                    tags = [c.text.lower() for c in item.findall("category") if c.text]

                    index_article({
                        "title":        title,
                        "summary":      summary,
                        "author":       author,
                        "source":       "arstechnica",
                        "url":          url,
                        "tags":         tags,
                        "image_url":    image_url,
                        "published_at": published_at,
                        "indexed_at":   datetime.now(timezone.utc).isoformat()
                    })
                    count += 1
                except Exception as e:
                    print(f"  Ars item error: {e}")
                    continue

        except Exception as e:
            print(f"  Ars feed error ({rss_url}): {e}")
            continue

    print(f"  Ars Technica: indexed {count} articles")