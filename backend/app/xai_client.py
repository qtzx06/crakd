import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

class XAIClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY environment variable not set")
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-4-1-fast-reasoning"

    async def _chat_completion(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def rate_developer(self, developer_data: dict, query: str) -> dict:
        prompt = f"""As an expert AI talent scout for software engineers, your task is to evaluate a developer's profile based on the provided data. The user is searching for: "{query}".

Analyze the following developer data:
{json.dumps(developer_data, indent=2)}

Based on the data, provide a "cracked_score" from 1 to 100, where 100 is a perfect match for a "cracked" developer according to the user's query. Also, provide a short "reasoning" for your score.

A "cracked" developer is someone who is exceptionally skilled, innovative, and productive. Consider factors like code quality, project complexity, innovation, and community impact.

Return ONLY a JSON object with two keys: "cracked_score" and "reasoning". No other text."""

        try:
            response = await self._chat_completion(prompt)
            json_response_str = response.strip().replace('`', '').replace('json', '')
            return json.loads(json_response_str)
        except Exception as e:
            print(f"Error generating rating for developer: {e}")
            return {"cracked_score": 0, "reasoning": "Error analyzing profile."}

    async def parse_query(self, query: str) -> dict:
        prompt = f"""You are an intelligent query parser for a developer search engine.
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

Return ONLY the JSON object. No other text."""

        try:
            response = await self._chat_completion(prompt)
            json_response_str = response.strip().replace('`', '').replace('json', '')
            parsed_query = json.loads(json_response_str)
            if 'keywords' not in parsed_query or not isinstance(parsed_query['keywords'], list):
                parsed_query['keywords'] = []
            return parsed_query
        except Exception as e:
            print(f"Error parsing query with AI: {e}")
            return {"language": None, "role": None, "keywords": query.split()}
