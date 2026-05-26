"""
Resume Template Personality Engine.
Configures typography scales, line spacing, segment emphasis, and bullet density
based on target organizational profiles (Startup, Enterprise, FAANG, Research, Minimalist, Executive).
"""

from typing import Dict, Any

TEMPLATE_PERSONALITIES = {
    "classic": {
        "font_family": "Cambria, Georgia, serif",
        "line_height": 1.25,
        "section_spacing_margin": "18px",
        "bullet_density": "high",
        "show_branding_border": False,
        "accent_color": "#1e293b",
        "recruiter_vibe": "Traditional corporate, legacy, finance-aligned"
    },
    "modern": {
        "font_family": "'Outfit', 'Inter', sans-serif",
        "line_height": 1.35,
        "section_spacing_margin": "22px",
        "bullet_density": "medium",
        "show_branding_border": True,
        "accent_color": "#4f46e5",
        "recruiter_vibe": "Sleek technical startup, product-first, SaaS-aligned"
    },
    "executive": {
        "font_family": "Garamond, Times New Roman, serif",
        "line_height": 1.20,
        "section_spacing_margin": "16px",
        "bullet_density": "high",
        "show_branding_border": True,
        "accent_color": "#0f172a",
        "recruiter_vibe": "Senior leadership, bold structures, scale-obsessed"
    },
    "startup": {
        "font_family": "'Inter', sans-serif",
        "line_height": 1.40,
        "section_spacing_margin": "24px",
        "bullet_density": "medium",
        "show_branding_border": False,
        "accent_color": "#06b6d4",
        "recruiter_vibe": "Agile builder, rapid iteration, ambiguous ownership"
    },
    "faang": {
        "font_family": "Arial, Helvetica, sans-serif",
        "line_height": 1.15,
        "section_spacing_margin": "14px",
        "bullet_density": "high",
        "show_branding_border": False,
        "accent_color": "#2563eb",
        "recruiter_vibe": "Hyper-scale, deep algorithmic execution, metrics-first"
    }
}


def configure_template_styling(template_id: str) -> Dict[str, Any]:
    """Generates the styling metrics dictionary matching a chosen template personality choice."""
    tid = str(template_id).strip().lower()
    
    # Resolve aliases
    if tid == "enterprise":
        tid = "classic"
    elif tid == "startup":
        tid = "startup"
    elif tid not in TEMPLATE_PERSONALITIES:
        tid = "modern"
        
    return TEMPLATE_PERSONALITIES[tid]
