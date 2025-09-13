import os
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from .utils import parse_query_with_ai

class GitHubClient:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        
        self.transport = AIOHTTPTransport(
            url="https://api.github.com/graphql",
            headers={'Authorization': f'bearer {self.github_token}'}
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    def _build_graphql_search_query(self, language=None, role=None, keywords=None):
        """Builds a GitHub GraphQL search query string."""
        query_parts = ["type:user", "followers:>100", "repos:>10"]
        if language:
            query_parts.append(f"language:{language}")
        
        # Combine role and keywords for a general search
        all_keywords = (keywords or []) + ([role] if role else [])
        if all_keywords:
            # Filter out None or empty strings from keywords
            valid_keywords = [kw for kw in all_keywords if kw]
            if valid_keywords:
                # Join keywords for a general search, not restricted to bio
                keyword_query = " ".join(valid_keywords)
                query_parts.append(keyword_query)
            
        return " ".join(query_parts)

    async def find_cracked_developers(self, query: str, limit: int = 10) -> list[dict]:
        """Finds developers using a single, efficient GraphQL query."""
        parsed_query = await parse_query_with_ai(query)
        github_query_str = self._build_graphql_search_query(
            language=parsed_query.get('language'),
            role=parsed_query.get('role'),
            keywords=parsed_query.get('keywords')
        )
        print(f"Executing GitHub GraphQL search with query: '{github_query_str}'")

        graphql_query = gql("""
            query search($query_str: String!, $limit: Int!) {
              rateLimit {
                limit
                cost
                remaining
                resetAt
              }
              search(query: $query_str, type: USER, first: $limit) {
                nodes {
                  ... on User {
                    login
                    name
                    bio
                    followers {
                      totalCount
                    }
                    following {
                      totalCount
                    }
                    repositories(first: 5, orderBy: {field: STARGAZERS, direction: DESC}) {
                      totalCount
                      nodes {
                        name
                        stargazerCount
                        forkCount
                        description
                        primaryLanguage {
                          name
                        }
                      }
                    }
                    contributionsCollection {
                      contributionCalendar {
                        totalContributions
                      }
                    }
                  }
                }
              }
            }
        """)

        try:
            async with self.client as session:
                result = await session.execute(graphql_query, variable_values={"query_str": github_query_str, "limit": limit})
            
            print(f"GitHub API Rate Limit: {result['rateLimit']}")

            candidates = []
            for user_node in result['search']['nodes']:
                if not user_node: continue

                top_repos = []
                # Gracefully handle cases where repositories or their nodes are None
                for repo in (user_node.get('repositories') or {}).get('nodes') or []:
                    if not repo: continue
                    top_repos.append({
                        "name": repo.get('name'),
                        "stargazers_count": repo.get('stargazerCount'),
                        "forks_count": repo.get('forkCount'),
                        "description": repo.get('description'),
                        "language": (repo.get('primaryLanguage') or {}).get('name')
                    })

                # Safely access nested fields
                followers_count = (user_node.get('followers') or {}).get('totalCount')
                following_count = (user_node.get('following') or {}).get('totalCount')
                public_repos_count = (user_node.get('repositories') or {}).get('totalCount')
                total_contributions = (user_node.get('contributionsCollection') or {}).get('contributionCalendar', {}).get('totalContributions', 0)

                dev_details = {
                    "username": user_node.get('login'),
                    "name": user_node.get('name'),
                    "bio": user_node.get('bio'),
                    "followers": followers_count,
                    "following": following_count,
                    "public_repos": public_repos_count,
                    "total_contributions": total_contributions,
                    "top_repositories": top_repos
                }
                candidates.append(dev_details)
            
            return candidates
        except Exception as e:
            print(f"Error executing GraphQL query for '{query}': {e}")
            # Check for common rate limit error message
            if 'rate limit' in str(e).lower():
                print("You may have hit the GitHub API rate limit. Check your token and usage.")
            return []

async def main():
    # Example usage for testing
    client = GitHubClient()
    devs = await client.find_cracked_developers("cracked rust engineer", limit=5)
    import json
    print(json.dumps(devs, indent=2))

if __name__ == '__main__':
    asyncio.run(main())