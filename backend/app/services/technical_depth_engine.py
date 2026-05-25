"""
Technical Depth Detection Engine.

Analyzes experience bullets and project descriptions to evaluate their technical complexity,
concurrency, database optimization, pipeline depth, and API patterns, allowing the system
to rank and prioritize high-depth engineering achievements.
"""

import re
from typing import Dict, Any, List

# Complexity scores for advanced software engineering dimensions
DEPTH_DIMENSIONS = {
    # Advanced Backend & Concurrency (Weight: 25)
    "concurrency_backend": {
        "keywords": [
            "rtsp", "onvif", "multithreading", "asynchronous", "async", "redis pub/sub", "redis pubsub",
            "websockets", "websocket", "grpc", "message broker", "rabbitmq", "kafka", "microservices",
            "api gateway", "concurrency", "fault-tolerant", "fault tolerance"
        ],
        "weight": 25.0
    },
    # Database Optimization & Storage (Weight: 25)
    "databases_storage": {
        "keywords": [
            "postgresql", "postgres", "query latency", "query optimization", "indexing", "database schema",
            "transaction isolation", "database write", "redis caching", "caching layers", "sqlite transactions",
            "nosql", "mongodb", "cassandra", "dynamodb", "elasticsearch"
        ],
        "weight": 25.0
    },
    # Machine Learning & Computer Vision Pipelines (Weight: 25)
    "ml_cv_pipelines": {
        "keywords": [
            "arcface", "facenet", "faiss", "yolo", "opencv", "cnn", "neural network", "image processing",
            "feature extraction", "predictive model", "classification model", "scikit-learn", "tensorflow",
            "pytorch", "keras", "smote", "randomforest", "xgboost", "data wrangling", "nlp", "transformers"
        ],
        "weight": 25.0
    },
    # Cloud Deployment, DevOps & Security (Weight: 25)
    "devops_security": {
        "keywords": [
            "docker", "containerized", "kubernetes", "k8s", "ci/cd", "github actions", "aws", "gcp",
            "azure", "jwt authentication", "oauth", "rate-limiting", "auth middleware", "security middleware",
            "nginx", "serverless", "cloud setup"
        ],
        "weight": 25.0
    }
}


def calculate_technical_depth(text: str) -> float:
    """Calculate a technical depth score from 0.0 to 100.0 for any bullet point or description.
    
    A higher score indicates the presence of advanced frameworks, system optimization,
    databases, APIs, ML pipelines, and production-ready architectures.
    """
    if not text or not text.strip():
        return 0.0
        
    text_lower = text.lower()
    score = 0.0
    
    for dimension, details in DEPTH_DIMENSIONS.items():
        dimension_score = 0.0
        keywords = details["keywords"]
        weight = details["weight"]
        
        # Match keywords using word boundary or precise substring check
        matches = []
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", text_lower) or (len(kw) > 4 and kw in text_lower):
                matches.append(kw)
                
        # Scale the score: 1 match gives 60% of the weight, 2+ matches give 100% of the weight
        if len(matches) >= 2:
            dimension_score = weight
        elif len(matches) == 1:
            dimension_score = weight * 0.6
            
        score += dimension_score
        
    # Standard length booster: slightly reward longer technical details up to +10pt
    words_count = len(text.split())
    if 15 <= words_count <= 35:
        score += 5.0
        
    return min(100.0, round(score, 2))


def rank_experience_bullets(bullets: List[str]) -> List[str]:
    """Sort bullets so that the highest technical depth bullets are positioned first."""
    if not bullets:
        return []
        
    scored = []
    for b in bullets:
        depth = calculate_technical_depth(b)
        scored.append((depth, b))
        
    # Sort descending by technical depth score
    scored_sorted = sorted(scored, key=lambda x: x[0], reverse=True)
    return [b for _, b in scored_sorted]


def rank_projects_by_depth(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort a list of project entries based on the technical depth of their descriptions and name."""
    if not projects:
        return []
        
    scored = []
    for p in projects:
        name = p.get("name", "")
        techs = " ".join(p.get("technologies", []))
        desc = " ".join(p.get("description", []))
        
        full_text = f"{name} {techs} {desc}"
        depth = calculate_technical_depth(full_text)
        scored.append((depth, p))
        
    scored_sorted = sorted(scored, key=lambda x: x[0], reverse=True)
    return [p for _, p in scored_sorted]
