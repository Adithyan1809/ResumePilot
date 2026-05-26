"""
Role Gap Analysis Engine.
Compares job requirements against candidate master profiles to identify missing skills,
classifying gaps by risk severity.
"""

from typing import List, Dict, Any


def analyze_role_gaps(
    candidate_skills: List[str],
    jd_required_techs: List[str],
    focus_domain: str
) -> Dict[str, Any]:
    """Identifies technology stack gaps and matches their risk metrics based on role domains."""
    if not jd_required_techs:
        return {"gaps": [], "gap_severity_score": 0.0}

    cand_lower = [s.lower() for s in candidate_skills if s]
    gaps = []
    high_count = 0
    
    for tech in jd_required_techs:
        tech_clean = str(tech).strip()
        tech_lower = tech_clean.lower()
        
        if tech_lower not in cand_lower:
            # Determine severity
            severity = "Medium"
            
            # High priority triggers
            if focus_domain == "backend" and tech_lower in ["python", "sql", "fastapi", "django", "postgresql", "postgres"]:
                severity = "High"
                high_count += 1
            elif focus_domain == "frontend" and tech_lower in ["react", "javascript", "typescript", "html", "css"]:
                severity = "High"
                high_count += 1
            elif focus_domain == "devops" and tech_lower in ["docker", "kubernetes", "k8s", "aws", "ci/cd"]:
                severity = "High"
                high_count += 1
            elif focus_domain == "data_science" and tech_lower in ["pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"]:
                severity = "High"
                high_count += 1
                
            gaps.append({
                "skill": tech_clean,
                "severity": severity,
                "domain": focus_domain
            })

    # Gap Severity Score calculation (0 to 100, where 100 means extreme gaps)
    total_gaps = len(gaps)
    if not total_gaps:
        severity_score = 0.0
    else:
        severity_score = min(100.0, (high_count * 20.0) + (total_gaps * 5.0))

    return {
        "gaps": gaps,
        "gap_severity_score": round(severity_score, 2)
    }
