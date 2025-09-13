# Crakd Architecture (Detailed Presentation Diagram)

This is a more detailed, yet presentation-friendly, Mermaid.js diagram. It uses a top-down flow, color-coding, and includes key file names for context, while ensuring correct syntax.

```mermaid
graph TD
    %% --- Style Definitions for Readability ---
    classDef client fill:#EBF5FB,stroke:#2980B9,stroke-width:2px,color:#000;
    classDef api fill:#FADBD8,stroke:#C0392B,stroke-width:2px,color:#000;
    classDef logic fill:#E8F8F5,stroke:#1ABC9C,stroke-width:2px,color:#000;
    classDef external fill:#FEF9E7,stroke:#F39C12,stroke-width:2px,color:#000;
    classDef data fill:#F4ECF7,stroke:#8E44AD,stroke-width:2px,color:#000;
    classDef output fill:#E5E7E9,stroke:#566573,stroke-width:2px,color:#000;

    subgraph "Clients"
        WebApp["Web App (crakd.co)"]
        CLI["Local CLI (cli.py)"]
    end

    subgraph "Backend API (Hosted on Render)"
        FastAPI["FastAPI Server (api.py)"]
    end

    subgraph "Core Logic Modules"
        GitHubClient["GitHub Client<br>(github_client.py)"]
        GeminiClient["Gemini Client<br>(gemini_client.py)"]
        Ranker["Developer Ranker<br>(ranking.py)"]
    end

    subgraph "External Services"
        GitHubAPI[("GitHub GraphQL API")]
        GeminiAPI[("Google Gemini API")]
    end

    subgraph "Data Analysis & Ranking"
        FeatureEng["Feature Engineering<br>(analysis.py)"]
        Ensemble["Ensemble Model<br>(ranking.py)"]
    end

    subgraph "Final Outputs"
        RankedJSON["Ranked JSON Response"]
        PCAImage["PCA Graph (pca_analysis.png)"]
    end

    %% --- Data Flow ---
    WebApp -- "HTTPS Request" --> FastAPI
    FastAPI --> Ranker
    Ranker --> GitHubClient
    GitHubClient -- "GraphQL Query" --> GitHubAPI
    GitHubAPI -- "Raw User Data" --> GitHubClient
    GitHubClient -- "Developer Profiles" --> Ranker
    
    Ranker --> FeatureEng
    FeatureEng -- "Quantitative Metrics" --> Ranker
    
    Ranker --> GeminiClient
    GeminiClient -- "Prompts" --> GeminiAPI
    GeminiAPI -- "Qualitative Scores & Reasoning" --> GeminiClient
    GeminiClient -- "Scores" --> Ranker
    
    Ranker -- "Combines Scores" --> Ensemble
    Ensemble -- "Final Ranked List" --> Ranker
    Ranker -- " " --> RankedJSON
    
    FeatureEng --> PCAImage

    RankedJSON -- "Top 3 Results" --> WebApp
    
    %% --- Local CLI Flow ---
    CLI --> GitHubClient & Ranker & FeatureEng
    Ranker -- "Top 50 List" --> CLI
    PCAImage -- "Saved to Disk" --> CLI

    %% --- Apply Styles ---
    class WebApp,CLI client;
    class FastAPI api;
    class GitHubClient,GeminiClient,Ranker logic;
    class GitHubAPI,GeminiAPI external;
    class FeatureEng,Ensemble data;
    class RankedJSON,PCAImage output;
```
