import logging

logger = logging.getLogger(__name__)

def establish_engineering_identity(profile_evidence: dict, target_jd: str) -> dict:
    """
    Engineering Identity Engine: Builds a coherent narrative (e.g., 'Backend Engineer', 'AI Systems Engineer').
    Shapes the summary and helps prioritize projects later.
    """
    logger.info("Running Engineering Identity Engine")
    
    # Analyze flat skills to detect primary identity
    skills = profile_evidence.get("skills", {})
    flat_skills = []
    if isinstance(skills, list):
        flat_skills = skills
    elif isinstance(skills, dict):
        for k, v in skills.items():
            flat_skills.extend(v)
            
    flat_skills_lower = [s.lower() for s in flat_skills]
    
    # Heuristics for identity
    identity_map = {
        "backend": ["python", "java", "go", "node.js", "postgresql", "api", "docker", "kubernetes", "aws", "microservices"],
        "ai_ml": ["pytorch", "tensorflow", "scikit-learn", "llm", "machine learning", "nlp", "computer vision", "pandas"],
        "frontend": ["react", "vue", "angular", "typescript", "javascript", "css", "html", "tailwind"],
        "data_engineering": ["spark", "hadoop", "airflow", "kafka", "etl", "snowflake", "redshift"]
    }
    
    scores = {k: 0 for k in identity_map.keys()}
    
    for identity, keywords in identity_map.items():
        for skill in flat_skills_lower:
            if skill in keywords or any(kw in skill for kw in keywords):
                scores[identity] += 1
                
    # Determine primary identity
    primary_identity = max(scores, key=scores.get) if any(scores.values()) else "software_engineering"
    
    logger.info(f"Detected Engineering Identity: {primary_identity}")
    
    return {
        "primary_identity": primary_identity,
        "identity_scores": scores,
        "narrative_focus": f"Specializing in {primary_identity.replace('_', ' ')}."
    }
