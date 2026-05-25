"""
Learning Recommendation Engine.

Provides actionable, honest project templates and educational guidelines 
to candidates for bridging their skill gaps without faking experiences.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Predefined premium learning recommendations mapped to missing frameworks and tools
RECOMMENDATIONS_POOL = {
    "react": {
        "projects": [
            "Interactive Job Board UI (React, TailwindCSS)",
            "Dynamic Task Management Dashboard with State Synchronization"
        ],
        "skills": ["React Virtual DOM fundamentals", "React Component Lifecycle & Hooks", "State Management (useState/useEffect)"]
    },
    "next.js": {
        "projects": [
            "Server-Side Rendered Static Blog (Next.js, TailwindCSS)",
            "Dynamic Search Portal leveraging Next.js App Router"
        ],
        "skills": ["Next.js Server Components", "Static Site Generation (SSG)", "Client vs Server Rendering models"]
    },
    "typescript": {
        "projects": [
            "TypeScript-Safe Metric Calculator Library",
            "TypeScript Schema Validator for REST API requests"
        ],
        "skills": ["TypeScript Types & Interfaces", "Strict Type Compilation", "Generic Functions & Safety Guards"]
    },
    "tailwind": {
        "projects": [
            "Responsive Utility-First Layout Kit",
            "Modern CSS Portfolio Page using Tailwind styling rules"
        ],
        "skills": ["Utility-First CSS Principles", "Responsive Layout breakpoints", "Tailwind Theme Customization"]
    },
    "fastapi": {
        "projects": [
            "Asynchronous Task Processing API (FastAPI, Redis)",
            "JWT-Secured User Access Manager Endpoint"
        ],
        "skills": ["FastAPI Pydantic Request Validation", "Asynchronous Route Handlers", "Dependency Injection patterns"]
    },
    "docker": {
        "projects": [
            "Containerized Multi-Service Web App (Docker Compose)",
            "Production-Grade Dockerfile for secure Python/Node runtimes"
        ],
        "skills": ["Multi-stage Docker builds", "Docker Compose Orchestration", "Image Size Reduction practices"]
    }
}

def generate_recommendations(skill_gaps: Dict[str, Any]) -> Dict[str, Any]:
    """Compile custom learning recommendations and honest growth projects based on identified skill gaps."""
    missing_fw = [f.lower() for f in skill_gaps.get("missing_frameworks", [])]
    missing_tools = [t.lower() for t in skill_gaps.get("missing_tools", [])]
    missing_skills = [s.lower() for s in skill_gaps.get("missing_skills", [])]
    
    gaps = missing_fw + missing_tools + missing_skills
    
    recommended_projects = []
    recommended_skills = []
    
    # Scan gap keys
    for key in RECOMMENDATIONS_POOL:
        if any(key in g for g in gaps):
            recommended_projects.extend(RECOMMENDATIONS_POOL[key]["projects"])
            recommended_skills.extend(RECOMMENDATIONS_POOL[key]["skills"])
            
    # Default fallbacks if no specific mapping was hit
    if not recommended_projects:
        recommended_projects = [
            "Responsive Personal Developer Portfolio website showcasing backend APIs",
            "Core Algorithm Sandbox demonstrating modular data structures and performance analysis"
        ]
    if not recommended_skills:
        recommended_skills = [
            "Modern Web Framework Fundamentals",
            "Containerization and Service Deployment",
            "Relational Database Query Optimization"
        ]
        
    return {
        "recommended_projects": list(dict.fromkeys(recommended_projects))[:3],
        "recommended_skills_to_learn": list(dict.fromkeys(recommended_skills))[:4]
    }
