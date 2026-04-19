import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from es_client import index_article

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TechNewsBot/1.0)"}

def crawl_techcrunch():
    print("Crawling TechCrunch...")
    try:
        res = requests.get("https://techcrunch.com/latest/", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        articles = soup.select("div.loop-card__content")

        count = 0
        for article in articles[:120]:
            try:
                title_el = article.select_one("a.loop-card__title-link")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                url   = title_el["href"]

                author_el = article.select_one("span.loop-card__author")
                author    = author_el.get_text(strip=True) if author_el else "TechCrunch"

                tag_el = article.select_one("a.loop-card__cat")
                tags   = [tag_el.get_text(strip=True).lower()] if tag_el else []

                img_el    = article.select_one("img")
                image_url = img_el["src"] if img_el else None

                summary = fetch_summary(url)

                index_article({
                    "title":        title,
                    "summary":      summary,
                    "author":       author,
                    "source":       "techcrunch",
                    "url":          url,
                    "tags":         tags,
                    "image_url":    image_url,
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "indexed_at":   datetime.now(timezone.utc).isoformat()
                })
                count += 1
            except Exception as e:
                print(f"  TC article error: {e}")
                continue

        print(f"  TechCrunch: indexed {count} articles")
    except Exception as e:
        print(f"  TechCrunch crawl failed: {e}")


def fetch_summary(url: str) -> str:
    try:
        res  = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        paras = soup.select("div.article-content p")
        return " ".join(p.get_text(strip=True) for p in paras[:3])[:600]
    except:
        return ""
