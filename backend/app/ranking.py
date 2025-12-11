from .models import Developer
from .xai_client import XAIClient
from .analysis import engineer_features
import numpy as np
import logging
import asyncio
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class DeveloperRanker:
    def __init__(self):
        self.xai_client = XAIClient()

    async def rank_developers(self, developers: list[dict], query: str) -> list[Developer]:
        """Original method for backwards compatibility."""
        return await self.rank_developers_with_progress(developers, query, progress_callback=None)

    async def rank_developers_with_progress(
        self,
        developers: list[dict],
        query: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> list[Developer]:
        if not developers:
            return []

        # 1. Get qualitative ratings from Grok concurrently
        tasks = []
        for dev_data in developers:
            logger.info(f"Rating developer '{dev_data.get('username')}' with Grok...")
            tasks.append(self.xai_client.rate_developer(dev_data, query))

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
        feature_sums = np.sum(features, axis=1)
        max_score = np.max(feature_sums)
        if max_score > 0:
            github_scores = (feature_sums / max_score) * 100
        else:
            github_scores = np.zeros(len(developers))

        # 3. Calculate ensemble score and update models
        for i, dev in enumerate(rated_developers):
            dev.github_score = github_scores[i]

            # Ensemble: 60% Grok, 40% GitHub Score
            dev.ensemble_score = (0.6 * dev.cracked_score) + (0.4 * dev.github_score)
            logger.debug(f"Scores for {dev.username}: Grok={dev.cracked_score}, GitHub={dev.github_score}, Ensemble={dev.ensemble_score}")

        # 4. Sort developers by the final ensemble score
        rated_developers.sort(key=lambda dev: dev.ensemble_score, reverse=True)
        logger.info("Finished ranking developers by ensemble score.")

        return rated_developers
