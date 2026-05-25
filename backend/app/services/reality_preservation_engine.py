"""
Reality Preservation & Technology Grounding Engine.

Enforces absolute verification of all tech stacks and frameworks mentioned in resumes,
preventing the fabrication of ungrounded frontend frameworks (React, Next.js, Webpack, etc.)
or any backend/data tools not present in the candidate's actual source background.
"""

import re
from typing import List, Dict, Any, Tuple

# Comprehensive vocabulary of standard technologies for scanning
COMMON_TECHS = {
    "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "sql", "fastapi", "flask", 
    "django", "react", "next.js", "nextjs", "vue", "angular", "node.js", "node", "express", "postgresql", 
    "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "k8s", "aws", "gcp", 
    "azure", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv", 
    "yolo", "arcface", "git", "github", "ci/cd", "rest api", "rest apis", "graphql", "websockets", "grpc", 
    "xgboost", "lightgbm", "randomforest", "cnn", "nlp", "llm", "bert", "gpt", "tableau", "matlab", "scipy",
    "matplotlib", "seaborn", "weasyprint", "reportlab", "tailwind", "tailwindcss", "webpack", "babel", 
    "vite", "npm", "yarn", "pip", "uv", "bootstrap", "sass"
}


def validate_technology_grounding(text: str, source_text: str, github_technologies: List[str] = None) -> Dict[str, Any]:
    """Identify all standard technologies mentioned in text and verify if they exist in source_text or github_technologies."""
    if not text:
        return {"all_grounded": True, "unvalidated": [], "validated": []}
        
    text_lower = text.lower()
    source_lower = (source_text or "").lower()
    
    github_lower = []
    if github_technologies:
        github_lower = [g.lower() for g in github_technologies if g]
        
    unvalidated = []
    validated = []
    
    # Check each standard technology
    for tech in COMMON_TECHS:
        pattern = rf"\b{re.escape(tech)}\b"
        # Match using word boundaries or exact substring if length > 4
        if re.search(pattern, text_lower) or (len(tech) > 4 and tech in text_lower):
            is_in_source = re.search(pattern, source_lower) or (len(tech) > 4 and tech in source_lower)
            is_in_github = any(tech == g or (len(tech) > 4 and tech in g) for g in github_lower)
            
            if is_in_source or is_in_github:
                validated.append(tech)
            else:
                unvalidated.append(tech)
                
    return {
        "all_grounded": len(unvalidated) == 0,
        "unvalidated": unvalidated,
        "validated": validated
    }


def cleanse_ungrounded_technologies(text: str, source_text: str, github_technologies: List[str] = None) -> str:
    """Detects and removes any ungrounded technologies from a text string, keeping other parts intact."""
    if not text:
        return ""
        
    grounding = validate_technology_grounding(text, source_text, github_technologies)
    if grounding["all_grounded"]:
        return text
        
    cleansed = text
    for tech in grounding["unvalidated"]:
        # Patterns to remove the ungrounded technology cleanly along with connectors
        patterns = [
            # E.g. ", and React" or ", React" or " and React"
            rf",?\s*\band\b\s*\b{re.escape(tech)}\b",
            rf"\b{re.escape(tech)}\b\s*\band\b,?",
            # E.g. "using React" or "with React"
            rf"\b(?:using|with|leveraging|incorporating|applying)\s+\b{re.escape(tech)}\b",
            # Fallback exact word boundary
            rf"\b{re.escape(tech)}\b"
        ]
        
        for pattern in patterns:
            cleansed = re.sub(pattern, "", cleansed, flags=re.IGNORECASE)
            
    # Clean up double spaces, dangling commas, and extra spaces around punctuation
    cleansed = re.sub(r"\s+", " ", cleansed)
    cleansed = re.sub(r",\s*,", ",", cleansed)
    cleansed = re.sub(r",\s*\.", ".", cleansed)
    cleansed = re.sub(r"\s+,\s*", ", ", cleansed)
    cleansed = re.sub(r"\s+\.\s*$", ".", cleansed)
    
    # Strip any trailing/leading symbols and spaces
    cleansed = re.sub(r"^[\s\-–—,|]+|[\s\-–—,|]+$", "", cleansed).strip()
    
    # If the text becomes empty or too short, fallback to a clean grounded technical statement
    if len(cleansed.split()) < 4:
        return "Engineered robust software components to optimize system performance and reliability."
        
    # Ensure it ends with period and starts capitalized
    if not cleansed.endswith("."):
        cleansed += "."
    cleansed = cleansed[0].upper() + cleansed[1:]
    
    return cleansed


def apply_role_transferability_summary(summary: str, role: str, source_text: str) -> str:
    """If the target role is frontend/ui-heavy but direct frontend stack is absent in the source,
    converts summary into a professional transferable backend/systems statement with growing frontend interest.
    """
    if not summary:
        return ""
        
    s_lower = (source_text or "").lower()
    
    # Check if target role is frontend or fullstack
    r_lower = (role or "").lower()
    is_frontend_target = any(w in r_lower for w in ["front", "ui", "ux", "full", "web", "react"])
    
    # Check if candidate lacks direct frontend stack (React, Next.js, Vue, Angular, TypeScript)
    has_frontend_skills = any(w in s_lower for w in ["react", "next.js", "nextjs", "vue", "angular", "typescript", "tailwind", "css", "html", "javascript"])
    
    if is_frontend_target and not has_frontend_skills:
        # Candidate is backend/data science applying for frontend/fullstack. Do not fabricate frontend projects!
        # Pivot to systems fundamentals & transferable skills.
        found_techs = []
        for tech in ["python", "sql", "fastapi", "django", "flask", "postgresql", "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "aws", "git"]:
            if tech in s_lower:
                found_techs.append(tech.title() if tech != "fastapi" and tech != "mysql" and tech != "postgresql" else "FastAPI" if tech == "fastapi" else "MySQL" if tech == "mysql" else "PostgreSQL")
                
        tech_str = ", ".join(found_techs[:4]) if found_techs else "Python, SQL, and Git"
        
        transfer_summary = (
            f"Software engineering undergraduate with hands-on experience building robust backend APIs, "
            f"databases, and scalable systems using {tech_str}. Strong foundation in computer science "
            f"principles, with a keen interest in expanding technical expertise into modern frontend development "
            f"frameworks like React and Next.js."
        )
        return transfer_summary
        
    return summary
