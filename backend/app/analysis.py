import logging
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)

def engineer_features(developers: list[dict]) -> np.ndarray:
    """Converts developer data into a numerical feature matrix."""
    features = []
    for dev in developers:
        # Calculate stats for top repositories
        avg_stars = np.mean([repo['stargazers_count'] for repo in dev.get('top_repositories', [])]) if dev.get('top_repositories') else 0
        avg_forks = np.mean([repo['forks_count'] for repo in dev.get('top_repositories', [])]) if dev.get('top_repositories') else 0
        
        # Feature vector
        feature_vector = [
            dev.get('followers', 0),
            dev.get('public_repos', 0),
            avg_stars,
            avg_forks,
        ]
        features.append(feature_vector)
    
    logger.info(f"Engineered features for {len(features)} developers.")
    return np.array(features)

def perform_pca_and_visualize(features: np.ndarray, developers: list[dict], output_path: str = 'pca_analysis.png'):
    """Performs PCA and generates a visualization."""
    if features.shape[0] < 2:
        logger.warning("Not enough data points to perform PCA.")
        return None

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_features)
    
    logger.info(f"PCA completed. Explained variance ratio: {pca.explained_variance_ratio_}")

    # Visualization
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(principal_components[:, 0], principal_components[:, 1], alpha=0.7)
    plt.title('PCA of Developer Profiles')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    
    # Annotate points with developer usernames
    for i, dev in enumerate(developers):
        plt.annotate(dev['username'], (principal_components[i, 0], principal_components[i, 1]), fontsize=9)
        
    plt.grid(True)
    plt.savefig(output_path)
    logger.info(f"PCA visualization saved to {output_path}")
    
    return principal_components
