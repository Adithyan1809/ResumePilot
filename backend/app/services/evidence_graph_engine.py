"""
Evidence Graph Engine.
Calculates weights, semantic overlaps, and technical relevance scores for whitelisted evidence nodes,
ranking achievements and projects against targeted Job Description profiles.
"""

from typing import List, Dict, Any

# Dynamic tech adjacency mappings
TECH_ADJACENCY = {
    "fastapi": ["python", "rest api", "backend", "websockets", "grpc"],
    "django": ["python", "postgresql", "backend", "rest api"],
    "flask": ["python", "rest api", "backend"],
    "react": ["javascript", "typescript", "html", "css", "tailwind", "webpack", "vite"],
    "next.js": ["react", "typescript", "javascript", "html", "css"],
    "kubernetes": ["docker", "k8s", "aws", "gcp", "ci/cd", "devops"],
    "docker": ["kubernetes", "aws", "gcp", "ci/cd", "devops", "linux"],
    "pytorch": ["python", "numpy", "machine learning", "deep learning", "ai_ml"],
    "tensorflow": ["python", "numpy", "machine learning", "deep learning", "ai_ml"],
}


def score_and_rank_evidence_nodes(
    nodes: List[Dict[str, Any]],
    jd_required_techs: List[str],
    focus_domain: str
) -> List[Dict[str, Any]]:
    """Determines relevance weights for each evidence node based on target JD stack and domain criteria."""
    if not nodes:
        return []

    jd_techs_lower = [t.lower() for t in jd_required_techs if t]
    ranked = []

    for node in nodes:
        score = 50.0  # Base score
        
        node_techs = [t.lower() for t in node.get("technologies", [])]
        
        # 1. Match Direct Tech Keywords
        direct_matches = 0
        for tech in node_techs:
            if tech in jd_techs_lower:
                score += 25.0
                direct_matches += 1
                
        # 2. Match Adjacent Tech Keywords
        for tech in node_techs:
            if tech in TECH_ADJACENCY:
                adjacents = TECH_ADJACENCY[tech]
                if any(adj in jd_techs_lower for adj in adjacents):
                    score += 10.0
                    
        # 3. Boost nodes containing verified metrics (extremely important for recruiters!)
        if node.get("metrics"):
            score += 15.0
            
        # 4. Domain Alignment boost
        node_type = node.get("type", "")
        content_lower = node.get("content", "").lower()
        
        if focus_domain == "backend" and any(w in content_lower for w in ["api", "database", "query", "redis", "concurrency", "scalable", "latency"]):
            score += 10.0
        elif focus_domain == "frontend" and any(w in content_lower for w in ["ui", "ux", "react", "dashboard", "component", "render"]):
            score += 10.0
        elif focus_domain == "devops" and any(w in content_lower for w in ["docker", "k8s", "kubernetes", "pipeline", "ci/cd", "aws", "deployment"]):
            score += 10.0
        elif focus_domain == "data_science" and any(w in content_lower for w in ["model", "pandas", "predict", "analytics", "churn", "training"]):
            score += 10.0
            
        ranked.append({
            "node": node,
            "score": round(score, 2),
            "direct_matches": direct_matches
        })

    # Sort nodes by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return [r["node"] for r in ranked]
