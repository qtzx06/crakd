from .models import Developer
from .gemini_client import GeminiClient

class DeveloperRanker:
    def __init__(self):
        self.gemini_client = GeminiClient()

    def rank_developers(self, developers: list[dict], query: str) -> list[Developer]:
        if not developers:
            return []

        ranked_developers = []
        for dev_data in developers:
            rating = self.gemini_client.rate_developer(dev_data, query)
            
            # Create a Developer model instance
            dev = Developer(
                username=dev_data.get("username"),
                name=dev_data.get("name"),
                bio=dev_data.get("bio"),
                followers=dev_data.get("followers"),
                following=dev_data.get("following"),
                public_repos=dev_data.get("public_repos"),
                repositories=dev_data.get("top_repositories", []),
                cracked_score=rating.get("cracked_score"),
                reasoning=rating.get("reasoning")
            )
            ranked_developers.append(dev)

        # Sort developers by score in descending order
        ranked_developers.sort(key=lambda dev: dev.cracked_score, reverse=True)

        return ranked_developers
