"""
Career Timeline Engine.
Predicts linear multi-year career progression tracks and milestones based on active candidate profiles.
"""

from typing import List, Dict, Any

PROGRESSION_TRACKS = {
    "backend": [
        {"title": "Backend Engineering Intern", "duration": "3-6 months", "milestone": "Master SQL index setups and API route containerization."},
        {"title": "Junior Backend Developer", "duration": "1-2 years", "milestone": "Own REST endpoint integrations and async database pools."},
        {"title": "Software Engineer II (Systems)", "duration": "2-3 years", "milestone": "Design scalable Redis caching architectures and gRPC pipelines."},
        {"title": "Senior Systems / AI Infrastructure Engineer", "duration": "3+ years", "milestone": "Orchestrate Kubernetes clusters and high-throughput data streams."}
    ],
    "frontend": [
        {"title": "Frontend Development Intern", "duration": "3-6 months", "milestone": "Master CSS layouts, responsive DOM renders, and React basic hooks."},
        {"title": "Junior Frontend Engineer", "duration": "1-2 years", "milestone": "Build polished dynamic dashboards and manage application state trees."},
        {"title": "Full Stack / UI Engineer", "duration": "2-3 years", "milestone": "Architect Next.js server components and custom design systems."},
        {"title": "Lead Frontend Architect", "duration": "3+ years", "milestone": "Oversee modular micro-frontends, rendering optimizations, and client scale."}
    ],
    "data_science": [
        {"title": "Data Analyst Intern", "duration": "3-6 months", "milestone": "Perform EDA, write Pandas queries, and compile data reports."},
        {"title": "ML Engineer (tabular models)", "duration": "1-2 years", "milestone": "Train decision forests and compile feature classification pipelines."},
        {"title": "ML Infrastructure Specialist", "duration": "2-3 years", "milestone": "Deploy PyTorch custom features on AWS clusters with high-throughput."},
        {"title": "Senior AI Systems Architect", "duration": "3+ years", "milestone": "Train and fine-tune large generative model matrices for scale operations."}
    ]
}


def predict_career_timeline(focus_domain: str, candidate_skills: List[str]) -> Dict[str, Any]:
    """Projects future career progression milestones based on active candidate focus."""
    domain = focus_domain.lower() if focus_domain else "backend"
    if domain not in PROGRESSION_TRACKS:
        domain = "backend"
        
    timeline = PROGRESSION_TRACKS[domain]
    
    # Analyze current step
    current_idx = 0
    if len(candidate_skills) > 6:
        current_idx = 1
    if len(candidate_skills) > 12:
        current_idx = 2
        
    return {
        "current_position_index": current_idx,
        "progression_path": timeline,
        "suggested_career_transition": f"Aim for the next milestone: {timeline[min(len(timeline)-1, current_idx + 1)]['title']} ({timeline[min(len(timeline)-1, current_idx + 1)]['duration']})",
        "next_technical_goal": timeline[min(len(timeline)-1, current_idx + 1)]["milestone"]
    }
