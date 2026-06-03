"""
Job description analysis prompts.
"""

JD_ANALYSIS_PROMPT = """
You are a technical recruiter. Analyze this job description and extract structured requirements.

<job_description>
{job_description}
</job_description>

Respond ONLY in this JSON format:
{{
    "must_have_skills": ["skill1", "skill2"],
    "nice_to_have_skills": ["skill3"],
    "key_responsibilities": ["responsibility1", "responsibility2"],
    "domain_keywords": ["keyword1", "keyword2"],
    "seniority_level": "internship/junior/mid/senior",
    "core_role_type": "backend/data-science/ml/fullstack/devops/frontend/etc"
}}
"""

CRITIQUE_PROMPT = """
You are a senior technical recruiter reviewing a tailored resume section.

Job Description Keywords: {jd_keywords}
Generated Content: {generated_content}

Evaluate each bullet or sentence on:
1. SPECIFICITY (1-5): Does it mention exact tools, architectures, and outcomes?
2. JD ALIGNMENT (1-5): Does it reflect the JD's priority keywords?
3. ACTION STRENGTH (1-5): Does it start with a powerful, unique verb?
4. FABRICATION RISK (pass/fail): Does it invent anything not in the whitelist?

For any score below 4, rewrite that item to improve it.

Respond ONLY in JSON format:
{{
    "scores": [
        {{
            "original": "text of bullet",
            "specificity": 4,
            "jd_alignment": 5,
            "action_strength": 3,
            "fabrication_risk": "pass",
            "rewritten": "Improved bullet text..."
        }}
    ],
    "refined_content": [
        "The final improved list of bullets or summary text"
    ]
}}
"""
