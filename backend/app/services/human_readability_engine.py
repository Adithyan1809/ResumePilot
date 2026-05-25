"""
Human Readability & Recruiter Friendliness Engine.

Programmatically assesses how natural, engaging, and professional the resume text is
for human recruiters, keeping a balance with raw ATS keyword density.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# List of bloated, weak corporate buzzwords that recruiters hate
BLOATED_BUZZWORDS = {
    "synergy", "synergized", "elite impact", "scale-resilient", "technical velocity",
    "agile leadership excellence", "results-oriented professional", "driven visionary",
    "outside the box", "go-getter", "team player", "paradigm shift", "disrupt", "disruptive",
    "thought leader", "next-gen", "cutting-edge", "game changer", "value-added", "empowered"
}

def calculate_readability_metrics(summary: str, experience_bullets: List[str]) -> Dict[str, Any]:
    """Calculate natural reading complexity and recruiter appeal.
    
    Returns a dict containing:
    - "human_readability_score": Score 0-100 indicating phrasing naturalness and readability.
    - "recruiter_friendliness_score": Score 0-100 indicating active tone, whitespace appeal, and lack of jargon.
    - "buzzword_count": Number of weak/bloated buzzwords found.
    - "suggestions": List of improvement suggestions.
    """
    suggestions = []
    
    # Compile text for analysis
    all_bullets = [b for b in experience_bullets if b]
    text_corpus = (summary or "") + " " + " ".join(all_bullets)
    text_lower = text_corpus.lower()
    
    # ── 1. Buzzword Density & Recruiter Score ──
    buzzwords_found = []
    for word in BLOATED_BUZZWORDS:
        # Use regex to find full-word matches
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            buzzwords_found.append(word)
            
    buzzword_penalty = len(buzzwords_found) * 8.0
    recruiter_score = 100.0 - buzzword_penalty
    
    if buzzwords_found:
        suggestions.append(
            f"Replace empty corporate jargon/buzzwords ({', '.join(buzzwords_found[:3])}) with specific, technically grounded action statements."
        )
        
    # ── 2. Active Phrasing / Action Verbs check ──
    # Check if experience bullets start with active verbs
    action_verb_count = 0
    passive_indicators = ["responsible for", "assisted", "helped", "supported", "involved in"]
    passive_count = 0
    
    for bullet in all_bullets:
        b_clean = bullet.strip().lower()
        if not b_clean:
            continue
        first_word = re.sub(r"[^\w]+", "", b_clean.split()[0]) if b_clean.split() else ""
        
        # High impact action verb matches
        if any(b_clean.startswith(v) for v in ["engineered", "developed", "designed", "implemented", "optimized", "built", "architected", "automated"]):
            action_verb_count += 1
            
        if any(passive in b_clean for passive in passive_indicators):
            passive_count += 1
            
    if len(all_bullets) > 0:
        action_ratio = action_verb_count / len(all_bullets)
        passive_ratio = passive_count / len(all_bullets)
        
        # Recruiter score improves with active tone, decays with passive structures
        recruiter_score += (action_ratio * 15.0) - (passive_ratio * 20.0)
    else:
        action_ratio = 1.0
        
    # ── 3. Sentence Naturalness & Human Readability (0-100) ──
    # Analyze sentence lengths. Very long sentences are hard to read; very short sound choppy.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text_corpus) if s.strip()]
    sentence_lengths = [len(s.split()) for s in sentences]
    
    readability_score = 85.0 # baseline
    
    if sentence_lengths:
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        # Penalize if sentences are too long on average (e.g. > 28 words)
        if avg_length > 28:
            readability_score -= 15.0
            suggestions.append("Some sentences are exceptionally long. Split them into shorter, punchier bullet points under 35 words.")
        elif avg_length < 8:
            readability_score -= 10.0
            suggestions.append("Your sentences are very short and choppy. Build out professional compound sentences to showcase technical context.")
            
        # Penalize for lack of sentence variety (highly repetitive sentence lengths)
        if len(sentence_lengths) > 2:
            import numpy as np
            std_dev = float(np.std(sentence_lengths))
            if std_dev < 3.0:
                readability_score -= 5.0 # monotonous sentence lengths
    else:
        avg_length = 0
        
    # ── 4. Keyword Stuffing Check ──
    # If the same technical word is repeated more than 5 times in experience and summary, it sounds robotic
    words_clean = re.findall(r"\b[a-zA-Z]{3,}\b", text_lower)
    word_frequencies = {}
    for w in words_clean:
        if w not in ["the", "and", "for", "with", "using", "automated", "designed", "developed", "engineered", "optimized", "system", "project"]:
            word_frequencies[w] = word_frequencies.get(w, 0) + 1
            
    stuffed_words = [w for w, freq in word_frequencies.items() if freq > 5]
    if stuffed_words:
        recruiter_score -= (len(stuffed_words) * 5.0)
        suggestions.append(
            f"Reduce repetitive usage of the keywords ({', '.join(stuffed_words[:3])}) across bullets to make your writing sound more natural."
        )
        
    # Bound scores
    human_readability_score = max(30.0, min(100.0, round(readability_score, 2)))
    recruiter_friendliness_score = max(30.0, min(100.0, round(recruiter_score, 2)))
    
    return {
        "human_readability_score": human_readability_score,
        "recruiter_friendliness_score": recruiter_friendliness_score,
        "buzzword_count": len(buzzwords_found),
        "suggestions": suggestions
    }
