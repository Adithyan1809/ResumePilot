"""
Semantic Bullet Deduplicator Engine.

Identifies and removes duplicate or near-duplicate sentences and repetitive syntactic structures
across all resume sections using SentenceTransformer embeddings and phrase overlap indicators.
"""

import re
import logging
from typing import List, Dict, Any

from app.services.semantic import calculate_semantic_similarity

logger = logging.getLogger(__name__)

async def calculate_bullet_similarity(b1: str, b2: str) -> float:
    """Compute deep contextual semantic similarity between two bullets."""
    if not b1 or not b2:
        return 0.0
    return await calculate_semantic_similarity(b1, b2)


def has_repetitive_structure(b1: str, b2: str) -> bool:
    """Detects if two bullets have near-identical verb/phrasing structures or heavy phrase overlap."""
    if not b1 or not b2:
        return False
        
    s1 = b1.lower().strip()
    s2 = b2.lower().strip()
    
    # 1. First verb/word identical check
    w1 = s1.split()[0] if s1.split() else ""
    w2 = s2.split()[0] if s2.split() else ""
    
    if w1 and w2 and w1 == w2:
        # Check if they share more than 3 consecutive words
        words1 = s1.split()
        words2 = s2.split()
        for i in range(len(words1) - 2):
            phrase = " ".join(words1[i:i+3])
            if phrase in s2:
                return True
                
    # 2. Token set Jaccard overlap check
    set1 = set(re.findall(r"\b\w+\b", s1))
    set2 = set(re.findall(r"\b\w+\b", s2))
    
    if not set1 or not set2:
        return False
        
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    jaccard = len(intersection) / len(union)
    
    # High token set overlap indicates duplicate structures
    if jaccard > 0.65:
        return True
        
    return False


async def deduplicate_section_bullets(bullets: List[str], unique_bullets: List[str], max_similarity: float = 80.0) -> List[str]:
    """Prunes near-duplicate bullets from a list, preserving the first (higher priority) one, against a global list."""
    if not bullets:
        return []
        
    kept_bullets = []
    for bullet in bullets:
        if not bullet:
            continue
            
        is_dup = False
        for existing in unique_bullets:
            # Check structure overlap
            if has_repetitive_structure(bullet, existing):
                is_dup = True
                break
                
            # Check deep semantic cosine similarity
            sim = await calculate_bullet_similarity(bullet, existing)
            if sim >= max_similarity:
                is_dup = True
                break
                
        if not is_dup:
            kept_bullets.append(bullet)
            unique_bullets.append(bullet)
            
    return kept_bullets


async def deduplicate_resume(sections: Dict[str, Any], max_similarity: float = 80.0) -> Dict[str, Any]:
    """Scans and deduplicates all experience, project, and summary blocks within the resume sections globally."""
    if not isinstance(sections, dict):
        return sections
        
    import copy
    cleaned = copy.deepcopy(sections)
    global_unique = []
    
    # Deduplicate Experience
    if "experience" in cleaned and isinstance(cleaned["experience"], list):
        for entry in cleaned["experience"]:
            if isinstance(entry, dict) and "bullets" in entry:
                entry["bullets"] = await deduplicate_section_bullets(entry["bullets"], global_unique, max_similarity)
                
    # Deduplicate Projects
    if "projects" in cleaned and isinstance(cleaned["projects"], list):
        for entry in cleaned["projects"]:
            if isinstance(entry, dict) and "description" in entry:
                entry["description"] = await deduplicate_section_bullets(entry["description"], global_unique, max_similarity)
                
    return cleaned
