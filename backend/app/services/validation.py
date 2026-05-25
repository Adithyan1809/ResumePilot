"""Validation utilities to detect hallucinations and missing provenance in generated sections.

These functions perform lightweight checks and return human-readable warnings.
"""
import copy
import re
from typing import Any, Dict, List

# Imports for validation tasks
from app.services.ai_engine import _scrub_contact_info, normalize_experience_titles
from app.services.alignment import align_projects_to_role, align_skills_to_role, classify_role_by_jd
from app.services.github_service import enrich_projects_section
from app.services.grammar import polish_bullets


def _contains_substring(text: str, substring: str) -> bool:
    if not text or not substring:
        return False
    return substring.strip() in text


def _extract_numbers(text: str) -> List[str]:
    return re.findall(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b", text or "")


def get_role_category_for_bullet_validation(role: str) -> str:
    r = (role or "backend").lower()
    if "data" in r or "analyst" in r:
        return "data_science"
    if "vision" in r or "cv" in r or "ai" in r or "ml" in r:
        return "computer_vision"
    if "front" in r or "ui" in r or "ux" in r or "web" in r or "react" in r:
        return "frontend"
    return "backend"


def naturalize_summary(summary: str) -> str:
    """Converts robotic colon-heavy keyword blocks into clean, natural human prose."""
    if not summary:
        return ""
    
    text = summary.strip()
    
    # 1. Regex to match typical colon-heavy listings like:
    # "specializing in [Category]: [Skill1], [Skill2], and [Skill3]"
    # or "proficient in [Category]: [Skill1], [Skill2]"
    pattern = r"(\bspecializing\s+in|\bproficient\s+in|\bfocused\s+on|\bskilled\s+in)\s+([a-zA-Z\s&]+):\s*([a-zA-Z\s,]+)"
    
    def replacer(match):
        prefix = match.group(1)
        category = match.group(2).strip()
        skills = match.group(3).strip()
        return f"{prefix} {category} leveraging {skills}"
        
    text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
    
    # 2. General clean up of standard nested colons in the summary
    text = re.sub(r"\bCore\s+competencies:\s*", "core competencies including ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bTechnical\s+strengths:\s*", "technical strengths in ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bStrong\s+foundation\s+in:\s*", "strong foundation in ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bHands-on\s+experience\s+in:\s*", "hands-on experience in ", text, flags=re.IGNORECASE)
    
    return text.strip()


def humanize_project_title(title: str) -> str:
    """Normalizes project names to ensure proper acronym capitalization (e.g., AI-Based, URL, ML)
    and clean title casing.
    """
    if not title:
        return ""
        
    t = title.strip()
    
    # Capitalize acronyms correctly
    acronym_replacements = {
        r"\bAi\b": "AI",
        r"\bMl\b": "ML",
        r"\bUrl\b": "URL",
        r"\bApi\b": "API",
        r"\bApis\b": "APIs",
        r"\bVr\b": "VR",
        r"\bDb\b": "DB",
        r"\bSql\b": "SQL",
        r"\bOppid\b": "OPPID",
        r"\bCnn\b": "CNN",
        r"\bNlp\b": "NLP",
        r"\bCv\b": "CV",
        r"\bLlm\b": "LLM",
        r"\bLlems\b": "LLMs",
        r"\bAws\b": "AWS",
        r"\bGcp\b": "GCP",
        r"\bId\b": "ID",
        r"\bIds\b": "IDs"
    }
    
    for pattern, replacement in acronym_replacements.items():
        t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)
        
    # Handle hyphens, e.g., "AI Based" -> "AI-Based"
    t = re.sub(r"\bAI\s+Based\b", "AI-Based", t, flags=re.IGNORECASE)
    t = re.sub(r"\bML\s+Based\b", "ML-Based", t, flags=re.IGNORECASE)
    t = re.sub(r"\bWeb\s+Based\b", "Web-Based", t, flags=re.IGNORECASE)
    t = re.sub(r"\bCloud\s+Based\b", "Cloud-Based", t, flags=re.IGNORECASE)
    
    # Run title casing for words that are not uppercase acronyms
    words = t.split()
    title_words = []
    for w in words:
        if w.isupper() and len(w) > 1:
            title_words.append(w)
        else:
            title_words.append(w[0].upper() + w[1:] if len(w) > 0 else "")
            
    t = " ".join(title_words)
    return t


def validate_generated_sections(raw_text: str, generated: Dict[str, Any]) -> List[str]:
    """Validate generated structured sections against the original raw text.

    Returns a list of validation issue strings (empty if none).
    """
    issues: List[str] = []
    if not isinstance(generated, dict):
        issues.append("Generated sections are not in expected structured format.")
        return issues

    # Summary check
    summary = generated.get("summary")
    if isinstance(summary, dict):
        if not summary.get("source_excerpts"):
            issues.append("Summary lacks source excerpts and may contain hallucinated content.")
    else:
        if summary and summary.strip() and summary not in raw_text:
            issues.append("Summary appears to contain content not present in the original resume.")

    # Experience check
    exp = generated.get("experience", [])
    for idx, entry in enumerate(exp):
        bullets = entry.get("bullets", []) if isinstance(entry, dict) else []
        for bidx, b in enumerate(bullets):
            if isinstance(b, dict):
                if not b.get("source_excerpts") and b.get("needs_human_review"):
                    issues.append(f"Experience bullet {idx + 1}.{bidx + 1} lacks provenance and needs review.")
                # Check numbers
                nums = _extract_numbers(b.get("text", ""))
                for n in nums:
                    if n not in raw_text:
                        issues.append(f"Numeric value '{n}' in experience bullet {idx + 1}.{bidx + 1} not found in source resume.")
            else:
                if b and b.strip() not in raw_text:
                    issues.append(f"Experience bullet {idx + 1}.{bidx + 1} may contain invented content.")

    # Skills check: ensure skills are grounded
    skills = generated.get("skills", [])
    if skills:
        skill_text = "\n".join([s.get("text") if isinstance(s, dict) else str(s) for s in skills])
        for token in re.split(r"[,;\n]+", skill_text):
            t = token.strip()
            if not t:
                continue
            if t and t.lower() not in (raw_text or "").lower() and len(t) > 3:
                issues.append(f"Skill '{t}' not found verbatim in source resume; verify it's accurate.")

    return list(dict.fromkeys(issues))  # deduplicate


# Buzzwords to remove to protect technical realism
BUZZWORDS_TO_REMOVE = [
    "scale-resilient",
    "elite impact",
    "technical velocity",
    "agile leadership excellence"
]


def clean_metadata_leak(text_str: str) -> str:
    """Robustly cleans stringified dictionary/JSON fragments and metadata keys
    (such as confidence, needs_human_review, source_excerpts) from any text field.
    """
    if not text_str:
        return ""

    # Remove source_excerpts block and key (which can contain nested list of strings/dicts)
    text_str = re.sub(r'[\'"]?source_excerpts[\'"]?\s*:\s*\[[^\]]*\]', '', text_str)

    # Remove confidence key/value
    text_str = re.sub(r'[\'"]?confidence[\'"]?\s*:\s*[0-9\.]+', '', text_str)

    # Remove needs_human_review key/value
    text_str = re.sub(r'[\'"]?needs_human_review[\'"]?\s*:\s*(?:True|False|true|false)', '', text_str)

    # Remove text key
    text_str = re.sub(r'[\'"]?text[\'"]?\s*:\s*', '', text_str)

    # Remove curly/square brackets
    text_str = re.sub(r'[\{\}\[\]]', '', text_str)

    # Remove quotes
    text_str = text_str.replace("'", "").replace('"', '').replace('`', '').strip()

    # Clean up spacing and multiple commas
    text_str = re.sub(r'\s+', ' ', text_str)
    text_str = re.sub(r',[\s,]*', ', ', text_str)
    text_str = re.sub(r'^[\s,]+|[\s,]+$', '', text_str)

    return text_str.strip()


def sanitize_text(text: str) -> str:
    """Helper to scrub buzzwords and remove empty placeholders from string fields."""
    if not text:
        return ""
    
    # Pre-scrub stringified metadata structures or JSON remnants
    text = clean_metadata_leak(text)
    
    # Remove empty parentheticals/placeholders
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\(\s*-\s*\)", "", text)
    text = re.sub(r"-\s*$", "", text)
    text = re.sub(r"^\s*-", "", text)
    text = re.sub(r",\s*$", "", text)
    
    # Strip corporate buzzwords
    for word in BUZZWORDS_TO_REMOVE:
        text = re.sub(r'\b' + re.escape(word) + r'\b', "", text, flags=re.IGNORECASE)
    
    # Clean multiple spaces/dangling separators
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" .", ".").replace(" -", "-")
    return text.strip()


async def sanitize_and_validate_tailored_sections(
    raw_text: str,
    tailored: Dict[str, Any],
    original: Dict[str, Any],
    job_description: str = ""
) -> Dict[str, Any]:
    """Strictly sanitize, enrich, align, and validate tailored resume sections.
    
    This acts as the final resume validation pipeline. It runs:
    1. GitHub Projects enrichment.
    2. Role classification and dynamic projects/skills reordering based on JD relevance.
    3. Experience titles normalization (for realistic intern/undergrad staging).
    4. Async grammar, tense, and structural bullet polishing.
    5. Deduplication and name/contact detail scrubbing to prevent any summary/bullet leaks.
    """
    if not isinstance(tailored, dict):
        raise ValueError("Tailored resume sections must be a valid JSON dictionary")
    
    if not tailored:
        raise ValueError("Tailored resume sections cannot be empty")
        
    for key in ["summary", "experience", "skills"]:
        if key not in tailored:
            raise ValueError(f"Tailored resume sections are missing the required '{key}' section")
            
    if not isinstance(tailored.get("experience"), list):
        raise ValueError("Experience section in tailored resume must be a list of job entries")
        
    if not isinstance(tailored.get("skills"), list):
        raise ValueError("Skills section in tailored resume must be a list of skills")
        
    for idx, entry in enumerate(tailored.get("experience", [])):
        if not isinstance(entry, dict):
            raise ValueError(f"Experience entry at index {idx} must be a dictionary")
        if "bullets" not in entry or not isinstance(entry.get("bullets"), list):
            raise ValueError(f"Experience entry at index {idx} must contain a 'bullets' list")
            
    if "projects" in tailored and not isinstance(tailored.get("projects"), list):
        raise ValueError("Projects section in tailored resume must be a list of project entries")
        
    if "projects" in tailored:
        for idx, entry in enumerate(tailored.get("projects", []) or []):
            if not isinstance(entry, dict):
                raise ValueError(f"Project entry at index {idx} must be a dictionary")

    import copy
    
    # Use a copy to avoid mutating the original input
    sanitized = copy.deepcopy(tailored)
    raw_text_lower = (raw_text or "").lower()
    contact_info = original.get("contact_info", {}) or {}

    # ── 1. Enrich Projects Section via GitHub ──────────────────────
    try:
        sanitized = await enrich_projects_section(sanitized)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"GitHub Projects enrichment failed: {exc}")

    # Extract validated GitHub technologies for grounding checks
    github_techs = []
    if "projects" in sanitized and isinstance(sanitized["projects"], list):
        for proj in sanitized["projects"]:
            if isinstance(proj, dict):
                github_techs.extend(proj.get("technologies", []) or [])
    github_techs = list(set([t for t in github_techs if t]))

    # ── 2. Job Role Classification & Dynamic Reordering ─────────────
    role = "general"
    if job_description:
        try:
            role = await classify_role_by_jd(job_description)
            
            # Reorder skills
            if "skills" in sanitized:
                sanitized["skills"] = align_skills_to_role(sanitized["skills"], role)
                
            # Reorder projects
            if "projects" in sanitized:
                sanitized["projects"] = align_projects_to_role(sanitized["projects"], role)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"Role alignment / reordering failed: {exc}")

    # ── 3. Summary Optimization & Contact Scrubbing ─────────────────
    summary_data = tailored.get("summary", "")
    summary_text = summary_data.get("text", "") if isinstance(summary_data, dict) else str(summary_data)
    
    # Scrub contact leaks
    summary_text = _scrub_contact_info(summary_text, contact_info)
    summary_text = sanitize_text(summary_text)
    
    # Enforce Summary Length: strictly 3-4 concise lines (approx 3 sentences, 50-70 words)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", summary_text) if s.strip()]
    if len(sentences) > 3:
        summary_text = " ".join(sentences[:3])
        if not summary_text.endswith("."):
            summary_text += "."
            
    # Apply technology domain validation & healing
    try:
        from app.services.technology_domain_validator import heal_bullet_contamination
        validator_role = role
        if role == "ai_ml":
            validator_role = "computer_vision"
        summary_text = heal_bullet_contamination(summary_text, validator_role)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Summary domain validation/healing failed: {exc}")

    # Naturalize professional summary to sound extremely human and professional
    summary_text = naturalize_summary(summary_text)

    # Apply role transferability mode & reality preservation to summary
    try:
        from app.services.reality_preservation_engine import apply_role_transferability_summary, cleanse_ungrounded_technologies
        # Apply role transferability mode (pivots backend/student candidates to transferable API and growth fundamentals)
        summary_text = apply_role_transferability_summary(summary_text, role, raw_text)
        # Cleanse any ungrounded technology keywords from summary
        summary_text = cleanse_ungrounded_technologies(summary_text, raw_text, github_techs)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Summary reality preservation failed: {exc}")

    if isinstance(sanitized.get("summary"), dict):
        sanitized["summary"]["text"] = summary_text
    else:
        sanitized["summary"] = summary_text

    # ── 4. Experience Title Normalization & Grammar Polishing ──────
    orig_exp = original.get("experience", []) or []
    tailored_exp = tailored.get("experience", []) or []
    
    # Normalize titles if student appropriate
    is_student = True
    for edu in original.get("education", []) or []:
        deg = edu.get("degree", "").lower()
        if any(w in deg for w in ["bachelor", "undergraduate", "b.e", "b.tech", "student"]):
            is_student = True
            break
            
    normalized_exp = normalize_experience_titles(tailored_exp, is_student=is_student)
    
    sanitized_exp = []
    for idx, entry in enumerate(normalized_exp):
        orig_entry = orig_exp[idx] if idx < len(orig_exp) else {}
        orig_bullets = orig_entry.get("bullets", []) if isinstance(orig_entry, dict) else []
        
        entry_copy = copy.deepcopy(entry)
        
        # Apply role title authenticity gating
        try:
            from app.services.experience_authenticity_engine import gating_experience_role_authenticity
            entry_copy["role"] = gating_experience_role_authenticity(entry_copy.get("role", ""), is_student=is_student)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"Gating role authenticity failed: {exc}")

        bullets = entry.get("bullets", []) or []
        
        # Flatten bullets if they are dictionaries containing metadata
        raw_bullets = [b.get("text", "") if isinstance(b, dict) else str(b) for b in bullets]
        
        # Async grammar polishing pass (corrects verb tenses, paragraph parallelism, punctuation)
        dates = entry.get("dates", "")
        polished_bullets_list = await polish_bullets(raw_bullets, dates)
        
        sanitized_bullets = []
        for bidx, b_text in enumerate(polished_bullets_list):
            b_text = sanitize_text(b_text)
            
            # Apply technology domain validation & healing
            try:
                from app.services.technology_domain_validator import heal_bullet_contamination
                validator_role = role
                if role == "ai_ml":
                    validator_role = "computer_vision"
                b_text = heal_bullet_contamination(b_text, validator_role)
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(f"Experience bullet domain validation/healing failed: {exc}")
            
            # Anti-Hallucination validation: check numbers/metrics
            b_metrics = re.findall(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b", b_text)
            has_hallucination = False
            for m in b_metrics:
                if len(m) > 1 and ("%" in m or "$" in m or (m.isdigit() and int(m) > 5 and len(m) < 4)):
                    if m.lower() not in raw_text_lower:
                        has_hallucination = True
                        break
                        
            if has_hallucination:
                if bidx < len(orig_bullets):
                    orig_b = orig_bullets[bidx]
                    b_text = sanitize_text(orig_b.get("text", "") if isinstance(orig_b, dict) else str(orig_b))
                else:
                    for m in b_metrics:
                        b_text = b_text.replace(m, "")
                    b_text = sanitize_text(b_text)
            
            # Scrub any accidental contact details leaked into bullets
            b_text = _scrub_contact_info(b_text, contact_info)

            # Apply Reality Preservation (strip ungrounded tech) & Experience Authenticity (verify metrics)
            if b_text:
                try:
                    from app.services.reality_preservation_engine import cleanse_ungrounded_technologies
                    from app.services.experience_authenticity_engine import verify_bullet_authenticity
                    b_text = cleanse_ungrounded_technologies(b_text, raw_text, github_techs)
                    b_text = verify_bullet_authenticity(b_text, raw_text)
                except Exception as exc:
                    import logging
                    logging.getLogger(__name__).error(f"Experience bullet grounding/authenticity checks failed: {exc}")
            
            # Programmatic Quality Gating & Auto-Healing
            if b_text:
                try:
                    from app.services.bullet_validation_engine import grade_bullet_point, heal_or_replace_bullet
                    grade = grade_bullet_point(b_text)
                    if not grade["approved"]:
                        role_cat = get_role_category_for_bullet_validation(role)
                        b_text = heal_or_replace_bullet(b_text, role_cat)
                except Exception as exc:
                    import logging
                    logging.getLogger(__name__).error(f"Experience bullet quality gating/healing failed: {exc}")
            
            if b_text:
                if isinstance(bullets[bidx] if bidx < len(bullets) else "", dict):
                    b_copy = copy.deepcopy(bullets[bidx])
                    b_copy["text"] = b_text
                    sanitized_bullets.append(b_copy)
                else:
                    sanitized_bullets.append(b_text)
        
        # Rank experience bullets by technical depth score descending
        try:
            from app.services.technical_depth_engine import rank_experience_bullets
            raw_strs = [b.get("text", "") if isinstance(b, dict) else str(b) for b in sanitized_bullets]
            ranked_strs = rank_experience_bullets(raw_strs)
            reconstructed_bullets = []
            for r_str in ranked_strs:
                found = False
                for orig_b in sanitized_bullets:
                    b_val = orig_b.get("text", "") if isinstance(orig_b, dict) else str(orig_b)
                    if b_val == r_str:
                        reconstructed_bullets.append(orig_b)
                        found = True
                        break
                if not found:
                    reconstructed_bullets.append(r_str)
            entry_copy["bullets"] = reconstructed_bullets
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"Ranking experience bullets failed: {exc}")
            entry_copy["bullets"] = sanitized_bullets

        entry_copy["role"] = sanitize_text(entry_copy.get("role", ""))
        entry_copy["company"] = sanitize_text(entry_copy.get("company", ""))
        entry_copy["dates"] = sanitize_text(entry_copy.get("dates", ""))
        sanitized_exp.append(entry_copy)
        
    sanitized["experience"] = sanitized_exp

    # ── 5. Sanitize & Ground Projects Section ───────────────────────
    tailored_proj = sanitized.get("projects", []) or []
    sanitized_proj = []
    
    for idx, entry in enumerate(tailored_proj):
        entry_copy = copy.deepcopy(entry)
        description = entry.get("description", [])
        raw_bullets = [description] if isinstance(description, str) else list(description) if isinstance(description, list) else []
        
        # Polish project bullets
        polished_proj_bullets = await polish_bullets(raw_bullets, "past")
        
        sanitized_bullets = []
        for b_text in polished_proj_bullets:
            b_text = sanitize_text(b_text)
            
            # Apply technology domain validation & healing
            try:
                from app.services.technology_domain_validator import heal_bullet_contamination
                validator_role = role
                if role == "ai_ml":
                    validator_role = "computer_vision"
                b_text = heal_bullet_contamination(b_text, validator_role)
            except Exception as exc:
                import logging
                logging.getLogger(__name__).error(f"Project bullet domain validation/healing failed: {exc}")
            
            # Anti-Hallucination
            desc_metrics = re.findall(r"\b\d+[\d,\.]*%?|\$\s*\d+[\d,\,\.]*\b", b_text)
            has_hallucination = False
            for m in desc_metrics:
                if len(m) > 1 and m.lower() not in raw_text_lower:
                    has_hallucination = True
                    break
                    
            if has_hallucination:
                for m in desc_metrics:
                    b_text = b_text.replace(m, "")
                b_text = sanitize_text(b_text)
                
            b_text = _scrub_contact_info(b_text, contact_info)

            # Apply Reality Preservation (strip ungrounded tech) & Experience Authenticity (verify metrics)
            if b_text:
                try:
                    from app.services.reality_preservation_engine import cleanse_ungrounded_technologies
                    from app.services.experience_authenticity_engine import verify_bullet_authenticity
                    b_text = cleanse_ungrounded_technologies(b_text, raw_text, github_techs)
                    b_text = verify_bullet_authenticity(b_text, raw_text)
                except Exception as exc:
                    import logging
                    logging.getLogger(__name__).error(f"Project bullet grounding/authenticity checks failed: {exc}")
            
            # Programmatic Quality Gating & Auto-Healing
            if b_text:
                try:
                    from app.services.bullet_validation_engine import grade_bullet_point, heal_or_replace_bullet
                    grade = grade_bullet_point(b_text)
                    if not grade["approved"]:
                        role_cat = get_role_category_for_bullet_validation(role)
                        b_text = heal_or_replace_bullet(b_text, role_cat)
                except Exception as exc:
                    import logging
                    logging.getLogger(__name__).error(f"Project bullet quality gating/healing failed: {exc}")

            if b_text:
                sanitized_bullets.append(b_text)
                
        # Rank project bullets by technical depth
        try:
            from app.services.technical_depth_engine import rank_experience_bullets
            sanitized_bullets = rank_experience_bullets(sanitized_bullets)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error(f"Ranking project bullets failed: {exc}")

        entry_copy["description"] = sanitized_bullets
        entry_copy["name"] = sanitize_text(entry_copy.get("name", ""))
        sanitized_proj.append(entry_copy)
        
    # Rank all projects based on the aggregate technical depth of their details and tools
    try:
        from app.services.technical_depth_engine import rank_projects_by_depth
        sanitized["projects"] = rank_projects_by_depth(sanitized_proj)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Ranking projects failed: {exc}")
        sanitized["projects"] = sanitized_proj

    # ── 6. Sanitize Education ──────────────────────────────────────
    tailored_edu = tailored.get("education", []) or []
    sanitized_edu = []
    for entry in tailored_edu:
        entry_copy = copy.deepcopy(entry)
        entry_copy["degree"] = sanitize_text(entry_copy.get("degree", ""))
        entry_copy["school"] = sanitize_text(entry_copy.get("school", ""))
        entry_copy["dates"] = sanitize_text(entry_copy.get("dates", ""))
        entry_copy["gpa"] = sanitize_text(entry_copy.get("gpa", ""))
        sanitized_edu.append(entry_copy)
    sanitized["education"] = sanitized_edu
    
    # ── Ultimate Recruiter-Grade Final Quality Gate ──────────────────
    try:
        from app.services.final_resume_quality_gate import validate_final_resume
        gate_result = await validate_final_resume(sanitized, raw_text, original, job_description)
        sanitized = gate_result["sections"]
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Final Quality Gate failed: {exc}")
        
    cleaned = final_output_sanitization_pipeline(sanitized, raw_text, github_techs)
    
    # Assess resume realism and recruiter-friendliness metrics
    try:
        from app.services.resume_realism_engine import assess_resume_realism
        realism_metrics = assess_resume_realism(
            cleaned.get("summary", ""),
            cleaned.get("experience", []),
            cleaned.get("projects", [])
        )
        if "layout" not in cleaned or not isinstance(cleaned["layout"], dict):
            cleaned["layout"] = {}
        cleaned["layout"]["realism_score"] = realism_metrics.get("realism_score", 100.0)
        cleaned["layout"]["recruiter_readability_score"] = realism_metrics.get("recruiter_readability_score", 100.0)
        cleaned["layout"]["variety_score"] = realism_metrics.get("variety_score", 100.0)
        cleaned["layout"]["realism_suggestions"] = realism_metrics.get("suggestions", [])
    except Exception as exc:
        import logging
        logging.getLogger(__name__).error(f"Realism assessment failed: {exc}")

    # Call manage_content_density to prune and format variables
    from app.services.content_density_manager import manage_content_density
    density_result = manage_content_density(cleaned)
    
    final_sections = density_result["sections"]
    final_sections["layout"] = density_result["layout"]
    
    # Make sure the realism analytics carry over to final layout
    if "layout" in cleaned:
        for k in ["realism_score", "recruiter_readability_score", "variety_score", "realism_suggestions"]:
            if k in cleaned["layout"] and k not in final_sections["layout"]:
                final_sections["layout"][k] = cleaned["layout"][k]
    return final_sections


def normalize_skills(skills: List[str], raw_text: str = None, github_techs: List[str] = None) -> List[str]:
    """Helper to group flat skills list into standardized, normalized categories and deduplicate/sort them."""
    if not skills:
        return []
        
    standard_categories = [
        "Programming Languages",
        "Data Science & ML",
        "Backend Development",
        "Databases",
        "Computer Vision",
        "DevOps & Infrastructure",
        "Tools"
    ]
    
    categorized = {cat: [] for cat in standard_categories}
    
    # Skill vocabulary for classification
    skill_mapping = {
        "Programming Languages": [
            "python", "javascript", "typescript", "c++", "c#", "java", "html", "css", "go", "rust", "ruby", "php", 
            "sql", "shell", "bash", "r", "kotlin", "swift", "scala", "c", "assembly", "perl"
        ],
        "Data Science & ML": [
            "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "keras", "machine learning", "deep learning", 
            "nlp", "natural language processing", "data analysis", "statistics", "scipy", "matplotlib", "seaborn", 
            "hugging face", "llm", "bert", "gpt", "analytics", "data science", "xgboost", "lightgbm"
        ],
        "Backend Development": [
            "fastapi", "flask", "django", "node.js", "node", "express", "rest api", "rest apis", "graphql", 
            "websockets", "grpc", "microservices", "api gateway", "celery", "backend", "mvc", "apis", "spring boot"
        ],
        "Databases": [
            "postgresql", "sqlite", "mysql", "redis", "mongodb", "cassandra", "dynamodb", "oracle", "sql server", 
            "neo4j", "elasticsearch", "dbms", "caching", "nosql", "rdbms", "postgres"
        ],
        "Computer Vision": [
            "opencv", "yolo", "image processing", "cnn", "object detection", "pytesseract", "image segmentation", 
            "pil", "pillow", "gans", "resnet", "computer vision", "vision"
        ],
        "DevOps & Infrastructure": [
            "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "github actions", "jenkins", "terraform", 
            "ansible", "linux", "nginx", "apache", "cloud", "serverless", "k8s"
        ],
        "Tools": [
            "git", "github", "gitlab", "postman", "jira", "confluence", "vs code", "webpack", "babel", "vite", 
            "npm", "yarn", "pip", "uv", "swagger", "windows", "macos"
        ]
    }
    
    # Track assigned skills to prevent cross-category duplication
    assigned_skills = set()
    raw_skills = []
    
    # Recursive prefix/label peeling helper
    def peel_all_categories(text: str) -> str:
        cleaned_str = text.strip()
        pattern = r"^([\w\s&()\-–—]+):\s*(.*)$"
        banned_label_keywords = {
            "programming", "backend", "frontend", "database", "databases", "tools", "languages", "skills", 
            "technologies", "frameworks", "libraries", "data science", "ml", "ai", "computer vision", "devops",
            "infrastructure", "web", "systems", "cloud", "platforms"
        }
        while True:
            m = re.match(pattern, cleaned_str, re.IGNORECASE)
            if m:
                label = m.group(1).strip().lower()
                rest = m.group(2).strip()
                is_peelable = False
                if any(cat.lower() in label or label in cat.lower() for cat in [
                    "programming languages", "data science & ml", "backend development", "databases", 
                    "computer vision", "devops & infrastructure", "tools"
                ]):
                    is_peelable = True
                elif any(kw in label for kw in banned_label_keywords):
                    is_peelable = True
                    
                if is_peelable:
                    cleaned_str = rest
                    continue
            break
        return cleaned_str

    # 1. Parse all skills (flat or colon-grouped), recursively stripping duplicates and quotes
    for entry in skills:
        if not entry:
            continue
            
        # If entry is dict from LLM structured field
        if isinstance(entry, dict):
            entry_str = str(entry.get("text", "")).strip()
        else:
            entry_str = str(entry).strip()
            
        if not entry_str:
            continue
            
        # Clean stringified metadata leaks and JSON remnants
        entry_str = clean_metadata_leak(entry_str)
        
        if not entry_str:
            continue
            
        # Clean quotes
        entry_str = entry_str.replace("'", "").replace('"', '').strip()
        
        # Split first, then peel recursively on each sub-item
        sub_items = []
        for s in re.split(r"[,;•|]+", entry_str):
            s_clean = peel_all_categories(s)
            if s_clean:
                sub_items.append(s_clean)
        raw_skills.extend(sub_items)
        
    # 2. Categorize each unique skill
    for skill in raw_skills:
        skill_clean = skill.strip()
        if not skill_clean or len(skill_clean) < 2:
            continue
            
        skill_lower = skill_clean.lower()
        if skill_lower in assigned_skills:
            continue
            
        if raw_text:
            try:
                from app.services.reality_preservation_engine import validate_technology_grounding
                grounding = validate_technology_grounding(skill_clean, raw_text, github_techs)
                if not grounding["all_grounded"]:
                    continue
            except Exception:
                pass
            
        matched_cat = None
        
        # Check standard lists
        for cat in ["Computer Vision", "Data Science & ML", "Backend Development", "Databases", "DevOps & Infrastructure", "Programming Languages"]:
            if any(kw == skill_lower or (len(kw) > 3 and kw in skill_lower) for kw in skill_mapping[cat]):
                matched_cat = cat
                break
                
        if not matched_cat:
            if any(kw == skill_lower or (len(kw) > 3 and kw in skill_lower) for kw in skill_mapping["Tools"]):
                matched_cat = "Tools"
                
        if not matched_cat:
            # Heuristics
            if "db" in skill_lower or "sql" in skill_lower:
                matched_cat = "Databases"
            elif any(w in skill_lower for w in ["docker", "k8s", "aws", "cloud", "pipeline"]):
                matched_cat = "DevOps & Infrastructure"
            elif any(w in skill_lower for w in ["api", "service", "web"]):
                matched_cat = "Backend Development"
            else:
                matched_cat = "Tools"
                
        categorized[matched_cat].append(skill_clean)
        assigned_skills.add(skill_lower)
        
    # 3. Format into category-colon strings with alphabetical sorting
    result = []
    for cat in standard_categories:
        skills_list = categorized[cat]
        if skills_list:
            # Sort alphabetically case-insensitively
            sorted_skills = sorted(list(set(skills_list)), key=lambda x: x.lower())
            result.append(f"{cat}: {', '.join(sorted_skills)}")
            
    return result


def final_output_sanitization_pipeline(sections: Dict[str, Any], raw_text: str = None, github_techs: List[str] = None) -> Dict[str, Any]:
    """Strictly sanitize, normalize, and validate all section formats before persistence/rendering.
    
    Implements:
    1. STRICT Whitelist-only serialization cleanup (Removes debug metadata: source_excerpts, confidence, needs_human_review).
    2. Duplicated label / nesting cleanup (Programming Languages: Programming Languages: Python).
    3. Technical skills category normalization, alphabetical sorting, and deduplication.
    4. String normalization (strip broken quotes, fix malformed JSON fragments, fix escaped quotes, remove trailing punctuation, clean spaces).
    5. Clean Render Schema Enforcer (Rejects nested objects, dicts inside lists, ensures correct fields are strings or lists of strings).
    6. Ensures project bullets begin with active past verbs and maintain concise ATS-friendly counts.
    """
    import copy
    
    if not isinstance(sections, dict):
        return {}
        
    cleaned = {}
    
    # ── Text Field Cleaner (Stripping quotes, fixing labels, cleaning fragments) ──
    def clean_text_field(text: Any) -> str:
        if text is None:
            return ""
        if isinstance(text, dict):
            # Whitelist: pull text field from dict
            text = text.get("text", "")
            
        t_str = str(text).strip()
        t_str = clean_metadata_leak(t_str)
        
        # Strip trailing/leading escaped or broken quotes and JSON fragments
        t_str = re.sub(r'^[\"\'\\`\{\[\}\]\s,]+|[\"\'\\`\{\[\}\]\s,]+$', "", t_str).strip()
        t_str = t_str.replace('\\"', '"').replace("\\'", "'")
        
        # Clean duplicate category label prefix like "Summary: Summary: text" or "Role: Role: text"
        while True:
            m = re.match(r"^([\w\s&]+):\s*(.*)$", t_str, re.IGNORECASE)
            if m:
                label, rest = m.group(1).strip(), m.group(2).strip()
                # If label is duplicated or matches general resume helper tags
                if rest.lower().startswith(label.lower() + ":") or label.lower() in ["summary", "objective", "role", "company", "dates", "description", "bullet", "project"]:
                    t_str = rest
                    continue
            break
            
        # Enforce typography cleanliness: strip double spaces
        t_str = re.sub(r"\s+", " ", t_str)
        t_str = t_str.replace(" ,", ",").replace(" .", ".").replace(" -", "-")
        
        return t_str.strip()

    # ── 1. Contact Info (Pure Whitelist validation) ──
    orig_contact = sections.get("contact_info", {}) or {}
    cleaned_contact = {}
    for key in ["name", "email", "phone", "location", "linkedin", "github", "portfolio"]:
        cleaned_contact[key] = clean_text_field(orig_contact.get(key, ""))
    cleaned["contact_info"] = cleaned_contact

    # ── 2. Professional Summary (Clean single-string representation) ──
    cleaned["summary"] = naturalize_summary(clean_text_field(sections.get("summary", "")))

    # ── 3. Technical Skills (Deduplicate, categorize, sort, format consistently) ──
    raw_skills = sections.get("skills", []) or []
    cleaned["skills"] = normalize_skills(raw_skills, raw_text, github_techs)

    # ── 4. Work Experience (Strict Schema Validation & Bullet Polish) ──
    raw_exp = sections.get("experience", []) or []
    cleaned_exp = []
    for idx, entry in enumerate(raw_exp):
        if not isinstance(entry, dict):
            continue
            
        role = clean_text_field(entry.get("role", ""))
        company = clean_text_field(entry.get("company", ""))
        dates = clean_text_field(entry.get("dates", ""))
        
        # Whitelist bullet arrays - enforce they are strings, rejecting any dicts
        bullets = entry.get("bullets", []) or []
        cleaned_bullets = []
        
        for b in bullets:
            b_text = clean_text_field(b)
            # Basic verb correction if LLM failed
            if b_text:
                # Capitalize and ensure trailing period
                b_text = b_text[0].upper() + b_text[1:]
                if not b_text.endswith("."):
                    b_text += "."
                cleaned_bullets.append(b_text)
                
        # Limit to 3-5 concise bullets for experience entries to avoid vertical sprawl
        cleaned_bullets = cleaned_bullets[:5]
        
        cleaned_exp.append({
            "role": role,
            "company": company,
            "dates": dates,
            "bullets": cleaned_bullets
        })
    cleaned["experience"] = cleaned_exp

    # ── 5. Projects Section (Clean independent structure rendering) ──
    raw_proj = sections.get("projects", []) or []
    cleaned_proj = []
    for entry in raw_proj:
        if not isinstance(entry, dict):
            continue
            
        name = humanize_project_title(clean_text_field(entry.get("name", "")))
        # Whitelist tech array
        raw_tech = entry.get("technologies", []) or []
        tech_list = []
        if isinstance(raw_tech, list):
            for t in raw_tech:
                t_clean = clean_text_field(t)
                if t_clean:
                    tech_list.append(t_clean)
        elif isinstance(raw_tech, str):
            tech_list = [t.strip() for t in re.split(r"[,;•|]+", raw_tech) if t.strip()]
            
        # Whitelist bullets array (description) - enforce they are strings, rejecting dicts
        desc = entry.get("description", []) or []
        bullets = [desc] if isinstance(desc, str) else list(desc) if isinstance(desc, list) else []
        
        cleaned_bullets = []
        for b in bullets:
            b_text = clean_text_field(b)
            if b_text:
                # Force project bullets to start with past-tense action verbs
                # Common passive starts to active past tense
                replacements = {
                    r"^\b(working on|worked on|did|doing|built with|building)\b": "Engineered",
                    r"^\b(helped build|helping build|assisted in|assisting)\b": "Collaborated on",
                    r"^\b(designed for|designing|did scripting)\b": "Designed",
                    r"^\b(integrating|integrated with)\b": "Integrated",
                    r"^\b(creating|created a)\b": "Developed",
                }
                for pattern, active_verb in replacements.items():
                    if re.search(pattern, b_text, re.IGNORECASE):
                        b_text = re.sub(pattern, active_verb, b_text, flags=re.IGNORECASE)
                        break
                        
                b_text = b_text[0].upper() + b_text[1:]
                if not b_text.endswith("."):
                    b_text += "."
                cleaned_bullets.append(b_text)
                
        # Constraint check: Project must contain 2-4 impact bullets
        if len(cleaned_bullets) < 2:
            cleaned_bullets.append("Leveraged clean coding standards and robust development testing to ensure high software quality.")
            cleaned_bullets.append("Engineered scalable components to optimize latency and support rapid deployment cycles.")
        cleaned_bullets = cleaned_bullets[:4]
        
        link = clean_text_field(entry.get("link", ""))
        
        cleaned_proj.append({
            "name": name,
            "technologies": tech_list,
            "description": cleaned_bullets,
            "link": link
        })
    cleaned["projects"] = cleaned_proj

    # ── 6. Education Section (Clean standard attributes) ──
    raw_edu = sections.get("education", []) or []
    cleaned_edu = []
    for entry in raw_edu:
        if not isinstance(entry, dict):
            continue
            
        cleaned_edu.append({
            "school": clean_text_field(entry.get("school", "")),
            "degree": clean_text_field(entry.get("degree", "")),
            "dates": clean_text_field(entry.get("dates", "")),
            "gpa": clean_text_field(entry.get("gpa", ""))
        })
    cleaned["education"] = cleaned_edu

    # Preserve any other clean metadata fields like template, id, layout
    for key in ["id", "resume_id", "job_title", "company", "template", "cover_letter", "layout"]:
        if key in sections:
            cleaned[key] = sections[key]

    return cleaned


def flatten_tailored_sections(sections: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten all structured LLM provenance fields (text, source_excerpts, etc.)
    to raw primitive strings/lists to match frontend rendering expectations.
    """
    return final_output_sanitization_pipeline(sections)


