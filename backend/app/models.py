from pydantic import BaseModel
from typing import List, Optional

class Repository(BaseModel):
    name: str
    stargazers_count: int
    forks_count: int
    description: Optional[str] = None
    language: Optional[str] = None

class Developer(BaseModel):
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    followers: int
    following: int
    public_repos: int
    repositories: List[Repository] = []
    cracked_score: Optional[float] = None # Score from Gemini
    github_score: Optional[float] = None # Score from quantitative metrics
    ensemble_score: Optional[float] = None # Combined score
    reasoning: Optional[str] = None
