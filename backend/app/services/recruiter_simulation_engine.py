"""
Recruiter Simulation Engine.
Simulates a recruiter's 6-second glance, predicting visual hierarchy, whitespace distribution,
and eye-tracking coordinates for metrics and role headers.
"""

import re
from typing import Dict, Any, List


def simulate_recruiter_scan(sections: Dict[str, Any], job_description: str = "") -> Dict[str, Any]:
    """Generates eye-tracking simulated heat-map zones, readability scores, and visual prominence metrics."""
    if not sections:
        return _get_empty_simulation()

    heatmap_points = []
    total_metrics = 0
    readability_warnings = []
    
    # 1. SCAN FOR HIGH-FOCUS METRICS & HEADERS (recruiter eye-tracking anchors)
    summary = sections.get("summary", "")
    if summary and isinstance(summary, str):
        # High-focus coordinates represent mock canvas placement grids (x/y percent scale)
        metrics = re.findall(r"\b\d+%\b|\$\d+k\b", summary)
        if metrics:
            heatmap_points.append({
                "text": metrics[0],
                "focus_score": 85,
                "reason": "Quantifiable metric in summary",
                "x_percent": 30,
                "y_percent": 15
            })
            total_metrics += len(metrics)

    # Experience Scan
    for exp_idx, exp in enumerate(sections.get("experience", []) or []):
        if not isinstance(exp, dict):
            continue
            
        role = exp.get("role", "")
        company = exp.get("company", "")
        
        # Role titles draw instant eye focus
        y_pos = 25 + (exp_idx * 15)
        heatmap_points.append({
            "text": f"{role} at {company}",
            "focus_score": 90,
            "reason": "Employment role header",
            "x_percent": 15,
            "y_percent": y_pos
        })
        
        for bullet in exp.get("bullets", []) or []:
            b_str = bullet.get("text", "") if isinstance(bullet, dict) else str(bullet)
            # Find metrics in experience bullets
            bullet_metrics = re.findall(r"\b\d+%\b|\$\d+k\b|\b\d+\+\b", b_str)
            for m in bullet_metrics:
                heatmap_points.append({
                    "text": m,
                    "focus_score": 95,
                    "reason": "Quantified accomplishment metrics",
                    "x_percent": 50,
                    "y_percent": y_pos + 3
                })
                total_metrics += 1

    # 2. Evaluate Visual Hierarchy & Spacing Heuristics
    whitespace_score = 85.0
    if len(heatmap_points) > 15:
        whitespace_score = 65.0  # Too dense
        readability_warnings.append("Text layout is extremely dense, potentially degrading recruiter scanning flow.")
    elif len(heatmap_points) < 4:
        whitespace_score = 95.0
        readability_warnings.append("Page layout feels sparse. Consider expanding detail matrices.")

    # 3. Calculate Overall Readability & Trust
    scan_score = 60.0
    if total_metrics >= 3:
        scan_score += 25.0
    elif total_metrics >= 1:
        scan_score += 15.0
        
    if whitespace_score >= 80.0:
        scan_score += 10.0
        
    final_scan_score = min(99.0, max(40.0, scan_score))

    return {
        "recruiter_readability_score": round(final_scan_score, 2),
        "whitespace_balance_score": whitespace_score,
        "total_metric_anchors": total_metrics,
        "heatmap_points": heatmap_points[:10],  # Return top 10 focal nodes
        "readability_warnings": readability_warnings
    }


def _get_empty_simulation() -> Dict[str, Any]:
    """Default empty recruiter scan payload."""
    return {
        "recruiter_readability_score": 50.0,
        "whitespace_balance_score": 75.0,
        "total_metric_anchors": 0,
        "heatmap_points": [],
        "readability_warnings": ["No sections provided for analysis."]
    }
