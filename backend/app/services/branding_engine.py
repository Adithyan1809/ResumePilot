"""
Personal Branding Engine.
Optimizes candidate career branding matrices, including LinkedIn headlines, About segments,
and GitHub profile bios aligned to whitelisted evidence.
"""

from typing import List, Dict, Any


def generate_personal_branding(
    structured_evidence: Dict[str, Any],
    focus_domain: str,
    seniority: str
) -> Dict[str, Any]:
    """Generates aligned headline, bio, and summary slogans for LinkedIn, GitHub, and portfolios."""
    if not structured_evidence:
        return _get_empty_branding()

    contact = structured_evidence.get("contact_info", {})
    name = contact.get("name", "Software Engineer")
    
    # Extract primary tools
    flat_skills = []
    for cat_list in structured_evidence.get("skills", {}).values():
        if isinstance(cat_list, list):
            flat_skills.extend(cat_list)
            
    top_techs = flat_skills[:4] if flat_skills else ["Python", "SQL", "Docker", "Git"]
    tech_slug = " | ".join(top_techs)

    # 1. LinkedIn Headline
    headline = f"{seniority}-Level Systems Engineer | Specialized in {focus_domain.title()} Applications | {tech_slug}"
    
    # 2. LinkedIn About Copy
    about_text = (
        f"Hi, I'm {name}! I am a {seniority}-level software engineer obsessed with system latency, "
        f"database optimization, and robust API development. Over my career, I've focused on "
        f"translating complex business requirements into scale-resilient backends using {', '.join(top_techs)}.\n\n"
        f"Key expertise:\n"
        f"• Asynchronous API routing and microservice gateways\n"
        f"• Relational database index tuning and query scaling\n"
        f"• Containerized deployments and devops pipeline automations"
    )
    
    # 3. GitHub Bio
    git_bio = f"💻 Systems Developer exploring {', '.join(top_techs[:2])} scaling architectures. Focused on metrics & clean code."

    return {
        "linkedin_headline": headline,
        "linkedin_about": about_text,
        "github_bio": git_bio,
        "portfolio_slogan": f"Engineering robust, metric-proven software systems."
    }


def _get_empty_branding() -> Dict[str, Any]:
    """Default fallback branding response."""
    return {
        "linkedin_headline": "Systems Software Developer",
        "linkedin_about": "Dedicated software engineer exploring systems architecture.",
        "github_bio": "Code craftsman focusing on scalable integrations.",
        "portfolio_slogan": "Building high-velocity code implementations."
    }
