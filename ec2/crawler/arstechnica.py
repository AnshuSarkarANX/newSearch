import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from es_client import index_article

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TechNewsBot/1.0)"}

def crawl_arstechnica():
    print("Crawling Ars Technica...")
    try:
        res  = requests.get("https://arstechnica.com/", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        articles = soup.select("li.article")

        count = 0
        for article in articles[:20]:
            try:
                title_el = article.select_one("h2 a")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                url   = title_el["href"]
                if not url.startswith("http"):
                    url = "https://arstechnica.com" + url

                summary_el = article.select_one("p.summary")
                summary    = summary_el.get_text(strip=True) if summary_el else ""

                author_el = article.select_one("span.author")
                author    = author_el.get_text(strip=True) if author_el else "Ars Technica"

                tag_el = article.select_one("a.category")
                tags   = [tag_el.get_text(strip=True).lower()] if tag_el else []

                img_el    = article.select_one("img")
                image_url = img_el.get("src") if img_el else None

                index_article({
                    "title":        title,
                    "summary":      summary,
                    "author":       author,
                    "source":       "arstechnica",
                    "url":          url,
                    "tags":         tags,
                    "image_url":    image_url,
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "indexed_at":   datetime.now(timezone.utc).isoformat()
                })
                count += 1
            except Exception as e:
                print(f"  Ars article error: {e}")
                continue

        print(f"  Ars Technica: indexed {count} articles")
    except Exception as e:
        print(f"  Ars Technica crawl failed: {e}")
