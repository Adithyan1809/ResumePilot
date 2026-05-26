"""
Evidence Extraction Engine.
Transforms candidate master profiles into granular, queryable technical evidence nodes
that can be mapped, scored, and indexed during graph-based resume assembly.
"""

import uuid
from typing import List, Dict, Any


def extract_evidence_nodes(structured_evidence: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Converts a structured evidence database into a list of queryable graph nodes."""
    if not structured_evidence:
        return []

    nodes = []

    # 1. Extract Experience Bullets as Nodes
    for exp in structured_evidence.get("experience", []):
        company = exp.get("company", "")
        role = exp.get("role", "")
        for bullet in exp.get("bullets", []):
            b_str = bullet.get("text", "") if isinstance(bullet, dict) else str(bullet)
            if not b_str:
                continue
                
            nodes.append({
                "id": str(uuid.uuid4()),
                "type": "experience_bullet",
                "content": b_str,
                "context": f"{role} at {company}",
                "technologies": bullet.get("technologies", []) if isinstance(bullet, dict) else [],
                "metrics": bullet.get("metrics", []) if isinstance(bullet, dict) else [],
                "source_metadata": {"company": company, "role": role, "dates": exp.get("dates", "")}
            })

    # 2. Extract Project Accomplishments as Nodes
    for proj in structured_evidence.get("projects", []):
        title = proj.get("title", "")
        desc_list = proj.get("description", [])
        for desc in desc_list:
            d_str = desc.get("text", "") if isinstance(desc, dict) else str(desc)
            if not d_str:
                continue
                
            nodes.append({
                "id": str(uuid.uuid4()),
                "type": "project_bullet",
                "content": d_str,
                "context": f"Project: {title}",
                "technologies": desc.get("technologies", []) if isinstance(desc, dict) else [],
                "metrics": desc.get("metrics", []) if isinstance(desc, dict) else [],
                "source_metadata": {"title": title, "link": proj.get("link", "")}
            })

    # 3. Extract Education Nodes
    for edu in structured_evidence.get("education", []):
        school = edu.get("school", "")
        degree = edu.get("degree", "")
        nodes.append({
            "id": str(uuid.uuid4()),
            "type": "education",
            "content": f"{degree} from {school}",
            "context": f"Education",
            "technologies": [],
            "metrics": [edu.get("gpa", "")] if edu.get("gpa") else [],
            "source_metadata": edu
        })

    return nodes
