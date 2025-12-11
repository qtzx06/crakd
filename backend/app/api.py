from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .github_client import GitHubClient
from .ranking import DeveloperRanker
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://crakd-rznc.onrender.com", "https://crakd-frontend.vercel.app", "https://crakd.co"],
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

@app.get("/search-stream/{query}")
async def search_cracked_devs_stream(query: str, limit: int = 10):
    async def event_generator():
        # Step 1: Parse query
        yield f"data: {json.dumps({'type': 'status', 'message': 'parsing your query with grok...'})}\n\n"

        # Step 2: Search GitHub
        yield f"data: {json.dumps({'type': 'status', 'message': 'searching github for developers...'})}\n\n"
        developers = await github_client.find_cracked_developers(query, limit=limit)

        if not developers:
            yield f"data: {json.dumps({'type': 'status', 'message': 'no developers found'})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'results': []})}\n\n"
            return

        yield f"data: {json.dumps({'type': 'status', 'message': f'found {len(developers)} candidates, analyzing with grok...'})}\n\n"

        # Step 3: Rank developers with progress updates
        ranked_developers = await ranker.rank_developers_with_progress(developers, query, progress_callback=None)

        # Convert to dict for JSON serialization
        results = [dev.model_dump() for dev in ranked_developers]

        yield f"data: {json.dumps({'type': 'status', 'message': 'ranking complete, here are your results'})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'results': results})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
