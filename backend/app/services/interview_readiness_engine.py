"""
Interview Readiness Engine.
Estimates technical interview preparedness, outlines likely system design and coding topics,
and flags weak knowledge domains requiring reinforcement.
"""

from typing import List, Dict, Any


def calculate_interview_readiness(
    structured_evidence: Dict[str, Any],
    required_techs: List[str],
    focus_domain: str,
    gap_severity_score: float
) -> Dict[str, Any]:
    """Generates multidimensional interview metrics, likely topics, and preparation checklists."""
    if not structured_evidence:
        return _get_empty_readiness()

    base_score = 65.0  # Safe base score
    
    # 1. Evaluate Skill Overlap Boost
    cand_skills = []
    for cat_list in structured_evidence.get("skills", {}).values():
        if isinstance(cat_list, list):
            cand_skills.extend([s.lower() for s in cat_list if s])
            
    matches = 0
    for tech in required_techs:
        if tech.lower() in cand_skills:
            base_score += 4.0
            matches += 1
            
    # 2. Evaluate Experience and Project Depth Boost
    exps = structured_evidence.get("experience", [])
    if len(exps) >= 2:
        base_score += 10.0
    elif len(exps) == 1:
        base_score += 5.0
        
    projs = structured_evidence.get("projects", [])
    if len(projs) >= 2:
        base_score += 10.0
    elif len(projs) == 1:
        base_score += 5.0
        
    # 3. Deduct based on Skill Gap severity
    final_score = max(25.0, min(98.0, base_score - (gap_severity_score * 0.4)))

    # 4. Predict Likely Interview Topics & Prep Actions
    topics = ["Data Structures & Core Algorithms", "Git Version Control basics"]
    weak_areas = []
    preps = ["Practice standard whiteboard/LeetCode array and string iterations.", "Mock explain your projects using STAR methodology."]
    
    if focus_domain == "backend":
        topics.extend(["Database normalizations & Indexing", "RESTful API design and status protocols", "Asynchronous Python (asyncio)"])
        preps.extend(["Revise SQL join structures and indexes.", "Review FastAPI dependency injection rules."])
    elif focus_domain == "frontend":
        topics.extend(["React Hook optimizations", "DOM rendering lifecycles", "CSS responsive styling grids"])
        preps.extend(["Review State management workflows.", "Practice raw JavaScript array map/filter manipulations."])
    elif focus_domain == "devops":
        topics.extend(["Docker layer optimization secrets", "Kubernetes cluster architecture", "CI/CD automated pipeline triggers"])
        preps.extend(["Practice building minimal Dockerfiles.", "Revise standard cloud VPC configurations."])
    elif focus_domain == "data_science":
        topics.extend(["Feature mapping metrics", "XGBoost and RandomForest decision models", "Data scaling & normalization secrets"])
        preps.extend(["Practice using Pandas aggregations.", "Revise standard model validation splitting methods."])

    # Map missing skills directly to weak knowledge domains
    missing_techs = [t for t in required_techs if t.lower() not in cand_skills]
    for tech in missing_techs[:3]:
        weak_areas.append(f"{tech} syntax & system implementations")
        preps.append(f"Build a miniature proof-of-concept project integrating {tech}.")

    return {
        "interview_readiness_score": round(final_score, 2),
        "likely_interview_topics": topics[:5],
        "weak_knowledge_areas": weak_areas if weak_areas else ["None detected"],
        "recommended_preparation_topics": preps[:6]
    }


def _get_empty_readiness() -> Dict[str, Any]:
    """Fallback empty readiness response."""
    return {
        "interview_readiness_score": 50.0,
        "likely_interview_topics": ["Data Structures", "Programming Fundamentals"],
        "weak_knowledge_areas": ["Insufficient profile metrics"],
        "recommended_preparation_topics": ["Upload a master resume profile to start calculations."]
    }
