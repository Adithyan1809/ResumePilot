import logging
import re

logger = logging.getLogger(__name__)

def calibrate_experience_level(bullets: list[str], target_level: str = "junior") -> list[str]:
    """
    Experience Level Calibration Engine: Ensures bullets match the candidate's level (student/intern/junior).
    Prevents staff-level claims, exaggerated enterprise optimization, and unrealistic architecture ownership.
    """
    logger.info(f"Running Experience Level Calibration Engine for level: {target_level}")
    
    calibrated_bullets = []
    
    # Overly senior claims that should be toned down for junior/intern levels
    senior_claims = [
        (r"\b(led|directed) enterprise-scale\b", "contributed to enterprise-scale"),
        (r"\barchitected (the )?entire\b", "assisted in designing"),
        (r"\bmanaged a team of\b", "collaborated with a team of"),
        (r"\bowned the delivery of\b", "contributed to the delivery of"),
        (r"\bdrove company-wide\b", "participated in company-wide")
    ]
    
    for bullet in bullets:
        text = str(bullet) if not isinstance(bullet, dict) else bullet.get("text", "")
        
        if target_level in ["intern", "junior", "student"]:
            for pattern, replacement in senior_claims:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                
        if isinstance(bullet, dict):
            bullet["text"] = text
            calibrated_bullets.append(bullet)
        else:
            calibrated_bullets.append(text)
            
    return calibrated_bullets
