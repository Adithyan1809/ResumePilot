"""
Skill Gap Analysis Engine.

Audits candidate tech stacks against job description expectations to identify 
missing tools, frameworks, programming languages, and domain exposures.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def analyze_skill_gaps(
    allowed_techs: List[str], 
    jd_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Compare allowed technologies against job description requirements to extract gaps."""
    allowed_lower = set(t.lower() for t in allowed_techs if t)
    
    req_hard = jd_analysis.get("required_hard_skills", []) or []
    req_tools = jd_analysis.get("required_tools_and_technologies", []) or []
    
    missing_skills = []
    missing_frameworks = []
    missing_tools = []
    missing_domains = []
    
    # Classify standard tech terms
    tech_categories = {
        "languages": ["python", "javascript", "typescript", "c++", "c#", "java", "go", "rust", "ruby", "php", "sql", "html", "css"],
        "frameworks": ["react", "next.js", "nextjs", "vue", "angular", "fastapi", "flask", "django", "node.js", "node", "express", "tensorflow", "pytorch", "keras"],
        "tools": ["docker", "kubernetes", "k8s", "aws", "gcp", "azure", "git", "github", "ci/cd", "postman", "jira", "webpack", "babel", "vite", "npm"]
    }
    
    all_requirements = list(set(req_hard + req_tools))
    
    for req in all_requirements:
        req_clean = req.strip()
        if not req_clean:
            continue
            
        req_lower = req_clean.lower()
        # Check if candidate lacks this requirement
        if not any(req_lower == allowed or req_lower in allowed for allowed in allowed_lower):
            # Categorize the gap
            if any(lang in req_lower for lang in tech_categories["languages"]):
                missing_skills.append(req_clean)
            elif any(fw in req_lower for fw in tech_categories["frameworks"]):
                missing_frameworks.append(req_clean)
            elif any(tool in req_lower for tool in tech_categories["tools"]):
                missing_tools.append(req_clean)
            else:
                # E.g. "Computer Vision", "CI/CD Deployment Pipelines"
                missing_domains.append(req_clean)
                
    return {
        "missing_skills": missing_skills,
        "missing_frameworks": missing_frameworks,
        "missing_tools": missing_tools,
        "missing_domain_exposure": missing_domains,
        "has_gaps": bool(missing_skills or missing_frameworks or missing_tools or missing_domains)
    }
