"""
Tailor / ATS scoring request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Requests ─────────────────────────────────────────────────────

class TailorRequest(BaseModel):
    """Request to tailor a resume for a specific job."""

    resume_id: uuid.UUID = Field(..., description="ID of the uploaded resume to tailor")
    job_description: str = Field(
        ...,
        min_length=50,
        description="Full job description text (min 50 chars)",
    )
    job_title: str = Field(default="", description="Target job title")
    company: str = Field(default="", description="Target company name")
    template: str = Field(
        default="classic",
        description="Resume template: classic, modern, executive",
    )


class CoverLetterRequest(BaseModel):
    """Request to generate a cover letter."""

    tailored_resume_id: uuid.UUID = Field(
        ..., description="ID of the tailored resume to base the cover letter on"
    )
    tone: str = Field(
        default="professional",
        description="Tone: professional, enthusiastic, conversational",
    )
    additional_notes: str = Field(
        default="",
        description="Any extra context for the cover letter",
    )


class DownloadRequest(BaseModel):
    """Request to download a tailored resume."""

    tailored_resume_id: uuid.UUID = Field(
        ..., description="ID of the tailored resume"
    )
    format: str = Field(
        default="pdf",
        description="Output format: pdf or docx",
    )
    template: str = Field(
        default="classic",
        description="Resume template: classic, modern, executive",
    )


# ── Response Sub-models ─────────────────────────────────────────

class ATSScoreBreakdown(BaseModel):
    """Detailed ATS score breakdown by dimension."""

    overall_score: float = Field(..., description="Composite ATS score 0-100")
    keyword_match_score: float = Field(
        ..., description="Hard/soft keyword match score 0-100"
    )
    semantic_similarity_score: float = Field(
        ..., description="Semantic cosine similarity score 0-100"
    )
    skills_alignment_score: float = Field(
        ..., description="Skills coverage score 0-100"
    )
    action_verb_score: float = Field(
        ..., description="Strong action verbs usage score 0-100"
    )
    achievement_score: float = Field(
        ..., description="Quantified achievements score 0-100"
    )
    formatting_score: float = Field(
        ..., description="Resume formatting quality score 0-100"
    )
    section_completeness_score: float = Field(
        ..., description="Section completeness score 0-100"
    )


class MissingKeyword(BaseModel):
    """A keyword found in the JD but missing from the resume."""

    keyword: str
    importance: str = Field(description="high, medium, or low")
    category: str = Field(description="hard_skill, soft_skill, tool, certification, etc.")


class Suggestion(BaseModel):
    """An actionable suggestion to improve the resume."""

    category: str = Field(description="Category: keywords, experience, skills, format, etc.")
    priority: str = Field(description="high, medium, or low")
    suggestion: str = Field(description="Human-readable suggestion text")


# ── Responses ────────────────────────────────────────────────────

class TailorResponse(BaseModel):
    """Full response after tailoring a resume."""

    id: uuid.UUID
    resume_id: uuid.UUID
    job_title: str
    company: str
    tailored_sections: Dict[str, Any]
    validation_issues: Optional[List[str]] = Field(
        default=None,
        description="List of validation / hallucination warnings detected for the generated sections",
    )
    ats_score: ATSScoreBreakdown
    missing_keywords: List[MissingKeyword]
    suggestions: List[Suggestion]
    cover_letter: Optional[str] = None
    template: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TailorListItem(BaseModel):
    """Minimal tailored resume info for list endpoints."""

    id: uuid.UUID
    resume_id: uuid.UUID
    job_title: str
    company: str
    overall_score: float
    template: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TailorListResponse(BaseModel):
    """List of tailored resumes."""

    total: int
    items: List[TailorListItem]


class CoverLetterResponse(BaseModel):
    """Generated cover letter response."""

    tailored_resume_id: uuid.UUID
    cover_letter: str
