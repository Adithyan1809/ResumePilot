"""
Sentence Integrity Validator.

Validates that tailored accomplishments and professional summaries are grammatically complete,
rejecting and healing dangling prepositions, partial technology fragments, and malformed conjunctions.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Banned partial technology fragments
PARTIAL_TECH_FRAGMENTS = {
    "pyth", "fastap", "postgre", "mongod", "dockerc", "kubernet"
}

# Dangling prepositions and conjunctions that make a sentence incomplete if located at the end
DANGLING_ENDWORDS = {
    "and", "or", "with", "for", "using", "to", "like", "by", "of", "from", "on"
}


def is_sentence_complete(sentence: str) -> bool:
    """Check if the sentence is complete and free of syntax corruption."""
    if not sentence or len(sentence.split()) < 3:
        return False
        
    s_lower = sentence.lower().strip()
    
    # 1. Reject partial tech words
    for frag in PARTIAL_TECH_FRAGMENTS:
        pattern = rf"\b{re.escape(frag)}\b"
        if re.search(pattern, s_lower):
            return False
            
    # 2. Reject malformed conjunctions like "andfor", "withfor", "using and"
    corruptions = ["andfor", "withfor", "using and", "and for to", "like."]
    if any(c in s_lower for c in corruptions):
        return False
        
    # 3. Reject dangling end words before punctuation
    # e.g., "Optimized database query latency using Python and."
    trimmed = re.sub(r"[.!?,\s\-]+$", "", s_lower).strip()
    words = trimmed.split()
    if words:
        last_word = words[-1]
        if last_word in DANGLING_ENDWORDS:
            return False
            
    # 4. Check for incomplete lists/placeholders
    placeholders = ["frameworks like.", "technologies such as.", "tools including."]
    if any(s_lower.endswith(p) for p in placeholders):
        return False
        
    return True


def heal_broken_sentence(text: str) -> str:
    """Programmatically heals and repairs broken or dangling sentence structures."""
    if not text:
        return ""
        
    healed = text.strip()
    
    # 1. Clean up spacing and double punctuation
    healed = re.sub(r"\s+", " ", healed)
    healed = healed.replace("andfor", "and").replace("withfor", "with").replace("using and", "using")
    
    # 2. Recursively peel trailing dangling prepositions and conjunctions
    while True:
        trimmed = re.sub(r"[.!?,\s\-–—,|]+$", "", healed).strip()
        words = trimmed.split()
        if not words:
            break
            
        last_word = words[-1].lower()
        if last_word in DANGLING_ENDWORDS or len(last_word) < 2:
            # Reconstruct the string without the last dangling word
            healed = " ".join(words[:-1])
            continue
        break
        
    # 3. Handle incomplete placeholder structures
    healed_lower = healed.lower()
    placeholders = {
        r"\bframeworks like\b": "frameworks",
        r"\btechnologies such as\b": "technologies",
        r"\btools including\b": "tools",
        r"\blibraries like\b": "libraries"
    }
    for pattern, replacement in placeholders.items():
        healed = re.sub(pattern, replacement, healed, flags=re.IGNORECASE)
        
    # 4. Final formatting: guarantee active starting verb capitalization and period
    healed = re.sub(r"\s+", " ", healed).strip()
    healed = re.sub(r"^[\s\-–—,|]+|[\s\-–—,|]+$", "", healed).strip()
    
    if len(healed.split()) < 4:
        # Fallback to standard grounded bullet if string became empty or too short
        return "Engineered robust software components to optimize system performance and reliability."
        
    if healed and not healed.endswith("."):
        healed += "."
        
    return healed[0].upper() + healed[1:] if healed else ""
