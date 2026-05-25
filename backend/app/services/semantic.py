"""
Semantic similarity service using Sentence Transformers.

Calculates deep contextual similarity between the resume text and the job description.
Includes a robust fallback to TF-IDF cosine similarity if sentence-transformers is loading
or failing due to OS/environment resource constraints.
"""

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Global cache for the sentence-transformer model
_model_instance = None


def get_embedding_model():
    """Retrieve or initialize the Sentence Transformer model instance with caching."""
    global _model_instance
    if _model_instance is not None:
        return _model_instance

    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading sentence-transformer model: {settings.SEMANTIC_MODEL_NAME}...")
        # Loads all-MiniLM-L6-v2 which is about 80MB
        _model_instance = SentenceTransformer(settings.SEMANTIC_MODEL_NAME)
        logger.info("Sentence-transformer loaded successfully.")
        return _model_instance
    except Exception as exc:
        logger.warning(
            f"Failed to load sentence-transformer ({settings.SEMANTIC_MODEL_NAME}): {exc}. "
            "Using TF-IDF fallback for semantic similarity scoring."
        )
        return None


async def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """Compute the cosine similarity score between two texts.

    Uses Sentence-Transformers embeddings if available, else falls back to TF-IDF.

    Args:
        text1: First input string (e.g. Resume).
        text2: Second input string (e.g. Job Description).

    Returns:
        Cosine similarity percentage (0.0 to 100.0).
    """
    if not text1.strip() or not text2.strip():
        return 0.0

    model = get_embedding_model()
    
    if model is not None:
        try:
            # Generate embeddings and compute cosine similarity
            # Since these are local, CPU-based calls, we execute synchronously
            embeddings = model.encode([text1, text2])
            
            # Re-verify shape
            import numpy as np
            emb1 = embeddings[0].reshape(1, -1)
            emb2 = embeddings[1].reshape(1, -1)
            
            similarity = float(cosine_similarity(emb1, emb2)[0][0])
            score = max(0.0, min(1.0, similarity)) * 100.0
            return round(score, 2)
        except Exception as exc:
            logger.error(f"Error computing sentence embeddings: {exc}. Falling back to TF-IDF.")

    # ── Fallback TF-IDF Cosine Similarity ───────────────────────────
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        score = max(0.0, min(1.0, similarity)) * 100.0
        return round(score, 2)
    except Exception as exc:
        logger.error(f"TF-IDF Fallback similarity failed: {exc}")
        return 50.0  # Safe neutral default
