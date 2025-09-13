import os
import time
from github import Github
from dotenv import load_dotenv
from .utils import parse_query

load_dotenv()

class GitHubClient:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        self.g = Github(self.github_token)
        self.cache = {}

    def _build_cracked_search_query(self, language=None, role=None, keywords=None):
        """Builds a GitHub search query designed to find top-tier developers."""
        base_filters = [
            "type:user",
            "followers:>1000",
            "repos:>20",
            "created:<2020-01-01", # Over 5 years of experience
        ]

        if language:
            base_filters.append(f"language:{language}")

        # Keywords from the query to search in bio
        bio_keywords = [
            "senior", "lead", "principal", "architect", 
            "founder", "cto", "staff", "distinguished"
        ]
        if role:
            bio_keywords.append(role)
        if keywords:
            bio_keywords.extend(keywords)
        
        # Remove duplicates
        bio_keywords = list(set(bio_keywords))

        query_parts = base_filters.copy()
        if bio_keywords:
            query_parts.append(f"({' OR '.join([f'{kw} in:bio' for kw in bio_keywords])})")
        
        return " ".join(query_parts)

    def get_user_details_with_cache(self, username: str) -> dict:
        """Gets user details, using a cache and checking rate limits."""
        if username in self.cache:
            return self.cache[username]

        rate_limit = self.g.get_rate_limit()
        if rate_limit.core.remaining < 20:
            print("Rate limit low. Waiting...")
            # Simple wait strategy. A real app might use reset time.
            time.sleep(60)

        try:
            user = self.g.get_user(username)
            repos = user.get_repos(sort="stargazers", direction="desc")
            
            developer_details = {
                "username": user.login,
                "name": user.name,
                "bio": user.bio,
                "followers": user.followers,
                "following": user.following,
                "public_repos": user.public_repos,
                "top_repositories": []
            }

            for i, repo in enumerate(repos):
                if i >= 5:
                    break
                
                repo_info = {
                    "name": repo.name,
                    "stargazers_count": repo.stargazers_count,
                    "forks_count": repo.forks_count,
                    "description": repo.description,
                    "language": repo.language,
                    "readme": "Not fetched in this version for brevity.",
                    "recent_commits": []
                }
                developer_details["top_repositories"].append(repo_info)

            self.cache[username] = developer_details
            return developer_details
        except Exception as e:
            print(f"Error fetching details for user {username}: {e}")
            return None

    def find_cracked_developers(self, query: str, limit: int = 10) -> list[dict]:
        """Finds developers using a smart, pre-filtered search."""
        parsed_query = parse_query(query)
        
        github_query = self._build_cracked_search_query(
            language=parsed_query.get('language'),
            role=parsed_query.get('role'),
            keywords=parsed_query.get('keywords')
        )
        print(f"Executing GitHub search with query: {github_query}")

        try:
            users = self.g.search_users(github_query, sort="followers", order="desc")
            
            candidates = []
            # Limit API calls for user details to 2*limit or 20, whichever is smaller
            api_budget = min(limit * 2, 20) 

            for user in users:
                if len(candidates) >= limit:
                    break
                if len(candidates) >= api_budget:
                    print("API budget for details exhausted.")
                    break
                    
                user_details = self.get_user_details_with_cache(user.login)
                if user_details:
                    candidates.append(user_details)
            
            return candidates
        except Exception as e:
            print(f"Error searching users for query '{query}': {e}")
            return []
