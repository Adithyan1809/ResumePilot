import pytest

from app.services.resume_parser import _parse_projects


def test_parse_structured_project_line():
    lines = [
        "Project: Smart Camera - Built a low-latency camera processing pipeline - Tech: Python, OpenCV, FFmpeg - Link: https://github.com/example/project",
    ]
    projects = _parse_projects(lines)
    assert len(projects) == 1
    p = projects[0]
    assert p["name"] == "Smart Camera"
    assert "camera processing pipeline" in p["description"]
    assert "Python" in p["technologies"] or "OpenCV" in p["technologies"]


def test_parse_fallback_project_block():
    lines = [
        "Smart Camera | Built a low-latency camera processing pipeline using Python and OpenCV",
        "Additional notes about deployment",
    ]
    projects = _parse_projects(lines)
    assert len(projects) == 1
    p = projects[0]
    assert "Smart Camera" in p["name"]
    assert "camera processing" in p["description"].lower()
