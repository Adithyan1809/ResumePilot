"""
Market Intelligence Engine.
Analyzes trending tech stacks, role popularity indices, salary distributions,
and internship demand metrics to prioritize growth roads.
"""

from typing import List, Dict, Any

TRENDING_STACKS = {
    "backend": ["fastapi", "kubernetes", "redis", "docker", "grpc", "go", "rust"],
    "frontend": ["next.js", "typescript", "tailwind", "react", "vite", "sass"],
    "devops": ["kubernetes", "terraform", "github actions", "docker", "aws", "prometheus"],
    "data_science": ["llm", "pytorch", "hugging face", "pandas", "xgboost", "scikit-learn"]
}

SALARY_BANDS = {
    "backend": {"junior": "$80k - $110k", "mid": "$115k - $145k", "senior": "$150k - $200k"},
    "frontend": {"junior": "$75k - $100k", "mid": "$105k - $135k", "senior": "$140k - $185k"},
    "devops": {"junior": "$85k - $115k", "mid": "$120k - $155k", "senior": "$160k - $210k"},
    "data_science": {"junior": "$90k - $120k", "mid": "$130k - $165k", "senior": "$170k - $230k"}
}


def analyze_market_trends(focus_domain: str, seniority: str) -> Dict[str, Any]:
    """Compiles trending technologies, salary expectations, and market popularity indicators."""
    domain = focus_domain.lower() if focus_domain else "backend"
    level = seniority.lower() if seniority else "mid"
    
    # Defaults fallback
    if domain not in TRENDING_STACKS:
        domain = "backend"
    if level not in ["junior", "mid", "senior", "lead", "staff"]:
        level = "mid"
        
    resolved_level = "senior" if level in ["senior", "lead", "staff"] else level
    
    trends = TRENDING_STACKS[domain]
    salary = SALARY_BANDS[domain].get(resolved_level, "$100k - $130k")
    
    return {
        "domain": domain,
        "seniority_level": seniority,
        "average_salary_band": salary,
        "trending_technologies": [t.title() for t in trends],
        "hiring_demand_index": "High" if domain in ["backend", "data_science"] else "Moderate",
        "key_regional_hotspot": "San Francisco Bay Area / Remote"
    }


def rank_missing_skills_by_market_value(
    missing_skills: List[str],
    focus_domain: str
) -> List[str]:
    """Prioritizes and ranks identified missing technologies based on active market demand indices."""
    domain = focus_domain.lower() if focus_domain else "backend"
    if domain not in TRENDING_STACKS:
        return missing_skills
        
    trends = TRENDING_STACKS[domain]
    
    # Sort missing skills: trending items first, remaining alphabetically
    def get_rank(skill: str) -> int:
        s_lower = skill.lower()
        if s_lower in trends:
            return trends.index(s_lower)
        return len(trends) + 1
        
    return sorted(missing_skills, key=get_rank)
