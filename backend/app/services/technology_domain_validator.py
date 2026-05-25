"""
Technology-Domain Validation Engine.

Ensures that frameworks, tools, and methodologies are strictly aligned to their respective
technical domains and prevents cross-role keyword contamination during resume tailoring.
"""

import re
import logging
from typing import List, Dict, Set

logger = logging.getLogger(__name__)

# Domain mapping definitions
DOMAIN_TECHNOLOGIES: Dict[str, Set[str]] = {
    "frontend": {
        "react", "typescript", "css", "html", "javascript", "next.js", "vue", "angular",
        "tailwind", "tailwindcss", "bootstrap", "sass", "ui/ux", "responsive design",
        "responsive layout", "user interface", "frontend", "dom", "webpack", "vite", "babel",
        "material ui", "chui", "figma", "flexbox", "grid", "npm", "yarn"
    },
    "backend": {
        "fastapi", "flask", "django", "node.js", "node", "express", "rest api", "rest apis",
        "graphql", "websockets", "grpc", "microservices", "api gateway", "celery", "spring boot",
        "postgresql", "sqlite", "mysql", "redis", "mongodb", "cassandra", "dynamodb", "oracle",
        "sql server", "rdbms", "nosql", "postgres", "jwt", "oauth", "gunicorn", "uvicorn", "docker",
        "kubernetes", "k8s", "aws", "gcp", "azure", "rabbitmq", "kafka"
    },
    "data_science": {
        "pandas", "numpy", "scikit-learn", "scikit", "sklearn", "xgboost", "lightgbm", "tensorflow",
        "pytorch", "keras", "jupyter", "eda", "data cleaning", "data visualization", "tableau",
        "matlab", "scipy", "matplotlib", "seaborn", "analytics", "churn", "imputation", "randomforest",
        "linear regression", "k-means", "pca", "data wrangling", "predictive", "supervised learning",
        "nlp", "natural language processing", "bert", "gpt", "hugging face", "transformer"
    },
    "computer_vision": {
        "opencv", "yolo", "arcface", "face recognition", "face detection", "image processing",
        "cnn", "object detection", "image segmentation", "resnet", "vision", "computer vision",
        "pytesseract", "ocr", "pil", "pillow", "gans", "detectron"
    }
}

# Exclusive keywords that define a domain and should NEVER cross-contaminate other domains
EXCLUSIVE_DOMAIN_KEYWORDS: Dict[str, Set[str]] = {
    "frontend": {
        "responsive design", "responsive layout", "ui/ux", "user interface", "css styling",
        "frontend developer", "next.js", "react", "flexbox", "grid styling", "tailwind"
    },
    "backend": {
        "microservices", "api gateway", "websockets", "grpc", "message broker", "rest api",
        "backend engineer", "fastapi", "django", "celery task"
    },
    "data_science": {
        "pandas", "scikit-learn", "xgboost", "randomforest", "data wrangling", "data cleaning",
        "data imputation", "exploratory data analysis", "predictive model", "supervised learning"
    },
    "computer_vision": {
        "opencv", "yolo", "arcface", "computer vision", "object detection", "image segmentation",
        "face recognition", "image processing"
    }
}

# Compatibility rules: defines which roles are allowed to use which keywords
# If a target role category is "backend", it can use "backend" and "computer_vision" or "data_science" (broad tech),
# but it must NOT use "frontend" exclusive keywords.
INCOMPATIBLE_CROSS_ROLES: Dict[str, List[str]] = {
    "backend": ["frontend"],
    "data_science": ["frontend"],
    "computer_vision": ["frontend"],
    "frontend": ["backend", "data_science", "computer_vision"] # frontend shouldn't claim deep DS pipelines or websockets gateway
}


def validate_bullet_domain_compatibility(bullet_text: str, role_category: str) -> bool:
    """Detects if a bullet contains incompatible cross-domain keywords.

    Args:
        bullet_text: The bullet point text string.
        role_category: The target role category ('frontend', 'backend', 'data_science', 'computer_vision', 'full_stack').

    Returns:
        True if the bullet is compatible, False if there is cross-domain contamination.
    """
    if not bullet_text or not role_category or role_category == "full_stack":
        return True

    bullet_lower = bullet_text.lower()
    incompatible_domains = INCOMPATIBLE_CROSS_ROLES.get(role_category, [])

    for domain in incompatible_domains:
        exclusive_words = EXCLUSIVE_DOMAIN_KEYWORDS.get(domain, set())
        for word in exclusive_words:
            # Word boundary check for exact keyword matches
            pattern = rf"\b{re.escape(word)}\b"
            if re.search(pattern, bullet_lower):
                # If we find a frontend keyword in a backend role, or vice-versa
                logger.warning(
                    f"Contamination detected! Incompatible keyword '{word}' (from '{domain}') "
                    f"found in bullet point for '{role_category}' role: '{bullet_text}'"
                )
                return False

    return True


def heal_bullet_contamination(bullet_text: str, role_category: str) -> str:
    """Heals cross-domain keyword contamination by stripping the exclusive words or fallback rephrasing.

    Args:
        bullet_text: The contaminated bullet text string.
        role_category: The target role category ('frontend', 'backend', 'data_science', 'computer_vision', 'full_stack').

    Returns:
        A cleaned, grounded compatible bullet string.
    """
    if not bullet_text or not role_category or role_category == "full_stack":
        return bullet_text

    healed = bullet_text
    incompatible_domains = INCOMPATIBLE_CROSS_ROLES.get(role_category, [])

    for domain in incompatible_domains:
        exclusive_words = EXCLUSIVE_DOMAIN_KEYWORDS.get(domain, set())
        for word in exclusive_words:
            pattern = rf"\b{re.escape(word)}\b"
            # Remove the incompatible word and clean surrounding punctuation/grammar
            if re.search(pattern, healed, re.IGNORECASE):
                # E.g. "Design interactive interfaces using Python and Pandas, applying responsive design principles."
                # If role is backend/data_science, strip "applying responsive design principles"
                # Strip occurrences cleanly
                healed = re.sub(rf",?\s*(?:applying|with|using|integrating)?\s*{re.escape(word)}\s*(?:principles|layouts)?\s*", "", healed, flags=re.IGNORECASE)
                healed = re.sub(pattern, "", healed, flags=re.IGNORECASE)

    # Clean double spaces, dangling commas, and ensure standard punctuation
    healed = re.sub(r"\s+", " ", healed).strip()
    healed = re.sub(r",\s*,", ",", healed)
    healed = re.sub(r"^[\s,]+|[\s,]+$", "", healed)
    healed = healed.replace(" ,", ",").replace(" .", ".")
    
    if healed:
        healed = healed[0].upper() + healed[1:]
        if not healed.endswith("."):
            healed += "."
    else:
        # Final fallback if bullet was completely emptied
        healed = "Engineered robust software components to optimize system performance and reliability."

    logger.info(f"Healed bullet: '{bullet_text}' \u2794 '{healed}'")
    return healed
