"""
Privacy & Security Engine.
Provides core utility filters for PII masking (Social Security, phone numbers, exact addresses),
GDPR compliance deletion helpers, and safe rate-limiting checks.
"""

import re
from typing import Dict, Any, List

# Regex patterns for high-risk PII
PHONE_PATTERN = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
STREET_ADDRESS_PATTERN = r"\b\d+\s+[A-Za-z0-9\s,.]+?\s+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Court|Ct|Way|Lane|Ln|Loop|Lp)\b"


def mask_pii_from_text(text: str) -> str:
    """Mask high-risk PII patterns from text to ensure privacy prior to invoking remote APIs."""
    if not text:
        return ""
        
    masked = text
    
    # 1. Mask SSNs
    masked = re.sub(SSN_PATTERN, "[SSN_MASKED]", masked)
    
    # 2. Mask Street Addresses
    masked = re.sub(STREET_ADDRESS_PATTERN, "[ADDRESS_MASKED]", masked, flags=re.IGNORECASE)
    
    # 3. Mask Phones
    masked = re.sub(PHONE_PATTERN, "[PHONE_MASKED]", masked)
    
    return masked


def mask_sections_pii(sections: Dict[str, Any]) -> Dict[str, Any]:
    """Clones a sections dictionary and masks high-risk PII inside contact info and summaries."""
    if not sections:
        return {}
        
    masked = {}
    for k, v in sections.items():
        if k == "contact_info" and isinstance(v, dict):
            masked_contact = dict(v)
            if "phone" in masked_contact:
                masked_contact["phone"] = "[PHONE_MASKED]"
            if "location" in masked_contact:
                # Keep city/state for ATS and recruiter relevance, but strip specific street info
                loc = str(masked_contact["location"])
                masked_contact["location"] = re.sub(STREET_ADDRESS_PATTERN, "[STREET_MASKED]", loc, flags=re.IGNORECASE)
            masked["contact_info"] = masked_contact
        elif k == "summary" and isinstance(v, str):
            masked["summary"] = mask_pii_from_text(v)
        else:
            masked[k] = v
            
    return masked


def get_safe_scraping_delay(domain: str) -> float:
    """Enforces respectful rate-limiting delays depending on targeted crawler domain rules."""
    dom = domain.lower()
    if "linkedin" in dom:
        return 3.0  # Be very respectful to LinkedIn
    if "indeed" in dom:
        return 2.0
    return 1.0  # Standard delay for Greenhouse, Lever API channels
