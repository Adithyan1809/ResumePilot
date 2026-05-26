"""
Resume Strategy Engine.
Allows candidates to orchestrate multiple targeted master tracks (Backend, AI/ML, Full Stack, Data Science)
from a single, shared whitelisted evidence graph database.
"""

from typing import List, Dict, Any

STRATEGY_TRACKS = {
    "backend": {
        "title_suffix": "Backend Systems Engineer",
        "focus_domain": "backend",
        "primary_techs": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "Kubernetes", "gRPC"],
        "summary_priorities": "Focus on API low-latency, database query indexing, microservice scalability, and Docker deployments."
    },
    "ai_ml": {
        "title_suffix": "Machine Learning Infrastructure Engineer",
        "focus_domain": "data_science",
        "primary_techs": ["Python", "PyTorch", "TensorFlow", "Pandas", "Scikit-Learn", "Hugging Face", "LLMs"],
        "summary_priorities": "Focus on custom model training, neural architectures, data ingestion pipelines, and ML serving optimizations."
    },
    "fullstack": {
        "title_suffix": "Full Stack Engineer",
        "focus_domain": "fullstack",
        "primary_techs": ["TypeScript", "React", "Next.js", "Node.js", "FastAPI", "TailwindCSS", "PostgreSQL"],
        "summary_priorities": "Focus on responsive dashboard designs, user state lifecycles, full-stack REST integrations, and deployment velocities."
    },
    "data_science": {
        "title_suffix": "Data Platform Analyst",
        "focus_domain": "data_science",
        "primary_techs": ["Python", "Pandas", "NumPy", "SQL", "Tableau", "Matplotlib", "Seaborn"],
        "summary_priorities": "Focus on complex analytical SQL queries, data pre-processing normalizations, statistical analytics, and metrics plotting."
    }
}


def configure_resume_strategy_track(
    strategy_track: str,
    original_skills: List[str]
) -> Dict[str, Any]:
    """Generates strategy mappings, target focus, and technology keyword targets for the chosen master track."""
    track_key = str(strategy_track).strip().lower()
    
    # Resolve aliases
    if "ai" in track_key or "ml" in track_key or "machine" in track_key:
        track_key = "ai_ml"
    elif "full" in track_key or "stack" in track_key:
        track_key = "fullstack"
    elif "data" in track_key or "analyst" in track_key:
        track_key = "data_science"
    else:
        track_key = "backend"
        
    strategy = STRATEGY_TRACKS[track_key]
    
    # Filter whitelisted skills from candidate's background matching the strategy
    cand_lower = [s.lower() for s in original_skills if s]
    matched_techs = [t for t in strategy["primary_techs"] if t.lower() in cand_lower]
    
    # Fallback to general techs if no overlap
    if not matched_techs:
        matched_techs = strategy["primary_techs"][:4]
        
    return {
        "strategy_track": track_key,
        "role_title_target": strategy["title_suffix"],
        "focus_domain": strategy["focus_domain"],
        "target_keywords": matched_techs,
        "summary_strategic_priorities": strategy["summary_priorities"]
    }
