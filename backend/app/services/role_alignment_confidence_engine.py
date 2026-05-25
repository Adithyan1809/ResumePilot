"""
Role Alignment & Recruiter Confidence Engine.

Calculates highly realistic, truth-preserving matching scores, transferable skill mapping,
and recruiter confidence ratings to support career transitions without keyword fabrication.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def calculate_role_alignment(
    allowed_techs: List[str],
    target_role: str,
    jd_analysis: Dict[str, Any],
    skill_gaps: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate multi-dimensional role match percentages and confidence metrics."""
    allowed_lower = set(t.lower() for t in allowed_techs if t)
    
    req_hard = jd_analysis.get("required_hard_skills", []) or []
    req_tools = jd_analysis.get("required_tools_and_technologies", []) or []
    total_reqs = list(set(req_hard + req_tools))
    
    # 1. Technical Overlap Score (direct verbatim matches)
    matched_reqs = 0
    for req in total_reqs:
        if req.lower() in allowed_lower:
            matched_reqs += 1
            
    overlap_score = (matched_reqs / len(total_reqs) * 100.0) if total_reqs else 80.0
    
    # 2. Transferable Skill Strength
    # Assess adjacent mapping (e.g. backend skills transfer reasonably to frontend or data science)
    backend_techs = {"python", "fastapi", "flask", "django", "postgresql", "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "k8s", "aws", "git"}
    frontend_techs = {"javascript", "typescript", "react", "next.js", "nextjs", "vue", "angular", "tailwind", "tailwindcss", "css", "html"}
    data_techs = {"pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv", "yolo", "xgboost", "lightgbm"}
    
    has_backend = any(t in allowed_lower for t in backend_techs)
    has_frontend = any(t in allowed_lower for t in frontend_techs)
    has_data = any(t in allowed_lower for t in data_techs)
    
    target_lower = (target_role or "backend").lower()
    is_front = any(w in target_lower for w in ["front", "ui", "ux", "web", "react"])
    is_back = any(w in target_lower for w in ["back", "api", "service"])
    is_ds = any(w in target_lower for w in ["data", "science", "analyst", "ai", "ml"])
    
    transferable_strength = 50.0
    if is_front:
        if has_frontend:
            transferable_strength = 90.0
        elif has_backend:
            transferable_strength = 75.0  # Backend APIs transfer well to frontend data-binding
        elif has_data:
            transferable_strength = 60.0
    elif is_back:
        if has_backend:
            transferable_strength = 95.0
        elif has_frontend:
            transferable_strength = 70.0
        elif has_data:
            transferable_strength = 65.0
    elif is_ds:
        if has_data:
            transferable_strength = 95.0
        elif has_backend:
            transferable_strength = 80.0  # Backend database/modeling transfers well to DS data prep
        elif has_frontend:
            transferable_strength = 55.0
            
    # 3. Missing Skill Severity
    gap_count = len(skill_gaps.get("missing_skills", [])) + len(skill_gaps.get("missing_frameworks", []))
    severity_score = max(0, 100 - (gap_count * 15))
    
    # 4. Overall match per category (Rule 6 requires examples: Frontend 48%, Backend 88%, Data Science 91%)
    # Construct alignments based on actual candidate capabilities
    front_score = 30.0 + (30.0 if has_frontend else 0.0) + (25.0 if has_backend else 0.0) + (10.0 if has_data else 0.0)
    back_score = 30.0 + (40.0 if has_backend else 0.0) + (15.0 if has_frontend else 0.0) + (10.0 if has_data else 0.0)
    ds_score = 30.0 + (40.0 if has_data else 0.0) + (20.0 if has_backend else 0.0) + (5.0 if has_frontend else 0.0)
    
    front_score = min(99.0, max(15.0, front_score))
    back_score = min(99.0, max(15.0, back_score))
    ds_score = min(99.0, max(15.0, ds_score))
    
    # Target Match %
    target_match_pct = front_score if is_front else ds_score if is_ds else back_score
    
    # 5. Recruiter Confidence Estimate
    # Reduced by gaps, boosted by high technical overlap and transferable strength
    base_confidence = 90.0
    if gap_count > 0:
        base_confidence -= (gap_count * 12)
        base_confidence += (transferable_strength * 0.25)
    recruiter_confidence = min(99.0, max(20.0, base_confidence))
    
    return {
        "role_match_percent": round(target_match_pct),
        "transferable_skill_strength": round(transferable_strength),
        "technical_overlap_score": round(overlap_score),
        "missing_skill_severity_score": round(severity_score),
        "recruiter_confidence_estimate": round(recruiter_confidence),
        "role_matches": {
            "Frontend Match": f"{round(front_score)}%",
            "Backend Match": f"{round(back_score)}%",
            "Data Science Match": f"{round(ds_score)}%"
        }
    }
