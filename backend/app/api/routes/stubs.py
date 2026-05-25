from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import datetime
import uuid

try:
    from typing import TypedDict
except Exception:
    TypedDict = dict

router = APIRouter()


@router.post("/tailor/download")
async def download_stub(body: dict):
    """Return a small, valid PDF generated with ReportLab when available.

    This produces a real, openable PDF for Windows users without requiring
    system-level PDF toolchains. If ReportLab is not installed, falls back
    to a minimal simulated stream.
    """
    # Try to generate a proper PDF with ReportLab (pure Python)
    try:
        from reportlab.pdfgen import canvas
        buf = BytesIO()
        c = canvas.Canvas(buf)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 750, "Tailored Resume")
        c.setFont("Helvetica", 11)
        c.drawString(72, 730, "This is a locally-generated sample PDF. Replace with real export in production.")
        c.showPage()
        c.save()
        buf.seek(0)
        headers = {"Content-Disposition": "attachment; filename=TailoredResume_sample.pdf"}
        return StreamingResponse(buf, media_type="application/pdf", headers=headers)
    except Exception:
        # Fallback: return the old simulated PDF-like byte stream
        content = (
            "%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            "2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n"
            "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R >>\nendobj\n"
            "4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 20 100 Td (Simulated PDF) Tj ET\nendstream\nendobj\n%%EOF"
        ).encode("utf-8")
        return StreamingResponse(BytesIO(content), media_type="application/pdf")


# -----------------------------
# Mock tailoring endpoints
# -----------------------------


@router.post("/tailor/analyze")
async def analyze_stub(body: dict):
    """Return a realistic mock tailored response for frontend dev when
    the real AI pipeline is unavailable.
    """
    tailored_id = str(uuid.uuid4())
    resume_id = body.get("resume_id") or str(uuid.uuid4())
    job_title = body.get("job_title") or "Senior Software Engineer"
    company = body.get("company") or "Acme Corp"

    now = datetime.utcnow().isoformat()

    resp = {
        "id": tailored_id,
        "resume_id": resume_id,
        "job_title": job_title,
        "company": company,
        "template": body.get("template", "classic"),
        "ats_score": {
            "overall_score": 86.0,
            "keyword_match_score": 88.0,
            "semantic_similarity_score": 82.0,
            "skills_alignment_score": 85.0,
            "action_verb_score": 90.0,
            "achievement_score": 78.0,
            "formatting_score": 94.0,
            "section_completeness_score": 100.0,
        },
        "missing_keywords": [
            {"keyword": "FastAPI", "importance": "high", "category": "hard_skill"},
            {"keyword": "Kubernetes", "importance": "high", "category": "tool"},
        ],
        "suggestions": [
            {"category": "keywords", "priority": "high", "suggestion": "Add 'FastAPI' to your skills section."},
        ],
        "tailored_sections": {
            "contact_info": {"name": "Jane Doe", "email": "jane@example.com"},
            "summary": "Senior Software Engineer with 6+ years building scalable APIs.",
            "experience": [
                {"company": "InnoTech", "role": "Senior Developer", "dates": "2022 - Present", "bullets": ["Built FastAPI services."]}
            ],
            "skills": ["Python", "FastAPI", "Docker", "Kubernetes"],
        },
        "validation_issues": None,
        "cover_letter": "",
        "created_at": now,
    }

    return resp


@router.get("/tailor/history")
async def history_stub():
    now = datetime.utcnow().isoformat()
    items = [
        {
            "id": str(uuid.uuid4()),
            "resume_id": str(uuid.uuid4()),
            "job_title": "Senior Full Stack Engineer",
            "company": "Innovate Inc",
            "overall_score": 87,
            "template": "classic",
            "created_at": now,
        }
        for _ in range(3)
    ]
    return {"total": len(items), "items": items}


@router.get("/tailor/{tailored_id}")
async def get_tailored_stub(tailored_id: str):
    now = datetime.utcnow().isoformat()
    return {
        "id": tailored_id,
        "resume_id": str(uuid.uuid4()),
        "job_title": "Senior Software Engineer",
        "company": "Acme Corp",
        "template": "classic",
        "ats_score": {
            "overall_score": 86.0,
            "keyword_match_score": 88.0,
            "semantic_similarity_score": 82.0,
            "skills_alignment_score": 85.0,
            "action_verb_score": 90.0,
            "achievement_score": 78.0,
            "formatting_score": 94.0,
            "section_completeness_score": 100.0,
        },
        "missing_keywords": [],
        "suggestions": [],
        "tailored_sections": {},
        "validation_issues": None,
        "cover_letter": "",
        "created_at": now,
    }


@router.post("/tailor/cover-letter")
async def cover_letter_stub(body: dict):
    return {"tailored_resume_id": body.get("tailored_resume_id"), "cover_letter": "Dear Hiring Team,\n\nThis is a generated cover letter (mock).\n"}
