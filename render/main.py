from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.search import router as search_router

app = FastAPI(
    title="TechPulse Search API",
    description="Search tech news indexed from TechCrunch, Ars Technica, The Verge & HN",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict to your Vercel URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "TechPulse Search API is running"}

@app.get("/health")
async def health():
    # Used by UptimeRobot to keep Render awake
    return {"status": "ok"}
