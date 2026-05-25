"""
Bullet Realism & Internship Calibrator Engine.

Evaluates bullet points for engineering credibility, internship appropriateness,
and technical realism, scaling down exaggerated enterprise claims and stripping corporate buzzwords.
"""

import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# List of hyper-inflated enterprise buzzwords to scale down
EXAGGERATED_KEYWORDS = {
    r"\bglobal enterprise\b": "software systems",
    r"\bmulti-region AWS\b": "cloud deployment",
    r"\b10M\+\s*(?:active\s*)?users\b": "optimized endpoints",
    r"\bmillion(?:s of)?\s*(?:active\s*)?users\b": "high-concurrency systems",
    r"\bVP of Engineering\b": "Software Engineering Intern",
    r"\bdivision budgets\b": "project components",
    r"\barchitected global\b": "optimized modular",
}

# List of redundant buzzwords to strip
BUZZWORDS = [
    "scale-resilient", "elite impact", "technical velocity", "agile leadership excellence", 
    "disruptive innovation", "world-class solutions", "bleeding-edge", "synergy"
]


def evaluate_bullet_realism(bullet: str, is_student: bool = True) -> Dict[str, Any]:
    """Evaluates the credibility and realism of a tailored accomplishment (0-100 score)."""
    if not bullet:
        return {"realism_score": 100.0, "approved": True, "suggestions": []}
        
    s_lower = bullet.lower()
    score = 100.0
    suggestions = []
    
    # 1. Audit enterprise scaling exaggeration
    for pattern in EXAGGERATED_KEYWORDS.keys():
        if re.search(pattern, bullet, flags=re.IGNORECASE):
            score -= 15.0
            suggestions.append(f"Scale down enterprise claim matching '{pattern}' for internship suitability.")
            
    # 2. Audit hyper-inflated metrics (e.g. >95% query improvement or saving millions of dollars)
    metrics_perc = re.findall(r"(\d+)%", bullet)
    for p in metrics_perc:
        if int(p) > 90:
            score -= 10.0
            suggestions.append("Verify percentage metric; values exceeding 90% appear exaggerated to recruiters.")
            
    # 3. Audit corporate buzzword clutter
    for word in BUZZWORDS:
        if word in s_lower:
            score -= 8.0
            suggestions.append(f"Remove fluff buzzword '{word}' to enhance technical realism.")
            
    return {
        "realism_score": max(0.0, score),
        "approved": score >= 80.0,
        "suggestions": suggestions
    }


def heal_exaggerated_bullet(bullet: str) -> str:
    """Scales down exaggerated enterprise claims into realistic, recruiter-friendly achievements."""
    if not bullet:
        return ""
        
    healed = bullet
    
    # 1. Cleanse high-level executive claims
    for pattern, replacement in EXAGGERATED_KEYWORDS.items():
        healed = re.sub(pattern, replacement, healed, flags=re.IGNORECASE)
        
    # 2. Cleanse buzzwords
    for word in BUZZWORDS:
        healed = re.sub(rf"\b{re.escape(word)}\b\s*,?\s*", "", healed, flags=re.IGNORECASE)
        
    # Clean up double spacing and dangling separators
    healed = re.sub(r"\s+", " ", healed)
    healed = re.sub(r",\s*,", ",", healed)
    healed = re.sub(r",\s*\.", ".", healed)
    healed = re.sub(r"\s+,\s*", ", ", healed)
    healed = re.sub(r"\s+\.\s*$", ".", healed)
    healed = re.sub(r"^[\s\-–—,|]+|[\s\-–—,|]+$", "", healed).strip()
    
    if healed and not healed.endswith("."):
        healed += "."
        
    return healed[0].upper() + healed[1:] if healed else ""
