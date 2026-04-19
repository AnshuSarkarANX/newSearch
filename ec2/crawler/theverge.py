from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
from es_client import index_article

def crawl_theverge():
    print("Crawling The Verge with Playwright...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page    = browser.new_page()
            page.goto("https://www.theverge.com/news", timeout=30000)
            page.wait_for_selector("article", timeout=10000)

            articles = page.query_selector_all("article")
            count    = 0

            for article in articles[:20]:
                try:
                    title_el   = article.query_selector("h2")
                    link_el    = article.query_selector("a")
                    summary_el = article.query_selector("p")

                    if not title_el or not link_el:
                        continue

                    title = title_el.inner_text().strip()
                    url   = link_el.get_attribute("href")
                    if url and not url.startswith("http"):
                        url = "https://www.theverge.com" + url

                    summary   = summary_el.inner_text().strip()[:600] if summary_el else ""
                    img_el    = article.query_selector("img")
                    image_url = img_el.get_attribute("src") if img_el else None

                    index_article({
                        "title":        title,
                        "summary":      summary,
                        "author":       "The Verge",
                        "source":       "theverge",
                        "url":          url,
                        "tags":         ["tech"],
                        "image_url":    image_url,
                        "published_at": datetime.now(timezone.utc).isoformat(),
                        "indexed_at":   datetime.now(timezone.utc).isoformat()
                    })
                    count += 1
                except Exception as e:
                    print(f"  Verge article error: {e}")
                    continue

            browser.close()
            print(f"  The Verge: indexed {count} articles")
    except Exception as e:
        print(f"  The Verge crawl failed: {e}")
