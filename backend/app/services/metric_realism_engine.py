import logging
import re

logger = logging.getLogger(__name__)

def validate_metric_realism(bullets: list[str], target_level: str = "junior") -> list[str]:
    """
    Metric Realism Engine: Prevents unrealistic optimization metrics (e.g., 90% performance gains).
    Validates metrics against project scale and candidate level.
    """
    logger.info("Running Metric Realism Engine")
    
    validated_bullets = []
    
    # Patterns for finding percentages and multipliers
    percentage_pattern = re.compile(r'(\d{2,3})%')
    multiplier_pattern = re.compile(r'(\d{1,3})x')
    
    for bullet in bullets:
        text = str(bullet) if not isinstance(bullet, dict) else bullet.get("text", "")
        
        # If intern/junior, extremely high percentages or multipliers are suspicious
        if target_level in ["intern", "junior", "student"]:
            # Cap percentages at 40% for students unless context is trivial
            def cap_percentage(match):
                val = int(match.group(1))
                if val > 50:
                    return "significant" # Replace unrealistic number with descriptive word
                return match.group(0)
                
            def cap_multiplier(match):
                val = int(match.group(1))
                if val > 5:
                    return "substantially"
                return match.group(0)
                
            text = percentage_pattern.sub(cap_percentage, text)
            text = multiplier_pattern.sub(cap_multiplier, text)
            
        if isinstance(bullet, dict):
            bullet["text"] = text
            validated_bullets.append(bullet)
        else:
            validated_bullets.append(text)
            
    return validated_bullets
