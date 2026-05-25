"""
Job description analysis prompts.
"""

JD_ANALYSIS_PROMPT = """
Analyze the following Job Description and extract structural information, required skills, core responsibilities, and key tools. 

Respond strictly in JSON format matching the schema below:
{{
    "job_title": "The exact or normalized job title",
    "company": "The company name (leave empty if not mentioned)",
    "required_hard_skills": [
        "Core technical skills required, e.g., Python, Kubernetes, AWS, SQL"
    ],
    "required_soft_skills": [
        "Core soft skills, e.g., Leadership, Communication, Agile methodologies"
    ],
    "required_tools_and_technologies": [
        "Specific software tools, platforms, or libraries mentioned, e.g., Docker, Scikit-learn, Jira"
    ],
    "core_responsibilities": [
        "Summary of the primary expectations of this role (keep them brief and concise)"
    ],
    "experience_level_expectation": "e.g., Entry, Mid, Senior, Lead, Executive"
}}

Ensure your response is valid JSON with NO additional text outside of the JSON block.

Job Description:
{job_description}
"""
