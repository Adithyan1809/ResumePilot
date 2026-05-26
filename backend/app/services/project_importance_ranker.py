import logging

logger = logging.getLogger(__name__)

def rank_projects_by_importance(projects: list[dict], jd_text: str = "", identity: str = "software_engineering") -> list[dict]:
    """
    Project Importance Ranker: Ranks projects using technical depth, JD relevance,
    engineering complexity, and measurable outcomes. Ensures the strongest projects appear first.
    """
    logger.info("Running Project Importance Ranker")
    
    if not projects:
        return []
        
    jd_lower = jd_text.lower()
    
    for project in projects:
        score = 0.0
        
        # 1. Technical Depth (number of valid technologies)
        techs = project.get("technologies", [])
        score += len(techs) * 0.5
        
        # 2. JD Relevance (how many project techs match JD)
        for tech in techs:
            if tech.lower() in jd_lower:
                score += 2.0
                
        # 3. Measurable Outcomes (presence of numbers/%/$)
        bullets = project.get("bullets", [])
        for bullet in bullets:
            text = str(bullet) if not isinstance(bullet, dict) else bullet.get("text", "")
            if any(char.isdigit() for char in text) or "%" in text or "$" in text:
                score += 1.0
                
        # 4. Identity alignment
        title = project.get("title", "").lower()
        if identity.replace("_", " ") in title or identity.split("_")[0] in title:
            score += 3.0
            
        project["importance_score"] = score
        
    # Sort descending by importance_score
    ranked_projects = sorted(projects, key=lambda x: x.get("importance_score", 0.0), reverse=True)
    
    return ranked_projects
