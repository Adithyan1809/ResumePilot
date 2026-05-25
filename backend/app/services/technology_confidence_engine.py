"""
Technology Confidence Classifier.

Classifies all verified technologies by usage pattern (primary, repeated, dependency-only,
inferred, direct implementation evidence) and generates a numerical confidence score (0.0 to 1.0).
Only high-confidence technologies should be promoted in tailored summaries, skills, and bullets.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def calculate_technology_confidence(
    tech: str, 
    raw_text: str, 
    github_techs: List[str] = None
) -> float:
    """Calculate a numerical confidence score (0.0 to 1.0) for a verified technology."""
    if not tech:
        return 0.0
        
    tech_lower = tech.lower()
    raw_lower = (raw_text or "").lower()
    github_lower = [g.lower() for g in github_techs] if github_techs else []
    
    score = 0.0
    
    # 1. Direct parsed resume matches (Direct Implementation Evidence)
    pattern = rf"\b{re.escape(tech_lower)}\b"
    resume_matches = len(re.findall(pattern, raw_lower))
    
    if resume_matches > 0:
        # Repeated resume mentions translate to higher baseline confidence
        if resume_matches >= 3:
            score += 0.85
        elif resume_matches == 2:
            score += 0.75
        else:
            score += 0.60
            
    # 2. GitHub repository matches
    if tech_lower in github_lower:
        # If the tech matches a primary language or explicitly named tag
        score += 0.40
    else:
        # Check if it matches parts of repository details
        for git_item in github_lower:
            if tech_lower in git_item or git_item in tech_lower:
                score += 0.20
                break
                
    # 3. Handle primary standard language weights (Python, JS, SQL are basic and robust)
    if tech_lower in ["python", "javascript", "sql", "git", "github"]:
        score += 0.15
        
    # Cap score at 1.0 maximum
    final_score = round(min(1.0, score), 2)
    return final_score


def get_high_confidence_technologies(
    raw_text: str, 
    github_techs: List[str] = None, 
    min_confidence: float = 0.50
) -> List[str]:
    """Scans and extracts all whitelisted technologies with a confidence score above the threshold."""
    from app.services.technology_grounding_engine import extract_allowed_technologies
    
    allowed = extract_allowed_technologies(raw_text, github_techs)
    high_confidence = []
    
    for tech in allowed:
        score = calculate_technology_confidence(tech, raw_text, github_techs)
        if score >= min_confidence:
            high_confidence.append(tech)
            
    return high_confidence
