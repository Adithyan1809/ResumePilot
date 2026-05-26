"""
Employability Score Engine.
Compiles a unified signature Employability Score, synthesizing ATS scores,
recruiter trust levels, project metrics depth, and market demand indices.
"""

from typing import Dict, Any, List


def calculate_signature_employability_score(
    ats_score: float,
    recruiter_trust_score: float,
    project_metrics_count: int,
    github_consistency_score: float,
    gap_severity_score: float,
    interview_readiness_score: float,
    market_popularity_index: str = "High"
) -> Dict[str, Any]:
    """Synthesizes technical alignment, visual scoring, and market demand into the signature index."""
    # 1. Base components
    score_components = [
        ats_score * 0.20,                  # ATS Layout Compatibility (20%)
        recruiter_trust_score * 0.20,      # Recruiter trust & realism (20%)
        interview_readiness_score * 0.20,  # Interview Prep Depth (20%)
        (100.0 - gap_severity_score) * 0.20 # Technical gap minimization (20%)
    ]
    
    # 2. Add Project Metrics boosts (up to 10%)
    metrics_bonus = min(10.0, project_metrics_count * 2.5)
    
    # 3. Add GitHub profile quality boosts (up to 10%)
    github_bonus = min(10.0, (github_consistency_score - 50.0) * 0.20) if github_consistency_score > 50.0 else 0.0
    
    overall = sum(score_components) + metrics_bonus + github_bonus
    
    # Bound final rating
    final_score = round(max(35.0, min(99.0, overall)), 2)
    
    # Determine band
    employability_band = "Moderate Competitiveness"
    if final_score >= 88.0:
        employability_band = "Recruiter Magnet (Top 2%)"
    elif final_score >= 80.0:
        employability_band = "Highly Employable (Top 10%)"
    elif final_score >= 65.0:
        employability_band = "Strong Foundations"

    return {
        "employability_score": final_score,
        "employability_band": employability_band,
        "composite_dimensions": {
            "ats_readiness": "Excellent" if ats_score >= 80.0 else "Solid",
            "recruiter_trust": "High Trust" if recruiter_trust_score >= 80.0 else "Needs calibration",
            "technical_depth": "Advanced architectures" if project_metrics_count >= 2 else "Standard",
            "market_alignment": "Fully aligned" if gap_severity_score < 15.0 else "Moderate alignment"
        }
    }
