"""
Text processing and cleaning utilities.
"""

import re
import unicodedata


def clean_text(text: str) -> str:
    """Clean and normalize extracted raw text from PDF/DOCX files.

    Removes excessive whitespace, normalizes quotes and hyphens, and handles
    encoding artifacts.

    Args:
        text: The raw input string.

    Returns:
        The normalized and cleaned text string.
    """
    if not text:
        return ""

    # Normalize unicode characters (NFKC format decomposes compatible characters)
    text = unicodedata.normalize("NFKC", text)

    # Normalize quotes, dashes, and bullet points
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # smart double quotes
    text = text.replace("\u2018", "'").replace("\u2019", "'")  # smart single quotes
    text = text.replace("\u2013", "-").replace("\u2014", "-")  # en and em dashes
    text = text.replace("\u2022", "•").replace("\u00b7", "•")  # bullet points

    # Clean up CID font artifacts (e.g. (cid:127)) left by some PDF parsers
    text = re.sub(r"\(cid:\d+\)", "", text)

    # Replace windows line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace multiple spaces with a single space, but preserve single linebreaks
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive consecutive linebreaks to maximum of two (for paragraph split)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def heal_bullet_text(prev: str, current: str) -> str:
    """Heal line breaks and hyphen splits between wrapped bullet lines.

    Args:
        prev: The previous bullet text segment.
        current: The current text segment to join.

    Returns:
        A merged and normalized single line.
    """
    prev = prev.strip()
    current = current.strip()
    if not prev:
        return current
    if not current:
        return prev

    # Handle word breaks split by hyphens (e.g., HR- \n integrated or develop- \n ment)
    if prev.endswith("-"):
        # Split into words to check the prefix before hyphen
        words = prev.split()
        if words:
            word_before = words[-1][:-1]  # strip the hyphen
            # Keep hyphen for common prefixes or short prefixes
            common_prefixes = {"co", "pre", "re", "hr", "non", "cross", "data", "scale", "self", "multi", "meta"}
            if word_before.lower() in common_prefixes or len(word_before) <= 3:
                return prev + current
            else:
                # Word break: merge without hyphen (e.g., develop- ment -> development)
                return prev[:-1] + current

    # Standard space join
    return prev + " " + current



def extract_emails(text: str) -> list[str]:
    """Extract all email addresses from a string.

    Args:
        text: Input string.

    Returns:
        List of email strings found.
    """
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def extract_phones(text: str) -> list[str]:
    """Extract standard phone numbers from a string.

    Handles standard international and domestic formats.

    Args:
        text: Input string.

    Returns:
        List of matching phone number strings.
    """
    # Pattern matching most standard format variations: +1 123-456-7890, (123) 456-7890, etc.
    pattern = r"(?:\+?\d{1,3}[ -]?)?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list[str]:
    """Extract URLs (specifically LinkedIn, GitHub, and portfolios) from a string.

    Args:
        text: Input string.

    Returns:
        List of URL strings.
    """
    # Simple regex for finding links
    pattern = r"(?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    urls = re.findall(pattern, text)
    # Filter for interesting sites
    target_urls = []
    for url in urls:
        url_lower = url.lower()
        if "linkedin.com" in url_lower or "github.com" in url_lower or "gitlab.com" in url_lower or "portfolio" in url_lower:
            target_urls.append(url)
    return target_urls
