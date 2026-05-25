"""
Transferable Skills Engine.

Identifies and maps adjacent technical capabilities and systems fundamentals
from the candidate's background to target role domains when specific technologies are absent,
completely preventing the fabrication of ungrounded skills.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Standard mapping of base skills to transferable target domain competencies
TRANSFERABLE_MAP = {
    "Backend Development": {
        "frontend": ["API Integration", "JSON/REST Data Flow", "State Synchronization", "Asynchronous Operations", "Client-Server Communication"],
        "data_science": ["Data Modeling", "SQL Query Optimization", "Object-Oriented Design", "Database Schemas", "File I/O"],
        "ai_ml": ["Algorithmic Optimization", "Computational Efficiency", "Data Ingestion Pipelines", "Data Structuring"],
    },
    "Databases": {
        "frontend": ["Client-Side Caching", "Data Schema Alignment", "Offline State Management", "Data Serialization"],
        "data_science": ["Relational Queries", "Complex Aggregations", "Data Normalization", "Indexed Search"],
        "ai_ml": ["Feature Storage", "Data Preprocessing", "SQL Ingestion", "High-Throughput Retrieval"],
    },
    "Data Science & ML": {
        "frontend": ["Data Visualization", "Dynamic Dashboards", "Statistical Plotting", "Metric Representation"],
        "backend": ["Statistical Modeling", "Analytical Processing", "Algorithmic Logic", "Data Cleaning Pipelines"],
    },
    "Computer Vision": {
        "frontend": ["Image Processing Concepts", "Canvas Rendering", "Media Constraints", "Frame-rate Optimization"],
        "backend": ["Asynchronous Video Streaming", "Image Decoding Pipelines", "Batch Processing Jobs"],
    }
}

def get_transferable_competencies(allowed_categories: Dict[str, List[str]], target_role: str) -> List[str]:
    """Retrieve list of transferable technical competencies based on candidate's allowed categories."""
    target = (target_role or "backend").lower()
    role_key = "frontend" if "front" in target or "ui" in target or "ux" in target or "web" in target or "react" in target else \
               "data_science" if "data" in target or "analyst" in target else \
               "ai_ml" if "ai" in target or "ml" in target or "vision" in target else \
               "backend"

    competencies = []
    for category, skills in allowed_categories.items():
        if not skills:
            continue
        if category in TRANSFERABLE_MAP and role_key in TRANSFERABLE_MAP[category]:
            competencies.extend(TRANSFERABLE_MAP[category][role_key])
            
    return list(dict.fromkeys(competencies))[:5]  # Deduplicated, max 5 key adjacent strengths
