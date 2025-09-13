CRAKD - AI THAT IDENTIFIES CRACKED TALENT

This project analyzes GitHub profiles to find underrated, highly skilled developers.

PROJECT STRUCTURE

- `cli.py`: Command-line interface for running analysis.
- `app/api.py`: FastAPI application for the web server.
- `app/github_client.py`: Fetches developer data from the GitHub API.
- `app/gemini_client.py`: Rates developers using the Gemini Pro model.
- `app/ranking.py`: Ranks developers using an ensemble model.
- `app/analysis.py`: Performs PCA and feature engineering.
- `crakd.log`: Detailed log file for debugging and analysis.
- `pca_analysis.png`: Visualization of developer clusters.

HOW TO RUN THE CLI

Use this to test the ranking algorithm and analyze developers from your terminal.

uv run python cli.py "your search query"
Example: uv run python cli.py "find me a cracked rust engineer"

HOW TO RUN THE API

Use this to serve the ranking functionality as a web API.

uv run uvicorn app.api:app --reload
The API will be available at http://127.0.0.1:8000.
