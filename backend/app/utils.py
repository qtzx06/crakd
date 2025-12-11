import asyncio
from .xai_client import XAIClient

async def parse_query_with_ai(query: str) -> dict:
    """
    Uses Grok to parse the user's query into structured data.
    """
    xai_client = XAIClient()
    return await xai_client.parse_query(query)

def parse_query(query: str) -> dict:
    """
    Synchronous wrapper for the async query parser.
    """
    return asyncio.run(parse_query_with_ai(query))