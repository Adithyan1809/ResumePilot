"""
Interview Simulation Engine.
Generates highly targeted, role-specific technical, behavioral, system design,
and project-based questions calibrated to the candidate's actual projects.
"""

from typing import List, Dict, Any


def generate_interview_questions(
    structured_evidence: Dict[str, Any],
    job_title: str,
    company: str,
    focus_domain: str
) -> Dict[str, Any]:
    """Compiles personalized interview question matrices based on target roles and whitelisted evidence."""
    domain = focus_domain.lower() if focus_domain else "backend"
    
    questions = {
        "technical": [
            "What is the difference in Python between multi-threading, multi-processing, and async/await task loops?",
            "How do indexing structures and B-Trees operate inside PostgreSQL databases to accelerate query lookups?"
        ],
        "project_based": [],
        "system_design": [
            f"How would you design a scalable system structure to process high-throughput API requests for {company or 'a tech startup'}?",
            "How do rate-limiting middleware algorithms (like token bucket) secure backend REST gateways?"
        ],
        "behavioral": [
            "Tell me about a time you had to debug a complex production bottleneck under tight delivery constraints. How did you proceed?",
            "How do you handle technical disagreements on API design patterns or framework choices with other engineers?"
        ]
    }

    # 1. Project-Based Questions (Calibrated to whitelisted candidate projects)
    projects = structured_evidence.get("projects", []) or []
    for proj in projects[:2]:
        title = proj.get("title", "Engineering Project")
        techs = proj.get("technologies", ["Python"])
        questions["project_based"].append(
            f"On your project '{title}' built using {', '.join(techs[:3])}, "
            f"how did you approach containerization or database setup to ensure system performance?"
        )
        
    if not questions["project_based"]:
        questions["project_based"].append(
            "Reviewing your project achievements, walk me through the system architecture design decisions "
            "you made to deliver key operational metrics."
        )

    # 2. Focus Domain customization
    if domain == "frontend":
        questions["technical"] = [
            "Explain the React rendering lifecycle differences between Client components and Server components.",
            "How do browsers optimize layout calculations, and how do you reduce repaint/reflow bottlenecks?"
        ]
        questions["system_design"] = [
            "How would you architect a reusable, highly-accessible CSS design system or components library?",
            "How do you manage client-side state caching to support offline capabilities on slow networks?"
        ]
    elif domain == "devops":
        questions["technical"] = [
            "Explain Docker multi-stage build caching, and how do you secure containers to run as non-root?",
            "How do Kubernetes Ingress controllers handle routing and certificate terminations?"
        ]
        questions["system_design"] = [
            "Design an automated CI/CD release workflow supporting canary and blue-green cloud deployments.",
            "How do you configure Prometheus and Grafana alert limits for high-availability systems?"
        ]
    elif domain == "data_science":
        questions["technical"] = [
            "Explain the mathematical differences between L1 (Lasso) and L2 (Ridge) regression regularizations.",
            "How do self-attention mechanisms in Transformer neural models operate to compute context vectors?"
        ]
        questions["system_design"] = [
            "Design an analytical model serving infrastructure to serve deep neural predictions with low-latency.",
            "How do you set up distributed feature stores to feed model training pipelines?"
        ]

    return {
        "job_title": job_title,
        "company": company,
        "interview_prep_checklist": [
            "Practice explaining your project milestones using the STAR model (Situation, Task, Action, Result).",
            "Be prepared to detail technical tradeoffs (concurrency vs simplicity, memory vs processing)."
        ],
        "simulated_questions": questions
    }
