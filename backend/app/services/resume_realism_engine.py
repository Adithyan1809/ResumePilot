"""
Resume Realism & Recruiter Appeal Engine.

Assesses the writing style of tailored resumes to ensure they read like high-quality,
human-written documents rather than robotic, keyword-stuffed AI templates.
Computes a composite realism score, recruiter readability index, and variety index.
"""

import re
from typing import List, Dict, Any

# Corporate buzzwords that signal low technical realism and prompt AI-like templates
BANNED_BUZZWORDS = {
    "synergy", "synergized", "elite impact", "scale-resilient", "technical velocity",
    "agile leadership excellence", "driven visionary", "thought leader", "next-gen",
    "cutting-edge", "game changer", "value-added", "empowered", "results-oriented professional",
    "leverage", "utilize", "harness", "outside the box", "paradigm shift"
}


def assess_resume_realism(
    summary: str, 
    experience: List[Dict[str, Any]], 
    projects: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Assess the realism and recruiter friendliness of the resume content.
    
    Returns:
    - realism_score: Float 0-100 (high is natural, low is AI-robotic)
    - recruiter_readability_score: Float 0-100 (high is readable, low is stuffed/choppy)
    - variety_score: Float 0-100 (sentence layout and starting verb diversity)
    - suggestions: List of specific feedback strings.
    """
    suggestions = []
    
    # 1. Collect all textual bullets
    bullets = []
    for entry in experience:
        bullets.extend([b for b in entry.get("bullets", []) if b])
    for entry in projects:
        desc = entry.get("description", [])
        if isinstance(desc, list):
            bullets.extend([b for b in desc if b])
        elif isinstance(desc, str):
            bullets.append(desc)
            
    full_text = (summary or "") + " " + " ".join(bullets)
    text_lower = full_text.lower()
    
    # ── 1. Buzzword Density & Realism Penalty ──
    buzzwords_found = []
    for word in BANNED_BUZZWORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            buzzwords_found.append(word)
            
    buzzword_penalty = len(buzzwords_found) * 10.0
    realism_score = 100.0 - buzzword_penalty
    
    if buzzwords_found:
        suggestions.append(
            f"Replace AI-generated corporate buzzwords ({', '.join(buzzwords_found[:3])}) with specific, direct engineering accomplishments."
        )
        
    # ── 2. Active Verb Repetition (Sentence Variety) ──
    first_verbs = []
    for b in bullets:
        words = b.strip().split()
        if words:
            verb = re.sub(r"[^\w]+", "", words[0]).lower()
            if len(verb) > 2:
                first_verbs.append(verb)
                
    verb_frequencies = {}
    for v in first_verbs:
        verb_frequencies[v] = verb_frequencies.get(v, 0) + 1
        
    repetitive_verbs = [v for v, count in verb_frequencies.items() if count >= 3]
    variety_penalty = len(repetitive_verbs) * 12.0
    variety_score = 100.0 - variety_penalty
    
    if repetitive_verbs:
        suggestions.append(
            f"Avoid starting multiple bullets with the exact same active verb ({', '.join(repetitive_verbs[:2])}). Use synonyms like Engineered, Designed, Optimized, or Implemented."
        )
        
    # ── 3. Colon-Heavy Keyword Stuffing ──
    # Checking if there are colons in the summary or excessive colon occurrences (excluding skills categories)
    colon_count = summary.count(":") if summary else 0
    if colon_count >= 2:
        realism_score -= 15.0
        suggestions.append("Simplify professional summary; avoid colon-heavy listings or keyword stuffing of technologies.")
        
    # ── 4. Recruiter Readability (Word Count and Clutter) ──
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", full_text) if s.strip()]
    sentence_lengths = [len(s.split()) for s in sentences]
    
    readability = 90.0 # baseline
    if sentence_lengths:
        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        if avg_len > 26:
            readability -= 20.0
            suggestions.append("Sentences are long on average. Break complex sentences into punchy bullet points under 30 words.")
        elif avg_len < 9:
            readability -= 10.0
            suggestions.append("Sentences are choppy. Connect short bullets into professional, compound technical statements.")
            
    # Standardize and bound scores
    realism_score = max(40.0, min(100.0, round(realism_score, 2)))
    variety_score = max(40.0, min(100.0, round(variety_score, 2)))
    recruiter_readability_score = max(45.0, min(100.0, round(readability, 2)))
    
    return {
        "realism_score": realism_score,
        "recruiter_readability_score": recruiter_readability_score,
        "variety_score": variety_score,
        "suggestions": suggestions
    }
