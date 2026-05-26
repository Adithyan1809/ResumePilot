import logging

logger = logging.getLogger(__name__)

def preserve_candidate_voice(bullets: list[str], seniority: str = "intern") -> list[str]:
    """
    Candidate Voice Engine: Preserves student/junior tone and authentic communication style.
    Reduces overly corporate, "AI-generated" dense phrasing while keeping technical depth.
    """
    logger.info(f"Running Candidate Voice Engine for seniority: {seniority}")
    
    refined_bullets = []
    
    corporate_buzzwords = [
        "leveraged", "spearheaded", "orchestrated", "synergized",
        "paradigm", "strategic", "cross-functional", "state-of-the-art"
    ]
    
    for bullet in bullets:
        text = str(bullet) if not isinstance(bullet, dict) else bullet.get("text", "")
        # Very basic mock logic for preservation - an LLM call would typically handle this
        # Here we just implement the rule engine structure
        
        # Replace common overly-corporate buzzwords with authentic alternatives
        text = text.replace("Leveraged", "Used").replace("leveraged", "used")
        text = text.replace("Spearheaded", "Led").replace("spearheaded", "led")
        text = text.replace("Orchestrated", "Built").replace("orchestrated", "built")
        text = text.replace("State-of-the-art", "Modern").replace("state-of-the-art", "modern")
        
        if isinstance(bullet, dict):
            bullet["text"] = text
            refined_bullets.append(bullet)
        else:
            refined_bullets.append(text)
            
    return refined_bullets
