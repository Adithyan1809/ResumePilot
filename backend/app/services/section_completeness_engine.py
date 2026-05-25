"""
Resume Section Completeness Engine.

Programmatically audits the presence, depth, and structural details of core sections
(summary, experience, education, skills, projects) and returns warnings and recommendations.
Does NOT fabricate any missing data.
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

def audit_section_completeness(sections: Dict[str, Any]) -> Dict[str, Any]:
    """Audits sections and calculates a granular completeness score (0-100).
    
    Checks:
    - Experience Presence & Bullet Counts (25 points)
    - Education Profile (degree, school, GPA, dates) (25 points)
    - Personal Projects Section & Details (20 points)
    - Professional Summary Word Count (15 points)
    - Technical Skills Categories (15 points)
    """
    warnings = []
    recommendations = []
    score = 100.0
    
    # ── 1. Audit Professional Summary (15 points) ──
    summary = sections.get("summary", "")
    summary_words = len(str(summary).split())
    
    if not summary:
        score -= 15.0
        warnings.append("Missing Professional Summary: Add a punchy, 3-4 line profile header.")
        recommendations.append("Draft a 50-70 word professional summary focusing on your AI/ML and engineering capabilities.")
    elif summary_words < 30:
        score -= 5.0
        warnings.append("Professional Summary is too brief: Currently contains fewer than 30 words.")
        recommendations.append("Expand your professional summary to highlight core technical stacks and targeted engineering roles.")
        
    # ── 2. Audit Professional Experience (25 points) ──
    experience = sections.get("experience", []) or []
    if not experience:
        score -= 25.0
        warnings.append("Missing Work Experience Section: Critical constraint for professional profiles.")
        recommendations.append("Detail your internship, lead, or freelance engineering roles, including company name, active dates, and bullet points.")
    else:
        for idx, entry in enumerate(experience):
            company = entry.get("company", "")
            role = entry.get("role", "")
            bullets = entry.get("bullets", []) or []
            
            if not company or not role:
                score -= 5.0
                warnings.append(f"Incomplete Work Experience Entry {idx+1}: Missing company name or role title.")
                recommendations.append(f"Provide the exact role title and company name for experience entry {idx+1}.")
                
            if len(bullets) < 2:
                score -= 5.0
                warnings.append(f"Insufficient Details in Experience Entry {idx+1}: Contains fewer than 2 bullet points.")
                recommendations.append(f"Write 3-4 action-oriented, metrics-driven bullet points for your role as '{role or 'Developer'}' at '{company or 'Company'}'.")
                
    # ── 3. Audit Personal Projects (20 points) ──
    projects = sections.get("projects", []) or []
    if not projects:
        score -= 20.0
        warnings.append("Missing Projects Section: Highly recommended for students and junior candidates.")
        recommendations.append("Include 2-3 technical projects (with technologies and GitHub links) to demonstrate hands-on system building.")
    else:
        for idx, entry in enumerate(projects):
            name = entry.get("name", "")
            techs = entry.get("technologies", []) or []
            desc = entry.get("description", []) or []
            bullets = [desc] if isinstance(desc, str) else list(desc) if isinstance(desc, list) else []
            
            if not name:
                score -= 4.0
                warnings.append(f"Incomplete Project {idx+1}: Missing project title.")
                recommendations.append(f"Add a clear, human-readable title for project entry {idx+1}.")
                
            if not techs:
                score -= 3.0
                warnings.append(f"Missing Tech Stack in Project {idx+1} ('{name or 'Project'}'): No technologies specified.")
                recommendations.append(f"Specify the technical stack (languages, frameworks) used to build '{name or 'Project'}'.")
                
            if len(bullets) < 2:
                score -= 3.0
                warnings.append(f"Insufficient Details in Project {idx+1} ('{name or 'Project'}'): Fewer than 2 bullets.")
                recommendations.append(f"Write at least 2 impact-focused description bullets for '{name or 'Project'}'.")

    # ── 4. Audit Technical Skills (15 points) ──
    skills = sections.get("skills", []) or []
    if not skills:
        score -= 15.0
        warnings.append("Missing Technical Skills Section: Mandatory for parsing filters.")
        recommendations.append("List programming languages, tools, frameworks, and database skills categorized for quick recruiter scannability.")
    elif len(skills) < 3:
        score -= 5.0
        warnings.append("Technical Skills coverage is thin: Contains fewer than 3 skills categories.")
        recommendations.append("Ensure you list at least 4 distinct technical skills categories (e.g. Languages, Databases, DevOps, Tools).")

    # ── 5. Audit Education (25 points) ──
    education = sections.get("education", []) or []
    if not education:
        score -= 25.0
        warnings.append("Missing Education Section: Critical for academic validation.")
        recommendations.append("Add your college/university history, including degrees, graduation dates, and GPAs.")
    else:
        for idx, entry in enumerate(education):
            school = entry.get("school", "")
            degree = entry.get("degree", "")
            dates = entry.get("dates", "")
            gpa = entry.get("gpa", "")
            
            if not school or not degree:
                score -= 5.0
                warnings.append(f"Incomplete Education Entry {idx+1}: Missing degree or school name.")
                recommendations.append(f"Specify school name and exact degree path for education entry {idx+1}.")
                
            if not gpa:
                warnings.append(f"Missing GPA in Education Entry {idx+1} ('{school or 'School'}'): GPA not specified.")
                recommendations.append(f"Add your cumulative GPA to education entry '{school or 'School'}' if above 3.0 to strengthen academic standing.")

    # Bound score
    completeness_score = max(10.0, min(100.0, round(score, 2)))
    
    return {
        "completeness_score": completeness_score,
        "warnings": warnings,
        "recommendations": recommendations
    }
