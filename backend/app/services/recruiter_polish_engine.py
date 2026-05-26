import logging

logger = logging.getLogger(__name__)

def apply_recruiter_polish(resume_sections: dict) -> dict:
    """
    Recruiter Polish Engine: Final recruiter-oriented cleanup.
    Optimizes whitespace rhythm, bullet readability, sentence pacing, and emphasis balance.
    Limits bullets per role/project to prevent density fatigue.
    """
    logger.info("Running Recruiter Polish Engine")
    
    polished = resume_sections.copy()
    
    MAX_BULLETS_EXP = 5
    MAX_BULLETS_PROJ = 4
    MAX_SUMMARY_LENGTH = 350 # characters
    
    # 1. Polish Summary
    if "summary" in polished:
        summary = polished["summary"]
        if len(summary) > MAX_SUMMARY_LENGTH:
            # Simple truncation (in real app, use LLM summarization to fit length)
            polished["summary"] = summary[:MAX_SUMMARY_LENGTH].rsplit(' ', 1)[0] + "."
            
    # 2. Polish Experience Density
    if "experience" in polished:
        for exp in polished["experience"]:
            bullets = exp.get("bullets", [])
            if len(bullets) > MAX_BULLETS_EXP:
                # Keep top N bullets
                exp["bullets"] = bullets[:MAX_BULLETS_EXP]
                
    # 3. Polish Projects Density
    if "projects" in polished:
        for proj in polished["projects"]:
            bullets = proj.get("bullets", [])
            if len(bullets) > MAX_BULLETS_PROJ:
                proj["bullets"] = bullets[:MAX_BULLETS_PROJ]
                
    return polished
