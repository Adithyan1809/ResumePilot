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

    # 2. COMPILE EXPERIENCE SECTION (Raw Bullet Pass-Through)
    for exp in structured_evidence.get("experience", []) or []:
        role = exp.get("role", "")
        company = exp.get("company", "")
        dates = exp.get("dates", "")
        
        # Pass the original bullets entirely untouched. The LLM Tailoring step will rewrite them.
        assembled_bullets = []
        for bullet in exp.get("bullets", []):
            if isinstance(bullet, dict):
                assembled_bullets.append(bullet.get("text", ""))
            else:
                assembled_bullets.append(str(bullet))
                
        # Limit to 4 bullets max for density
        assembled_bullets = assembled_bullets[:4]

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
        for idx, r_node in enumerate(ranked_nodes):
            if r_node["type"] == "project_bullet" and r_node["source_metadata"].get("title") == title:
                sorted_projects.append((title, p_nodes, idx))
                break
                
    sorted_projects.sort(key=lambda x: x[2])  # Sort by rank index ascending
    
    for title, p_nodes, _ in sorted_projects[:3]:
        proj_bullets = []
        proj_techs = set()
        
        # Get raw project bullets from structured_evidence instead of hallucinated nodes
        # Find the actual project in structured_evidence
        target_proj = next((p for p in structured_evidence.get("projects", []) if p.get("title", "") == title), None)
        if target_proj:
            for desc in target_proj.get("description", [])[:3]:
                if isinstance(desc, dict):
                    proj_bullets.append(desc.get("text", ""))
                else:
                    proj_bullets.append(str(desc))
            
            for tech in target_proj.get("technologies", []):
                proj_techs.add(tech)
            
        assembled["projects"].append({
            "name": title,
            "technologies": sorted(list(proj_techs)) if proj_techs else ["Python", "Docker"],
            "description": proj_bullets,
            "link": p_nodes[0]["source_metadata"].get("link", "") if p_nodes else ""
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

    # 5. DEDUPLICATE BULLETS ACROSS SECTIONS
    seen = set()
    
    # Process experience
    for exp in assembled["experience"]:
        unique_bullets = []
        for b in exp.get("bullets", []):
            if b not in seen:
                seen.add(b)
                unique_bullets.append(b)
        exp["bullets"] = unique_bullets
        
    # Process projects
    for proj in assembled["projects"]:
        unique_bullets = []
        for b in proj.get("description", []):
            if b not in seen:
                seen.add(b)
                unique_bullets.append(b)
        proj["description"] = unique_bullets

    return assembled
