"""
Automated unit and integration test suite for the Deterministic ATS Resume Engine (V2).
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

# Prepend the parent directory (backend) to the Python path to allow app.* imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.validation import sanitize_and_validate_tailored_sections
from app.services.content_density_manager import manage_content_density
from app.services.alignment import classify_role_by_jd, reorder_sections_by_role
from app.services.resume_quality_engine import evaluate_resume_quality
from app.services.doc_generator import generate_pdf, generate_docx

# ── Mock Data for Resume and JD ───────────────────────────────
MOCK_RAW_TEXT = """
Jane Doe
Software Engineer
jane@example.com | 123-456-7890 | Seattle, WA
linkedin.com/in/janedoe

SUMMARY
Experienced software developer specializing in React and backend services. Optimized database queries and system latency.

EXPERIENCE
Software Engineer at Innovate Corp (2023 - Present)
- Developed attendance modules using React and Python.
- Optimized query latency by 35% on critical Postgres endpoints.
- Managed and deployed CI/CD pipelines on AWS.

SKILLS
Python, JavaScript, React, PostgreSQL, Docker, AWS, Git

EDUCATION
Bachelor of Science in Computer Science, University of Washington (2020 - 2024), GPA: 3.8
"""

MOCK_ORIGINAL_SECTIONS = {
    "contact_info": {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "123-456-7890",
        "location": "Seattle, WA",
        "linkedin": "linkedin.com/in/janedoe"
    },
    "summary": "Experienced software developer specializing in React and backend services.",
    "experience": [
        {
            "role": "Software Engineer",
            "company": "Innovate Corp",
            "dates": "2023 - Present",
            "bullets": [
                "Developed attendance modules using React and Python.",
                "Optimized query latency by 35% on critical Postgres endpoints.",
                "Managed and deployed CI/CD pipelines on AWS."
            ]
        }
    ],
    "skills": ["Python", "JavaScript", "React", "PostgreSQL", "Docker", "AWS", "Git"],
    "education": [
        {
            "school": "University of Washington",
            "degree": "Bachelor of Science in Computer Science",
            "dates": "2020 - 2024",
            "gpa": "3.8"
        }
    ]
}

MOCK_TAILORED_SECTIONS = {
    "summary": "Experienced software developer specializing in React and backend services.",
    "experience": [
        {
            "role": "Software Engineer",
            "company": "Innovate Corp",
            "dates": "2023 - Present",
            "bullets": [
                "Developed attendance modules using React and Python.",
                "Optimized query latency by 35% on critical Postgres endpoints.",
                "Managed and deployed CI/CD pipelines on AWS."
            ]
        }
    ],
    "skills": ["Python", "JavaScript", "React", "PostgreSQL", "Docker", "AWS", "Git"]
}

MOCK_JD_TEXT = """
We are looking for a Backend Engineer with strong expertise in Python, FastAPI, PostgreSQL, Redis, and Docker.
You will design scalable APIs and manage database query optimizations.
"""

async def test_loud_schema_failures():
    """Verify that malformed tailored sections raise explicit ValueErrors (no silent repair)."""
    # 1. Non-dict tailored sections
    try:
        await sanitize_and_validate_tailored_sections(MOCK_RAW_TEXT, "not a dict", MOCK_ORIGINAL_SECTIONS)
        assert False, "Should have raised ValueError for non-dictionary tailored input"
    except ValueError as e:
        assert "Tailored resume sections must be a valid JSON dictionary" in str(e)

    # 2. Missing key sections
    malformed_missing = {"summary": "Only summary"}
    try:
        await sanitize_and_validate_tailored_sections(MOCK_RAW_TEXT, malformed_missing, MOCK_ORIGINAL_SECTIONS)
        assert False, "Should have raised ValueError for missing sections"
    except ValueError as e:
        assert "Tailored resume sections are missing the required" in str(e)

    # 3. Malformed experience bullet type
    malformed_bullets = {
        "summary": "Summary text",
        "experience": [{"role": "Eng", "bullets": "not a list"}],
        "skills": ["Python"]
    }
    try:
        await sanitize_and_validate_tailored_sections(MOCK_RAW_TEXT, malformed_bullets, MOCK_ORIGINAL_SECTIONS)
        assert False, "Should have raised ValueError for malformed experience bullet list"
    except ValueError as e:
        assert "must contain a 'bullets' list" in str(e)

def test_content_density_manager():
    """Verify density manager trims lists and establishes layout variables."""
    # Create large list of bullets/skills to trigger density compaction
    oversized_sections = {
        "contact_info": {},
        "summary": "Summary text",
        "experience": [
            {
                "role": "Eng",
                "bullets": [f"Bullet point {i}" for i in range(10)] # triggers limit
            }
        ],
        "skills": [
            "Programming Languages: Python, Go, C++, Rust, Java, JS, TS, Ruby, SQL",
            "Databases: Postgres, MySQL, Redis, MongoDB, Cassandra, DynamoDB, SQLite",
            "Tools: Git, Docker, Kubernetes, AWS, GCP, Terraform, Jenkins",
            "Libraries: React, FastAPI, Numpy, Pandas, PyTorch, TensorFlow, OpenCV"
        ],
        "projects": [
            {
                "name": "P1",
                "technologies": ["React"],
                "description": ["Desc 1", "Desc 2", "Desc 3", "Desc 4", "Desc 5"]
            }
        ]
    }
    
    result = manage_content_density(oversized_sections)
    
    # Assert experience bullets are limited to MAX_EXPERIENCE_BULLETS (4)
    assert len(result["sections"]["experience"][0]["bullets"]) == 4
    
    # Assert project bullets are limited to MAX_PROJECT_BULLETS (3)
    assert len(result["sections"]["projects"][0]["description"]) == 3
    
    # Assert skills per category trimmed to MAX_SKILLS_PER_CATEGORY (7)
    skills_row = result["sections"]["skills"][0]
    assert len(skills_row.split(":")[1].split(",")) <= 7
    
    # Assert layout variables are populated
    assert "layout" in result
    assert result["layout"]["density_status"] == "compact"
    assert result["layout"]["page_margin_inches"] == 0.5

async def test_role_classification_and_reordering():
    """Verify JD role classification and section/project alignment."""
    # 1. Classify role
    role = await classify_role_by_jd(MOCK_JD_TEXT)
    assert role == "backend"
    
    # 2. Reorder sections
    reordered = reorder_sections_by_role(MOCK_TAILORED_SECTIONS, role)
    assert list(reordered.keys())[0] == "summary" # or contact_info if present

def test_resume_quality_evaluation():
    """Verify the 9-dimensional quality scores evaluate mathematically."""
    ats_score_mock = {
        "scores": {
            "overall_score": 85.0,
            "keyword_match_score": 80.0,
            "semantic_similarity_score": 90.0,
            "skills_alignment_score": 85.0,
            "action_verb_score": 75.0,
            "achievement_score": 80.0,
            "formatting_score": 95.0,
            "section_completeness_score": 90.0
        }
    }
    layout_data = {
        "layout": {
            "whitespace_balance_score": 90.0,
            "density_status": "optimal"
        }
    }
    
    # Pre-hydrated with layout
    sections = dict(MOCK_ORIGINAL_SECTIONS)
    sections["layout"] = layout_data["layout"]
    
    quality_profile = evaluate_resume_quality(
        sections=sections,
        original_sections=MOCK_ORIGINAL_SECTIONS,
        job_description=MOCK_JD_TEXT,
        ats_score_result=ats_score_mock,
        layout_data=layout_data
    )
    
    assert quality_profile["overall_score"] > 0
    assert "warnings" in quality_profile
    assert "recommendations" in quality_profile
    assert quality_profile["formatting_cleanliness"] == 90.0

async def test_document_generation():
    """Verify WeasyPrint PDF and Word document compilers generate bytes successfully."""
    # Ensure layout data is present
    sections = dict(MOCK_ORIGINAL_SECTIONS)
    sections["layout"] = {
        "page_margin_inches": 0.75,
        "font_size_pt": 10.5,
        "line_spacing": 1.2,
        "space_after_section": 8,
        "density_status": "optimal",
        "whitespace_balance_score": 90.0
    }
    
    from unittest.mock import patch
    with patch("app.services.final_resume_quality_gate.validate_final_resume") as mock_gate:
        mock_gate.return_value = {
            "approved": True,
            "diagnostics": {},
            "sections": sections
        }
        
        # Test Word generation
        docx_bytes = await generate_docx(sections, "classic")
        assert isinstance(docx_bytes, bytes)
        assert len(docx_bytes) > 0
        
        # Test PDF generation (ReportLab fallback will run if WeasyPrint is missing)
        pdf_bytes = await generate_pdf(sections, "classic")
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0


def test_metadata_scrubbing():
    """Verify that normalize_skills and final_output_sanitization_pipeline strip metadata leaks."""
    from app.services.validation import normalize_skills, final_output_sanitization_pipeline
    
    # Test normalize_skills with a stringified metadata leak
    leak_skills = [
        "Programming Languages: JavaScript, SQL, {text: Programming Languages: Python",
        "Tools: confidence: 0.9, Data Visualization, Git, GitHub, MATLAB, needs_human_review: True}, source_excerpts: [], {text: Tools: Tableau"
    ]
    
    normalized = normalize_skills(leak_skills)
    
    # Assert that all standard metadata tags are fully removed
    for s in normalized:
        assert "confidence" not in s
        assert "needs_human_review" not in s
        assert "source_excerpts" not in s
        assert "text" not in s
        assert "{" not in s
        assert "}" not in s

    # Ensure actual skills are categorized correctly and deduplicated
    skill_str = "\n".join(normalized)
    assert "Python" in skill_str
    assert "JavaScript" in skill_str
    assert "SQL" in skill_str
    assert "Tableau" in skill_str
    assert "Git" in skill_str
    assert "GitHub" in skill_str
    assert "MATLAB" in skill_str
    assert "Data Visualization" in skill_str

    # Test final_output_sanitization_pipeline on string fields with similar leaks
    leak_sections = {
        "summary": "AI & ML undergraduate with experience, confidence: 0.95, source_excerpts: ['exp1'], {text: and passion for tech}",
        "skills": leak_skills,
        "experience": [
            {
                "role": "Software Engineer",
                "company": "Innovate Corp",
                "dates": "2023 - Present",
                "bullets": [
                    "Developed backend services using Python, needs_human_review: True",
                    "{text: Optimized query latency by 35% on critical Postgres endpoints, confidence: 0.9}"
                ]
            }
        ]
    }
    
    cleaned = final_output_sanitization_pipeline(leak_sections)
    
    # Assert summary is fully scrubbed
    summary = cleaned["summary"]
    assert "confidence" not in summary
    assert "source_excerpts" not in summary
    assert "text" not in summary
    assert "{" not in summary
    
    # Assert experience bullets are fully scrubbed
    bullet_1 = cleaned["experience"][0]["bullets"][0]
    bullet_2 = cleaned["experience"][0]["bullets"][1]
    
    assert "needs_human_review" not in bullet_1
    assert "text" not in bullet_2
    assert "confidence" not in bullet_2
    assert "{" not in bullet_2
    
    print("PASS: test_metadata_scrubbing passed!")


def test_technology_domain_validator():
    """Verify that cross-domain keyword contamination is successfully detected and healed."""
    from app.services.technology_domain_validator import validate_bullet_domain_compatibility, heal_bullet_contamination
    
    # 1. Frontend keyword in backend bullet
    bad_bullet_1 = "Design interactive interfaces using Python and Pandas, applying responsive design principles."
    assert not validate_bullet_domain_compatibility(bad_bullet_1, "backend")
    
    healed_1 = heal_bullet_contamination(bad_bullet_1, "backend")
    assert "responsive design" not in healed_1.lower()
    
    # 2. Incompatible tools check
    bad_bullet_2 = "Developed next.js features and react state management for real-time web services."
    assert not validate_bullet_domain_compatibility(bad_bullet_2, "data_science")
    
    healed_2 = heal_bullet_contamination(bad_bullet_2, "data_science")
    assert "next.js" not in healed_2.lower()
    assert "react" not in healed_2.lower()
    
    print("PASS: test_technology_domain_validator passed!")

def test_bullet_quality_threshold_system():
    """Verify that weak/filler bullets are successfully graded and rejected, and only qualified tech-specific bullets pass."""
    from app.services.bullet_validation_engine import grade_bullet_point, heal_or_replace_bullet
    
    # 1. Weak filler bullet
    weak_bullet = "Perform daily duties as part of the core operational team."
    grade_weak = grade_bullet_point(weak_bullet)
    assert not grade_weak["approved"], "Weak generic bullet should be rejected"
    assert grade_weak["score"] < 55.0, "Weak bullet score should be under 55.0"
    
    # 2. Heal the weak bullet
    healed = heal_or_replace_bullet(weak_bullet, "backend")
    grade_healed = grade_bullet_point(healed)
    assert grade_healed["approved"], "Healed bullet should be approved"
    assert grade_healed["score"] >= 55.0, "Healed bullet score should exceed 55.0"
    
    # 3. Qualified bullet
    good_bullet = "Developed AI-based attendance modules using FastAPI and PostgreSQL for automated IN/OUT logging."
    grade_good = grade_bullet_point(good_bullet)
    assert grade_good["approved"], "Good bullet point should be approved"
    
    print("PASS: test_bullet_quality_threshold_system passed!")


def test_technical_depth_detection():
    """Verify that high-complexity backend/ML concepts score higher than generic scripting, validating proper bullet sorting."""
    from app.services.technical_depth_engine import calculate_technical_depth, rank_experience_bullets
    
    low_depth = "Wrote simple python scripts to clean data from csv files."
    high_depth = "Engineered real-time face detection attendance pipelines integrating OpenCV and ArcFace model embeddings."
    
    score_low = calculate_technical_depth(low_depth)
    score_high = calculate_technical_depth(high_depth)
    
    assert score_high > score_low, f"High complexity ML/CV should score higher than basic scripting ({score_high} vs {score_low})"
    
    # Test sorting
    sorted_bullets = rank_experience_bullets([low_depth, high_depth])
    assert sorted_bullets[0] == high_depth, "High depth bullets should be sorted first"
    
    print("PASS: test_technical_depth_detection passed!")


def test_resume_realism_scoring():
    """Verify that sentence variety and natural prose produce higher realism scores than repetitive, colon-heavy AI wording."""
    from app.services.resume_realism_engine import assess_resume_realism
    
    # 1. Heavy colon and repetitive verbs summary/experience
    summary_repetitive = "specializing in Data Science & ML: Python, Pandas, and NumPy. focused on Backend Development: FastAPI, Flask."
    experience_repetitive = [
        {"bullets": ["Developed backend API using FastAPI.", "Developed frontend using React.", "Developed SQL queries."]}
    ]
    projects_repetitive = []
    
    metrics_bad = assess_resume_realism(summary_repetitive, experience_repetitive, projects_repetitive)
    
    # 2. Natural summary/experience
    summary_natural = "AI & ML undergraduate with hands-on experience building real-time computer vision and backend systems utilizing Python, FastAPI, and OpenCV."
    experience_natural = [
        {"bullets": ["Developed backend API using FastAPI to handle authentication.", "Engineered responsive frontend using React.", "Optimized SQL queries in PostgreSQL."]}
    ]
    
    metrics_good = assess_resume_realism(summary_natural, experience_natural, projects_repetitive)
    
    assert metrics_good["realism_score"] > metrics_bad["realism_score"], f"Natural prose should score higher realism than colon-heavy repetitive prose ({metrics_good['realism_score']} vs {metrics_bad['realism_score']})"
    assert metrics_good["variety_score"] > metrics_bad["variety_score"], "Natural variety of first verbs should score higher variety"
    
    print("PASS: test_resume_realism_scoring passed!")


def test_reality_preservation_grounding():
    """Verify that ungrounded frameworks are stripped from bullets and skills normalizer."""
    from app.services.reality_preservation_engine import cleanse_ungrounded_technologies
    from app.services.validation import normalize_skills

    # Source resume text only has Python, OpenCV, and FastAPI
    src_text = "Experienced with Python, OpenCV, and FastAPI."
    github_techs = ["Docker", "git"]

    # Test bullet cleansing
    raw_bullet = "Developed backend service using FastAPI, React, and Next.js."
    cleansed = cleanse_ungrounded_technologies(raw_bullet, src_text, github_techs)
    # React and Next.js should be stripped as they are not in src_text or github_techs
    assert "React" not in cleansed
    assert "Next.js" not in cleansed
    assert "FastAPI" in cleansed

    # Test skills normalizer cleansing
    skills = [
        "Programming Languages: Python, React, Next.js, Docker"
    ]
    normalized = normalize_skills(skills, raw_text=src_text, github_techs=github_techs)
    normalized_str = "\n".join(normalized)
    assert "Python" in normalized_str
    assert "Docker" in normalized_str
    assert "React" not in normalized_str
    assert "Next.js" not in normalized_str
    print("PASS: test_reality_preservation_grounding passed!")


def test_role_transferability_summary():
    """Verify backend-only candidates seeking frontend JDs get a clean fundamentals/growth-mindset statement."""
    from app.services.reality_preservation_engine import apply_role_transferability_summary

    # Candidate has Python, SQL, and FastAPI in source text
    src_text = "Built backend APIs using Python, SQL, and FastAPI."
    # Target summary contains fabricated React/Next.js
    fabricated_summary = "Frontend Developer skilled in React and Next.js to build user interfaces."
    
    # JD role is frontend, but candidate lacks frontend skills
    pivoted_summary = apply_role_transferability_summary(fabricated_summary, "Frontend Developer", src_text)
    
    # Should pivot to backend APIs and a growth mindset/keen interest in React/Next.js
    assert "backend APIs" in pivoted_summary
    assert "keen interest in expanding technical expertise into modern frontend development" in pivoted_summary
    print("PASS: test_role_transferability_summary passed!")


def test_experience_authenticity():
    """Verify ungrounded senior titles and exaggerated metrics are programmatically gated."""
    from app.services.experience_authenticity_engine import gating_experience_role_authenticity, verify_bullet_authenticity

    # 1. Gating senior title for a student candidate
    senior_role = "Senior Software Engineer"
    gated_role = gating_experience_role_authenticity(senior_role, is_student=True)
    assert gated_role == "Software Engineering Intern"

    # 2. Gating fabricated metrics in experience bullets
    src_text = "Developed database query optimizations."
    fabricated_bullet = "Optimized database query latency by 45% using Postgres endpoints, saving $10,000."
    
    cleansed_bullet = verify_bullet_authenticity(fabricated_bullet, src_text)
    
    # 45% and $10,000 are not in src_text, they must be stripped
    assert "45%" not in cleansed_bullet
    assert "$10,000" not in cleansed_bullet
    assert "Optimized database query latency using Postgres endpoints." in cleansed_bullet
    print("PASS: test_experience_authenticity passed!")


async def test_semantic_technology_grounding():
    """Verify concept-level technology grounding using semantic matching."""
    from app.services.technology_grounding_engine import is_technology_concept_grounded, filter_ungrounded_technologies_from_text
    
    allowed = ["opencv", "fastapi", "python"]
    
    # "face recognition" is semantically related to opencv (computer vision)
    res = await is_technology_concept_grounded("face recognition", allowed)
    assert res is True
    
    # "react" is not grounded
    res_react = await is_technology_concept_grounded("react", allowed)
    assert res_react is False
    
    # Test cleansing
    cleansed = await filter_ungrounded_technologies_from_text("Built UI using React and FastAPI.", allowed)
    assert "React" not in cleansed
    assert "FastAPI" in cleansed
    print("PASS: test_semantic_technology_grounding passed!")


def test_technology_confidence_scoring():
    """Verify technology confidence engine outputs robust weights."""
    from app.services.technology_confidence_engine import calculate_technology_confidence, get_high_confidence_technologies
    
    raw_text = "Highly experienced in Python development. Used Python for multiple API endpoints."
    git_techs = ["Python", "FastAPI"]
    
    score_python = calculate_technology_confidence("Python", raw_text, git_techs)
    # Repeated mentions and primary status should rank high confidence (>0.70)
    assert score_python >= 0.70
    
    high_techs = get_high_confidence_technologies(raw_text, git_techs, min_confidence=0.50)
    assert "Python" in high_techs
    print("PASS: test_technology_confidence_scoring passed!")


async def test_semantic_deduplication():
    """Verify duplicate and near-duplicate bullets are successfully pruned."""
    from app.services.semantic_bullet_deduplicator import deduplicate_section_bullets
    
    bullets = [
        "Developed scalable backend APIs using FastAPI and PostgreSQL.",
        "Engineered scalable backend APIs using FastAPI and PostgreSQL.", # near-duplicate structure/semantics
        "Implemented real-time face detection utilizing OpenCV."
    ]
    
    deduped = await deduplicate_section_bullets(bullets, max_similarity=80.0)
    assert len(deduped) == 2
    assert deduped[0] == "Developed scalable backend APIs using FastAPI and PostgreSQL."
    assert deduped[1] == "Implemented real-time face detection utilizing OpenCV."
    print("PASS: test_semantic_deduplication passed!")


def test_sentence_integrity_validator():
    """Verify dangling prepositions and malformed conjunctions are successfully repaired."""
    from app.services.sentence_integrity_validator import is_sentence_complete, heal_broken_sentence
    
    incomplete = "Optimized database query latency using Python andfor data-driven insights"
    dangling_prep = "Designed a real-time object detection module with."
    
    assert not is_sentence_complete(incomplete)
    assert not is_sentence_complete(dangling_prep)
    
    healed_incomplete = heal_broken_sentence(incomplete)
    assert "andfor" not in healed_incomplete
    assert healed_incomplete.endswith(".")
    
    healed_prep = heal_broken_sentence(dangling_prep)
    assert healed_prep.endswith("module.")
    print("PASS: test_sentence_integrity_validator passed!")


def test_bullet_realism_evaluator():
    """Verify exaggerated enterprise scaling statements are scaled down."""
    from app.services.bullet_realism_engine import evaluate_bullet_realism, heal_exaggerated_bullet
    
    exaggerated = "Architected multi-region AWS cloud deployments supporting 10M+ active users."
    realism = evaluate_bullet_realism(exaggerated)
    assert not realism["approved"]
    
    healed = heal_exaggerated_bullet(exaggerated)
    assert "10M+" not in healed
    assert "multi-region AWS" not in healed
    print("PASS: test_bullet_realism_evaluator passed!")


def test_recruiter_simulation_engine():
    """Verify 6-second scan and readability metrics compute correctly."""
    from app.services.recruiter_review_engine import simulate_recruiter_scan
    
    mock_sections = {
        "summary": "AI undergraduate with experience in Python and FastAPI.",
        "skills": ["Programming Languages: Python, SQL", "Tools: Git"],
        "experience": [
            {
                "role": "Intern",
                "bullets": ["Bullet 1", "Bullet 2"]
            }
        ]
    }
    
    review = simulate_recruiter_scan(mock_sections)
    assert review["recruiter_readability_score"] >= 80.0
    assert review["shortlist_likelihood"] in ["High", "Medium"]
    print("PASS: test_recruiter_simulation_engine passed!")


async def test_final_quality_gate():
    """Verify the quality gate coordinates validations and handles auto-healing."""
    from app.services.final_resume_quality_gate import validate_final_resume
    
    mock_original = {
        "education": [{"degree": "Bachelor of Science in CS"}]
    }
    
    mock_tailored = {
        "job_title": "Software Engineering Intern",
        "summary": "Software Engineer with experience, frameworks like.",
        "experience": [
            {
                "role": "VP of Engineering", # should gate down
                "bullets": [
                    "Developed backend service using React and FastAPI.", # React should be stripped as it is not allowed
                    "Developed backend service using React and FastAPI."  # Duplicate bullet, should be stripped
                ]
            }
        ]
    }
    
    # Raw text only has FastAPI and Python
    raw_text = "FastAPI, Python, SQL"
    
    result = await validate_final_resume(mock_tailored, raw_text, mock_original, strict_mode=False)
    assert result["approved"] is False
    assert len(result["diagnostics"]["failures"]) > 0
    
    sections = result["sections"]
    assert "VP of Engineering" not in sections["experience"][0]["role"]
    assert "Software Engineering Intern" in sections["experience"][0]["role"]
    
    bullets = sections["experience"][0]["bullets"]
    assert len(bullets) == 1
    assert "React" not in bullets[0]
    assert "FastAPI" in bullets[0]
    print("PASS: test_final_quality_gate passed!")


if __name__ == "__main__":
    import sys
    
    async def run_all_tests():
        print("1. Running test_loud_schema_failures...")
        await test_loud_schema_failures()
        print("PASS: test_loud_schema_failures passed!")
        
        print("\n2. Running test_content_density_manager...")
        test_content_density_manager()
        print("PASS: test_content_density_manager passed!")
        
        print("\n3. Running test_role_classification_and_reordering...")
        await test_role_classification_and_reordering()
        print("PASS: test_role_classification_and_reordering passed!")
        
        print("\n4. Running test_resume_quality_evaluation...")
        test_resume_quality_evaluation()
        print("PASS: test_resume_quality_evaluation passed!")
        
        print("\n5. Running test_document_generation...")
        await test_document_generation()
        print("PASS: test_document_generation passed!")
        
        print("\n6. Running test_metadata_scrubbing...")
        test_metadata_scrubbing()
        print("PASS: test_metadata_scrubbing passed!")
        
        print("\n7. Running test_technology_domain_validator...")
        test_technology_domain_validator()
        print("PASS: test_technology_domain_validator passed!")
        
        print("\n8. Running test_bullet_quality_threshold_system...")
        test_bullet_quality_threshold_system()
        
        print("\n9. Running test_technical_depth_detection...")
        test_technical_depth_detection()
        
        print("\n10. Running test_resume_realism_scoring...")
        test_resume_realism_scoring()

        print("\n11. Running test_reality_preservation_grounding...")
        test_reality_preservation_grounding()

        print("\n12. Running test_role_transferability_summary...")
        test_role_transferability_summary()

        print("\n13. Running test_experience_authenticity...")
        test_experience_authenticity()

        print("\n14. Running test_semantic_technology_grounding...")
        await test_semantic_technology_grounding()

        print("\n15. Running test_technology_confidence_scoring...")
        test_technology_confidence_scoring()

        print("\n16. Running test_semantic_deduplication...")
        await test_semantic_deduplication()

        print("\n17. Running test_sentence_integrity_validator...")
        test_sentence_integrity_validator()

        print("\n18. Running test_bullet_realism_evaluator...")
        test_bullet_realism_evaluator()

        print("\n19. Running test_recruiter_simulation_engine...")
        test_recruiter_simulation_engine()

        print("\n20. Running test_final_quality_gate...")
        await test_final_quality_gate()
        
        print("\nSUCCESS: ALL V2 deterministic resume engine recruiter-grade tests passed successfully!")

    try:
        asyncio.run(run_all_tests())
    except Exception as exc:
        print(f"FAIL: Test suite failed with exception: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
