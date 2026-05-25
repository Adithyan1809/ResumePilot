"""
Recruiter Simulation Engine.

Simulates real recruiter scanning behaviors to grade formatting, 6-second readability,
technical clarity, skills visibility, and generate shortlist likelihood metrics.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def simulate_recruiter_scan(
    sections: Dict[str, Any], 
    job_description: str = ""
) -> Dict[str, Any]:
    """Grade the resume from a simulated recruiter's perspective, scoring readability and shortlist potential."""
    if not sections or not isinstance(sections, dict):
        return {"recruiter_readability_score": 50.0, "shortlist_likelihood": "Medium", "warnings": []}
        
    warnings = []
    
    # 1. 6-Second Readability Evaluation (sentence lengths & layout balance)
    summary_text = str(sections.get("summary", ""))
    summary_words = len(summary_text.split())
    
    readability_score = 100.0
    if summary_words > 80:
        readability_score -= 15.0
        warnings.append("Professional Summary is too long for a 6-second scan. Shorten to 50-70 words.")
    elif summary_words < 25 and summary_words > 0:
        readability_score -= 10.0
        warnings.append("Professional Summary is too brief. Expand to 3 structured lines.")
        
    # 2. Experience Density Evaluation
    experience = sections.get("experience", []) or []
    if len(experience) > 3:
        warnings.append("Over 3 work experience entries might push the resume to 2 pages. Restructure to 2-3 key roles.")
        
    for idx, entry in enumerate(experience):
        bullets = entry.get("bullets", []) or []
        if len(bullets) > 5:
            readability_score -= 10.0
            warnings.append(f"Work Experience entry {idx+1} has too many bullets ({len(bullets)}). Recruiter suggest limit is 5.")
        elif len(bullets) < 2:
            warnings.append(f"Work Experience entry {idx+1} has too few bullets. Provide at least 2 key achievements.")
            
    # 3. Technical Clarity & Skills Visibility
    skills = sections.get("skills", []) or []
    if not skills:
        readability_score -= 20.0
        warnings.append("Missing Skills section. High priority warning for technical recruiters.")
    elif len(skills) > 8:
        warnings.append("Skills section contains too many categories. Compress to 5-7 standardized groups.")
        
    # 4. Shortlist Likelihood Mapping
    final_readability = max(0.0, readability_score)
    
    if final_readability >= 85.0 and len(warnings) <= 2:
        shortlist_likelihood = "High"
    elif final_readability >= 65.0:
        shortlist_likelihood = "Medium"
    else:
        shortlist_likelihood = "Low"
        
    return {
        "recruiter_readability_score": final_readability,
        "shortlist_likelihood": shortlist_likelihood,
        "warnings": warnings
    }
