import re

EXAGGERATED_KEYWORDS = {
    r"\bglobal enterprise\b": "software systems",
    r"\bmulti-region AWS\b": "cloud deployment",
    r"\b10M\+\s*(?:active\s*)?users\b": "optimized endpoints",
    r"\bmillion(?:s of)?\s*(?:active\s*)?users\b": "high-concurrency systems",
    r"\bVP of Engineering\b": "Software Engineering Intern",
    r"\bdivision budgets\b": "project components",
    r"\barchitected global\b": "optimized modular",
}

bullet = "Architected multi-region AWS cloud deployments supporting 10M+ active users."
print("Bullet:", bullet)

for pattern in EXAGGERATED_KEYWORDS.keys():
    match = re.search(pattern, bullet, flags=re.IGNORECASE)
    print(f"Pattern '{pattern}': matched =", bool(match))
    if match:
        print("  Group:", match.group(0))
