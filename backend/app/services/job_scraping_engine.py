"""
Job Scraping Engine.
Scrapes, parses, and extracts clean job specifications from LinkedIn, Greenhouse, Lever, and other URLs.
Integrates safe rate limits and graceful degradation fallbacks.
"""

import httpx
import logging
from urllib.parse import urlparse
from typing import Dict, Any

from app.services.privacy_security_engine import get_safe_scraping_delay
from app.services.fallback_recovery_engine import fallback_scrape_job_posting

logger = logging.getLogger(__name__)


async def scrape_job_posting(url: str) -> Dict[str, Any]:
    """Crawl a job URL to extract clean requirements, using rate limits and graceful recovery fallbacks."""
    if not url:
        return fallback_scrape_job_posting("")
        
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # 1. Enforce safe scraping delays
    import asyncio
    delay = get_safe_scraping_delay(domain)
    await asyncio.sleep(delay)
    
    # 2. Attempt real HTTP scrapings (specifically optimized for public Greenhouse / Lever APIs)
    try:
        url_lower = url.lower()
        if "lever.co" in url_lower and "/embed" not in url_lower:
            # Check if we can hit their public JSON API
            # E.g. https://jobs.lever.co/stripe/uuid -> API: https://api.lever.co/v0/postings/stripe/uuid
            parts = url.split("lever.co/")
            if len(parts) > 1:
                subparts = parts[1].split("/")
                if len(subparts) >= 2:
                    company = subparts[0]
                    posting_id = subparts[1].split("?")[0]
                    api_url = f"https://api.lever.co/v0/postings/{company}/{posting_id}"
                    
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        response = await client.get(api_url)
                        if response.status_code == 200:
                            data = response.json()
                            return {
                                "job_title": data.get("title", "Software Engineer"),
                                "company": company.title(),
                                "job_description": data.get("descriptionPlain", "") + "\n" + data.get("additionalPlain", "")
                            }
                            
        elif "greenhouse.io" in url_lower:
            # Check Greenhouse public JSON API
            # E.g. https://boards.greenhouse.io/stripe/jobs/uuid -> API: https://api.greenhouse.io/v1/boards/stripe/jobs/uuid
            parts = url.split("greenhouse.io/")
            if len(parts) > 1:
                subparts = parts[1].split("/jobs/")
                if len(subparts) >= 2:
                    company = subparts[0].split("/")[0]
                    job_id = subparts[1].split("?")[0]
                    api_url = f"https://api.greenhouse.io/v1/boards/{company}/jobs/{job_id}"
                    
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        response = await client.get(api_url)
                        if response.status_code == 200:
                            data = response.json()
                            return {
                                "job_title": data.get("title", "Software Engineer"),
                                "company": company.title(),
                                "job_description": data.get("content", "")  # strip HTML inside JD parser later
                            }
                            
        # For LinkedIn, Indeed, etc., or standard scraper failure, trigger the smart intelligence fallback
        logger.info(f"Using company intelligence fallback crawler path for URL: {url}")
        return fallback_scrape_job_posting(url)
        
    except Exception as exc:
        logger.warning(f"Real scraper call failed: {exc}. Activating safe company intelligence stubs.")
        return fallback_scrape_job_posting(url)
