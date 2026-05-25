"""
Keyword and skill extraction service using spaCy.

Extracts technical skills, soft skills, tools, certifications, action verbs, and
quantifiable achievements from raw resume texts and job descriptions.
"""

import logging
import re
from typing import Any, Dict, List, Set, Tuple

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

# Global cache for the spaCy language model
_nlp_instance = None

# Curated taxonomies of skills and keywords for tech resumes
HARD_SKILLS = {
    # Languages
    "python", "javascript", "typescript", "golang", "java", "c++", "c#", "rust", "php", "ruby", "swift", "kotlin", "sql", "html", "css", "r", "scala",
    # Frameworks
    "fastapi", "django", "flask", "react", "next.js", "nextjs", "vue", "angular", "express", "spring boot", "laravel", "ruby on rails", "pytorch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy", "react native", "flutter",
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins", "ci/cd", "github actions", "gitlab", "prometheus", "grafana", "nginx", "apache",
    # Databases
    "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "cassandra", "dynamodb", "sqlite", "mariadb", "oracle", "neo4j",
    # Architectures & Concepts
    "rest api", "restful api", "graphql", "grpc", "microservices", "system architecture", "serverless", "distributed systems", "oop", "functional programming", "mvc", "data structures", "algorithms",
    # AI/ML & Data
    "machine learning", "deep learning", "nlp", "natural language processing", "llm", "large language models", "artificial intelligence", "data science", "data engineering", "computer vision", "generative ai", "neural networks",
}

SOFT_SKILLS = {
    "leadership", "project management", "teamwork", "collaboration", "communication", "problem solving", "agile", "scrum", "kanban", "critical thinking", "mentoring", "negotiation", "time management", "public speaking", "creativity", "adaptability", "conflict resolution", "emotional intelligence",
}

TOOLS = {
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "trello", "slack", "figma", "postman", "visual studio code", "vscode", "docker desktop", "aws console", "pgadmin", "mongodb compass", "jupyter notebook",
}

STRONG_ACTION_VERBS = {
    "spearheaded", "architected", "engineered", "optimized", "developed", "designed", "implemented", "delivered", "increased", "reduced", "led", "managed", "orchestrated", "modernized", "accelerated", "consolidated", "maximized", "pioneered", "championed", "streamlined", "formulated", "revamped", "conceptualized", "overhauled", "cultivated", "standardized", "mentored", "empowered",
}

WEAK_ACTION_VERBS = {
    "worked", "helped", "assisted", "responsible", "handled", "participated", "did", "made", "tried", "kept", "showed", "gave",
}


def get_nlp_model():
    """Retrieve or load the spaCy en_core_web_sm model instance with caching."""
    global _nlp_instance
    if _nlp_instance is not None:
        return _nlp_instance

    try:
        logger.info("Loading spaCy model en_core_web_sm...")
        _nlp_instance = spacy.load("en_core_web_sm")
        logger.info("spaCy model loaded successfully.")
        return _nlp_instance
    except Exception as exc:
        logger.warning(
            f"Failed to load spaCy model en_core_web_sm: {exc}. "
            "Attempting to fall back to a simple rule-based string processor."
        )
        return None


def extract_all_keywords(text: str) -> Dict[str, Set[str]]:
    """Extract standard keywords from a text string.

    Classifies them into hard_skills, soft_skills, tools, action_verbs, and certifications.

    Args:
        text: Input string.

    Returns:
        Dict containing categorized sets of found keywords.
    """
    if not text:
        return {
            "hard_skills": set(),
            "soft_skills": set(),
            "tools": set(),
            "action_verbs": set(),
            "certifications": set(),
        }

    text_lower = text.lower()
    
    # 1. Simple regex taxonomy matching (highly reliable for specific tech terms)
    found_hard = {s for s in HARD_SKILLS if _has_word(text_lower, s)}
    found_soft = {s for s in SOFT_SKILLS if _has_word(text_lower, s)}
    found_tools = {t for t in TOOLS if _has_word(text_lower, t)}
    found_verbs = {v for v in STRONG_ACTION_VERBS if _has_word(text_lower, v)}

    # 2. Extract Certifications (e.g. AWS Certified, PMP, Scrum Master)
    found_certs = set()
    cert_patterns = [
        r"\baws\s+(?:certified\s+)?(?:solutions\s+architect|developer|sysops|security|cloud\s+practitioner)\b",
        r"\bpmp\b",
        r"\bcertified\s+scrum\s+master\b|\bcsm\b",
        r"\bcomptia\s+(?:a\+|network\+|security\+|cybersecurity)\b",
        r"\bcisco\s+(?:certified\s+)?(?:ccna|ccnp|ccie)\b",
        r"\bitil\b",
        r"\bgoogle\s+cloud\s+certified\s+professional\b",
        r"\bcertified\s+information\s+systems\s+security\s+professional\b|\bcissp\b",
    ]
    for pattern in cert_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            found_certs.add(match.strip().title())

    # 3. Enhance with spaCy Named Entities and noun chunks if available
    nlp = get_nlp_model()
    if nlp is not None:
        try:
            doc = nlp(text[:50000])  # limit text length for safety
            # Gather proper nouns and noun chunks that look like technologies
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip().lower()
                # If it matches any words, let's keep it (e.g. "scikit-learn library")
                if len(chunk_text) < 30 and chunk_text in HARD_SKILLS:
                    found_hard.add(chunk_text)
        except Exception as exc:
            logger.error(f"Error running spaCy NER enhancement: {exc}")

    return {
        "hard_skills": found_hard,
        "soft_skills": found_soft,
        "tools": found_tools,
        "action_verbs": found_verbs,
        "certifications": found_certs,
    }


def analyze_keyword_importance(jd_text: str, found_keywords: Dict[str, Set[str]]) -> List[Dict[str, str]]:
    """Determine the relative importance of job description keywords.

    Uses TF-IDF scoring of terms to classify them as high, medium, or low importance.

    Args:
        jd_text: Job Description raw text.
        found_keywords: Extracted keywords from the JD.

    Returns:
        List of dictionaries with keyword details: keyword, importance, category.
    """
    all_jd_keywords = []
    
    # Flatten categories with their category tag
    categories = {
        "hard_skill": found_keywords["hard_skills"],
        "soft_skill": found_keywords["soft_skills"],
        "tool": found_keywords["tools"],
        "certification": found_keywords["certifications"],
    }
    
    # Calculate word frequency counts in JD to assign raw weights
    jd_words = [w.strip(".,()[]{}|") for w in jd_text.lower().split()]
    
    for category_name, kw_set in categories.items():
        for kw in kw_set:
            # Simple count frequency in JD
            # Escape regex characters
            pattern = re.escape(kw)
            freq = len(re.findall(r"\b" + pattern + r"\b", jd_text.lower()))
            
            # Rate importance based on count and placement
            if freq >= 4 or category_name == "certification":
                importance = "high"
            elif freq >= 2:
                importance = "medium"
            else:
                importance = "low"
                
            all_jd_keywords.append({
                "keyword": kw.title() if len(kw) > 4 or category_name != "tool" else kw.upper(),
                "importance": importance,
                "category": category_name,
            })
            
    return all_jd_keywords


def detect_measurable_achievements(bullets: List[str]) -> Tuple[int, List[str]]:
    """Scan work experience bullet points for quantifiable metrics.

    Metrics include percentages, dollar amounts, scale counts, ratios, or speed gains.

    Args:
        bullets: List of experience bullet points.

    Returns:
        A tuple of (count_of_quantified_bullets, list_of_bullet_feedback).
    """
    metric_pattern = r"\b\d+%\b|\b\d+\s*(?:percent|percent|x-factor|times|fold|users|revenue|dollars|savings|clients|projects|million|thousand|billion|k|m|b)\b|\$\s*\d+(?:,\d{3})*(?:\.\d{2})?\b"
    
    quantified_count = 0
    feedback = []
    
    for idx, bullet in enumerate(bullets):
        if not bullet.strip():
            continue
        
        match = re.search(metric_pattern, bullet.lower())
        if match:
            quantified_count += 1
        else:
            feedback.append(f"Bullet {idx + 1} lacks measurable results.")
            
    return quantified_count, feedback


def detect_weak_verbs(bullets: List[str]) -> List[Dict[str, Any]]:
    """Identify weak or passive verbs in bullet points and suggest strong alternatives.

    Args:
        bullets: List of bullet points.

    Returns:
        List of dicts representing weak verbs detected and recommended alternatives.
    """
    detected = []
    
    for idx, bullet in enumerate(bullets):
        bullet_lower = bullet.lower()
        found_weak = [w for w in WEAK_ACTION_VERBS if _has_word(bullet_lower, w)]
        
        if found_weak:
            detected.append({
                "bullet_index": idx,
                "bullet_text": bullet,
                "weak_verbs": found_weak,
                "suggestions": ["spearheaded", "engineered", "optimized", "architected", "pioneered", "implemented"]
            })
            
    return detected


def _has_word(text: str, word: str) -> bool:
    """Helper to detect if a word or phrase exists in a text with proper word boundaries."""
    # Special character escaping (e.g. c++, c#, .net)
    escaped_word = re.escape(word)
    # Custom word boundary handling for tech keywords like C++, C#, .NET
    if word.endswith("+") or word.endswith("#") or word.startswith("."):
        pattern = r"(?:\b|\s)" + escaped_word + r"(?:\b|\s|$)"
    else:
        pattern = r"\b" + escaped_word + r"\b"
    return bool(re.search(pattern, text))
