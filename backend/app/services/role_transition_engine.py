"""
Role Transition Engine.

Assists career-pivoting candidates by framing their resume accomplishments, professional summaries,
and skills in a highly realistic, truth-preserving manner that highlights core software engineering 
fundamentals and natural growth interest rather than faking tech stack expertise.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def adjust_summary_for_transition(
    summary: str, 
    target_role: str, 
    allowed_techs: List[str]
) -> str:
    """Modifies the professional summary to show transition potential honestly.
    Emphasizes backend APIs, scalability, database design, and mentions frontend learning interest naturally.
    """
    if not summary:
        return ""
        
    role_lower = (target_role or "backend").lower()
    is_frontend_target = any(w in role_lower for w in ["front", "ui", "ux", "full", "web", "react"])
    
    allowed_lower = [t.lower() for t in allowed_techs if t]
    has_frontend_tech = any(w in allowed_lower for w in ["react", "next.js", "nextjs", "vue", "angular", "typescript", "tailwind", "css", "html", "javascript"])
    
    if is_frontend_target and not has_frontend_tech:
        # Candidate lacks frontend tech but is applying to a frontend/fullstack role. 
        # Apply the transition mindset!
        tech_list = []
        for t in ["Python", "SQL", "FastAPI", "Django", "Flask", "PostgreSQL", "MySQL", "Redis", "Docker", "Git"]:
            if t.lower() in allowed_lower:
                tech_list.append(t)
                
        tech_str = ", ".join(tech_list[:4]) if tech_list else "Python, SQL, and Git"
        
        transition_summary = (
            f"Software Engineer with a robust foundation in building backend APIs, "
            f"databases, and scalable systems using {tech_str}. Demonstrates strong engineering "
            f"fundamentals and systems design, with a dedicated interest and growing focus on expanding "
            f"expertise into frontend architectures like React and modern web development."
        )
        return transition_summary
        
    return summary

def adjust_bullet_for_transition(
    bullet: str,
    target_role: str,
    allowed_techs: List[str]
) -> str:
    """Transforms bullet points to ensure that backend developers transitioning to frontend
    highlight the API contracts, data models, and dashboard feeds they created instead of fabricating React/Next.js UI.
    """
    if not bullet:
        return ""
        
    bullet_lower = bullet.lower()
    role_lower = (target_role or "backend").lower()
    is_frontend_target = any(w in role_lower for w in ["front", "ui", "ux", "full", "web", "react"])
    
    allowed_lower = [t.lower() for t in allowed_techs if t]
    has_frontend_tech = any(w in allowed_lower for w in ["react", "next.js", "nextjs", "vue", "angular", "typescript", "tailwind", "css", "html", "javascript"])
    
    if is_frontend_target and not has_frontend_tech:
        # If the LLM has injected a fake React or Next.js claim, intercept and map it back to a scalable API feed.
        if any(w in bullet_lower for w in ["react", "next.js", "nextjs", "tailwind", "typescript", "webpack", "css", "ui"]):
            base_tech = "FastAPI" if "fastapi" in allowed_lower else "Flask" if "flask" in allowed_lower else "Python" if "python" in allowed_lower else "backend services"
            db_tech = "PostgreSQL" if "postgresql" in allowed_lower else "SQLite" if "sqlite" in allowed_lower else "databases"
            
            pivoted = (
                f"Designed and optimized web-accessible REST API feeds using {base_tech} and {db_tech} "
                f"to power responsive interfaces with fast data serialization and stable network endpoints."
            )
            return pivoted
            
    return bullet
