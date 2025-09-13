import asyncio
from .gemini_client import GeminiClient
import json

async def parse_query_with_ai(query: str) -> dict:
    """
    Uses a generative model to parse the user's query into structured data.
    """
    gemini_client = GeminiClient()
    prompt = f"""
    You are an intelligent query parser for a developer search engine.
    Your task is to analyze the user's query and extract the primary programming language, the developer's role, and any other relevant keywords.

    User Query: "{query}"

    Analyze the query and return a JSON object with three keys:
    1. "language": The primary programming language mentioned (e.g., "python", "rust", "typescript"). If none, use null.
    2. "role": The primary job role mentioned (e.g., "engineer", "developer", "architect"). If none, use null.
    3. "keywords": A list of any other important technical keywords or phrases from the query (e.g., ["react native", "machine learning"]). Do not include conversational filler like "find me" or "gimme".

    Example 1:
    Query: "find me a cracked rust engineer"
    Output: {{"language": "rust", "role": "engineer", "keywords": []}}

    Example 2:
    Query: "gimme react native devs"
    Output: {{"language": "react", "role": "developer", "keywords": ["react native"]}}
    
    Example 3:
    Query: "senior python developer with machine learning experience"
    Output: {{"language": "python", "role": "developer", "keywords": ["senior", "machine learning"]}}

    Now, parse the user's query provided above.
    """
    try:
        response = await gemini_client.model.generate_content_async(prompt)
        json_response_str = response.text.strip().replace('`', '').replace('json', '')
        parsed_query = json.loads(json_response_str)
        # Ensure keywords is always a list
        if 'keywords' not in parsed_query or not isinstance(parsed_query['keywords'], list):
            parsed_query['keywords'] = []
        return parsed_query
    except Exception as e:
        print(f"Error parsing query with AI: {e}")
        # Fallback to a very simple parser
        return {"language": None, "role": None, "keywords": query.split()}

def parse_query(query: str) -> dict:
    """
    Synchronous wrapper for the async query parser.
    """
    return asyncio.run(parse_query_with_ai(query))