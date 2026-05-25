"""
Role Transferability Engine.

Handles realistic career/role transitions (e.g. backend developer applying to frontend role)
by emphasizing transferable systems fundamentals and growth interest instead of fabricating experience.
"""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)

def convert_summary_for_transferability(
    summary: str, 
    target_role: str, 
    allowed_techs: List[str]
) -> str:
    """If the target role is frontend/full-stack but the candidate lacks direct frontend technologies,
    converts summary into a professional transferable systems statement with growing frontend interest.
    """
    if not summary:
        return ""
        
    role_lower = (target_role or "").lower()
    is_frontend_target = any(w in role_lower for w in ["front", "ui", "ux", "full", "web", "react"])
    
    # Check if candidate possesses direct frontend skills
    allowed_lower = [t.lower() for t in allowed_techs]
    has_frontend_skills = any(w in allowed_lower for w in ["react", "next.js", "nextjs", "vue", "angular", "typescript", "tailwind", "css", "html", "javascript"])
    
    if is_frontend_target and not has_frontend_skills:
        # Candidate is backend/data science applying for frontend/fullstack. Do not fabricate frontend projects!
        # Pivot to systems fundamentals & transferable skills.
        found_techs = []
        for tech in ["python", "sql", "fastapi", "django", "flask", "postgresql", "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "aws", "git"]:
            for allowed in allowed_techs:
                if tech == allowed.lower() and allowed.title() not in found_techs:
                    found_techs.append(allowed)
                    
        tech_str = ", ".join(found_techs[:4]) if found_techs else "Python, SQL, and Git"
        
        transfer_summary = (
            f"Software engineering undergraduate with hands-on experience building robust backend APIs, "
            f"databases, and scalable systems using {tech_str}. Strong foundation in computer science "
            f"principles, with a keen interest in expanding technical expertise into modern frontend development "
            f"frameworks like React and Next.js."
        )
        return transfer_summary
        
    return summary


def convert_bullet_for_transferability(
    bullet: str, 
    target_role: str, 
    allowed_techs: List[str]
) -> str:
    """Pivots a bullet point to showcase transferable engineering principles instead of fabricated stack experience."""
    if not bullet:
        return ""
        
    role_lower = (target_role or "").lower()
    is_frontend_target = any(w in role_lower for w in ["front", "ui", "ux", "full", "web", "react"])
    
    allowed_lower = [t.lower() for t in allowed_techs]
    has_frontend_skills = any(w in allowed_lower for w in ["react", "next.js", "nextjs", "vue", "angular", "typescript", "tailwind", "css", "html", "javascript"])
    
    # If the LLM fabricated React/Next.js optimization claims for a backend developer, pivot it back to systems.
    if is_frontend_target and not has_frontend_skills:
        bullet_lower = bullet.lower()
        if "react" in bullet_lower or "next.js" in bullet_lower or "nextjs" in bullet_lower or "webpack" in bullet_lower:
            # Reconstruct the bullet as a clean, transferable systems API / web architecture bullet
            tech_word = "FastAPI" if "fastapi" in allowed_lower else "Python" if "python" in allowed_lower else "web frameworks"
            db_word = "PostgreSQL" if "postgresql" in allowed_lower else "Postgres" if "postgres" in allowed_lower else "databases"
            
            pivoted = (
                f"Developed scalable web interface components and REST APIs using {tech_word} "
                f"and {db_word} to ensure high-performance data serialization and stable endpoints."
            )
            return pivoted
            
    return bullet
