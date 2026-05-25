"""
Technology Grounding Engine with Contextual Semantic Matching.

Enforces absolute verification of all tech stacks and frameworks mentioned in resumes,
preventing the fabrication of ungrounded frontend/backend technologies, while supporting
context-level semantic matching (e.g. mapping "face recognition" to "computer vision pipeline").
"""

import re
import logging
from typing import List, Dict, Any

from app.services.semantic import calculate_semantic_similarity

logger = logging.getLogger(__name__)

# Comprehensive vocabulary of standard technologies for scanning
STANDARD_TECH_VOCAB = {
    "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "sql", "fastapi", "flask", 
    "django", "react", "next.js", "nextjs", "vue", "angular", "node.js", "node", "express", "postgresql", 
    "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "k8s", "aws", "gcp", 
    "azure", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv", 
    "yolo", "arcface", "git", "github", "ci/cd", "rest api", "rest apis", "graphql", "websockets", "grpc", 
    "xgboost", "lightgbm", "randomforest", "cnn", "nlp", "llm", "bert", "gpt", "tableau", "matlab", "scipy",
    "matplotlib", "seaborn", "weasyprint", "reportlab", "tailwind", "tailwindcss", "webpack", "babel", 
    "vite", "npm", "yarn", "pip", "uv", "bootstrap", "sass"
}

# High-level domain concept maps to allow natural wording variations
CONCEPT_MAPPINGS = {
    "computer vision": ["opencv", "yolo", "arcface", "cnn", "image processing", "face recognition", "face detection", "object detection"],
    "machine learning": ["tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost", "lightgbm", "randomforest", "pandas", "numpy", "predictive model"],
    "backend api": ["fastapi", "flask", "django", "rest api", "rest apis", "graphql", "websockets", "grpc", "node", "express"],
    "database system": ["postgresql", "postgres", "sqlite", "mysql", "redis", "mongodb", "sql"],
    "devops pipeline": ["docker", "kubernetes", "k8s", "aws", "gcp", "azure", "ci/cd", "github actions", "jenkins"]
}

# Industry-standard properly cased technology names
BEAUTIFUL_TECH_NAMES = {
    "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", "c++": "C++", "c#": "C#", "java": "Java", 
    "html": "HTML", "css": "CSS", "sql": "SQL", "fastapi": "FastAPI", "flask": "Flask", "django": "Django", 
    "react": "React", "next.js": "Next.js", "nextjs": "Next.js", "vue": "Vue", "angular": "Angular", 
    "node.js": "Node.js", "node": "Node.js", "express": "Express", "postgresql": "PostgreSQL", "postgres": "PostgreSQL", 
    "sqlite": "SQLite", "mysql": "MySQL", "redis": "Redis", "mongodb": "MongoDB", "docker": "Docker", 
    "kubernetes": "Kubernetes", "k8s": "Kubernetes", "aws": "AWS", "gcp": "GCP", "azure": "Azure", 
    "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn", "sklearn": "Scikit-Learn", 
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras", "opencv": "OpenCV", "yolo": "YOLO", 
    "arcface": "ArcFace", "git": "Git", "github": "GitHub", "ci/cd": "CI/CD", "rest api": "REST API", 
    "rest apis": "REST APIs", "graphql": "GraphQL", "websockets": "WebSockets", "grpc": "gRPC", 
    "xgboost": "XGBoost", "lightgbm": "LightGBM", "randomforest": "Random Forest", "cnn": "CNN", "nlp": "NLP", 
    "llm": "LLM", "bert": "BERT", "gpt": "GPT", "tableau": "Tableau", "matlab": "MATLAB", "scipy": "SciPy",
    "matplotlib": "Matplotlib", "seaborn": "Seaborn", "weasyprint": "WeasyPrint", "reportlab": "ReportLab", 
    "tailwind": "TailwindCSS", "tailwindcss": "TailwindCSS", "webpack": "Webpack", "babel": "Babel", 
    "vite": "Vite", "npm": "NPM", "yarn": "Yarn", "pip": "Pip", "uv": "uv", "bootstrap": "Bootstrap", "sass": "Sass"
}


def extract_allowed_technologies(raw_text: str, github_techs: List[str] = None) -> List[str]:
    """Identify all verified technologies present in raw_text or github_techs."""
    if not raw_text:
        return []
        
    text_lower = raw_text.lower()
    github_lower = [g.lower() for g in github_techs if g] if github_techs else []
    
    allowed = []
    for tech in STANDARD_TECH_VOCAB:
        pattern = rf"\b{re.escape(tech)}\b"
        is_in_source = re.search(pattern, text_lower) or (len(tech) > 4 and tech in text_lower)
        is_in_github = any(tech == g or (len(tech) > 4 and tech in g) for g in github_lower)
        
        if is_in_source or is_in_github:
            cased_name = BEAUTIFUL_TECH_NAMES.get(tech, tech.title())
            if cased_name not in allowed:
                allowed.append(cased_name)
            
    return allowed


async def is_technology_concept_grounded(concept: str, allowed_techs: List[str], threshold: float = 75.0) -> bool:
    """Checks if a technology concept is semantically grounded by any allowed base technologies."""
    if not concept or not allowed_techs:
        return False
        
    concept_lower = concept.lower()
    allowed_lower = [t.lower() for t in allowed_techs if t]
    
    # 1. Direct match check
    for tech in allowed_lower:
        if tech in concept_lower or concept_lower in tech:
            return True
            
    # 2. Rule-based concept grouping check
    for parent_concept, children in CONCEPT_MAPPINGS.items():
        if parent_concept in concept_lower:
            # If the concept references a parent, verify we have at least one child tech grounded
            if any(child in allowed_techs for child in children):
                return True
        # If the concept is a child tech, check if we possess the parent or siblings
        if any(child in concept_lower for child in children):
            if any(sibling in allowed_techs for sibling in children):
                return True
                
    # 3. Deep semantic similarity fallback using embeddings
    allowed_str = ", ".join(allowed_techs)
    similarity = await calculate_semantic_similarity(concept_lower, allowed_str)
    if similarity >= threshold:
        return True
        
    return False


async def filter_ungrounded_technologies_from_text(text: str, allowed_techs: List[str]) -> str:
    """Detects and removes ungrounded technologies from a sentence, preserving semantic concept compatibility."""
    if not text:
        return ""
        
    words = re.findall(r"\b[a-zA-Z0-9\.\+\#\-]+\b", text)
    unvalidated = []
    
    for word in words:
        word_lower = word.lower()
        if word_lower in STANDARD_TECH_VOCAB:
            # Check concept-level grounding
            is_grounded = await is_technology_concept_grounded(word_lower, allowed_techs)
            if not is_grounded:
                unvalidated.append(word)
                
    cleansed = text
    for tech in list(set(unvalidated)):
        # Patterns to remove the ungrounded technology cleanly along with connectors
        patterns = [
            rf",?\s*\band\b\s*\b{re.escape(tech)}\b",
            rf"\b{re.escape(tech)}\b\s*\band\b,?",
            rf"\b(?:using|with|leveraging|incorporating|applying)\s+\b{re.escape(tech)}\b",
            rf"\b{re.escape(tech)}\b"
        ]
        for pattern in patterns:
            cleansed = re.sub(pattern, "", cleansed, flags=re.IGNORECASE)
            
    # Clean up spacing, trailing punctuation, double spaces, and clean margins
    cleansed = re.sub(r"\s+", " ", cleansed)
    cleansed = re.sub(r",\s*,", ",", cleansed)
    cleansed = re.sub(r",\s*\.", ".", cleansed)
    cleansed = re.sub(r"\s+,\s*", ", ", cleansed)
    cleansed = re.sub(r"\s+\.\s*$", ".", cleansed)
    cleansed = re.sub(r"^[\s\-–—,|]+|[\s\-–—,|]+$", "", cleansed).strip()
    
    if len(cleansed.split()) < 4:
        return "Engineered robust software components to optimize system performance and reliability."
        
    if cleansed and not cleansed.endswith("."):
        cleansed += "."
        
    return cleansed[0].upper() + cleansed[1:] if cleansed else ""
