"""
ATS Simulation Engine.
Simulates standard parser behaviors to inspect layout styles, parsing blockages,
text density, and section header compliance, calculating an overall ATS compatibility score.
"""

from typing import Dict, Any, List


def simulate_ats_parsing(sections: Dict[str, Any], template: str) -> Dict[str, Any]:
    """Audits the resume structure against standard ATS parsing constraints."""
    if not sections:
        return {"ats_compatibility_score": 0.0, "parsing_warnings": []}

    warnings = []
    base_compatibility = 95.0

    # 1. Inspect Template layout risks
    if template == "executive":
        # Executive templates might use heavy header styling or lines that block some parsers
        warnings.append("Executive template uses horizontal accent borders which some legacy ATS parsers classify as section dividers.")
        base_compatibility -= 5.0
    elif template == "creative":
        warnings.append("Multi-column and sidebar templates reduce standard linear parsing correctness in older ATS engines.")
        base_compatibility -= 15.0

    # 2. Inspect Section Title Standards
    standard_keys = {"summary", "experience", "skills", "education", "contact_info"}
    missing_standards = []
    for key in standard_keys:
        if key not in sections or not sections[key]:
            missing_standards.append(key)
            
    if missing_standards:
        warnings.append(f"Missing standard resume segments: {', '.join(missing_standards)}. ATS indexers may rate completeness lower.")
        base_compatibility -= len(missing_standards) * 5.0

    # 3. Inspect Text Density and Keyword volumes
    summary_obj = sections.get("summary", "")
    summary_text = summary_obj.get("text", "") if isinstance(summary_obj, dict) else str(summary_obj)
    
    skills_obj = sections.get("skills", [])
    skills_list = []
    if isinstance(skills_obj, dict):
        for v in skills_obj.values():
            if isinstance(v, list):
                skills_list.extend([str(item) for item in v])
    elif isinstance(skills_obj, list):
        skills_list.extend([s.get("text", "") if isinstance(s, dict) else str(s) for s in skills_obj])
        
    flat_text = summary_text + " " + " ".join(skills_list)
    word_count = len(flat_text.split())
    
    if word_count < 50:
        warnings.append("Keyword density is extremely low. ATS search matching could fail to register relevance.")
        base_compatibility -= 10.0
    elif word_count > 600:
        warnings.append("High word density detected. Overly verbose structures may degrade ATS keyword weight ratios.")
        base_compatibility -= 5.0

    # Ensure score stays in bounding limits
    compatibility_score = max(30.0, min(99.0, base_compatibility))

    return {
        "ats_compatibility_score": round(compatibility_score, 2),
        "is_linear_layout": template != "creative",
        "has_standard_headers": len(missing_standards) == 0,
        "parsing_warnings": warnings
    }
