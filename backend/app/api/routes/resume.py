"""
Resume upload and management API routes.
"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import get_settings
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeListResponse, ResumeListItem, ResumeResponse
# Import heavy parsing function lazily inside the endpoint to avoid
# requiring python-docx / pdfplumber at import time during startup.

router = APIRouter(prefix="/resumes", tags=["resumes"])
settings = get_settings()

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a resume (PDF or DOCX)",
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX, max 10 MB)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeResponse:
    """Upload a resume file, extract text, and parse sections.

    Args:
        file: The uploaded resume file.
        db: Async database session.
        current_user: The authenticated user.

    Returns:
        The created Resume with parsed sections.

    Raises:
        HTTPException 400: If the file type is unsupported or too large.
        HTTPException 500: If text extraction / parsing fails.
    """
    # ── Validate file type ───────────────────────────────────────
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type. Allowed: PDF, DOCX. Got: {file.content_type}",
            )

    # ── Validate file size ───────────────────────────────────────
    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB} MB",
        )

    # ── Save file to disk ────────────────────────────────────────
    file_ext = Path(file.filename or "resume.pdf").suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_name

    with open(file_path, "wb") as f:
        f.write(contents)

    # ── Parse the document ───────────────────────────────────────
    try:
        # Lazy import to avoid import-time failures when optional native
        # dependencies are not installed in developer environments.
        from app.services.resume_parser import parse_document

        raw_text, parsed_sections = await parse_document(
            file_path=str(file_path),
            content_type=file.content_type or f"application/{file_ext.lstrip('.')}",
        )
    except Exception as exc:
        # Clean up the saved file on parse failure
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume: {str(exc)}",
        )

    # ── Persist to database ──────────────────────────────────────
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename or unique_name,
        file_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        raw_text=raw_text,
        parsed_sections=parsed_sections,
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeResponse.model_validate(resume)


@router.get(
    "/",
    response_model=ResumeListResponse,
    summary="List all uploaded resumes",
)
async def list_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeListResponse:
    """Return all resumes uploaded by the current user.

    Args:
        db: Async database session.
        current_user: The authenticated user.

    Returns:
        A list of resume summaries with total count.
    """
    count_result = await db.execute(
        select(func.count()).select_from(Resume).where(Resume.user_id == current_user.id)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )
    resumes = result.scalars().all()

    return ResumeListResponse(
        total=total,
        resumes=[ResumeListItem.model_validate(r) for r in resumes],
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
    summary="Get a resume by ID",
)
async def get_resume(
    resume_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeResponse:
    """Return the full details of a specific resume.

    Args:
        resume_id: The UUID of the resume to retrieve.
        db: Async database session.
        current_user: The authenticated user.

    Returns:
        The full Resume detail.

    Raises:
        HTTPException 404: If the resume is not found or doesn't belong to the user.
    """
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
    )
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return ResumeResponse.model_validate(resume)


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a resume",
)
async def delete_resume(
    resume_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a resume and its associated file.

    Args:
        resume_id: The UUID of the resume to delete.
        db: Async database session.
        current_user: The authenticated user.

    Raises:
        HTTPException 404: If the resume is not found or doesn't belong to the user.
    """
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
    )
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    # Remove file from disk
    file_path = Path(resume.file_path)
    if file_path.exists():
        os.remove(file_path)

    await db.delete(resume)
    await db.commit()
