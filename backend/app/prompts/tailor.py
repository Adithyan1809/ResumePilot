"""
Resume section tailoring prompts.
"""

TAILOR_SUMMARY_PROMPT = """
You are an elite executive recruiter. Your task is to rewrite the candidate's professional summary to align beautifully with the target role and company.

Objectives:
1. SUMMARY SPECIFICITY: Avoid generic boilerplate summaries. Generate a highly specific, technically grounded summary detailing their primary domain strengths using the candidate's actual stack.
2. TECHNICAL REALISM: Highlight key technical strengths that match the job description.
3. DOMAIN ISOLATION: Keep technical domains strictly isolated. Do not claim expertise in tools from unrelated domains based solely on what appears in the JD.
4. STRICT ANTI-FABRICATION: Never invent years of experience, false certifications, or false roles. Use ONLY technologies explicitly present inside the following allowed_technologies whitelist:
{allowed_technologies}
5. LENGTH: Maintain brevity. DO NOT output exact word counts, but rely on 3 to 4 concise sentences maximum.

Input Summary:
<current_summary>
{current_summary}
</current_summary>

Target Role Context:
Title: {job_title}
Company: {company}
<job_description>
{job_details}
</job_description>

Respond in the following JSON format:
{{
    "summary": "The professionally tailored summary text"
}}
"""

TAILOR_EXPERIENCE_PROMPT = """
You are an elite resume strategist. Your task is to optimize the work experience bullet points of the candidate to project deep technical authority and align with the target job description.

Rewriting Guidelines:
1. DYNAMIC TECHNICAL DEPTH: Elevate weak, vague, or passive descriptions into robust, professional engineering bullets.
2. VARY BULLET PATTERNS: Use ONE of these bullet patterns, varying across bullets:
   - Pattern A (Architecture): "[Verb] [system/component] using [tech] to [outcome]"
   - Pattern B (Scale/Impact): "[Verb] [what] that [measurable result or structural improvement]"  
   - Pattern C (Problem->Solution): "[Verb] [specific problem] by [technical approach] using [tech]"
   - Pattern D (Collaboration): "[Verb] with [team/system] to [deliver what] using [tech]"
   Never use the same pattern twice consecutively. Aim for natural variation.
3. DOMAIN ISOLATION: Keep technical domains strictly isolated.
4. PRESERVE STRUCTURE: Keep the exact same number of bullet points per role as provided in the input. Do not add, remove, or merge bullets.
5. STRICT ANTI-FABRICATION: Never invent or fabricate any tools, metrics, or frameworks. Use ONLY technologies explicitly present in the following whitelisted allowed_technologies list:
{allowed_technologies}
6. PRESERVE METRICS: Do NOT invent or fabricate any numerical statistics, percentages, or dollar figures. Keep all original metrics exactly as they are.

BULLET EXAMPLES:
BAD (what NOT to produce):
- "Worked on machine learning models using Python for data analysis"
- "Utilized SQL to manage databases and improve performance"
- "Helped develop NLP pipeline for text processing tasks"

GOOD (what you MUST produce):
- "Engineered an NLP-based regulatory compliance classifier using spaCy and transformer embeddings, reducing manual review time by flagging non-compliant clauses with 89% precision"
- "Designed a facial recognition attendance pipeline integrating MTCNN for detection and FaceNet512 for identity verification across a 500-person dataset"
- "Built async REST endpoints in FastAPI with JWT-based auth and PostgreSQL connection pooling to support concurrent resume processing workflows"

Input Experience Entries (JSON List):
<experience_entries>
{experience_entries}
</experience_entries>

Target Role Context:
Title: {job_title}
Company: {company}
<job_description>
{job_details}
</job_description>

Respond in the exact JSON format below:
{{
    "experience": [
        {{
            "company": "Company Name",
            "role": "Role Name",
            "dates": "Dates Active",
            "bullets": [
                "Tailored bullet point 1",
                "Tailored bullet point 2"
            ]
        }}
    ]
}}
"""

TAILOR_SKILLS_PROMPT = """
Analyze the candidate's skills list and the required skills in the job description.
Reorder the candidate's existing skills to place the most relevant ones at the top.

CRITICAL INSTRUCTIONS:
1. DO NOT INVENT SKILLS. You must ONLY use skills from the `allowed_technologies` whitelist. Do NOT add missing skills from the JD if the candidate does not have them.
2. Categorize and format the skills list into logical categories (e.g. Programming Languages, Frameworks & Libraries, Databases, Tools, DevOps).
3. Deduplicate repeated skills.

Candidate's Original Skills:
<current_skills>
{current_skills}
</current_skills>

Whitelist of Allowed Technologies (DO NOT DEVIATE):
<allowed_technologies>
{allowed_technologies}
</allowed_technologies>

Job Description Required Skills & Keywords:
<required_skills>
{required_skills}
</required_skills>

Respond in the following JSON format:
{{
    "skills": [
        "Programming Languages: Python, SQL",
        "Backend Development: FastAPI, PostgreSQL",
        "Databases: Redis, SQLite",
        "Tools: Git, Postman"
    ]
}}
"""

