"""
Whitespace, Spacing, and Content Density Management Engine.

Enforces visual layout rules programmatically, dynamically calibrating page margins,
font sizes, line heights, and section boundaries to guarantee a highly readable one-page resume.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Core constraints for clean 1-page resumes
MAX_EXPERIENCE_BULLETS = 4
MAX_PROJECTS = 3
MAX_PROJECT_BULLETS = 3
MAX_SKILLS_PER_CATEGORY = 7

def manage_content_density(sections: Dict[str, Any]) -> Dict[str, Any]:
    """Inspects content size, trims over-spilled lists, and computes optimal layout margins and sizes.
    
    Returns a dict containing:
    - "sections": The cleaned/trimmed resume sections.
    - "layout": Spacing and formatting instructions for rendering (font size, margins, spacing).
    """
    if not isinstance(sections, dict):
        return {"sections": {}, "layout": {}}
        
    cleaned_sections = {}
    
    # ── 1. Copy Contact and Summary Verbatim ──
    cleaned_sections["contact_info"] = sections.get("contact_info", {})
    cleaned_sections["summary"] = sections.get("summary", "")
    
    # ── 2. Trim Experience Bullets (Enforce visual constraint) ──
    raw_exp = sections.get("experience", []) or []
    cleaned_exp = []
    total_exp_bullets = 0
    
    for entry in raw_exp:
        if not isinstance(entry, dict):
            continue
        entry_copy = dict(entry)
        bullets = entry.get("bullets", []) or []
        # Enforce max bullets per experience entry
        entry_copy["bullets"] = bullets[:MAX_EXPERIENCE_BULLETS]
        total_exp_bullets += len(entry_copy["bullets"])
        cleaned_exp.append(entry_copy)
        
    cleaned_sections["experience"] = cleaned_exp
    
    # ── 3. Trim Projects and Bullets ──
    raw_proj = sections.get("projects", []) or []
    cleaned_proj = []
    total_proj_bullets = 0
    
    # Enforce max projects
    for entry in raw_proj[:MAX_PROJECTS]:
        if not isinstance(entry, dict):
            continue
        entry_copy = dict(entry)
        desc = entry.get("description", []) or []
        bullets = [desc] if isinstance(desc, str) else list(desc) if isinstance(desc, list) else []
        # Enforce max project bullets
        entry_copy["description"] = bullets[:MAX_PROJECT_BULLETS]
        total_proj_bullets += len(entry_copy["description"])
        cleaned_proj.append(entry_copy)
        
    cleaned_sections["projects"] = cleaned_proj
    
    # ── 4. Prevent Skill Overload & Truncate Large Lists ──
    raw_skills = sections.get("skills", []) or []
    cleaned_skills = []
    total_skills_count = 0
    
    for skill_entry in raw_skills:
        skill_str = str(skill_entry).strip()
        if not skill_str:
            continue
            
        if ":" in skill_str:
            cat, items = skill_str.split(":", 1)
            # Trim individual skills to avoid horizontal overflows
            skills_list = [s.strip() for s in items.split(",") if s.strip()]
            trimmed_skills = skills_list[:MAX_SKILLS_PER_CATEGORY]
            cleaned_skills.append(f"{cat.strip()}: {', '.join(trimmed_skills)}")
            total_skills_count += len(trimmed_skills)
        else:
            cleaned_skills.append(skill_str)
            total_skills_count += 1
            
    cleaned_sections["skills"] = cleaned_skills
    
    # ── 5. Copy Education ──
    cleaned_sections["education"] = sections.get("education", []) or []
    
    # ── 6. Dynamically Calibrate Page Formatting & Whitespace Balance ──
    # Heuristics based on total bullet count and tech skills count
    total_bullets = total_exp_bullets + total_proj_bullets
    
    margin_inches = 0.75
    font_size_pt = 10.5
    line_spacing = 1.2
    space_after_section = 8 # points
    
    # Visual overcrowding index (characters & paragraphs volume)
    # 1. Very Dense (Needs tight margins and smaller text to fit 1-page)
    if total_bullets > 12 or total_skills_count > 25:
        margin_inches = 0.50
        font_size_pt = 9.5
        line_spacing = 1.15
        space_after_section = 6
        density_status = "compact"
        whitespace_score = 65.0
    # 2. Very Sparse (Needs larger margins and text to spread out visually)
    elif total_bullets < 6 and total_skills_count < 12:
        margin_inches = 1.0
        font_size_pt = 11.0
        line_spacing = 1.3
        space_after_section = 12
        density_status = "expanded"
        whitespace_score = 75.0
    # 3. Perfectly Balanced
    else:
        margin_inches = 0.75
        font_size_pt = 10.5
        line_spacing = 1.2
        space_after_section = 8
        density_status = "optimal"
        whitespace_score = 90.0
        
    return {
        "sections": cleaned_sections,
        "layout": {
            "page_margin_inches": margin_inches,
            "font_size_pt": font_size_pt,
            "line_spacing": line_spacing,
            "space_after_section": space_after_section,
            "density_status": density_status,
            "whitespace_balance_score": whitespace_score
        }
    }
