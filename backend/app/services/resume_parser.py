"""
Resume parsing service for PDF and DOCX documents.
"""

import logging
import re
from typing import Any, Dict, Tuple

from docx import Document
import pdfplumber
import logging

_LOGGER = logging.getLogger(__name__)

# Optional OCR imports (used only if available)
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    _OCR_AVAILABLE = True
except Exception:
    _OCR_AVAILABLE = False

from app.utils.text import clean_text, extract_emails, extract_phones, extract_urls, heal_bullet_text

logger = logging.getLogger(__name__)

# Heuristic header mappings to classify section content
SECTION_PATTERNS = {
    "summary": r"\b(summary|profile|objective|professional summary|about me|career objective|executive summary)\b",
    "experience": r"\b(experience|work experience|employment|employment history|work history|professional experience|professional background|career history)\b",
    "education": r"\b(education|academic background|academic history|degrees|credentials|academic qualifications)\b",
    "skills": r"\b(skills|technical skills|core competencies|technologies|expertise|areas of expertise|professional skills|skills & expertise)\b",
    "certifications": r"\b(certifications|certification|licenses|courses|accreditations|professional certifications)\b",
    "projects": r"\b(projects|key projects|personal projects|selected projects|academic projects)\b",
    "languages": r"\b(languages|language|language proficiency)\b",
    "awards": r"\b(awards|honours|honors|achievements|distinctions|fellowships)\b",
    "publications": r"\b(publications|patents|research papers|articles)\b",
    "volunteer": r"\b(volunteer|volunteering|volunteer experience|community service|social work)\b",
}

# ... [unchanged code above] ...

def _parse_projects(lines: list[str]) -> list[Dict[str, Any]]:
    """Helper to convert projects text into structured entries with smart boundary detection and robust fallback parsing."""
    if not lines:
        return []
    cleaned_lines = [l.strip() for l in lines if l.strip()]
    if not cleaned_lines:
        return []
    project_blocks = []
    current_block = []
    # Smart boundary detection as before
    for idx, line in enumerate(cleaned_lines):
        is_boundary = False
        # Rule 1: Starts with explicit project keyword
        if re.match(r"^project\b", line, re.IGNORECASE) and not re.search(r"bullet|description|detail", line, re.IGNORECASE):
            is_boundary = True
        # Rule 2: Short line and next line starts with Tech Stack or bullet points, and we already have some lines in current block
        elif current_block and len(line) < 50 and not line.startswith(("-", "•", "*", "•")):
            next_line = cleaned_lines[idx + 1] if idx + 1 < len(cleaned_lines) else ""
            if next_line and (
                re.search(r"\b(technologies|tech stack|built with|tools?):\s*", next_line, re.IGNORECASE) or
                next_line.startswith(("-", "•", "*", "•"))
            ):
                is_boundary = True
        elif "github.com/" in line.lower() and len(line) < 80 and current_block:
            has_bullets = any(l.startswith(("-", "•", "*")) for l in current_block)
            if has_bullets:
                is_boundary = True
        if is_boundary and current_block:
            project_blocks.append(current_block)
            current_block = []
        current_block.append(line)
    if current_block:
        project_blocks.append(current_block)
    entries = []
    for block_lines in project_blocks:
        if not block_lines:
            continue
        # Fallback: try to robustly support "Name | Description" or "Name - Description" style blocks
        name = ""
        desc_lines = []
        technologies = []
        link = ""
        # If the first line has "|" or " - " use that as a fallback
        m = re.split(r"\s*\|\s*", block_lines[0], maxsplit=1)
        if len(m) == 2:
            name = m[0].strip()
            desc_lines = [m[1].strip()]
        else:
            # Try dash/hyphen fallback
            dash_parts = re.split(r"\s+-\s+", block_lines[0], maxsplit=1)
            if len(dash_parts) == 2:
                name = dash_parts[0].strip()
                desc_lines = [dash_parts[1].strip()]
            else:
                name = block_lines[0].strip()
        # Handle any bullets/extra description lines
        for line in block_lines[1:]:
            lc = line.strip()
            # If the line has a link/URL, store it
            if ("github.com/" in lc.lower() or "http" in lc.lower()):
                urls = extract_urls(lc)
                if urls:
                    link = urls[0]
                    continue
            # Check for explicit tech stack line
            tech_match = re.search(r"\b(tech|technologies|tech stack|built with|tools?):\s*(.*)\b", lc, re.IGNORECASE)
            if tech_match:
                tech_vals = tech_match.group(2)
                technologies = [t.strip() for t in re.split(r"[,;•|]+", tech_vals) if t.strip()]
                continue
            # Treat as an extra description line
            desc_lines.append(lc)
        # If still no technologies, try to extract some from the description lines
        if not technologies:
            tech_keywords = ["python", "opencv", "ffmpeg", "react", "django", "flask", "tensorflow", "pytorch", "docker", "aws", "azure", "gcp", "sql", "mongodb"]
            for desc in desc_lines:
                for kw in tech_keywords:
                    if kw in desc.lower() and kw not in technologies:
                        technologies.append(kw.title())
        entries.append({
            "name": name,
            "technologies": technologies,
            "description": desc_lines,
            "link": link
        })
    return entries

# ... [unchanged code below] ...
