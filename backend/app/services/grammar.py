"""
Grammar, tense, and structural polishing service for resume sections.
"""
import json
import logging
import re
from typing import Any, Dict, List

from app.services.ai_engine import _call_llm_completion

logger = logging.getLogger(__name__)

GRAMMAR_POLISH_PROMPT = """
You are a meticulous professional resume editor. Correct and polish the following resume bullet points.

Your tasks are:
1. Ensure perfect grammatical correctness, proper punctuation, and crisp sentence structure.
2. Enforce strict tense consistency:
   - For PAST experience/roles, every bullet point must start with a strong past-tense action verb (e.g., "Optimized", "Designed", "Built", "Implemented").
   - For CURRENT experience/roles, bullets should start with present-tense action verbs (e.g., "Optimize", "Design", "Build") or active gerunds ("Optimizing", "Designing").
3. Convert passive, awkward, or mixed phrases into punchy, parallel structures.
   - Example of awkward mix: "Optimized system latency by 20% and supports 90+ camera feeds."
   - Proper replacement: "Optimized system latency by 20%, supporting 90+ camera feeds."
4. Eliminate weak corporate filler words and weak start verbs (e.g., change "helped build" to "Engineered", "did" to "Implemented", "worked on" to "Developed").
5. Do not invent, hallucinate, or add any new achievements, metrics, or technologies. Keep the factual details exactly the same.
6. Make sure every bullet point ends with a period.

Input Bullet Points (JSON list):
{content}

Return a JSON object matching this exact structure:
{{
    "polished_bullets": [
        "First polished bullet point",
        "Second polished bullet point"
    ]
}}
"""


async def polish_bullets(bullets: List[str], dates: str) -> List[str]:
    """Polish a list of bullet points for grammar, tense consistency, and structural parallelism.

    Args:
        bullets: List of raw bullet point strings.
        dates: Date string to determine tense.

    Returns:
        List of polished bullet point strings.
    """
    if not bullets:
        return []

    # Clean empty/whitespace bullets
    bullets = [b.strip() for b in bullets if b.strip()]
    if not bullets:
        return []

    # Deduplicate repeated bullets
    seen = set()
    deduped_bullets = []
    for b in bullets:
        b_lower = b.lower()
        if b_lower not in seen:
            deduped_bullets.append(b)
            seen.add(b_lower)

    # Determine if past or present role
    is_past = True
    if dates and "present" in dates.lower():
        is_past = False

    try:
        content_json = json.dumps(deduped_bullets)
        role_type = "PAST role (enforce past tense verbs like Optimized, Designed)" if is_past else "CURRENT role (enforce present tense verbs like Optimize, Design)"
        
        prompt = GRAMMAR_POLISH_PROMPT.format(content=content_json)
        # Append target tense expectation
        prompt += f"\nNote: The target is a {role_type}."

        logger.info(f"Polishing {len(deduped_bullets)} bullets using LLM grammar checker...")
        result = await _call_llm_completion(
            messages=[
                {"role": "system", "content": "You are a professional resume editor."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            json_mode=True,
        )
        
        data = json.loads(result)
        polished = data.get("polished_bullets", [])
        if isinstance(polished, list) and len(polished) > 0:
            # Basic validation: ensure we didn't drop all bullets
            return [str(b).strip() for b in polished if b]
    except Exception as exc:
        logger.error(f"LLM grammar polishing failed: {exc}. Falling back to standard heuristic cleaning.")

    # Rule-based fallback if LLM call fails
    return [_heuristic_bullet_clean(b, is_past) for b in deduped_bullets]


def _heuristic_bullet_clean(bullet: str, is_past: bool) -> str:
    """Fallback rule-based cleaning to fix basic starting verbs and punctuation."""
    b = bullet.strip()
    if not b:
        return ""

    # Replace weak start verbs
    replacements = {
        "worked on": "Developed",
        "helped build": "Engineered",
        "did": "Implemented",
        "assisted in": "Supported",
        "handled": "Managed",
    }
    
    b_lower = b.lower()
    for weak, strong in replacements.items():
        if b_lower.startswith(weak):
            b = strong + b[len(weak):]
            break

    # Fix mixed supports/optimized starting tense mismatch (like "Optimized ... and supports")
    if is_past:
        # e.g., replace "and supports" with ", supporting"
        b = re.sub(r"\band supports\b", ", supporting", b, flags=re.IGNORECASE)
        b = re.sub(r"\band implements\b", ", implementing", b, flags=re.IGNORECASE)
        b = re.sub(r"\band manages\b", ", managing", b, flags=re.IGNORECASE)
    else:
        b = re.sub(r"\boptimized\b", "optimize", b, flags=re.IGNORECASE)
        b = re.sub(r"\bdesigned\b", "design", b, flags=re.IGNORECASE)

    # Capitalize first letter
    if len(b) > 0:
        b = b[0].upper() + b[1:]

    # Ensure ending period
    if b and b[-1] not in [".", "!", "?"]:
        b += "."

    return b
