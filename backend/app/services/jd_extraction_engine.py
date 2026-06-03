"""
JD Extraction Engine.
Extracts required technical skills, seniority level, core responsibilities, and recruiter expectations
from raw scraped job descriptions.
"""

import re
import json
from typing import Dict, Any, List
from app.services.evidence_storage_engine import extract_technologies_from_text
from app.services.model_router_engine import route_and_call_llm
from app.prompts.analysis import JD_ANALYSIS_PROMPT
import logging

logger = logging.getLogger(__name__)

async def extract_job_details(jd_text: str) -> Dict[str, Any]:
    """Analyzes raw JD text using the LLM to extract keywords, seniority, focus domains, and recruiter expectations."""
    default_response = {
        "required_techs": [],
        "seniority": "Mid",
        "focus_domain": "backend",
        "recruiter_expectations": "Looking for a collaborative generalist with strong coding skills.",
        "must_have_skills": [],
        "nice_to_have_skills": [],
        "domain_keywords": []
    }
    
    if not jd_text:
        return default_response

    try:
        # Call LLM to parse JD
        prompt = JD_ANALYSIS_PROMPT.format(job_description=jd_text)
        response_text = await route_and_call_llm(prompt=prompt, task_type="json_parsing")
        
        # Clean JSON and parse
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(response_text)
        
        must_have = parsed.get("must_have_skills", [])
        nice_to_have = parsed.get("nice_to_have_skills", [])
        
        # Combine into required_techs for backward compatibility with orchestrator
        all_techs = must_have + nice_to_have
        
        seniority = parsed.get("seniority_level", "Mid")
        focus_domain = parsed.get("core_role_type", "backend")
        
        expectations = "Key Responsibilities: " + ", ".join(parsed.get("key_responsibilities", []))

        return {
            "required_techs": all_techs,
            "must_have_skills": must_have,
            "nice_to_have_skills": nice_to_have,
            "domain_keywords": parsed.get("domain_keywords", []),
            "seniority": seniority,
            "focus_domain": focus_domain,
            "recruiter_expectations": expectations,
            "raw_jd_analysis": parsed
        }
        
    except Exception as e:
        logger.error(f"Failed to parse JD with LLM: {str(e)}. Falling back to heuristics.")
        
        # Fallback to original heuristics
        jd_lower = jd_text.lower()
        required_techs = extract_technologies_from_text(jd_text)
        
        seniority = "Mid"
        if any(w in jd_lower for w in ["lead", "principal", "staff", "architect", "director", "manager"]):
            seniority = "Lead"
        elif "senior" in jd_lower or "sr" in jd_lower or "5+" in jd_lower or "8+" in jd_lower:
            seniority = "Senior"
        elif "junior" in jd_lower or "jr" in jd_lower or "entry" in jd_lower or "1+" in jd_lower:
            seniority = "Junior"
        elif "intern" in jd_lower or "undergraduate" in jd_lower or "co-op" in jd_lower:
            seniority = "Intern"

        focus_domain = "backend"
        if any(w in jd_lower for w in ["front", "ui", "ux", "react", "next.js", "nextjs", "javascript", "typescript", "css"]):
            focus_domain = "frontend"
        elif any(w in jd_lower for w in ["devops", "cloud", "infra", "sre", "kubernetes", "docker", "ci/cd", "deployment"]):
            focus_domain = "devops"
        elif any(w in jd_lower for w in ["data science", "ml", "ai", "machine learning", "tensorflow", "pytorch", "deep learning", "cv"]):
            focus_domain = "data_science"
        elif "fullstack" in jd_lower or "full stack" in jd_lower:
            focus_domain = "fullstack"

        expectations = (
            f"Looking for a {seniority}-level engineer specializing in {focus_domain} architectures. "
            f"Key priorities: scaling software using {', '.join(required_techs[:4]) if required_techs else 'Python and Docker'}."
        )

        return {
            "required_techs": required_techs,
            "must_have_skills": required_techs,
            "nice_to_have_skills": [],
            "domain_keywords": [],
            "seniority": seniority.title(),
            "focus_domain": focus_domain,
            "recruiter_expectations": expectations
        }
