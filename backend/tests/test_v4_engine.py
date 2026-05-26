"""
Automated unit and integration test suite for the ResumePilot v4 AI Employability Operating System.
Tests all 9 V4 core engines for career intelligence, tracking, timelines, and strategy optimization.
"""

import os
import sys
import uuid
import asyncio
from unittest.mock import AsyncMock, MagicMock

# Prepend backend parent path to sys path to import app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import V4 core engines
from app.services.application_tracking_engine import log_job_application, update_application_status, get_applications_analytics
from app.services.market_intelligence_engine import analyze_market_trends, rank_missing_skills_by_market_value
from app.services.career_timeline_engine import predict_career_timeline
from app.services.interview_simulation_engine import generate_interview_questions
from app.services.portfolio_generation_engine import generate_portfolio_assets
from app.services.employability_score_engine import calculate_signature_employability_score
from app.services.resume_strategy_engine import configure_resume_strategy_track
from app.services.branding_engine import generate_personal_branding
from app.services.explainability_engine import generate_optimization_explanations

# ── Mock Structured Evidence Mappings ─────────────────────────────────────
MOCK_STRUCTURED_EVIDENCE = {
    "contact_info": {
        "name": "Jordan Vance",
        "email": "jordan@vance.dev",
        "github": "github.com/jordanvance"
    },
    "skills": {
        "Programming Languages": ["Python", "Go", "TypeScript"],
        "Databases": ["PostgreSQL", "Redis"],
        "Tools": ["Docker", "Kubernetes", "Git"]
    },
    "projects": [
        {
            "title": "ScaleResilient API Gateway",
            "technologies": ["Python", "FastAPI", "Redis", "Docker"],
            "description": [
                "Designed a rate-limited REST gateway processing 15k requests/sec.",
                "Integrated Redis connection pooling reducing server response times by 35%."
            ]
        }
    ]
}


async def test_application_tracking_engine():
    """Verify application tracking logs and calibration weights based on outcomes."""
    # 1. Test analytics compiler
    mock_log = {
        "applications": [
            {"id": "1", "company": "Stripe", "job_title": "Backend Engineer", "status": "callback"},
            {"id": "2", "company": "Google", "job_title": "SWE", "status": "applied"},
            {"id": "3", "company": "Meta", "job_title": "Production Engineer", "status": "rejected"}
        ]
    }
    analytics = get_applications_analytics(mock_log)
    assert analytics["total_applied"] == 3
    assert analytics["callbacks"] == 1
    assert analytics["rejections"] == 1
    assert analytics["success_rate"] == 33.33

    # 2. Test database application logger with mocked AsyncSession
    db_mock = AsyncMock()
    user_id = uuid.uuid4()
    
    profile_mock = MagicMock()
    profile_mock.applications_log = {}
    profile_mock.profile_memory = {}
    
    # Setup master profile resolver mock directly on the imported module in application_tracking_engine
    import app.services.application_tracking_engine
    orig_get_profile = app.services.application_tracking_engine.get_master_profile
    app.services.application_tracking_engine.get_master_profile = AsyncMock(return_value=profile_mock)
    
    try:
        # Test logging application
        log_res = await log_job_application(db_mock, user_id, "Stripe", "Backend Systems Engineer")
        assert log_res["success"] is True
        assert "application_id" in log_res
        
        # Test updating status
        app_id = log_res["application_id"]
        update_res = await update_application_status(db_mock, user_id, app_id, "rejected")
        assert update_res["success"] is True
        assert profile_mock.profile_memory["calibrated_rejection_weight"] == 1.5
    finally:
        app.services.application_tracking_engine.get_master_profile = orig_get_profile


def test_market_intelligence_engine():
    """Verify that market intelligence compiles trends and ranks missing tech stacks."""
    # 1. Test market trends compiler
    trends = analyze_market_trends("backend", "senior")
    assert trends["domain"] == "backend"
    assert trends["seniority_level"] == "senior"
    assert trends["average_salary_band"] == "$150k - $200k"
    assert "Fastapi" in trends["trending_technologies"]
    assert "Go" in trends["trending_technologies"]
    
    # 2. Test prioritizing missing skills
    missing = ["Sass", "Kubernetes", "Matplotlib", "Fastapi"]
    ranked = rank_missing_skills_by_market_value(missing, "backend")
    # Kubernetes and FastAPI are trending in backend stack, so they should be prioritized first
    assert ranked[0] in ["Fastapi", "Kubernetes"]
    assert ranked[1] in ["Fastapi", "Kubernetes"]


def test_career_timeline_engine():
    """Assert linear multi-year career path predictions map milestones correctly."""
    skills = ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "Git", "Kubernetes", "gRPC"]
    timeline = predict_career_timeline("backend", skills)
    
    assert timeline["current_position_index"] == 1
    assert len(timeline["progression_path"]) == 4
    assert timeline["progression_path"][0]["title"] == "Backend Engineering Intern"
    assert "gRPC" in timeline["suggested_career_transition"] or "Systems" in timeline["suggested_career_transition"]


def test_interview_simulation_engine():
    """Verify simulated STAR and technical questions generated from resume evidence."""
    sim = generate_interview_questions(MOCK_STRUCTURED_EVIDENCE, "Backend Systems Engineer", "Stripe", "backend")
    
    assert sim["job_title"] == "Backend Systems Engineer"
    assert sim["company"] == "Stripe"
    assert len(sim["simulated_questions"]["technical"]) >= 2
    assert len(sim["simulated_questions"]["project_based"]) >= 1
    assert "ScaleResilient API Gateway" in sim["simulated_questions"]["project_based"][0]


def test_portfolio_generation_engine():
    """Verify markdown portfolio and recruiter-focused case studies compilation."""
    github_report = {"username": "jordanvance", "engineering_consistency_score": 85.0}
    assets = generate_portfolio_assets(MOCK_STRUCTURED_EVIDENCE, github_report)
    
    assert assets["github_linked"] is True
    assert "Featured Engineering Projects" in assets["portfolio_markdown"]
    assert "ScaleResilient API Gateway" in assets["portfolio_markdown"]
    assert len(assets["case_studies"]) == 1
    assert assets["case_studies"][0]["project_name"] == "ScaleResilient API Gateway"


def test_employability_score_engine():
    """Assert composite employability signature score synthesis."""
    score_data = calculate_signature_employability_score(
        ats_score=85.0,
        recruiter_trust_score=90.0,
        project_metrics_count=3,
        github_consistency_score=82.0,
        gap_severity_score=10.0,
        interview_readiness_score=80.0,
        market_popularity_index="High"
    )
    
    assert score_data["employability_score"] >= 80.0
    assert score_data["employability_band"] in ["Recruiter Magnet (Top 2%)", "Highly Employable (Top 10%)"]
    assert score_data["composite_dimensions"]["ats_readiness"] == "Excellent"
    assert score_data["composite_dimensions"]["recruiter_trust"] == "High Trust"


def test_resume_strategy_engine():
    """Verify master track strategy alignments from the same evidence base."""
    # Test Backend Strategy
    backend_strategy = configure_resume_strategy_track("backend", ["Python", "FastAPI", "React", "PostgreSQL"])
    assert backend_strategy["strategy_track"] == "backend"
    assert "FastAPI" in backend_strategy["target_keywords"]
    
    # Test AI/ML Strategy aliases
    ai_strategy = configure_resume_strategy_track("ai", ["Python", "PyTorch", "Pandas", "React"])
    assert ai_strategy["strategy_track"] == "ai_ml"
    assert "PyTorch" in ai_strategy["target_keywords"]


def test_branding_engine():
    """Verify optimized personal branding copy creation."""
    branding = generate_personal_branding(MOCK_STRUCTURED_EVIDENCE, "backend", "Senior")
    
    assert "Senior-Level Systems Engineer" in branding["linkedin_headline"]
    assert "Jordan Vance" in branding["linkedin_about"]
    assert "Systems Developer exploring" in branding["github_bio"]


def test_explainability_engine():
    """Verify optimization explainability cards detailing layout reasoning."""
    explanations = generate_optimization_explanations(
        tailored_sections=MOCK_STRUCTURED_EVIDENCE,
        job_description="We are seeking a Backend Engineer with Python and FastAPI skills.",
        focus_domain="backend"
    )
    
    assert len(explanations) >= 3
    assert explanations[0]["component"] == "Professional Summary"
    assert "Technical Skills Matrix" in [e["component"] for e in explanations]


async def test_orchestrator_integration():
    """Verify that the full v4 orchestrator pipeline compiles and executes cleanly with mocked dependencies."""
    from app.services.workflow_orchestrator import orchestrate_employability_pipeline
    import app.services.workflow_orchestrator
    
    # Mock master profile
    profile_mock = MagicMock()
    profile_mock.structured_evidence = MOCK_STRUCTURED_EVIDENCE
    profile_mock.master_resume_id = uuid.uuid4()
    profile_mock.profile_memory = {}
    profile_mock.applications_log = {}
    
    # Store originals
    orig_get_profile = app.services.workflow_orchestrator.get_master_profile
    orig_update_memory = app.services.workflow_orchestrator.update_profile_memory
    orig_call_llm = app.services.workflow_orchestrator.route_and_call_llm
    
    # Setup mocks
    app.services.workflow_orchestrator.get_master_profile = AsyncMock(return_value=profile_mock)
    app.services.workflow_orchestrator.update_profile_memory = AsyncMock(return_value=profile_mock)
    app.services.workflow_orchestrator.route_and_call_llm = AsyncMock(return_value="Polished summary evidence.")
    
    db_mock = AsyncMock()
    user_id = uuid.uuid4()
    
    try:
        response = await orchestrate_employability_pipeline(
            db=db_mock,
            user_id=user_id,
            job_description="We need a Backend Systems Engineer skilled in Python, FastAPI, Redis, and Docker.",
            job_title="Backend Systems Engineer",
            company="Stripe",
            strategy_track="backend",
            github_url="https://github.com/jordanvance"
        )
        
        # Verify the v4 response structure is fully compiled
        assert response["job_title"] == "Backend Systems Engineer"
        assert response["company"] == "Stripe"
        assert "employability_index" in response
        assert "market_intelligence" in response
        assert "career_progression" in response
        assert "interview_simulation" in response
        assert "portfolio_assets" in response
        assert "branding_profiles" in response
        assert "explainability_rationales" in response
        assert "application_tracking" in response
        assert response["employability_index"]["employability_score"] >= 35.0
    finally:
        # Restore originals
        app.services.workflow_orchestrator.get_master_profile = orig_get_profile
        app.services.workflow_orchestrator.update_profile_memory = orig_update_memory
        app.services.workflow_orchestrator.route_and_call_llm = orig_call_llm
