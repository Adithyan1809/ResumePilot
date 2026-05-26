import logging

logger = logging.getLogger(__name__)

def optimize_story_flow(resume_sections: dict, identity: str) -> dict:
    """
    Story Flow Engine: Optimizes how a recruiter reads the resume.
    Ensures the sequence logically answers Who, What, How, and Why.
    (Summary -> Core Skills -> Experience -> Projects -> Education)
    """
    logger.info("Running Story Flow Engine")
    
    # Normally we might rearrange keys or inject transition phrases in the summary.
    # For now, we will just ensure the 'summary' acts as the strong "Who" statement,
    # and the sections are ordered correctly.
    
    flow_ordered = {}
    
    # 1. Who (Summary)
    if "summary" in resume_sections:
        flow_ordered["summary"] = resume_sections["summary"]
        
    # 2. What/How (Skills)
    if "skills" in resume_sections:
        flow_ordered["skills"] = resume_sections["skills"]
        
    # 3. Where/When (Experience)
    if "experience" in resume_sections:
        flow_ordered["experience"] = resume_sections["experience"]
        
    # 4. Proof (Projects)
    if "projects" in resume_sections:
        flow_ordered["projects"] = resume_sections["projects"]
        
    # 5. Foundation (Education)
    if "education" in resume_sections:
        flow_ordered["education"] = resume_sections["education"]
        
    # Catch any remaining sections
    for key, val in resume_sections.items():
        if key not in flow_ordered:
            flow_ordered[key] = val
            
    return flow_ordered
