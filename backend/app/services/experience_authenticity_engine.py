"""
Experience Authenticity Engine.

Verifies that all job roles and technical metrics align with the candidate's actual source resume
and realistically match student/intern levels rather than fabricating exaggerated seniority.
"""

import re
from typing import Dict, Any, List

def gating_experience_role_authenticity(role: str, is_student: bool = True) -> str:
    """Ensures that tailored job roles reflect realistic student experience levels,
    preventing fabricated senior titles unless explicitly present in the source.
    """
    if not role:
        return "Software Engineer Intern"
        
    if not is_student:
        return role
        
    role_lower = role.lower()
    
    # If the candidate is a student/intern but role contains a senior designation
    is_intern = any(w in role_lower for w in ["intern", "trainee", "fellow", "co-op", "student", "assistant"])
    
    if not is_intern:
        senior_mappings = {
            r"\btechnical lead\b": "Technical Lead Intern",
            r"\btech lead\b": "Technical Lead Intern",
            r"\blead architect\b": "Software Engineering Intern",
            r"\bsystems architect\b": "Systems Engineering Intern",
            r"\bsenior software engineer\b": "Software Engineering Intern",
            r"\bsenior engineer\b": "Software Engineering Intern",
            r"\bsenior developer\b": "Software Engineering Intern",
            r"\blead engineer\b": "Software Engineering Intern",
            r"\bmanager\b": "Software Engineering Intern",
            r"\bdirector\b": "Software Engineering Intern",
            r"\bvp of engineering\b": "Software Engineering Intern",
            r"\bhead of\b": "Software Engineering Intern"
        }
        
        for pattern, replacement in senior_mappings.items():
            if re.search(pattern, role_lower):
                return re.sub(pattern, replacement, role, flags=re.IGNORECASE).strip()
                
        # If it contains any other lead/architect/manager words, append Intern
        if any(kw in role_lower for kw in ["lead", "architect", "manager", "head"]):
            return f"{role} Intern"
            
    return role


def verify_bullet_authenticity(bullet: str, source_text: str) -> str:
    """Inspects a tailored bullet point for numeric metrics and verifies that every metric
    (percentage, dollar sign, or large numbers) exists in the original source resume verbatim.
    If it is fabricated (hallucinated), it programmatically strips the fake metric to preserve realism.
    """
    if not bullet:
        return ""
        
    source_lower = (source_text or "").lower()
    
    # Eagerly match dollar signs first, then plus-terminated numbers, then percentages/general numbers
    # Avoid capturing trailing punctuation like commas or periods
    metrics = re.findall(r"\$\s*\d+(?:[\d,\.]*\d)?|(?<!\w)\d+\+|(?<!\w)\d+(?:[\d,\.]*\d)?%?", bullet)
    
    cleansed_bullet = bullet
    for m in metrics:
        if len(m) > 1:
            is_check_worthy = False
            if "%" in m or "$" in m:
                is_check_worthy = True
            elif m.isdigit() and int(m) > 5 and len(m) < 4:
                is_check_worthy = True
            elif "+" in m:
                is_check_worthy = True
                
            if is_check_worthy:
                if m.lower() not in source_lower:
                    m_esc = re.escape(m)
                    # Cleanly replace metric with preceding action connector words (e.g. "by 45%", "saving $10,000")
                    patterns = [
                        rf"(?<!\w)(?:saving|saved|generating|generated|increased|increasing|reduced|reducing|improved|improving|managing|managed|by|of|to)\s+{m_esc}(?!\w)",
                        m_esc
                    ]
                    for pat in patterns:
                        cleansed_bullet = re.sub(pat, "", cleansed_bullet, flags=re.IGNORECASE)
                        
    # Clean up spacing, trailing punctuation, double spaces, and clean margins
    cleansed_bullet = re.sub(r"\s+", " ", cleansed_bullet)
    cleansed_bullet = re.sub(r",\s*,", ",", cleansed_bullet)
    cleansed_bullet = re.sub(r",\s*\.", ".", cleansed_bullet)
    cleansed_bullet = re.sub(r"\s+,\s*", ", ", cleansed_bullet)
    cleansed_bullet = re.sub(r"\s+\.\s*$", ".", cleansed_bullet)
    
    cleansed_bullet = re.sub(r"^[\s\-–—,|]+|[\s\-–—,|]+$", "", cleansed_bullet).strip()
    
    if cleansed_bullet and not cleansed_bullet.endswith("."):
        cleansed_bullet += "."
        
    return cleansed_bullet[0].upper() + cleansed_bullet[1:] if cleansed_bullet else ""
