from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .github_client import GitHubClient
from .ranking import DeveloperRanker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://crakd-rznc.onrender.com", "https://crakd-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_client = GitHubClient()
ranker = DeveloperRanker()

@app.get("/search/{query}")
async def search_cracked_devs(query: str, limit: int = 10):
    developers = await github_client.find_cracked_developers(query, limit=limit)
    ranked_developers = await ranker.rank_developers(developers, query)
    return ranked_developers
