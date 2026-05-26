"""
JD Extraction Engine.
Extracts required technical skills, seniority level, core responsibilities, and recruiter expectations
from raw scraped job descriptions.
"""

import re
from typing import Dict, Any, List
from app.services.evidence_storage_engine import extract_technologies_from_text


def extract_job_details(jd_text: str) -> Dict[str, Any]:
    """Analyzes raw JD text to extract keywords, seniority, focus domains, and recruiter expectations."""
    if not jd_text:
        return {
            "required_techs": [],
            "seniority": "Mid",
            "focus_domain": "backend",
            "recruiter_expectations": "Looking for a collaborative generalist with strong coding skills."
        }

    jd_lower = jd_text.lower()

    # 1. Extract Whitelisted Technologies
    required_techs = extract_technologies_from_text(jd_text)

    # 2. Detect Seniority Level
    seniority = "Mid"
    if any(w in jd_lower for w in ["lead", "principal", "staff", "architect", "director", "manager"]):
        seniority = "Lead"
    elif "senior" in jd_lower or "sr" in jd_lower or "5+" in jd_lower or "8+" in jd_lower:
        seniority = "Senior"
    elif "junior" in jd_lower or "jr" in jd_lower or "entry" in jd_lower or "1+" in jd_lower:
        seniority = "Junior"
    elif "intern" in jd_lower or "undergraduate" in jd_lower or "co-op" in jd_lower:
        seniority = "Intern"

    # 3. Detect Primary Focus Domain
    focus_domain = "backend"
    if any(w in jd_lower for w in ["front", "ui", "ux", "react", "next.js", "nextjs", "javascript", "typescript", "css"]):
        focus_domain = "frontend"
    elif any(w in jd_lower for w in ["devops", "cloud", "infra", "sre", "kubernetes", "docker", "ci/cd", "deployment"]):
        focus_domain = "devops"
    elif any(w in jd_lower for w in ["data science", "ml", "ai", "machine learning", "tensorflow", "pytorch", "deep learning", "cv"]):
        focus_domain = "data_science"
    elif "fullstack" in jd_lower or "full stack" in jd_lower:
        focus_domain = "fullstack"

    # 4. Infer Recruiter Expectations
    expectations = (
        f"Looking for a {seniority}-level engineer specializing in {focus_domain} architectures. "
        f"Key priorities: scaling software using {', '.join(required_techs[:4]) if required_techs else 'Python and Docker'}, "
        f"ensuring robust unit testing, and displaying strong architectural velocity."
    )

    return {
        "required_techs": required_techs,
        "seniority": seniority,
        "focus_domain": focus_domain,
        "recruiter_expectations": expectations
    }
