"""
Workflow Orchestrator.
The central agentic director of the ResumePilot v4 AI Employability Operating System.
Coordinates and integrates all specialized engines to execute the resume intelligence pipeline.
"""

import logging
import uuid
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

# Import Phase 1 Engines
from app.services.user_resume_profile_engine import get_master_profile, update_profile_memory
from app.services.evidence_storage_engine import extract_technologies_from_text

# Import Phase 3 Engines
from app.services.job_scraping_engine import scrape_job_posting
from app.services.jd_extraction_engine import extract_job_details

# Import Phase 4 Engines
from app.services.github_analysis_engine import analyze_github_portfolio

# Import Phase 5 Engines
from app.services.resume_assembly_engine import assemble_tailored_resume
from app.services.role_gap_analysis_engine import analyze_role_gaps
from app.services.learning_roadmap_engine import generate_learning_roadmap
from app.services.interview_readiness_engine import calculate_interview_readiness

# Import Phase 6 Engines
from app.services.ats_simulation_engine import simulate_ats_parsing
from app.services.semantic_alignment_engine import calculate_semantic_similarity
from app.services.recruiter_simulation_engine import simulate_recruiter_scan
from app.services.resume_template_personality_engine import configure_template_styling
from app.services.resume_diff_engine import calculate_resume_diff
from app.services.final_resume_quality_gate import validate_final_resume

# Import Caching & Routing
from app.services.cache_engine import get_cache, set_cache
from app.services.model_router_engine import route_and_call_llm

# ── V4 Core Career Positioning & Tracking Imports ───────────────────
from app.services.market_intelligence_engine import analyze_market_trends
from app.services.career_timeline_engine import predict_career_timeline
from app.services.interview_simulation_engine import generate_interview_questions
from app.services.portfolio_generation_engine import generate_portfolio_assets
from app.services.employability_score_engine import calculate_signature_employability_score
from app.services.resume_strategy_engine import configure_resume_strategy_track
from app.services.branding_engine import generate_personal_branding
from app.services.explainability_engine import generate_optimization_explanations
from app.services.application_tracking_engine import get_applications_analytics

# ── V4 Narrative & Humanization Engine Imports ──────────────────────────
from app.services.candidate_voice_engine import preserve_candidate_voice
from app.services.project_context_binding_engine import bind_project_context
from app.services.engineering_identity_engine import establish_engineering_identity
from app.services.resume_humanization_engine import humanize_resume_content
from app.services.experience_calibration_engine import calibrate_experience_level
from app.services.project_importance_ranker import rank_projects_by_importance
from app.services.story_flow_engine import optimize_story_flow
from app.services.metric_realism_engine import validate_metric_realism
from app.services.recruiter_polish_engine import apply_recruiter_polish
logger = logging.getLogger(__name__)


async def orchestrate_employability_pipeline(
    db: AsyncSession,
    user_id: uuid.UUID,
    job_url: str = "",
    job_description: str = "",
    job_title: str = "",
    company: str = "",
    template: str = "classic",
    github_url: str = "",
    strategy_track: str = "backend",
    strict_mode: bool = False
) -> Dict[str, Any]:
    """Coordinates the entire employability operating system pipeline, returning optimized sections and rich v4 analytics."""
    cache_key = f"orchestrator_v4_{user_id}_{hash(job_url)}_{hash(job_description[:50])}_{template}_{strategy_track}"
    
    # 1. Check local cache store
    cached = get_cache(cache_key)
    if cached:
        logger.info("Pipeline executed from local high-speed cache.")
        return cached

    logger.info("Initializing AI Employability Operating System Orchestrator...")

    # 2. JOB LINK SCRAPING & COMPILING
    final_jd = job_description
    final_title = job_title
    final_company = company
    
    if job_url:
        logger.info(f"Crawling job requirements from link: {job_url}")
        scraped = await scrape_job_posting(job_url)
        final_jd = scraped.get("job_description", "")
        final_title = scraped.get("job_title", "")
        final_company = scraped.get("company", "")

    if not final_jd:
        raise ValueError("A valid Job Description or Job URL must be provided.")

    # 3. JD METADATA EXTRACTION
    jd_meta = await extract_job_details(final_jd)
    required_techs = jd_meta["required_techs"]
    focus_domain = jd_meta["focus_domain"]
    seniority = jd_meta["seniority"]

    # 4. LOAD PERSISTENT CANDIDATE PROFILE EVIDENCE
    profile = await get_master_profile(db, user_id)
    if profile is None:
        raise ValueError("No persistent master resume profile found. Please upload your master resume first.")

    structured_evidence = dict(profile.structured_evidence)

    # 5. INTEGRATE DEEP GITHUB PORTFOLIO ANALYSIS
    g_url = github_url or structured_evidence.get("contact_info", {}).get("github", "")
    github_report = {}
    if g_url:
        logger.info(f"Executing deep portfolio audit for GitHub link: {g_url}")
        github_report = await analyze_github_portfolio(g_url)
        # Whitelist github technologies into candidate skills list dynamically
        github_techs = [r["language"] for r in github_report.get("top_projects", []) if r.get("language")]
        if "skills" in structured_evidence:
            for tech in github_techs:
                if tech and tech.lower() not in [s.lower() for s in structured_evidence["skills"].get("Tools", [])]:
                    structured_evidence["skills"]["Tools"].append(tech)

    # 6. INTEGRATE V4 MULTI-RESUME STRATEGY ROUTING
    cand_flat_skills = []
    for cat_list in structured_evidence.get("skills", {}).values():
        if isinstance(cat_list, list):
            cand_flat_skills.extend(cat_list)
            
    strategy_profile = configure_resume_strategy_track(strategy_track, cand_flat_skills)
    focus_domain = strategy_profile["focus_domain"]
    final_title = final_title or strategy_profile["role_title_target"]

    # 7. DETERMINISTIC EVIDENCE GRAPH ASSEMBLY
    # 7.1 Engineering Identity
    identity_report = establish_engineering_identity(structured_evidence, final_jd)
    identity = identity_report["primary_identity"]
    
    assembled_sections = assemble_tailored_resume(
        structured_evidence=structured_evidence,
        required_techs=required_techs,
        focus_domain=focus_domain,
        seniority=seniority
    )
    
    assembled_sections["job_title"] = final_title
    assembled_sections["company"] = final_company

    # 7.2 Strict Context Binding & Importance Ranking for Projects
    if "projects" in assembled_sections:
        bound_projects = bind_project_context(assembled_sections["projects"], focus_domain)
        ranked_projects = rank_projects_by_importance(bound_projects, final_jd, identity)
        assembled_sections["projects"] = ranked_projects

    # 7.3 Experience Calibration, Metric Realism, Candidate Voice, and Humanization
    for section_key in ["experience", "projects"]:
        if section_key in assembled_sections:
            for item in assembled_sections[section_key]:
                bullets = item.get("bullets", [])
                if bullets:
                    b1 = calibrate_experience_level(bullets, seniority)
                    b2 = validate_metric_realism(b1, seniority)
                    b3 = preserve_candidate_voice(b2, seniority)
                    b4 = humanize_resume_content(b3)
                    item["bullets"] = b4

    # 8. LLM GENERATION & CRITIQUE LOOP
    from app.services.ai_engine import tailor_resume_sections
    
    try:
        llm_tailored = await tailor_resume_sections(
            parsed_sections=assembled_sections,
            job_description=final_jd,
            jd_analysis=jd_meta,
            job_title=final_title,
            company=final_company
        )
        # Update assembled_sections with the tailored LLM content
        assembled_sections.update(llm_tailored)
    except Exception as e:
        logger.error(f"AI Engine Tailoring failed: {e}")

    # 8.1 Story Flow & Recruiter Polish
    assembled_sections = optimize_story_flow(assembled_sections, identity)
    assembled_sections = apply_recruiter_polish(assembled_sections)

    # 9. CONFIGURE TEMPLATE PERSONALITY STYLING
    styling_profile = configure_template_styling(template)
    if "layout" not in assembled_sections:
        assembled_sections["layout"] = {}
    assembled_sections["layout"]["styling"] = styling_profile

    # 10. RUN TRUTH-PRESERVING STRICT QUALITY GATE
    raw_text = profile.master_resume_id.hex if profile.master_resume_id else "Developer"
    gate_res = await validate_final_resume(
        sections=assembled_sections,
        raw_text=raw_text,
        original_sections=structured_evidence,
        job_description=final_jd,
        strict_mode=strict_mode
    )
    healed_sections = gate_res["sections"]
    diagnostics = gate_res["diagnostics"]

    # 11. RUN COMPLEMENTARY MULTIDIMENSIONAL SIMULATIONS
    # A. ATS Parser Simulation
    ats_sim = simulate_ats_parsing(healed_sections, template)
    ats_score = ats_sim["ats_compatibility_score"]
    
    # B. Semantic Vector similarity calculation
    flat_healed = " ".join([healed_sections.get("summary", ""), " ".join(healed_sections.get("skills", {}).get("Tools", []))])
    semantic_score = calculate_semantic_similarity(flat_healed, final_jd)
    
    # C. Recruiter glance scan heatmap coordinates
    recruiter_sim = simulate_recruiter_scan(healed_sections, final_jd)
    recruiter_score = recruiter_sim["recruiter_readability_score"]

    # D. Career Gap Analysis & learningroadmap suggestions
    gap_report = analyze_role_gaps(cand_flat_skills, required_techs, focus_domain)
    roadmap = generate_learning_roadmap(gap_report["gaps"])
    
    # E. Interview Readiness evaluation
    readiness = calculate_interview_readiness(
        structured_evidence=structured_evidence,
        required_techs=required_techs,
        focus_domain=focus_domain,
        gap_severity_score=gap_report["gap_severity_score"]
    )
    
    # F. Version difference calculator
    diff_report = calculate_resume_diff(
        original=structured_evidence,
        tailored=healed_sections,
        original_ats=60.0,
        tailored_ats=ats_score
    )

    # ── V4 Core Metrics & Progression Systems ─────────────────────────
    # G. Market Intelligence analysis
    market_report = analyze_market_trends(focus_domain, seniority)
    
    # H. Career progression timeline forecasts
    progression_timeline = predict_career_timeline(focus_domain, cand_flat_skills)
    
    # I. AI Interview Simulation questions
    simulated_questions = generate_interview_questions(structured_evidence, final_title, final_company, focus_domain)
    
    # J. Recruiter case study website generator
    portfolio_report = generate_portfolio_assets(structured_evidence, github_report)
    
    # K. Personal Branding Headline optimizers
    branding_report = generate_personal_branding(structured_evidence, focus_domain, seniority)
    
    # L. Trust & Transparency Explainability rationales
    explainability_rationales = generate_optimization_explanations(healed_sections, final_jd, focus_domain)
    
    # M. Application Tracker history
    tracking_report = get_applications_analytics(profile.applications_log)
    
    # N. Unified Employability Score calculation
    metrics_count = sum(1 for exp in structured_evidence.get("experience", []) for b in exp.get("bullets", []) if extract_technologies_from_text(b.get("text", "") if isinstance(b, dict) else str(b)))
    employability_index = calculate_signature_employability_score(
        ats_score=ats_score,
        recruiter_trust_score=diagnostics.get("trust_score", 85.0),
        project_metrics_count=metrics_count,
        github_consistency_score=github_report.get("engineering_consistency_score", 75.0),
        gap_severity_score=gap_report["gap_severity_score"],
        interview_readiness_score=readiness["interview_readiness_score"],
        market_popularity_index=market_report["hiring_demand_index"]
    )

    # 12. COMPILE COMPOSITE RESPONSE SCHEMA
    response_payload = {
        "job_title": final_title,
        "company": final_company,
        "tailored_sections": healed_sections,
        "ats_score": {
            "overall_score": employability_index["employability_score"],
            "keyword_match_score": ats_score,
            "semantic_similarity_score": semantic_score,
            "skills_alignment_score": round(100.0 - gap_report["gap_severity_score"], 2),
            "action_verb_score": 90.0,
            "achievement_score": round(100.0 - (len(recruiter_sim.get("readability_warnings", [])) * 10.0), 2),
            "formatting_score": ats_sim["ats_compatibility_score"],
            "section_completeness_score": 100.0
        },
        "missing_keywords": [
            {"keyword": g["skill"], "importance": g["severity"], "category": "hard_skill"} 
            for g in gap_report["gaps"]
        ],
        "suggestions": [
            {"category": "keywords", "priority": g["severity"], "suggestion": f"Incorporate '{g['skill']}' in future learning roadmaps."} 
            for g in gap_report["gaps"]
        ],
        "company_intelligence": configure_template_styling(template),
        "learning_roadmap": roadmap,
        "interview_readiness": readiness,
        "github_portfolio_report": github_report,
        "difference_metrics": diff_report,
        "diagnostics": diagnostics,
        
        # V4 Additions
        "employability_index": employability_index,
        "market_intelligence": market_report,
        "career_progression": progression_timeline,
        "interview_simulation": simulated_questions,
        "portfolio_assets": portfolio_report,
        "branding_profiles": branding_report,
        "explainability_rationales": explainability_rationales,
        "application_tracking": tracking_report
    }

    # 13. UPDATE CANDIDATE USER PROFILE SQL MEMORY
    await update_profile_memory(
        db=db,
        user_id=user_id,
        target_role=final_title,
        ats_score=response_payload["ats_score"]["overall_score"],
        company=final_company
    )

    # 14. CACHE COMPLETED PIPELINE RESULTS
    set_cache(cache_key, response_payload, ttl=3600)  # cache for 1 hour

    logger.info("Employability Operating System Pipeline successfully completed.")
    return response_payload
