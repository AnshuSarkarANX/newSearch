import time
from apscheduler.schedulers.blocking import BlockingScheduler
from elasticsearch import ConnectionError, ConnectionTimeout
from es_client import create_index, es
from crawler.techcrunch  import crawl_techcrunch
from crawler.arstechnica import crawl_arstechnica
from crawler.hackernews  import crawl_hackernews
from crawler.theverge    import crawl_theverge

def wait_for_elasticsearch(max_retries=20, delay=10):
    print("Waiting for Elasticsearch to be ready...")
    for attempt in range(1, max_retries + 1):
        try:
            health = es.cluster.health(wait_for_status="yellow", timeout="5s")
            print(f"Elasticsearch is ready! Status: {health['status']}")
            return True
        except (ConnectionError, ConnectionTimeout, Exception) as e:
            print(f"  Attempt {attempt}/{max_retries} — not ready yet ({type(e).__name__}). Retrying in {delay}s...")
            time.sleep(delay)
    print("ERROR: Elasticsearch never became ready. Exiting.")
    return False

def run_all_crawlers():
    print("\n=== Crawl cycle started ===")
    crawl_hackernews()
    crawl_techcrunch()
    crawl_arstechnica()
  # crawl_theverge()
    print("=== Crawl cycle complete ===\n")

if __name__ == "__main__":
    if not wait_for_elasticsearch():
        exit(1)

    create_index()
    run_all_crawlers()

    scheduler = BlockingScheduler()
    scheduler.add_job(run_all_crawlers, "interval", minutes=30)
    print("Scheduler running — next crawl in 30 minutes")
    scheduler.start()