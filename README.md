# TechPulse — Tech News Search Engine

Search across TechCrunch, Ars Technica, The Verge, and Hacker News — powered by Elasticsearch.

## Architecture

| Layer          | Where        | Role                                  |
|----------------|--------------|---------------------------------------|
| Elasticsearch  | AWS EC2      | Stores + indexes articles             |
| Crawler        | AWS EC2      | Crawls 4 sources every 30 min         |
| FastAPI API    | Render (free)| Handles search queries only           |
| React Frontend | Vercel (free)| Search UI                             |

## Folder Structure

    tech-news-search/
    ├── ec2/          ← runs on AWS EC2 (Elasticsearch + Crawler)
    ├── render/       ← deploy to Render (FastAPI search API)
    └── vercel/       ← deploy to Vercel (React frontend)

---

## EC2 Setup (Elasticsearch + Crawler)

```bash
# 1. SSH into your EC2 instance
ssh -i your-key.pem ubuntu@<ec2-public-ip>

# 2. Clone the repo
git clone https://github.com/yourusername/tech-news-search.git
cd tech-news-search/ec2

# 3. Start Elasticsearch + Crawler
docker-compose up -d --build

# 4. Check logs
docker-compose logs -f crawler
```

On startup the crawler indexes articles immediately, then re-crawls every 30 minutes.

---

## Render Setup (FastAPI)

1. Push `render/` folder to GitHub
2. Go to render.com → New Web Service → connect your repo
3. Set **Root Directory** to `render`
4. Set environment variable: `ES_HOST = http://<ec2-public-ip>:9200`
5. Deploy

Make sure EC2 Security Group allows port 9200 from 0.0.0.0/0.

---

## Vercel Setup (React)

1. Push `vercel/` folder to GitHub
2. Go to vercel.com → New Project → connect your repo
3. Set **Root Directory** to `vercel`
4. Add environment variable: `VITE_API_URL = https://your-app.onrender.com/api`
5. Deploy

---

## Local Development

```bash
# Terminal 1 — Elasticsearch (from ec2/ folder)
docker-compose up elasticsearch

# Terminal 2 — Crawler (from ec2/ folder)
pip install -r requirements.txt
playwright install chromium
python run_crawler.py

# Terminal 3 — FastAPI (from render/ folder)
pip install -r requirements.txt
ES_HOST=http://localhost:9200 uvicorn main:app --reload

# Terminal 4 — React (from vercel/ folder)
npm install && npm run dev
```

## API Reference

GET /api/search

| Param  | Type   | Options                                        |
|--------|--------|------------------------------------------------|
| q      | string | any search query                               |
| source | string | techcrunch, arstechnica, hackernews, theverge  |
| time   | string | hour, today, week, month                       |
| sort   | string | relevant, latest                               |
| page   | int    | page number                                    |
| size   | int    | results per page (default 10)                  |
