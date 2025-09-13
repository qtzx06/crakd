import argparse
import logging
from app.github_client import GitHubClient
from app.ranking import DeveloperRanker
from app.analysis import engineer_features, perform_pca_and_visualize

# --- Setup Logging ---
log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=log_format,
                    handlers=[
                        logging.FileHandler("crakd.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="CRAKD: AI That Identifies Cracked Talent")
    parser.add_argument("query", type=str, help="The search query to find developers (e.g., 'cracked rust engineer')")
    parser.add_argument("--limit", type=int, default=10, help="Number of developers to return")
    args = parser.parse_args()

    logger.info(f"Starting CRAKD analysis for query: '{args.query}' with limit: {args.limit}")

    # 1. Find candidate developers
    github_client = GitHubClient()
    developers_data = github_client.find_cracked_developers(args.query, limit=args.limit)

    if not developers_data:
        logger.warning("No developers found matching the criteria.")
        return

    # 2. Perform PCA and visualization
    features = engineer_features(developers_data)
    perform_pca_and_visualize(features, developers_data)

    # 3. Rank developers using the ensemble model
    ranker = DeveloperRanker()
    ranked_developers = ranker.rank_developers(developers_data, args.query)

    # 4. Display results
    logger.info("--- CRACKED DEVELOPER RANKING ---")
    for i, dev in enumerate(ranked_developers):
        print(f"\n--- Rank #{i+1} ---")
        print(f"Username: {dev.username}")
        print(f"Name: {dev.name}")
        print(f"Bio: {dev.bio}")
        print(f"Followers: {dev.followers}")
        print(f"Ensemble Score: {dev.ensemble_score:.2f} (Gemini: {dev.cracked_score}, GitHub: {dev.github_score:.2f})")
        print(f"Reasoning: {dev.reasoning}")
    logger.info("--- END OF RANKING ---")


if __name__ == "__main__":
    main()
