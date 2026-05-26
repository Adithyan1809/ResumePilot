"""
Semantic Alignment Engine.
Computes dense vector similarity between resume content and JD requirements using SentenceTransformers,
falling back to character n-gram TF-IDF cosine metrics on environment restrictions.
"""

import logging
from typing import List
from app.core.config import get_settings
from app.services.fallback_recovery_engine import fallback_cosine_similarity

logger = logging.getLogger(__name__)
settings = get_settings()

_MODEL_INSTANCE = None


def _get_embedding_model():
    """Lazily load SentenceTransformer model to prevent startup lags."""
    global _MODEL_INSTANCE
    if _MODEL_INSTANCE is not None:
        return _MODEL_INSTANCE
        
    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading dense vector semantic model: {settings.SEMANTIC_MODEL_NAME}")
        # Disable offline warnings
        import os
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        _MODEL_INSTANCE = SentenceTransformer(settings.SEMANTIC_MODEL_NAME)
        return _MODEL_INSTANCE
    except Exception as exc:
        logger.warning(f"Could not load SentenceTransformers: {exc}. Activating TF-IDF fallbacks.")
        return None


def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Computes semantic similarity score between resume draft and job description."""
    if not resume_text or not jd_text:
        return 0.0
        
    model = _get_embedding_model()
    
    if model is None:
        # Use our highly optimized cosine similarity fallback
        return fallback_cosine_similarity(resume_text, jd_text)
        
    try:
        # Vector embeddings
        embeddings = model.encode([resume_text, jd_text])
        
        # Calculate Cosine Similarity
        import numpy as np
        vec1 = embeddings[0]
        vec2 = embeddings[1]
        
        dot_product = np.dot(vec1, vec2)
        norm_a = np.linalg.norm(vec1)
        norm_b = np.linalg.norm(vec2)
        
        cosine_sim = dot_product / (norm_a * norm_b)
        
        # Scale to 0-100 percentage
        score = float(cosine_sim) * 100.0
        # Normalization constraints
        return round(min(100.0, max(0.0, score)), 2)
        
    except Exception as exc:
        logger.error(f"Semantic embedding calculation failed: {exc}. Degrading gracefully.")
        return fallback_cosine_similarity(resume_text, jd_text)
