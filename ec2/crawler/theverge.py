import requests
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from es_client import index_article

RSS_URL = "https://www.theverge.com/rss/index.xml"

def crawl_theverge():
    print("Crawling The Verge via RSS...")
    try:
        res  = requests.get(RSS_URL, timeout=10)
        # Atom feed namespace
        ns = {
            "atom":    "http://www.w3.org/2005/Atom",
            "media":   "http://search.yahoo.com/mrss/",
            "dc":      "http://purl.org/dc/elements/1.1/"
        }
        root = ET.fromstring(res.content)

        entries = root.findall("atom:entry", ns)
        count   = 0
        for entry in entries[:20]:
            try:
                title   = entry.findtext("atom:title", "", ns).strip()
                url     = entry.find("atom:link", ns)
                url     = url.get("href") if url is not None else ""
                summary = entry.findtext("atom:summary", "", ns).strip()[:600]
                author  = entry.findtext("atom:author/atom:name", "The Verge", ns).strip()

                # Date
                pub_date = entry.findtext("atom:published", "", ns)
                try:
                    published_at = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).isoformat()
                except:
                    published_at = datetime.now(timezone.utc).isoformat()

                # Image from media:thumbnail
                img_el    = entry.find("media:thumbnail", ns)
                image_url = img_el.get("url") if img_el is not None else None

                # Tags
                tags = [c.get("term", "").lower() for c in entry.findall("atom:category", ns) if c.get("term")]

                index_article({
                    "title":        title,
                    "summary":      summary,
                    "author":       author,
                    "source":       "theverge",
                    "url":          url,
                    "tags":         tags,
                    "image_url":    image_url,
                    "published_at": published_at,
                    "indexed_at":   datetime.now(timezone.utc).isoformat()
                })
                count += 1
            except Exception as e:
                print(f"  Verge item error: {e}")
                continue

        print(f"  The Verge: indexed {count} articles")
    except Exception as e:
        print(f"  The Verge RSS failed: {e}")