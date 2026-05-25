"""
Achievement Extraction & Pre-Hydration Engine.

Programmatically identifies weak, vague bullet points and pre-hydrates them
with candidate skills and active past-tense verb structures before the LLM rewrite pass.
Does NOT fabricate any numbers or metrics.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# List of weak verbs that indicate vague/weak achievements
WEAK_VERBS = {
    "worked on", "worked with", "helped", "assisted", "did", "handled", "doing",
    "responsible for", "participated in", "involved in", "support", "supported"
}

# Mapping of common nouns to generic active structures
VAGUE_BULLET_PATTERNS = [
    (r"\b(?:worked on|helped with|did)\s+attendance(?:\s+system)?\b", "Developed attendance modules incorporating automated IN/OUT logging"),
    (r"\b(?:worked on|helped with|did)\s+database(?:\s+management)?\b", "Designed and optimized database schemas to secure transactional integrity"),
    (r"\b(?:worked on|helped with|did)\s+frontend(?:\s+development)?\b", "Engineered responsive frontend interfaces to improve user interaction"),
    (r"\b(?:worked on|helped with|did)\s+backend(?:\s+development)?\b", "Designed scalable backend API services to handle core application pipelines"),
    (r"\b(?:worked on|helped with|did)\s+testing\b", "Implemented comprehensive automated test suites to ensure robust software quality"),
    (r"\b(?:worked on|helped with|did)\s+face recognition\b", "Engineered automated face recognition attendance pipelines to streamline identification"),
    (r"\b(?:worked on|helped with|did)\s+surveillance\b", "Designed intelligent surveillance parsing services to process live camera feeds"),
]

def extract_measurable_metrics(bullet: str) -> List[str]:
    """Extract measurable outcomes (percentages, currencies, quantities, scale stats)."""
    if not bullet:
        return []
    # Match percents, dollar figures, or numbers indicating scale (e.g. 50+, 10000, 90%)
    matches = re.findall(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b|\b\d+\+\b", bullet)
    return [m.strip() for m in matches if len(m) > 1]

def extract_technologies(bullet: str, skills_list: List[str]) -> List[str]:
    """Identify which of the candidate's skills are referenced in the bullet point."""
    if not bullet or not skills_list:
        return []
    
    bullet_lower = bullet.lower()
    found_tech = []
    
    # Flatten skill categories if colon-formatted (e.g. "Programming Languages: Python")
    flat_skills = []
    for s in skills_list:
        if ":" in str(s):
            parts = str(s).split(":", 1)[1]
            flat_skills.extend([x.strip() for x in re.split(r"[,;•|]+", parts)])
        else:
            flat_skills.append(str(s).strip())
            
    for skill in set(flat_skills):
        skill_clean = skill.strip()
        if not skill_clean or len(skill_clean) < 3:
            continue
        # Use word boundaries to check if the skill exists verbatim in the bullet
        pattern = r"\b" + re.escape(skill_clean.lower()) + r"\b"
        if re.search(pattern, bullet_lower):
            found_tech.append(skill_clean)
            
    return found_tech

def is_vague_bullet(bullet: str) -> Tuple[bool, str]:
    """Detect if a bullet point is vague, short, or passive."""
    if not bullet or not bullet.strip():
        return True, "empty"
        
    b = bullet.strip().lower()
    
    # Check length
    words = b.split()
    if len(words) < 6:
        return True, "too_short"
        
    # Check weak verbs
    for weak in WEAK_VERBS:
        if b.startswith(weak) or re.search(r"\b" + re.escape(weak) + r"\b", b):
            return True, "weak_verbs"
            
    # Check if lacks active impact phrases
    if not any(act in b for act in ["engineered", "developed", "designed", "optimized", "implemented", "reduced", "increased", "secured", "streamlined"]):
        # And also has no technologies
        return True, "no_action_verb"
        
    return False, ""

def pre_hydrate_bullet(bullet: str, skills_list: List[str]) -> str:
    """Pre-hydrate a vague bullet point with active verbs and matching candidate skills."""
    if not bullet:
        return ""
        
    is_weak, reason = is_vague_bullet(bullet)
    if not is_weak:
        return bullet # Return verbatim if it's already strong
        
    b_text = bullet.strip()
    
    # 1. Apply pattern mapping for common vague projects/roles
    for pattern, replacement in VAGUE_BULLET_PATTERNS:
        if re.search(pattern, b_text, re.IGNORECASE):
            b_text = replacement
            break
            
    # 2. Extract technologies from candidate's skills list to inject
    flat_skills = []
    for s in skills_list:
        if ":" in str(s):
            parts = str(s).split(":", 1)[1]
            flat_skills.extend([x.strip() for x in re.split(r"[,;•|]+", parts) if x.strip()])
        else:
            flat_skills.append(str(s).strip())
            
    # Find matching skills that the candidate has but aren't listed in the bullet
    available_techs = [s for s in flat_skills if s.lower() not in b_text.lower()][:2]
    
    # If the bullet is still very weak/short, structure it actively
    if b_text.lower() in ["worked on a project", "helped the team", "did website", "database work", "testing code"]:
        if len(available_techs) >= 2:
            b_text = f"Developed application pipelines using {available_techs[0]} and {available_techs[1]} to optimize performance."
        elif len(available_techs) == 1:
            b_text = f"Developed application components leveraging {available_techs[0]} to improve operational workflows."
        else:
            b_text = "Engineered custom software modules to optimize local performance and streamline code delivery."
    else:
        # Append available matching skills if none are referenced in the bullet
        existing_extracted = extract_technologies(b_text, skills_list)
        if not existing_extracted and available_techs:
            tech_suffix = f" leveraging {', '.join(available_techs)}"
            # Strip trailing periods to append tech suffix nicely
            if b_text.endswith("."):
                b_text = b_text[:-1] + tech_suffix + "."
            else:
                b_text = b_text + tech_suffix + "."
                
    # 3. Capitalize and ensure trailing period
    b_text = b_text[0].upper() + b_text[1:]
    if not b_text.endswith("."):
        b_text += "."
        
    logger.info(f"Hydrated bullet '{bullet}' ➔ '{b_text}'")
    return b_text
