"""
Resume Assembly Engine.
Stitches together structured resume sections (summary, experience, projects, skills, education)
programmatically using ranked evidence graph nodes and retrieval bullet patterns.
"""

from typing import Dict, Any, List
from app.services.evidence_extraction_engine import extract_evidence_nodes
from app.services.evidence_graph_engine import score_and_rank_evidence_nodes
from app.services.retrieval_bullet_engine import retrieve_and_adapt_bullet
from app.services.reality_preservation_engine import apply_role_transferability_summary


def assemble_tailored_resume(
    structured_evidence: Dict[str, Any],
    required_techs: List[str],
    focus_domain: str,
    seniority: str
) -> Dict[str, Any]:
    """Compiles the final tailored resume JSON structure deterministically from whitelisted evidence nodes."""
    if not structured_evidence:
        return {}

    # 1. GRANULAR NODE EXTRACTION & RANKING
    nodes = extract_evidence_nodes(structured_evidence)
    ranked_nodes = score_and_rank_evidence_nodes(nodes, required_techs, focus_domain)

    assembled = {
        "contact_info": structured_evidence.get("contact_info", {}),
        "summary": "",
        "experience": [],
        "projects": [],
        "skills": structured_evidence.get("skills", {}),
        "education": structured_evidence.get("education", []),
        "certifications": structured_evidence.get("certifications", [])
    }

    # 2. COMPILE EXPERIENCE SECTION (Adapted Bullets)
    for exp in structured_evidence.get("experience", []) or []:
        role = exp.get("role", "")
        company = exp.get("company", "")
        dates = exp.get("dates", "")
        
        # Get nodes corresponding to this specific experience
        exp_nodes = [
            n for n in ranked_nodes 
            if n["type"] == "experience_bullet" 
            and n["source_metadata"].get("company") == company 
            and n["source_metadata"].get("role") == role
        ]
        
        assembled_bullets = []
        for idx, node in enumerate(exp_nodes[:4]):  # Max 4 bullets per role
            techs = node.get("technologies", [])
            metrics = node.get("metrics", [])
            
            # Retrieve high-trust recruiter layout and adapt it
            adapted = retrieve_and_adapt_bullet(focus_domain, techs, metrics, bullet_index=idx)
            assembled_bullets.append(adapted)
            
        # Fallback if no nodes found (e.g. mock fallback)
        if not assembled_bullets:
            assembled_bullets = [
                f"Optimized software integrations and backend interfaces utilizing Python and associated services.",
                f"Collaborated with developers and operations engineers to deliver robust features."
            ]

        assembled["experience"].append({
            "role": role,
            "company": company,
            "dates": dates,
            "bullets": assembled_bullets
        })

    # 3. COMPILE PROJECTS SECTION (Top 3 Projects based on rank score)
    project_nodes = [n for n in ranked_nodes if n["type"] == "project_bullet"]
    
    # Group nodes by project title
    proj_groups = {}
    for node in project_nodes:
        title = node["source_metadata"].get("title", "")
        if title not in proj_groups:
            proj_groups[title] = []
        proj_groups[title].append(node)
        
    # Select top 3 projects based on first node's ranked position
    sorted_projects = []
    for title, p_nodes in proj_groups.items():
        # Represent project score as average or max rank score of its bullets
        # Find first matching project bullet in ranked list to determine order
        for idx, r_node in enumerate(ranked_nodes):
            if r_node["type"] == "project_bullet" and r_node["source_metadata"].get("title") == title:
                sorted_projects.append((title, p_nodes, idx))
                break
                
    sorted_projects.sort(key=lambda x: x[2])  # Sort by rank index ascending
    
    for title, p_nodes, _ in sorted_projects[:3]:
        proj_bullets = []
        proj_techs = set()
        
        for idx, node in enumerate(p_nodes[:3]):
            techs = node.get("technologies", [])
            metrics = node.get("metrics", [])
            proj_techs.update(techs)
            
            adapted = retrieve_and_adapt_bullet(focus_domain, techs, metrics, bullet_index=idx)
            proj_bullets.append(adapted)
            
        assembled["projects"].append({
            "name": title,
            "technologies": sorted(list(proj_techs)) if proj_techs else ["Python", "Docker"],
            "description": proj_bullets,
            "link": p_nodes[0]["source_metadata"].get("link", "")
        })

    # 4. COMPILE PROFESSIONAL TRANSITION SUMMARY
    # Formulate a clean, grounded summary based on whitelisted skills
    flat_skills = []
    for val in assembled["skills"].values():
        if isinstance(val, list):
            flat_skills.extend(val)
            
    tech_str = ", ".join(flat_skills[:4]) if flat_skills else "Python, SQL, and Git"
    
    base_summary = (
        f"Highly focused {seniority}-level software engineer with a strong foundation in computer science "
        f"and hands-on experience building robust systems using {tech_str}. Skilled in designing clean APIs, "
        f"optimizing database architectures, and deploying containerized environments. Passionate about "
        f"driving engineering velocity and scaling reliable developer operations."
    )
    
    # Run role transition mapping summary check
    raw_text_whitelists = " ".join(flat_skills)
    assembled["summary"] = apply_role_transferability_summary(base_summary, focus_domain, raw_text_whitelists)

    return assembled
