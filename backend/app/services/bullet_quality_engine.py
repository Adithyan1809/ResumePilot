"""
Bullet Point Quality Gating & Scoring Engine.

Programmatically grades and approves individual experience/project bullet points
based on action verb strength, technical specificity, length boundaries, and outcome metrics.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# Strong active verbs that are highly prioritized
STRONG_VERBS = {
    "engineered", "developed", "designed", "implemented", "optimized", "spearheaded",
    "architected", "integrated", "automated", "streamlined", "formulated", "enhanced",
    "coordinated", "executed", "collaborated", "constructed", "orchestrated", "deployed",
    "compiled", "resolved"
}

def grade_bullet_point(bullet: str, target_keywords: List[str] = None) -> Dict[str, Any]:
    """Calculate a detailed quality score from 0.0 to 100.0 for a single bullet point.
    
    Grading Dimensions:
    1. Action Verb Strength (25%) - Starts with a strong past-tense action verb.
    2. Specificity & Readability (25%) - Length boundaries (ideally 10 to 35 words).
    3. Keyword Density (20%) - Presence of technical keywords/tools.
    4. Outcome & Scale Impact (20%) - Measurable outcomes (numbers, stats, scale metrics).
    5. Formatting Cleanliness (10%) - Capitalized, ends with period, no duplicate tags.
    """
    if not bullet or not bullet.strip():
        return {"score": 0.0, "approved": False, "breakdown": {}}
        
    b = bullet.strip()
    words = b.split()
    word_count = len(words)
    b_lower = b.lower()
    
    # ── 1. Action Verb Strength (25%) ──
    verb_score = 0.0
    first_word = words[0].lower() if words else ""
    # Strip any ending punctuation from first word
    first_word_clean = re.sub(r"[^\w]+", "", first_word)
    
    if first_word_clean in STRONG_VERBS:
        verb_score = 25.0
    elif first_word_clean.endswith("ed") or first_word_clean.endswith("ing"):
        verb_score = 15.0 # decent verb but not in our high-impact list
    elif first_word_clean:
        verb_score = 5.0 # weak or passive verb
        
    # ── 2. Specificity & Readability (25%) ──
    # Ideal range is 10 to 35 words. Flexible range of 8 to 40.
    length_score = 0.0
    if 10 <= word_count <= 35:
        length_score = 25.0
    elif 8 <= word_count <= 40:
        length_score = 15.0
    elif word_count < 8:
        length_score = 5.0 # too short/shallow
    else:
        length_score = 5.0 # too long/robotic
        
    # ── 3. Keyword Density (20%) ──
    keyword_score = 0.0
    if target_keywords:
        target_set = {k.lower().strip() for k in target_keywords if k}
        matched_kws = [k for k in target_set if re.search(r"\b" + re.escape(k) + r"\b", b_lower)]
        if len(matched_kws) >= 2:
            keyword_score = 20.0
        elif len(matched_kws) == 1:
            keyword_score = 10.0
    else:
        # Heuristically count capital words inside the bullet that are likely techs (excluding first word)
        tech_cap_matches = re.findall(r"\b[A-Z][a-zA-Z0-9\+\#\.]*\b", b)
        other_caps = [w for w in tech_cap_matches if w.lower() != first_word_clean]
        if len(other_caps) >= 2:
            keyword_score = 20.0
        elif len(other_caps) == 1:
            keyword_score = 10.0
            
    # ── 4. Outcome & Scale Impact (20%) ──
    impact_score = 0.0
    # Search for numbers, percentages, scales, or key impact clauses like "reducing", "optimizing", "securing"
    has_metrics = bool(re.search(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b|\b\d+\+\b", b))
    has_impact_clause = any(w in b_lower for w in ["resulting in", "reducing", "securing", "optimizing", "reducing latency", "supporting", "streamlining"])
    
    if has_metrics and has_impact_clause:
        impact_score = 20.0
    elif has_metrics or has_impact_clause:
        impact_score = 12.0
        
    # ── 5. Formatting Cleanliness (10%) ──
    formatting_score = 0.0
    starts_capital = b[0].isupper() if b else False
    ends_period = b.endswith(".")
    no_quote_leak = not any(q in b for q in ["'", '"', '`'])
    
    if starts_capital:
        formatting_score += 3.0
    if ends_period:
        formatting_score += 4.0
    if no_quote_leak:
        formatting_score += 3.0
        
    total_score = verb_score + length_score + keyword_score + impact_score + formatting_score
    total_score = round(total_score, 2)
    
    # Gate approval at a score of 50.0
    approved = total_score >= 50.0
    
    return {
        "score": total_score,
        "approved": approved,
        "breakdown": {
            "verb_strength": verb_score,
            "length_readability": length_score,
            "keyword_density": keyword_score,
            "measurable_impact": impact_score,
            "formatting_cleanliness": formatting_score
        }
    }

def score_experience_bullets(bullets: List[str], target_keywords: List[str] = None) -> Tuple[float, List[Dict[str, Any]]]:
    """Score a full collection of bullets and identify weak entries."""
    if not bullets:
        return 0.0, []
        
    results = []
    total_earned = 0.0
    
    for b in bullets:
        res = grade_bullet_point(b, target_keywords)
        results.append(res)
        total_earned += res["score"]
        
    avg_score = round(total_earned / len(bullets), 2)
    return avg_score, results
