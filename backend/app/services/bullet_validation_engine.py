"""
Bullet Point Quality Validation Engine.

Provides programmatic scoring, quality gating, and healing for experience/project bullet points,
enforcing active tone, technical depth, explicit tool mentions, and outcome metrics, while
rejecting generic passive corporate filler.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# Highly-rated active past-tense engineering verbs
STRONG_VERBS = {
    "engineered", "developed", "designed", "implemented", "optimized", "spearheaded",
    "architected", "integrated", "automated", "streamlined", "formulated", "enhanced",
    "coordinated", "executed", "collaborated", "constructed", "orchestrated", "deployed",
    "compiled", "resolved", "built", "trained", "analyzed", "minimized", "maximized",
    "designed", "streamlined", "conducted", "led", "managed", "created", "leveraged",
    "containerized"
}

# Technical keywords and tools vocabulary for parsing validation
COMMON_TECHS = {
    "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "sql", "fastapi", "flask", 
    "django", "react", "next.js", "nextjs", "vue", "angular", "node.js", "node", "express", "postgresql", 
    "postgres", "sqlite", "mysql", "redis", "mongodb", "docker", "kubernetes", "k8s", "aws", "gcp", 
    "azure", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "opencv", 
    "yolo", "arcface", "git", "github", "ci/cd", "rest api", "rest apis", "graphql", "websockets", "grpc", 
    "xgboost", "lightgbm", "randomforest", "cnn", "nlp", "llm", "bert", "gpt", "tableau", "matlab", "scipy",
    "matplotlib", "seaborn", "weasyprint", "reportlab", "pandas", "neural", "deep learning", "machine learning"
}

# Absolute banned passive filler phrases
BANNED_PHRASES = [
    "responsible for",
    "worked on",
    "assisted with",
    "performed daily duties",
    "helped the team",
    "participated in",
    "perform daily duties"
]


def grade_bullet_point(bullet: str) -> Dict[str, Any]:
    """Grade an individual resume bullet point.
    
    Returns a dict containing:
    - "score": Float 0-100 indicating technical density and active phrasing quality.
    - "approved": Boolean indicating if it exceeds the quality threshold.
    - "reason": String listing quality shortcomings (if rejected).
    """
    if not bullet or not bullet.strip():
        return {"score": 0.0, "approved": False, "reason": "Empty bullet point."}
        
    b = bullet.strip()
    b_lower = b.lower()
    words = b.split()
    word_count = len(words)
    
    # ── 1. Strict Phrase Rejections ──
    for phrase in BANNED_PHRASES:
        if phrase in b_lower:
            return {
                "score": 10.0,
                "approved": False,
                "reason": f"Contains unacceptable passive filler phrase: '{phrase}'."
            }
            
    # Explicit check for generic filler bullets
    if "perform daily duties" in b_lower or "part of the core operational team" in b_lower:
        return {
            "score": 5.0,
            "approved": False,
            "reason": "Generic low-quality operational filler bullet."
        }
        
    # ── 2. Word Count Gating ──
    if word_count < 8:
        return {
            "score": 15.0,
            "approved": False,
            "reason": f"Too short ({word_count} words). Bullet lacks technical context."
        }
        
    # ── 3. Action Verb Strength (25%) ──
    verb_score = 0.0
    first_word = words[0].lower() if words else ""
    first_word_clean = re.sub(r"[^\w]+", "", first_word)
    
    if first_word_clean in STRONG_VERBS:
        verb_score = 25.0
    elif first_word_clean.endswith("ed") or first_word_clean in ["build", "write", "make", "lead"]:
        verb_score = 15.0
    else:
        # Fails to start with active past-tense verb
        return {
            "score": 20.0,
            "approved": False,
            "reason": f"Does not start with an active past-tense engineering verb. Starts with '{words[0]}'."
        }
        
    # ── 4. Technical Task specificity (25%) ──
    # Check for technical terms or engineering actions
    tech_actions = ["pipeline", "schema", "api", "model", "query", "database", "latency", "optimization", 
                    "classification", "regression", "stream", "dashboard", "neural", "automation", "deploy",
                    "docker", "container", "webpack", "interface", "component", "architecture", "microservice"]
    task_matches = [w for w in tech_actions if w in b_lower]
    
    task_score = 0.0
    if len(task_matches) >= 2:
        task_score = 25.0
    elif len(task_matches) == 1:
        task_score = 15.0
    else:
        task_score = 5.0
        
    # ── 5. Explicit Technology Mentions (25%) ──
    tech_matches = [t for t in COMMON_TECHS if re.search(r"\b" + re.escape(t) + r"\b", b_lower)]
    
    # Reject outright if NO technologies are mentioned
    if not tech_matches:
        return {
            "score": 25.0,
            "approved": False,
            "reason": "Mentions zero frameworks, tools, or programming languages. Lacks technical depth."
        }
        
    tech_score = 0.0
    if len(tech_matches) >= 2:
        tech_score = 25.0
    elif len(tech_matches) == 1:
        tech_score = 15.0
        
    # ── 6. Outcome & Measurable Impact (15%) ──
    impact_score = 0.0
    has_metrics = bool(re.search(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b|\b\d+\+\b", b))
    has_impact_clause = any(w in b_lower for w in ["resulting in", "reducing", "securing", "optimizing", "latency", "accuracy", "supporting", "streamlining", "saving", "saving 50%", "improving", "achieving", "maximizing", "minimizing", "increasing", "decreasing", "establishing"])
    
    if has_metrics and has_impact_clause:
        impact_score = 15.0
    elif has_metrics or has_impact_clause:
        impact_score = 8.0
        
    # ── 7. Formatting & Readability (10%) ──
    formatting_score = 0.0
    starts_capital = b[0].isupper()
    ends_period = b.endswith(".")
    if starts_capital:
        formatting_score += 5.0
    if ends_period:
        formatting_score += 5.0
        
    total_score = verb_score + task_score + tech_score + impact_score + formatting_score
    total_score = round(total_score, 2)
    
    # Threshold approval at a score of 55.0
    approved = total_score >= 55.0
    reason = "" if approved else "Fails to meet minimum quality threshold (55.0)."
    
    return {
        "score": total_score,
        "approved": approved,
        "reason": reason
    }


def heal_or_replace_bullet(bullet: str, role_category: str = "backend") -> str:
    """Heal or replace a low-quality bullet point with a premium, technically-grounded version."""
    if not bullet or not bullet.strip():
        return "Engineered robust software components to optimize system performance and reliability."
        
    b = bullet.strip()
    
    # Dictionary of standard premium bullet alternatives sorted by role
    PREMIUM_TEMPLATES = {
        "backend": [
            "Designed and implemented scalable REST APIs using FastAPI and PostgreSQL, reducing endpoint latency by 20%.",
            "Engineered asynchronous processing task channels using Redis and Celery, optimizing database write latency.",
            "Containerized core service modules using multi-stage Docker builds, establishing secure local developer staging.",
            "Optimized query execution paths and database index profiles inside PostgreSQL to support high transaction volumes."
        ],
        "data_science": [
            "Developed predictive classification pipelines using Scikit-learn and Pandas to analyze customer churn indicators.",
            "Conducted extensive Exploratory Data Analysis (EDA) on 10,000+ data samples, uncovering crucial system insights.",
            "Trained machine learning regression models in Jupyter, achieving over 92% scoring accuracy on evaluation metrics.",
            "Built data wrangling workflows using NumPy and SQL to aggregate disparate metrics into centralized analytics."
        ],
        "computer_vision": [
            "Engineered real-time face detection attendance pipelines integrating OpenCV and ArcFace model embeddings.",
            "Optimized RTSP video stream frames ingestion, reducing frame processing latency by 15% under concurrent loads.",
            "Implemented object detection models using YOLO and PyTorch, achieving accurate real-time classification metrics."
        ],
        "frontend": [
            "Developed highly responsive user interfaces using React and TailwindCSS to provide seamless web layout controls.",
            "Optimized client-side bundle sizes using Next.js and Webpack, improving initial page load times by 25%.",
            "Designed modular component architectures in TypeScript to ensure long-term code quality and state consistency."
        ]
    }
    
    # Determine the role category safely
    role = role_category.lower() if role_category else "backend"
    if role not in PREMIUM_TEMPLATES:
        role = "backend"
        
    # Clean the bullet's banned phrases dynamically first if possible
    healed = b
    for phrase in BANNED_PHRASES:
        pattern = rf"\b{re.escape(phrase)}\b"
        if re.search(pattern, healed, re.IGNORECASE):
            healed = re.sub(rf",?\s*(?:applying|with|using|integrating)?\s*{re.escape(phrase)}\s*", "", healed, flags=re.IGNORECASE)
            healed = re.sub(pattern, "", healed, flags=re.IGNORECASE)
            
    # Clean first word if weak
    words = healed.split()
    if words:
        first_word = re.sub(r"[^\w]+", "", words[0]).lower()
        if first_word not in STRONG_VERBS and not first_word.endswith("ed"):
            # Swap first word with a strong active verb
            healed = "Developed " + " ".join(words[1:])
            
    # Check if healed bullet passes the threshold now
    grade = grade_bullet_point(healed)
    if grade["approved"]:
        logger.info(f"Successfully healed weak bullet: '{bullet}' => '{healed}'")
        return healed
        
    # Fallback to premium template if healing failed to elevate quality
    templates = PREMIUM_TEMPLATES[role]
    import random
    selected = random.choice(templates)
    logger.info(f"Replaced low-quality bullet '{bullet}' with premium template '{selected}'")
    return selected
