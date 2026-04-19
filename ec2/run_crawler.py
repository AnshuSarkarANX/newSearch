import time
from apscheduler.schedulers.blocking import BlockingScheduler
from es_client import create_index
from crawler.techcrunch  import crawl_techcrunch
from crawler.arstechnica import crawl_arstechnica
from crawler.hackernews  import crawl_hackernews
from crawler.theverge    import crawl_theverge

def run_all_crawlers():
    print("\n=== Crawl cycle started ===")
    crawl_hackernews()
    crawl_techcrunch()
    crawl_arstechnica()
    crawl_theverge()
    print("=== Crawl cycle complete ===\n")

if __name__ == "__main__":
    print("Waiting for Elasticsearch to be ready...")
    time.sleep(15)

    create_index()

    # Run immediately on startup
    run_all_crawlers()

    # Then schedule every 30 minutes
    scheduler = BlockingScheduler()
    scheduler.add_job(run_all_crawlers, "interval", minutes=30)
    print("Scheduler running — next crawl in 30 minutes")
    scheduler.start()
