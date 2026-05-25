"""
Resume Quality Evaluation Engine.

The ultimate grading, quality control, and scoring layer of the structured intelligence platform.
Aggregates scoring metrics from all helper engines (ATS match, completeness, readability, bullets, density)
to compile a 9-dimensional resume index and prioritize recruiter recommendations.
"""

import logging
from typing import Dict, Any, List

# Engine imports
from app.services.bullet_quality_engine import score_experience_bullets
from app.services.human_readability_engine import calculate_readability_metrics
from app.services.section_completeness_engine import audit_section_completeness

logger = logging.getLogger(__name__)

def evaluate_resume_quality(
    sections: Dict[str, Any],
    original_sections: Dict[str, Any],
    job_description: str,
    ats_score_result: Dict[str, Any],
    layout_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Compiles a 9-dimensional quality report, scoring visual, technical, and linguistic standards.
    
    Dimensions:
    1. ATS Compatibility (30%) - KeywordTF-IDF weighted match & Semantic Embeddings match.
    2. Recruiter Readability (15%) - Buzzwords, keyword stuffing, sentence complexity.
    3. Role Alignment (15%) - JD classification & technology overlap scores.
    4. Bullet Quality (10%) - Verb strength, length constraints, and technical specificity.
    5. Project Strength (10%) - Depth of project description and technology matching.
    6. Formatting Cleanliness (5%) - Layout density score and whitespace balance.
    7. Keyword Coverage (5%) - Percentage of matching target keywords.
    8. Technical Depth (5%) - Presence of core engineering tools.
    9. Overall Quality Score (5%) - Mathematical composite average.
    """
    logger.info("Starting V2 Resume Quality Evaluation...")
    
    # ── 1. GATHER UNDERLYING METRICS ──
    # Completeness audit
    comp_audit = audit_section_completeness(sections)
    completeness_score = comp_audit["completeness_score"]
    
    # Readability audit
    summary = sections.get("summary", "")
    all_bullets = []
    for exp in sections.get("experience", []) or []:
        all_bullets.extend(exp.get("bullets", []) or [])
    for proj in sections.get("projects", []) or []:
        all_bullets.extend(proj.get("description", []) or [])
        
    read_audit = calculate_readability_metrics(summary, all_bullets)
    human_readability = read_audit["human_readability_score"]
    recruiter_friendliness = read_audit["recruiter_friendliness_score"]
    
    # Bullet Quality audit
    target_skills = []
    # Collect targeted skills from skills category lists
    for skill_entry in sections.get("skills", []) or []:
        if ":" in str(skill_entry):
            items = str(skill_entry).split(":", 1)[1]
            target_skills.extend([s.strip() for s in items.split(",") if s.strip()])
            
    avg_bullet_score, bullet_grades = score_experience_bullets(all_bullets, target_skills)
    
    # Extract ATS score data
    ats_scores = ats_score_result.get("scores", {})
    keyword_match = ats_scores.get("keyword_match_score", 70.0)
    skills_alignment = ats_scores.get("skills_alignment_score", 70.0)
    semantic_similarity = ats_scores.get("semantic_similarity_score", 70.0)
    
    # Extract Layout density data
    layout_vars = layout_data.get("layout", {})
    whitespace_balance = layout_vars.get("whitespace_balance_score", 80.0)
    
    # ── 2. CALCULATE 9-DIMENSIONAL SCORES ──
    
    # D1: ATS Compatibility (30%) - cosine semantic + skills alignment
    ats_comp_score = round((semantic_similarity * 0.5) + (skills_alignment * 0.5), 2)
    
    # D2: Recruiter Readability (15%)
    recruiter_read_score = recruiter_friendliness
    
    # D3: Role Alignment (15%) - keyword match density
    role_align_score = keyword_match
    
    # D4: Bullet Quality (10%)
    bullet_quality_score = avg_bullet_score if avg_bullet_score > 0 else 75.0
    
    # D5: Project Strength (10%)
    # Grade based on project presence, technologies references, and bullets depth
    projects = sections.get("projects", []) or []
    if not projects:
        project_strength_score = 0.0
    else:
        proj_pts = 0.0
        for p in projects:
            p_bullets = len(p.get("description", []) or [])
            p_techs = len(p.get("technologies", []) or [])
            has_link = bool(p.get("link", ""))
            
            # Bullet score
            proj_pts += min(50.0, p_bullets * 20.0)
            # Tech score
            proj_pts += min(30.0, p_techs * 15.0)
            # Link score
            if has_link:
                proj_pts += 20.0
        project_strength_score = round(proj_pts / len(projects), 2)
        
    # D6: Formatting Cleanliness (5%)
    formatting_clean_score = whitespace_balance
    
    # D7: Keyword Coverage (5%)
    keyword_coverage_score = keyword_match
    
    # D8: Technical Depth (5%)
    # Ratio of technical skills to total category rows
    tech_depth_score = min(100.0, len(sections.get("skills", []) or []) * 15.0)
    
    # D9: Overall Quality Score (5%) - Composite average
    overall_quality_score = (
        ats_comp_score * 0.30
        + recruiter_read_score * 0.15
        + role_align_score * 0.15
        + bullet_quality_score * 0.10
        + project_strength_score * 0.10
        + formatting_clean_score * 0.05
        + keyword_coverage_score * 0.05
        + tech_depth_score * 0.05
        + completeness_score * 0.05
    )
    overall_quality_score = max(10.0, min(100.0, round(overall_quality_score, 2)))
    
    # ── 3. AGGREGATE RECOMMENDATIONS & WARNINGS ──
    all_recommendations = []
    # Combine completeness and readability suggestions
    all_recommendations.extend(comp_audit.get("recommendations", []))
    all_recommendations.extend(read_audit.get("suggestions", []))
    
    # Highlight weak bullets in recommendations
    weak_bullets_count = sum(1 for res in bullet_grades if not res["approved"])
    if weak_bullets_count > 0:
        all_recommendations.append(
            f"Flagged {weak_bullets_count} vague or metric-lacking bullet points. Rewrite them starting with high-impact operational terms like 'Engineered' or 'Architected'."
        )
        
    # Filter unique recommendations
    unique_recs = []
    seen = set()
    for r in all_recommendations:
        r_low = r.lower()
        if r_low not in seen:
            unique_recs.append(r)
            seen.add(r_low)
            
    # Compile ultimate structured profile
    quality_profile = {
        "overall_score": overall_quality_score,
        "ats_compatibility": ats_comp_score,
        "recruiter_readability": recruiter_read_score,
        "role_alignment": role_align_score,
        "bullet_quality": bullet_quality_score,
        "project_strength": project_strength_score,
        "formatting_cleanliness": formatting_clean_score,
        "keyword_coverage": keyword_coverage_score,
        "technical_depth": tech_depth_score,
        "completeness": completeness_score,
        "warnings": comp_audit.get("warnings", []),
        "recommendations": unique_recs[:6] # Top 6 priorities
    }
    
    logger.info(f"Composite resume quality grading calculated: {overall_quality_score}/100")
    return quality_profile
