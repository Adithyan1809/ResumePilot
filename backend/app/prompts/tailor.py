"""
Resume section tailoring prompts.
"""

TAILOR_SUMMARY_PROMPT = """
You are an elite executive recruiter. Your task is to rewrite the candidate's professional summary to align beautifully with the target role and company.
 
Objectives:
1. SUMMARY SPECIFICITY: Avoid generic boilerplate summaries like "Software Engineer with experience in building scalable backends...". Instead, generate a highly specific, technically grounded summary detailing their primary domain strengths (e.g. AI & ML undergraduate, data analysis pipelines, computer vision systems, or async backend architectures) using the candidate's actual stack.
2. TECHNICAL REALISM & CONCISENESS: Rephrase the summary to highlight key technical strengths that match the job description. Keep it highly realistic and appropriate for their career stage (student/junior/mid-level).
3. ROLE CONTAMINATION PROTECTION: Do NOT mix backend/data-science tools with frontend concepts. If tailoring a backend/data role, do not claim expertise in "responsive web design" or "CSS layout styling". Keep domains strictly isolated.
4. DO NOT FABRICATE: Never invent years of experience, false certifications, or false roles. Use ONLY technologies explicitly present inside the following allowed_technologies whitelist: {allowed_technologies}
5. LENGTH: Strictly 3 to 4 concise sentences maximum (50-70 words).
6. NO CONTACT DETAILS: Under no circumstances include names, email, phone numbers, or links.
 
Input Summary:
{current_summary}
 
Target Job Title: {job_title}
Target Company: {company}
Target Job Description:
{job_details}
 
Respond in the following JSON format:
{{
    "summary": "The professionally tailored summary text"
}}
"""
 
TAILOR_EXPERIENCE_PROMPT = """
You are an elite resume strategist. Your task is to optimize the work experience bullet points of the candidate to project deep technical authority and align with the target job description.
 
Rewriting Guidelines:
1. DYNAMIC TECHNICAL DEPTH: Elevate weak, vague, or passive descriptions into robust, professional engineering bullets. For example, if a bullet says "worked on databases", elevate it to "Designed and optimized database schemas using PostgreSQL to ensure transactional integrity."
2. HUMAN BULLET VARIATION: Write with natural, diverse sentence structures and active verbs. Avoid robotic, repetitive AI templates (e.g. do not start multiple bullets with "Leveraged Python to..." or "Utilized SQL for..."). Start each bullet directly with a unique action verb.
3. ROLE CONTAMINATION PROTECTION: Keep technical domains strictly isolated. Do NOT mix backend/data-science tools with frontend styling concepts.
4. MATCH THE JD: Seamlessly incorporate relevant methodologies, design patterns, and keywords from the job description (e.g., API gateways, query optimizations, responsive layouts) using ONLY whitelisted tech.
5. ACTION-VERB START: Every single bullet point must start with a powerful past-tense action verb (e.g. Optimized, Engineered, Architected, Spearheaded, Implemented, Developed).
6. STRICT BULLET STRUCTURE: Every bullet point must strictly adhere to the following sequence:
   [Action Verb] + [Real Technical Task] + [Real Technologies from the Allowed Whitelist] + [Real Purpose/Impact].
7. DO NOT FABRICATE: Never invent or fabricate any tools, metrics, or frameworks. Use ONLY technologies explicitly present in the following whitelisted allowed_technologies list: {allowed_technologies}
8. PRESERVE METRICS: Do NOT invent or fabricate any numerical statistics, percentages, or dollar figures. Keep all original metrics exactly as they are. If no metrics are present, focus on describing the technical implementation and structural results.
9. CONCISE WORDING: Target under 35 words per bullet. Phrasing must feel technically realistic and appropriate for internship/student-level candidates.
 
Input Experience Entries (JSON List):
{experience_entries}
 
Target Job Details:
Job Title: {job_title}
Company: {company}
Job Description:
{job_details}
 
Respond in the exact JSON format below. You must replicate the experience list structure exactly:
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
Reorder the candidate's existing skills to place the most relevant ones at the top, and optionally add 2-3 highly related skills that the candidate likely possesses based on their experience but forgot to list.

Do NOT add highly specialized skills that require separate certifications (like "AWS Certified Solutions Architect" unless present in their original resume), but common technical skills like "REST APIs", "Git", or library names are fine.

CRITICAL: You must categorize and format the skills list into EXACTLY the following 7 normalized categories (omit a category ONLY if there are absolutely no skills matching it, but do NOT rename or merge them):
- Programming Languages
- Data Science & ML
- Backend Development
- Databases
- Computer Vision
- DevOps & Infrastructure
- Tools

Each list item in your output array must be in the format 'Category Name: Skill 1, Skill 2, Skill 3'.
Example:
"skills": [
    "Programming Languages: Python, JavaScript, SQL",
    "Backend Development: FastAPI, PostgreSQL, Redis",
    "Tools: Git, Postman"
]

DO NOT output one single giant flat list or paragraph. Deduplicate repeated skills.

Candidate's Original Skills:
{current_skills}

Job Description Required Skills & Keywords:
{required_skills}

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
