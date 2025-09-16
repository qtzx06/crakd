# crakd.co

AI-Powered Talent Identification for Developers.

crakd.co is a web application and local analysis tool designed to identify "cracked" (exceptionally talented) software developers. It leverages a hybrid AI model that combines quantitative GitHub metrics with qualitative analysis from a Large Language Model (Gemini) to rank developers based on natural language queries.

## Demo

<div align="center">
  <img src="./media/landing.jpeg" alt="Landing Page" style="height: 400px;">
  <br><br>
  <a href="https://www.youtube.com/watch?v=xA1j3hPEz9I&feature=youtu.be">
    <img src="./media/demo_downscaled.gif" alt="Demo" style="height: 400px;">
  </a>
</div>

## Slideshow

<div align="center">
<a href="https://docs.google.com/presentation/d/1BpHcg1xGJRs0n8QMZO2NZ-OzX1LANCFfSVIV0zRcYII/edit?usp=sharing">
  <img src="./media/slideshow.png" alt="Slideshow" style="height: 400px;">
</a>
</div>

## Tech Stack

- **Frontend:** React, Vite, Framer Motion
- **Backend:** Python, FastAPI, Docker
- **APIs:** GitHub GraphQL, Google Gemini

## Architecture

<div align="center">
  <img src="./media/mermaid.svg" alt="Architecture Diagram">
</div>

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3.8+ and pip
- Docker

### Installation & Usage

#### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

#### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  Create a `.env` file and add your API keys:
    ```
    GITHUB_TOKEN=your_github_token
    GEMINI_API_KEY=your_gemini_api_key
    ```
4.  Run the FastAPI server:
    ```bash
    uvicorn app.api:app --reload
    ```

#### Local Analysis Tool (CLI)

1.  Navigate to the `backend` directory.
2.  Run the CLI tool with your query:
    ```bash
    python cli.py "your search query"
    ```

This will output the ranked list and generate a `pca_analysis.png` visualization.
