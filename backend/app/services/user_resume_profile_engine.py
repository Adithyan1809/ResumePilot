"""
User Resume Profile Engine.
Manages persistent database operations for UserResumeProfiles, facilitating single-upload resume storage
and candidate profile memory capabilities.
"""

import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import UserResumeProfile
from app.services.evidence_storage_engine import extract_evidence_from_parsed_sections


async def get_master_profile(db: AsyncSession, user_id: uuid.UUID) -> Optional[UserResumeProfile]:
    """Retrieve the master resume profile for a specific user from the database."""
    stmt = select(UserResumeProfile).where(UserResumeProfile.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def save_master_profile(
    db: AsyncSession,
    user_id: uuid.UUID,
    resume_id: uuid.UUID,
    parsed_sections: dict,
    raw_text: str
) -> UserResumeProfile:
    """Extracts whitelisted evidence from parsed sections, and saves or updates the user's master profile."""
    # Extract structured evidence
    evidence = extract_evidence_from_parsed_sections(parsed_sections)
    
    # Check if profile already exists
    profile = await get_master_profile(db, user_id)
    
    if profile is None:
        # Create a new profile
        profile = UserResumeProfile(
            user_id=user_id,
            master_resume_id=resume_id,
            structured_evidence=evidence,
            profile_memory={
                "target_roles_history": [],
                "tailored_counts": 0,
                "average_ats_score": 0.0,
                "recruiter_feedback_log": []
            }
        )
        db.add(profile)
    else:
        # Update existing profile
        profile.master_resume_id = resume_id
        profile.structured_evidence = evidence
        
    await db.commit()
    await db.refresh(profile)
    return profile


async def update_profile_memory(
    db: AsyncSession,
    user_id: uuid.UUID,
    target_role: str,
    ats_score: float,
    company: str
) -> Optional[UserResumeProfile]:
    """Appends tailored metrics to the profile memory to enhance future evidence matching weights."""
    profile = await get_master_profile(db, user_id)
    if profile is None:
        return None
        
    memory = dict(profile.profile_memory)
    
    # 1. Update tailoring counts
    tailored_counts = memory.get("tailored_counts", 0) + 1
    memory["tailored_counts"] = tailored_counts
    
    # 2. Update average score
    avg_score = memory.get("average_ats_score", 0.0)
    new_avg = round(((avg_score * (tailored_counts - 1)) + ats_score) / tailored_counts, 2)
    memory["average_ats_score"] = new_avg
    
    # 3. Add to targeted roles history
    roles_history = list(memory.get("target_roles_history", []))
    roles_history.append({
        "role": target_role,
        "company": company,
        "score": ats_score,
        "timestamp": uuid.uuid4().hex  # simple unique identifier/timestamp simulation
    })
    memory["target_roles_history"] = roles_history[-10:]  # keep last 10 roles
    
    profile.profile_memory = memory
    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_master_profile(db: AsyncSession, user_id: uuid.UUID) -> bool:
    """Deletes a user's persistent master profile (GDPR-style deletion)."""
    profile = await get_master_profile(db, user_id)
    if profile is None:
        return False
        
    await db.delete(profile)
    await db.commit()
    return True
