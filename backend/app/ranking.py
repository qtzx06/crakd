from .models import Developer
from .gemini_client import GeminiClient
from .analysis import engineer_features
import numpy as np
import logging
import asyncio

logger = logging.getLogger(__name__)

class DeveloperRanker:
    def __init__(self):
        self.gemini_client = GeminiClient()

    async def rank_developers(self, developers: list[dict], query: str) -> list[Developer]:
        if not developers:
            return []

        # 1. Get qualitative ratings from Gemini concurrently
        tasks = []
        for dev_data in developers:
            logger.info(f"Rating developer '{dev_data.get('username')}' with Gemini...")
            tasks.append(self.gemini_client.rate_developer(dev_data, query))
        
        ratings = await asyncio.gather(*tasks)

        rated_developers = []
        for i, dev_data in enumerate(developers):
            rating = ratings[i]
            dev = Developer(
                username=dev_data.get("username"),
                name=dev_data.get("name"),
                bio=dev_data.get("bio"),
                followers=dev_data.get("followers"),
                following=dev_data.get("following"),
                public_repos=dev_data.get("public_repos"),
                repositories=dev_data.get("top_repositories", []),
                cracked_score=rating.get("cracked_score", 0),
                reasoning=rating.get("reasoning", "")
            )
            rated_developers.append(dev)
        
        # 2. Calculate quantitative GitHub score
        features = engineer_features(developers)
        # Normalize features to a 0-100 scale. We'll use a simple sum for now.
        # A more complex model could be used here (e.g., weighted sum, k-NN).
        feature_sums = np.sum(features, axis=1)
        max_score = np.max(feature_sums)
        if max_score > 0:
            github_scores = (feature_sums / max_score) * 100
        else:
            github_scores = np.zeros(len(developers))

        # 3. Calculate ensemble score and update models
        for i, dev in enumerate(rated_developers):
            dev.github_score = github_scores[i]
            
            # Ensemble: 60% Gemini, 40% GitHub Score
            dev.ensemble_score = (0.6 * dev.cracked_score) + (0.4 * dev.github_score)
            logger.debug(f"Scores for {dev.username}: Gemini={dev.cracked_score}, GitHub={dev.github_score}, Ensemble={dev.ensemble_score}")

        # 4. Sort developers by the final ensemble score
        rated_developers.sort(key=lambda dev: dev.ensemble_score, reverse=True)
        logger.info("Finished ranking developers by ensemble score.")

        return rated_developers
