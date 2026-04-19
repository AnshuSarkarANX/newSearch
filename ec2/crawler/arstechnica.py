import requests
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from es_client import index_article

RSS_URL = "https://feeds.arstechnica.com/arstechnica/index"

def crawl_arstechnica():
    print("Crawling Ars Technica via RSS...")
    try:
        res  = requests.get(RSS_URL, timeout=10)
        root = ET.fromstring(res.content)
        ns   = {"content": "http://purl.org/rss/1.0/modules/content/",
                "dc":      "http://purl.org/dc/elements/1.1/"}

        items = root.findall(".//item")
        count = 0
        for item in items[:20]:
            try:
                title   = item.findtext("title", "").strip()
                url     = item.findtext("link",  "").strip()
                summary = item.findtext("description", "").strip()[:600]
                author  = item.findtext("dc:creator", "Ars Technica", ns).strip()

                # Extract image from enclosure or media
                image_url = None
                enclosure = item.find("enclosure")
                if enclosure is not None:
                    image_url = enclosure.get("url")

                # Parse date
                pub_date = item.findtext("pubDate", "")
                try:
                    from email.utils import parsedate_to_datetime
                    published_at = parsedate_to_datetime(pub_date).isoformat()
                except:
                    published_at = datetime.now(timezone.utc).isoformat()

                # Tags from categories
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

        print(f"  Ars Technica: indexed {count} articles")
    except Exception as e:
        print(f"  Ars Technica RSS failed: {e}")