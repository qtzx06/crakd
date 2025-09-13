from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .github_client import GitHubClient
from .ranking import DeveloperRanker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_client = GitHubClient()
ranker = DeveloperRanker()

@app.get("/search/{query}")
async def search_cracked_devs(query: str, limit: int = 10):
    developers = github_client.find_cracked_developers(query, limit=limit)
    ranked_developers = ranker.rank_developers(developers, query)
    return ranked_developers
