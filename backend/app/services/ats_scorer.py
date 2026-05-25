"""
ATS Compatibility Scoring Service.

Computes a comprehensive, multi-dimensional ATS score between 0.0 and 100.0,
representing how well a resume aligns with a specific job description.
"""

import logging
from typing import Any, Dict, List

from app.services.keyword_extractor import (
    analyze_keyword_importance,
    detect_measurable_achievements,
    detect_weak_verbs,
)
from app.services.semantic import calculate_semantic_similarity

logger = logging.getLogger(__name__)


async def calculate_ats_score(
    resume_text: str,
    resume_sections: Dict[str, Any],
    job_description: str,
    resume_keywords: Dict[str, Any],
    jd_keywords: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate a multi-dimensional ATS score with granular feedback and improvements.

    Scoring Dimensions:
    1. Keyword Match (30%) - TF-IDF weighted overlap of keywords.
    2. Skills Alignment (25%) - Specific required skills coverage.
    3. Semantic Similarity (15%) - Contextual deep-learning cosine match.
    4. Action Verbs (10%) - Frequency of strong active verbs vs weak/passive verbs.
    5. Achievements (10%) - Measurable, data-backed metric inclusions.
    6. Formatting (10%) - structural cleanliness, paragraph size, layouts.
    7. Completeness (10%) - Presence of core expected resume segments.

    Args:
        resume_text: Full raw text of the candidate's resume.
        resume_sections: Segmented sections of the resume.
        job_description: Target job description text.
        resume_keywords: Extracted resume keyword sets.
        jd_keywords: Extracted JD keyword sets.

    Returns:
        Dict containing:
        - "scores": The detailed breakdown matching ATSScoreBreakdown schema.
        - "missing_keywords": List of missing keyword dicts matching MissingKeyword schema.
        - "suggestions": List of actionable suggestion dicts matching Suggestion schema.
    """
    logger.info("Computing multi-dimensional ATS score...")

    suggestions = []
    missing_keywords = []

    # ── 1. Analyze JD Keywords & Importance ────────────────────────
    jd_keywords_details = analyze_keyword_importance(job_description, jd_keywords)
    
    # Flatten resume keywords for easy checks
    flat_resume_kws = set()
    for cat in ["hard_skills", "soft_skills", "tools", "certifications"]:
        flat_resume_kws.update(resume_keywords.get(cat, []))

    # Evaluate matches
    matched_kws = []
    unmatched_kws = []
    
    for item in jd_keywords_details:
        kw = item["keyword"].lower()
        if kw in flat_resume_kws or any(kw in r_kw.lower() for r_kw in flat_resume_kws):
            matched_kws.append(item)
        else:
            unmatched_kws.append(item)
            missing_keywords.append({
                "keyword": item["keyword"],
                "importance": item["importance"],
                "category": item["category"],
            })

    # Compute Keyword Match Score (weighted by importance)
    total_weight = 0.0
    earned_weight = 0.0
    importance_weights = {"high": 3.0, "medium": 2.0, "low": 1.0}
    
    for kw in jd_keywords_details:
        weight = importance_weights.get(kw["importance"], 1.0)
        total_weight += weight
        if kw in matched_kws:
            earned_weight += weight

    keyword_match_score = (earned_weight / total_weight * 100.0) if total_weight > 0 else 80.0
    keyword_match_score = round(keyword_match_score, 2)

    # ── 2. Compute Skills Alignment Score ─────────────────────────
    # Focus purely on hard_skills and tools matching
    jd_skills = jd_keywords.get("hard_skills", set()).union(jd_keywords.get("tools", set()))
    res_skills = resume_keywords.get("hard_skills", set()).union(resume_keywords.get("tools", set()))
    
    skills_matched = jd_skills.intersection(res_skills)
    skills_score = (len(skills_matched) / len(jd_skills) * 100.0) if jd_skills else 80.0
    skills_score = round(skills_score, 2)

    # Add missing skills to suggestions
    high_missing = [m for m in missing_keywords if m["importance"] == "high"][:5]
    if high_missing:
        suggestions.append({
            "category": "keywords",
            "priority": "high",
            "suggestion": f"Incorporate missing core skills: {', '.join([m['keyword'] for m in high_missing])} to drastically increase ATS matching.",
        })

    # ── 3. Compute Semantic Similarity ───────────────────────────
    semantic_similarity_score = await calculate_semantic_similarity(resume_text, job_description)

    # ── 4. Action Verbs Score ──────────────────────────────────────
    # Check experience bullets
    experience_entries = resume_sections.get("experience", [])
    all_bullets = []
    for entry in experience_entries:
        all_bullets.extend(entry.get("bullets", []))

    strong_verbs_count = len(resume_keywords.get("action_verbs", set()))
    weak_verbs_feedback = detect_weak_verbs(all_bullets)
    weak_verbs_count = len(weak_verbs_feedback)

    # Scoring out of 100. Base score of 70, +5 for strong verbs, -5 for weak ones.
    verb_score = 70.0 + (strong_verbs_count * 3.0) - (weak_verbs_count * 5.0)
    verb_score = max(30.0, min(100.0, verb_score))
    verb_score = round(verb_score, 2)

    if weak_verbs_feedback:
        suggestions.append({
            "category": "experience",
            "priority": "medium",
            "suggestion": f"Replace passive action verbs (e.g. '{weak_verbs_feedback[0]['weak_verbs'][0]}') in experience bullets with high-impact operational terms.",
        })

    # ── 5. Achievements Score ──────────────────────────────────────
    quantified_count, quantified_feedback = detect_measurable_achievements(all_bullets)
    total_bullets = len(all_bullets)

    # We want at least 50% of the bullet points to be quantified for a perfect score
    if total_bullets > 0:
        pct_quantified = quantified_count / total_bullets
        achievement_score = min(100.0, pct_quantified * 200.0)  # 50% = 100
    else:
        achievement_score = 70.0  # safe default

    achievement_score = round(achievement_score, 2)
    
    if total_bullets > 0 and quantified_count < (total_bullets / 2):
        suggestions.append({
            "category": "experience",
            "priority": "high",
            "suggestion": "Quantify your achievements. Add percentages, budget savings, or scale statistics to at least half of your experience bullet points.",
        })

    # ── 6. Formatting Score ──────────────────────────────────────
    # Heuristics:
    # - Avoid too long paragraphs (more than 4 lines)
    # - Bullet point counts (should have between 3 and 7 bullets per experience entry)
    formatting_score = 100.0
    
    for entry in experience_entries:
        b_count = len(entry.get("bullets", []))
        if b_count > 8:
            formatting_score -= 10.0
        elif b_count < 2:
            formatting_score -= 5.0

    # Max length safety
    if len(resume_text) > 12000:
        formatting_score -= 15.0  # too long for typical 1-2 pages
        suggestions.append({
            "category": "format",
            "priority": "medium",
            "suggestion": "Resume length is exceptionally long. Condense formatting to fit under 2 pages.",
        })

    formatting_score = max(40.0, min(100.0, formatting_score))
    formatting_score = round(formatting_score, 2)

    # ── 7. Completeness Score ────────────────────────────────────
    completeness_score = 100.0
    core_sections = ["summary", "experience", "education", "skills"]
    missing_sections = []
    
    for sec in core_sections:
        content = resume_sections.get(sec)
        if not content:
            completeness_score -= 25.0
            missing_sections.append(sec)

    if missing_sections:
        suggestions.append({
            "category": "format",
            "priority": "high",
            "suggestion": f"Your resume is missing critical sections: {', '.join(missing_sections)}. Complete them to satisfy basic parser constraints.",
        })

    # Missing Projects Diagnostic
    projects = resume_sections.get("projects")
    if not projects or len(projects) == 0:
        completeness_score -= 15.0
        suggestions.append({
            "category": "format",
            "priority": "high",
            "suggestion": "Missing Projects Section: Include 2–3 technical projects (ideally with GitHub links) to demonstrate hands-on ML/data skills, especially for data science internships.",
        })

    completeness_score = max(0.0, completeness_score)

    # ── 8. Composite Overall Score ───────────────────────────────
    overall_score = (
        keyword_match_score * 0.30
        + skills_score * 0.25
        + semantic_similarity_score * 0.15
        + verb_score * 0.10
        + achievement_score * 0.10
        + formatting_score * 0.05
        + completeness_score * 0.05
    )
    overall_score = max(0.0, min(100.0, overall_score))
    overall_score = round(overall_score, 2)

    scores_breakdown = {
        "overall_score": overall_score,
        "keyword_match_score": keyword_match_score,
        "semantic_similarity_score": semantic_similarity_score,
        "skills_alignment_score": skills_score,
        "action_verb_score": verb_score,
        "achievement_score": achievement_score,
        "formatting_score": formatting_score,
        "section_completeness_score": completeness_score,
    }

    return {
        "scores": scores_breakdown,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
    }
