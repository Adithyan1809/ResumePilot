"""
Cache Engine.
High-speed, persistent, TTL-supported local cache store.
Caches scraped job details, embeddings, ATS metrics, and recruiter review results.
"""

import os
import json
import time
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

CACHE_FILE = "uploads/cache_store.json"


class LocalCache:
    """Standard, thread-safe persistent cache engine utilizing local JSON serialization."""

    def __init__(self):
        self.store = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache store from disk."""
        if not os.path.exists(CACHE_FILE):
            self.store = {}
            return
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                self.store = json.load(f)
        except Exception as exc:
            logger.warning(f"Failed to load local cache file: {exc}. Starting fresh.")
            self.store = {}

    def _save_cache(self):
        """Persist cache store to disk."""
        try:
            # Ensure upload directory exists
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.store, f, indent=2)
        except Exception as exc:
            logger.error(f"Failed to save local cache file: {exc}")

    def get(self, key: str) -> Optional[Any]:
        """Fetch a value from cache, enforcing TTL expirations."""
        if key not in self.store:
            return None
        
        entry = self.store[key]
        expire_time = entry.get("expire_time", 0)
        
        # Check if expired
        if expire_time > 0 and time.time() > expire_time:
            self.delete(key)
            return None
            
        return entry.get("value")

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Stores a value in cache with a configurable TTL (default 1 hour)."""
        expire_time = time.time() + ttl if ttl > 0 else 0
        self.store[key] = {
            "value": value,
            "expire_time": expire_time
        }
        self._save_cache()

    def delete(self, key: str):
        """Remove an item from the cache."""
        if key in self.store:
            del self.store[key]
            self._save_cache()

    def clear(self):
        """Clear all entries in the cache."""
        self.store = {}
        self._save_cache()


# Global Singleton instance
cache = LocalCache()


def get_cache(key: str) -> Optional[Any]:
    """Helper shortcut function to load cache values."""
    return cache.get(key)


def set_cache(key: str, value: Any, ttl: int = 3600):
    """Helper shortcut function to store cache values."""
    cache.set(key, value, ttl)
