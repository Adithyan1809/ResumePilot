"""
Company Intelligence Engine.
Curates database profiles for top engineering companies and dynamically infers corporate tech stacks,
hiring patterns, and engineering culture priorities for other companies.
"""

from typing import Dict, Any

COMPANY_DB = {
    "google": {
        "name": "Google",
        "engineering_culture": "Scale-first, algorithmic rigor, systems reliability, deep technical ownership, high engineering standards.",
        "tech_stack": ["C++", "Java", "Python", "Go", "Borg", "MapReduce", "Protobuf", "gRPC", "SQL"],
        "values": ["Focus on the user", "Respect the user", "Scale through engineering", "Shared ownership"],
        "recruiter_persona": "Rigorous engineer scanning for algorithmic depth, deep systems understanding, and clean patterns."
    },
    "meta": {
        "name": "Meta",
        "engineering_culture": "Move fast, focus on impact, open source, shipping quickly, extreme developer autonomy, scalability.",
        "tech_stack": ["React", "PyTorch", "Hack", "PHP", "Rust", "C++", "Python", "MyRocks", "Memcached"],
        "values": ["Move fast", "Focus on impact", "Build awesome things", "Live in the future"],
        "recruiter_persona": "Pragmatic builder scanning for high shipping speed, impact metrics, product ownership, and open-source contributions."
    },
    "stripe": {
        "name": "Stripe",
        "engineering_culture": "API elegance, meticulous documentation, precision, systems reliability, high code quality.",
        "tech_stack": ["Ruby", "Java", "Go", "TypeScript", "React", "Sorbet", "PostgreSQL", "Kafka", "MongoDB"],
        "values": ["Users first", "API beauty", "Meticulous execution", "Move with urgency"],
        "recruiter_persona": "Craftsman recruiter looking for extreme attention to detail, polished APIs, clean architecture, and robust testing."
    },
    "netflix": {
        "name": "Netflix",
        "engineering_culture": "Freedom & responsibility, high autonomy, microservice resilience, scale optimization.",
        "tech_stack": ["Java", "JavaScript", "React", "Node.js", "Python", "AWS", "Cassandra", "Kafka", "Eureka"],
        "values": ["Freedom and responsibility", "High performance", "Stunning colleagues", "Context, not control"],
        "recruiter_persona": "Senior engineer looking for high scale experience, microservice reliability knowledge, and high ownership culture alignment."
    },
    "amazon": {
        "name": "Amazon",
        "engineering_culture": "Customer obsession, scale resilience, extreme operational excellence, two-pizza teams, writing documents over slides.",
        "tech_stack": ["Java", "C++", "Python", "AWS", "PostgreSQL", "DynamoDB", "Redshift", "Docker"],
        "values": ["Customer obsession", "Ownership", "Invent and simplify", "Deliver results", "Bias for action"],
        "recruiter_persona": "Operational leader checking for scale metrics, customer impact, cost optimization, and adherence to leadership principles."
    },
    "airbnb": {
        "name": "Airbnb",
        "engineering_culture": "Design elegance, modern web design systems, user experience obsession, high-quality frontends.",
        "tech_stack": ["Ruby", "Rails", "JavaScript", "TypeScript", "React", "Sass", "MySQL", "AWS", "Redis"],
        "values": ["Champion the mission", "Be a host", "Embrace the adventure", "Never fail a guest"],
        "recruiter_persona": "Visual craftsman looking for UI aesthetics, deep frontend architecture understanding, and high product empathy."
    }
}


def get_company_profile(company_name: str) -> Dict[str, Any]:
    """Retrieves or infers an engineering profile for a targeted company name."""
    name_clean = str(company_name).strip().lower()
    
    # 1. Match in tier-1 DB
    for key, profile in COMPANY_DB.items():
        if key in name_clean:
            return profile
            
    # 2. Heuristics fallback: Startup vs. Enterprise
    is_enterprise = len(name_clean) > 8 or any(w in name_clean for w in ["group", "global", "solutions", "bank", "systems", "insurance", "holdings", "inc"])
    
    if is_enterprise:
        return {
            "name": company_name,
            "engineering_culture": "Enterprise reliability, standard operating procedures, multi-team collaborations, scale & compliance alignment.",
            "tech_stack": ["Java", "C#", "SQL Server", "Oracle", "AWS", "Docker", "CI/CD"],
            "values": ["Security", "Scalability", "Collaboration", "Reliability"],
            "recruiter_persona": "Standard enterprise hiring manager looking for robust teamwork, predictable clean code, and solid system testing foundations."
        }
    else:
        # Startup profile
        return {
            "name": company_name,
            "engineering_culture": "Rapid velocity, high ambiguity, full technical ownership, building from scratch, fast iteration.",
            "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Vite", "AWS"],
            "values": ["Velocity", "Ownership", "Adaptability", "User Focus"],
            "recruiter_persona": "Startup engineer looking for generalist capabilities, rapid prototyping, independent ownership, and strong API integrations."
        }
