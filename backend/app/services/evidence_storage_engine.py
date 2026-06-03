"""
Evidence Storage Engine.
Parses, extracts, and normalizes candidate resume data into structured whitelisted evidence JSON,
establishing the ground truth database for zero-fabrication resume optimization.
"""

import re
from typing import Dict, List, Any

# Technology vocab for grounding & classification
STANDARD_TECH_VOCAB = {
    "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "sql", "fastapi", "flask",
    "django", "react", "next.js", "nextjs", "vue", "angular", "node.js", "node", "express", "postgresql",
    "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "k8s", "aws", "gcp",
    "azure", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv",
    "yolo", "arcface", "git", "github", "ci/cd", "rest api", "rest apis", "graphql", "websockets", "grpc",
    "xgboost", "lightgbm", "randomforest", "cnn", "nlp", "llm", "bert", "gpt", "tableau", "matlab", "scipy",
    "matplotlib", "seaborn", "weasyprint", "reportlab", "tailwind", "tailwindcss", "webpack", "babel",
    "vite", "npm", "yarn", "pip", "uv", "bootstrap", "sass", "go", "rust", "ruby", "php"
}

SKILL_MAPPING = {
    "Programming Languages": [
        "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "go", "rust", "ruby", "php",
        "sql", "shell", "bash", "r", "kotlin", "swift", "scala", "c", "assembly", "perl"
    ],
    "Data Science & ML": [
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "keras", "machine learning", "deep learning",
        "nlp", "natural language processing", "data analysis", "statistics", "scipy", "matplotlib", "seaborn",
        "hugging face", "llm", "bert", "gpt", "analytics", "data science", "xgboost", "lightgbm"
    ],
    "Backend Development": [
        "fastapi", "flask", "django", "node.js", "node", "express", "rest api", "rest apis", "graphql",
        "websockets", "grpc", "microservices", "api gateway", "celery", "backend", "mvc", "apis", "spring boot"
    ],
    "Databases": [
        "postgresql", "sqlite", "mysql", "redis", "mongodb", "cassandra", "dynamodb", "oracle", "sql server",
        "neo4j", "elasticsearch", "dbms", "caching", "nosql", "rdbms", "postgres"
    ],
    "Computer Vision": [
        "opencv", "yolo", "image processing", "cnn", "object detection", "pytesseract", "image segmentation",
        "pil", "pillow", "gans", "resnet", "computer vision", "vision"
    ],
    "DevOps & Infrastructure": [
        "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "github actions", "jenkins", "terraform",
        "ansible", "linux", "nginx", "apache", "cloud", "serverless", "k8s"
    ],
    "Tools": [
        "git", "github", "gitlab", "postman", "jira", "confluence", "vs code", "webpack", "babel", "vite",
        "npm", "yarn", "pip", "uv", "swagger", "windows", "macos"
    ]
}


def extract_metrics_from_text(text: str) -> List[str]:
    """Extract quantified metrics (percentages, dollar amounts, scaling numbers) from a text string."""
    if not text:
        return []
    # Match patterns like 35%, $10k, 10,000+, 2.5M, etc.
    pattern = r"\b\d+(?:[\d,\.]*\d)?%|\$\s*\d+(?:[\d,\.]*\d)?[kKmMbB]?|\b\d+\+\b|\b\d+(?:[\d,\.]*\d)?\s*(?:x|X|fold)\b|\b\d+(?:[\d,\.]*\d)?[kKmMbB]\b"
    metrics = re.findall(pattern, text)
    return [m.strip() for m in metrics]


def extract_technologies_from_text(text: str) -> List[str]:
    """Identify whitelisted technical skills and tools explicitly mentioned in a text string."""
    if not text:
        return []
    text_lower = text.lower()
    found = []
    for tech in STANDARD_TECH_VOCAB:
        pattern = rf"\b{re.escape(tech)}\b"
        if re.search(pattern, text_lower):
            found.append(tech)
    return sorted(list(set(found)))


def categorize_skills_list(skills: List[str]) -> Dict[str, List[str]]:
    """Group a flat list of skills into standardized whitelisted skill categories."""
    categories = {
        "Programming Languages": [],
        "Data Science & ML": [],
        "Backend Development": [],
        "Databases": [],
        "Computer Vision": [],
        "DevOps & Infrastructure": [],
        "Tools": []
    }
    
    assigned = set()
    for skill in skills:
        if not skill:
            continue
        skill_clean = str(skill).strip().replace("'", "").replace('"', '')
        skill_lower = skill_clean.lower()
        
        matched_cat = None
        for cat, keywords in SKILL_MAPPING.items():
            if any(kw == skill_lower or (len(kw) > 3 and kw in skill_lower) for kw in keywords):
                matched_cat = cat
                break
        
        if matched_cat:
            if skill_lower not in assigned:
                categories[matched_cat].append(skill_clean)
                assigned.add(skill_lower)
        else:
            # Default fallback category if unclassified
            if skill_lower not in assigned:
                categories["Tools"].append(skill_clean)
                assigned.add(skill_lower)
                
    return categories


def extract_evidence_from_parsed_sections(parsed_sections: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms raw parsed resume sections into a clean, structured whitelisted evidence database schema."""
    if not parsed_sections:
        return {}

    evidence = {
        "contact_info": parsed_sections.get("contact_info", {}),
        "summary": parsed_sections.get("summary", ""),
        "skills": {},
        "experience": [],
        "projects": [],
        "education": parsed_sections.get("education", []),
        "certifications": parsed_sections.get("certifications", [])
    }

    # 1. Standardize and Categorize Skills
    raw_skills = parsed_sections.get("skills", [])
    if isinstance(raw_skills, dict):
        # Already grouped skills dictionary
        flat_skills = []
        for val in raw_skills.values():
            if isinstance(val, list):
                flat_skills.extend(val)
        evidence["skills"] = categorize_skills_list(flat_skills)
    elif isinstance(raw_skills, list):
        evidence["skills"] = categorize_skills_list(raw_skills)

    # 2. Extract Experience Evidence (Achievements, Tech, Metrics)
    for exp in parsed_sections.get("experience", []) or []:
        if not isinstance(exp, dict):
            continue
        bullets = exp.get("bullets", []) or []
        processed_bullets = []
        achievements = []
        all_exp_techs = set()
        
        for b in bullets:
            b_str = b.get("text", "") if isinstance(b, dict) else str(b)
            if not b_str:
                continue
            
            # Analyze metrics and technical capabilities in bullet
            metrics = extract_metrics_from_text(b_str)
            techs = extract_technologies_from_text(b_str)
            all_exp_techs.update(techs)
            
            processed_bullets.append({
                "text": b_str,
                "metrics": metrics,
                "technologies": techs
            })
            
            # Bullets with metrics are highly-valued achievements
            if metrics:
                achievements.append(b_str)
                
        evidence["experience"].append({
            "company": exp.get("company", ""),
            "role": exp.get("role", ""),
            "dates": exp.get("dates", ""),
            "bullets": processed_bullets,
            "achievements": achievements,
            "technologies": sorted(list(all_exp_techs))
        })

    # 3. Extract Projects Evidence
    for proj in parsed_sections.get("projects", []) or []:
        if not isinstance(proj, dict):
            continue
        description = proj.get("description", []) or []
        processed_desc = []
        all_proj_techs = set(t.lower() for t in proj.get("technologies", []) if t)
        all_proj_metrics = []
        
        for d in description:
            d_str = d.get("text", "") if isinstance(d, dict) else str(d)
            if not d_str:
                continue
            
            metrics = extract_metrics_from_text(d_str)
            techs = extract_technologies_from_text(d_str)
            all_proj_techs.update(techs)
            all_proj_metrics.extend(metrics)
            
            processed_desc.append({
                "text": d_str,
                "metrics": metrics,
                "technologies": techs
            })

        evidence["projects"].append({
            "title": proj.get("title", ""),
            "description": processed_desc,
            "technologies": sorted(list(all_proj_techs)),
            "metrics": all_proj_metrics
        })

    return evidence

def build_weighted_whitelist(resume_techs: List[str], jd_techs: List[str]) -> str:
    """Builds a weighted 3-tier technology whitelist to prevent hallucination while matching JD priority."""
    resume_lower = [t.lower().strip() for t in resume_techs if t]
    jd_lower = [t.lower().strip() for t in jd_techs if t]
    
    overlap = sorted(list(set(t for t in resume_lower if t in jd_lower)))
    resume_only = sorted(list(set(t for t in resume_lower if t not in jd_lower)))
    
    return f"""
    HIGH PRIORITY (in both resume and JD — use these prominently): {overlap}
    AVAILABLE (in resume only — use if relevant): {resume_only}
    DO NOT USE: anything not in the above two lists
    """
