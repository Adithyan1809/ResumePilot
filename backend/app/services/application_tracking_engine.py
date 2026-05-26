"""
Application Tracking Engine.
Manages candidate job applications history logs (invitations, rejections, callbacks),
and dynamically calibrates portfolio matching parameters based on real-world outcomes.
"""

import uuid
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_resume_profile_engine import get_master_profile


async def log_job_application(
    db: AsyncSession,
    user_id: uuid.UUID,
    company: str,
    job_title: str,
    status: str = "applied"
) -> Dict[str, Any]:
    """Records a new job application log in the user's persistent profile database."""
    profile = await get_master_profile(db, user_id)
    if profile is None:
        return {"success": False, "message": "Master profile not found"}
        
    apps = dict(profile.applications_log) if profile.applications_log else {}
    app_list = list(apps.get("applications", []))
    
    app_id = str(uuid.uuid4())
    app_list.append({
        "id": app_id,
        "company": company,
        "job_title": job_title,
        "status": status,  # applied, callback, oa, interview, offer, rejected
        "timestamp": uuid.uuid4().hex[:8]  # mock timestamp representation
    })
    
    apps["applications"] = app_list
    profile.applications_log = apps
    
    await db.commit()
    return {"success": True, "application_id": app_id}


async def update_application_status(
    db: AsyncSession,
    user_id: uuid.UUID,
    application_id: str,
    new_status: str
) -> Dict[str, Any]:
    """Updates status for a specific application log, triggering calibration updates."""
    profile = await get_master_profile(db, user_id)
    if profile is None:
        return {"success": False}
        
    apps = dict(profile.applications_log) if profile.applications_log else {}
    app_list = list(apps.get("applications", []))
    
    found = False
    for app in app_list:
        if app["id"] == application_id:
            app["status"] = new_status
            found = True
            break
            
    if not found:
        return {"success": False, "message": "Application ID not found"}
        
    apps["applications"] = app_list
    profile.applications_log = apps
    
    # Calibrate Recruiter Heuristics based on outcomes
    memory = dict(profile.profile_memory) if profile.profile_memory else {}
    if new_status == "rejected":
        # Increment rejection weight to make strict validation gates slightly more critical
        memory["calibrated_rejection_weight"] = memory.get("calibrated_rejection_weight", 0.0) + 1.5
    elif new_status in ["callback", "offer"]:
        memory["calibrated_callback_weight"] = memory.get("calibrated_callback_weight", 0.0) + 2.0
        
    profile.profile_memory = memory
    await db.commit()
    return {"success": True}


def get_applications_analytics(applications_log: Dict[str, Any]) -> Dict[str, Any]:
    """Compiles statistics and conversion rates from application history."""
    if not applications_log or "applications" not in applications_log:
        return {"total_applied": 0, "callbacks": 0, "success_rate": 0.0}
        
    apps = applications_log.get("applications", [])
    total = len(apps)
    if total == 0:
        return {"total_applied": 0, "callbacks": 0, "success_rate": 0.0}
        
    callbacks = sum(1 for a in apps if a["status"] in ["callback", "interview", "offer"])
    rejections = sum(1 for a in apps if a["status"] == "rejected")
    
    success_rate = (callbacks / total) * 100.0
    
    return {
        "total_applied": total,
        "callbacks": callbacks,
        "rejections": rejections,
        "success_rate": round(success_rate, 2)
    }
