"""
Job Role Alignment, Classification, and Section Reordering Engine.

Employs a combination of SentenceTransformer semantic embeddings and keyword-density scoring
to classify job descriptions into five standardized templates, deterministically reordering
resume sections, technical skills categories, and project relevance lists.
"""

import logging
import re
from typing import Any, Dict, List

# Import semantic similarity helper
from app.services.semantic import calculate_semantic_similarity

logger = logging.getLogger(__name__)

# Predefined reference profiles for SentenceTransformer matching
ROLE_PROFILES = {
    "frontend": (
        "Front-End Engineering React Next.js TypeScript CSS User Interface UI UX design "
        "responsive web layouts Tailwind HTML5 JavaScript styling components web browser client development"
    ),
    "backend": (
        "Back-End Web Development FastAPI PostgreSQL databases Redis docker containers system design APIs "
        "microservices REST Django Python backend scale queries caching sql backend pipelines"
    ),
    "data_science": (
        "Data Science Pandas Numpy Scikit-learn predictive modeling data analysis analytics Jupyter churn "
        "regression classification exploratory data analysis EDA Seaborn stats math machine learning pipelines"
    ),
    "ai_ml": (
        "Artificial Intelligence Machine Learning Deep Learning Computer Vision PyTorch TensorFlow YOLO CNN "
        "image processing object detection ArcFace neural networks NLP LLMs embeddings reinforcement learning"
    ),
    "full_stack": (
        "Full Stack Development Node.js Express NextJS MongoDB databases fullstack web applications "
        "integrated frontend backend deployment cloud hosting APIs full-stack user experience"
    )
}

# Predefined keyword lists for deterministic density checks
ROLE_KEYWORDS = {
    "frontend": ["frontend", "front-end", "react", "next.js", "nextjs", "javascript", "typescript", "html", "css", "tailwind", "ui", "ux", "vue", "web developer"],
    "backend": ["backend", "back-end", "fastapi", "django", "flask", "postgresql", "postgres", "sql", "redis", "docker", "microservices", "api", "apis", "system design", "databases", "database"],
    "data_science": ["data science", "data scientist", "machine learning", "ml", "pandas", "numpy", "scikit-learn", "data analysis", "analytics", "churn", "jupyter", "statistics", "matplotlib", "seaborn"],
    "ai_ml": ["pytorch", "tensorflow", "keras", "computer vision", "opencv", "yolo", "deep learning", "neural network", "cnn", "llm", "ai", "artificial intelligence", "face recognition", "detection"],
    "full_stack": ["fullstack", "full-stack", "express", "node", "node.js", "web developer", "nextjs", "mongodb", "web application", "integrated"]
}

async def classify_role_by_jd(jd_text: str) -> str:
    """Classifies Job Description into frontend, backend, data_science, ai_ml, or full_stack.
    
    Combines deterministic keyword-density counts with sentence-embedding contextual similarity.
    """
    if not jd_text or len(jd_text.strip()) < 10:
        return "general"
        
    jd_lower = jd_text.lower()
    
    # 1. Deterministic Keyword Scoring
    kw_scores = {}
    for role, kw_list in ROLE_KEYWORDS.items():
        score = sum(2.0 for kw in kw_list if kw in jd_lower) # Match weights
        kw_scores[role] = score
        
    # 2. Embedding Contextual Scoring
    semantic_scores = {}
    for role, profile_str in ROLE_PROFILES.items():
        try:
            sim = await calculate_semantic_similarity(jd_text, profile_str)
            semantic_scores[role] = sim
        except Exception as exc:
            logger.warning(f"Semantic checking failed for {role}: {exc}")
            semantic_scores[role] = 40.0 # safe fallback
            
    # 3. Combine scores (weighted: 40% Keyword, 60% Semantic)
    combined_scores = {}
    for role in ROLE_PROFILES.keys():
        kw_part = (kw_scores.get(role, 0.0) / 20.0) * 100.0 # scale keyword matches
        sem_part = semantic_scores.get(role, 0.0)
        combined_scores[role] = (kw_part * 0.40) + (sem_part * 0.60)
        
    logger.info(f"V2 Combined Role alignment grading: {combined_scores}")
    
    # Pick highest scoring role
    best_role = max(combined_scores, key=combined_scores.get)
    if combined_scores[best_role] > 40.0:
        return best_role
        
    return "general"

def reorder_sections_by_role(sections: Dict[str, Any], role: str) -> Dict[str, Any]:
    """Deterministically reorders the resume sections based on the classified job role template."""
    ROLE_ORDER = {
        "frontend": ["contact_info", "summary", "skills", "experience", "projects", "education"],
        "backend": ["contact_info", "summary", "skills", "experience", "projects", "education"],
        "full_stack": ["contact_info", "summary", "skills", "experience", "projects", "education"],
        "data_science": ["contact_info", "summary", "experience", "projects", "skills", "education"],
        "ai_ml": ["contact_info", "summary", "projects", "experience", "skills", "education"],
        "general": ["contact_info", "summary", "skills", "experience", "projects", "education"]
    }
    
    order = ROLE_ORDER.get(role, ROLE_ORDER["general"])
    reordered = {}
    
    # Fill reordered with keys in the exact order specified
    for key in order:
        if key in sections:
            reordered[key] = sections[key]
            
    # Add any remaining metadata keys like id, template, etc.
    for key, val in sections.items():
        if key not in reordered:
            reordered[key] = val
            
    return reordered

def align_skills_to_role(skills: List[str], role: str) -> List[str]:
    """Dynamically prioritize skills categories at the top based on the target role."""
    if not skills:
        return []
        
    # Standardized allowed categories prioritizing order
    prioritized_kws = []
    if role == "frontend":
        prioritized_kws = ["Programming Languages", "Tools"]
    elif role == "backend":
        prioritized_kws = ["Backend Development", "Databases", "DevOps & Infrastructure", "Programming Languages"]
    elif role == "data_science":
        prioritized_kws = ["Data Science & ML", "Databases", "Programming Languages"]
    elif role == "ai_ml":
        prioritized_kws = ["Data Science & ML", "Computer Vision", "Programming Languages"]
    elif role == "full_stack":
        prioritized_kws = ["Programming Languages", "Backend Development", "Databases", "Tools"]
        
    matched = []
    remainder = []
    
    for s in skills:
        s_str = str(s)
        s_lower = s_str.lower()
        
        is_priority = False
        for kw in prioritized_kws:
            if kw.lower() in s_lower:
                matched.append((prioritized_kws.index(kw), s_str))
                is_priority = True
                break
                
        if not is_priority:
            remainder.append(s_str)
            
    matched_sorted = [item[1] for item in sorted(matched, key=lambda x: x[0])]
    return matched_sorted + remainder

def align_projects_to_role(projects: List[Dict[str, Any]], role: str) -> List[Dict[str, Any]]:
    """Dynamically prioritizes projects that correspond to the target role."""
    if not projects:
        return []
        
    matched = []
    remainder = []
    
    fe_terms = ["web", "react", "ui", "ux", "frontend", "next.js", "nextjs", "dashboard", "streamlit", "client", "website"]
    ds_terms = ["ml", "machine learning", "predictive", "tensor", "tensorflow", "pytorch", "analytics", "churn", "pandas", "numpy", "scikit"]
    be_terms = ["backend", "gateway", "redis", "pubsub", "postgres", "fastapi", "django", "flask", "websocket", "docker", "api", "apis", "engine", "system"]
    ai_terms = ["pytorch", "tensorflow", "computer vision", "opencv", "yolo", "deep learning", "neural network", "cnn", "llm", "ai", "face recognition", "detection"]
    fs_terms = ["fullstack", "full-stack", "express", "node", "node.js", "web developer", "nextjs", "mongodb", "web application"]
    
    target_terms = []
    if role == "frontend":
        target_terms = fe_terms
    elif role == "backend":
        target_terms = be_terms
    elif role == "data_science":
        target_terms = ds_terms
    elif role == "ai_ml":
        target_terms = ai_terms
    elif role == "full_stack":
        target_terms = fs_terms
        
    for p in projects:
        name = p.get("name", "").lower()
        techs = [t.lower() for t in p.get("technologies", [])]
        bullets = " ".join(p.get("description", [])).lower()
        
        score = 0
        for term in target_terms:
            if term in name:
                score += 3
            if term in techs:
                score += 2
            if term in bullets:
                score += 1
                
        if score > 0:
            matched.append((score, p))
        else:
            remainder.append(p)
            
    matched_sorted = [item[1] for item in sorted(matched, key=lambda x: x[0], reverse=True)]
    return matched_sorted + remainder
