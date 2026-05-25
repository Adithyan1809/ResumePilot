"""
Resume request/response schemas.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ParsedSections(BaseModel):
    """Structured representation of parsed resume sections."""

    contact_info: Dict[str, Any] = Field(
        default_factory=dict,
        description="Name, email, phone, LinkedIn, location",
    )
    summary: str = Field(default="", description="Professional summary / objective")
    experience: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Work experience entries",
    )
    education: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Education entries",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="List of skills",
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="Certifications and licenses",
    )
    projects: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Project entries",
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Spoken / written languages",
    )
    awards: List[str] = Field(
        default_factory=list,
        description="Awards and honours",
    )
    publications: List[str] = Field(
        default_factory=list,
        description="Publications",
    )
    volunteer: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Volunteer experience",
    )
    additional: str = Field(
        default="",
        description="Any additional / uncategorized content",
    )


class ResumeResponse(BaseModel):
    """Full resume detail response."""

    id: uuid.UUID
    user_id: uuid.UUID
    filename: str
    content_type: str
    raw_text: str
    parsed_sections: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeListItem(BaseModel):
    """Minimal resume info for list endpoints."""

    id: uuid.UUID
    filename: str
    content_type: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    """Paginated list of resumes."""

    total: int = Field(..., description="Total number of resumes")
    resumes: List[ResumeListItem]
