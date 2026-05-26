import logging
import re

logger = logging.getLogger(__name__)

def humanize_resume_content(bullets: list[str]) -> list[str]:
    """
    Resume Humanization Engine: Reduces robotic, AI-polished phrasing.
    Detects and simplifies excessive corporate buzzwords, unnatural optimization language,
    and over-engineered wording to ensure strong recruiter readability.
    """
    logger.info("Running Resume Humanization Engine")
    
    humanized_bullets = []
    
    # Dictionary of AI-isms and overly complex phrases mapped to simpler alternatives
    replacements = {
        r"\boptimization architectures\b": "optimized systems",
        r"\bengineering scalable systems\b": "building scalable systems",
        r"\bdistributed orchestration paradigms\b": "distributed systems",
        r"\barchitected comprehensive solutions\b": "designed solutions",
        r"\bleveraging advanced methodologies\b": "using",
        r"\butilizing cutting-edge\b": "using modern",
        r"\bseamlessly integrated\b": "integrated",
        r"\bdrastically improved\b": "improved",
        r"\bspearheaded the development of\b": "led development of",
        r"\bsynergized\b": "collaborated on"
    }
    
    for bullet in bullets:
        text = str(bullet) if not isinstance(bullet, dict) else bullet.get("text", "")
        
        # Apply replacements
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            
        if isinstance(bullet, dict):
            bullet["text"] = text
            humanized_bullets.append(bullet)
        else:
            humanized_bullets.append(text)
            
    return humanized_bullets
