"""
Final Resume Quality Gate.

Acts as the absolute final approval layer before PDF/DOCX rendering, validating and
auto-healing realism, grounding, bullet uniqueness, sentence integrity, and layout consistency.
"""

import logging
from typing import Dict, Any, List

from app.services.technology_grounding_engine import extract_allowed_technologies, filter_ungrounded_technologies_from_text
from app.services.semantic_bullet_deduplicator import deduplicate_resume
from app.services.sentence_integrity_validator import is_sentence_complete, heal_broken_sentence
from app.services.bullet_realism_engine import evaluate_bullet_realism, heal_exaggerated_bullet
from app.services.recruiter_review_engine import simulate_recruiter_scan
from app.services.role_transferability_engine import convert_summary_for_transferability, convert_bullet_for_transferability
from app.services.experience_authenticity_engine import gating_experience_role_authenticity, verify_bullet_authenticity

logger = logging.getLogger(__name__)

async def validate_final_resume(
    sections: Dict[str, Any],
    raw_text: str,
    original_sections: Dict[str, Any],
    job_description: str = ""
) -> Dict[str, Any]:
    """Runs a multi-layer validation audit on tailored resume sections, auto-healing any defects on the fly."""
    if not sections or not isinstance(sections, dict):
        return {"approved": False, "diagnostics": {"error": "Invalid resume sections input"}, "sections": {}}
        
    import copy
    healed = copy.deepcopy(sections)
    
    # ── 1. Technology Grounding Pass ──
    allowed_techs = extract_allowed_technologies(raw_text, github_techs=[])
    
    # Cleanse summary ungrounded tech
    summary_text = str(healed.get("summary", ""))
    summary_text = await filter_ungrounded_technologies_from_text(summary_text, allowed_techs)
    
    # Apply Role Transferability Summary pivoting
    job_title = sections.get("job_title", "")
    summary_text = convert_summary_for_transferability(summary_text, job_title, allowed_techs)
    healed["summary"] = summary_text
    
    # ── 2. Experience & Bullets Factuality Pass ──
    is_student = True
    for edu in original_sections.get("education", []) or []:
        deg = edu.get("degree", "").lower()
        if any(w in deg for w in ["bachelor", "undergraduate", "b.e", "b.tech", "student"]):
            is_student = True
            break
            
    if "experience" in healed and isinstance(healed["experience"], list):
        for entry in healed["experience"]:
            if isinstance(entry, dict):
                # Gate Title Seniority
                entry["role"] = gating_experience_role_authenticity(entry.get("role", ""), is_student=is_student)
                
                bullets = entry.get("bullets", []) or []
                healed_bullets = []
                for b in bullets:
                    b_str = b.get("text", "") if isinstance(b, dict) else str(b)
                    
                    # Verify numeric metrics and strip hallucinations
                    b_str = verify_bullet_authenticity(b_str, raw_text)
                    
                    # Convert ungrounded concepts in bullets (transferability)
                    b_str = convert_bullet_for_transferability(b_str, job_title, allowed_techs)
                    
                    # Filter ungrounded tech in bullets
                    b_str = await filter_ungrounded_technologies_from_text(b_str, allowed_techs)
                    
                    # Evaluate Realism and heal exaggeration
                    b_str = heal_exaggerated_bullet(b_str)
                    
                    # Sentence Integrity Check & Healing
                    b_str = heal_broken_sentence(b_str)
                    
                    if b_str:
                        if isinstance(b, dict):
                            b_copy = copy.deepcopy(b)
                            b_copy["text"] = b_str
                            healed_bullets.append(b_copy)
                        else:
                            healed_bullets.append(b_str)
                entry["bullets"] = healed_bullets
                
    # ── 3. Semantic Deduplication Pass ──
    healed = await deduplicate_resume(healed)
    
    # ── 4. Recruiter Simulation Audit ──
    sim_results = simulate_recruiter_scan(healed, job_description)
    
    # Embed recruiter metrics inside the layout payload
    if "layout" not in healed or not isinstance(healed["layout"], dict):
        healed["layout"] = {}
        
    healed["layout"]["recruiter_readability_score"] = sim_results.get("recruiter_readability_score", 100.0)
    healed["layout"]["shortlist_likelihood"] = sim_results.get("shortlist_likelihood", "High")
    healed["layout"]["recruiter_suggestions"] = sim_results.get("warnings", [])
    
    approved = sim_results.get("recruiter_readability_score", 100.0) >= 60.0
    
    return {
        "approved": approved,
        "diagnostics": {
            "recruiter_readability_score": sim_results.get("recruiter_readability_score", 100.0),
            "shortlist_likelihood": sim_results.get("shortlist_likelihood", "High"),
            "warnings": sim_results.get("warnings", [])
        },
        "sections": healed
    }
