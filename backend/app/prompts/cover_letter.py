"""
Cover letter generation prompts.
"""

COVER_LETTER_PROMPT = """
You are an expert copywriter. Generate a persuasive, highly tailored, and professional cover letter for the candidate applying to the target job description.

Candidate Name: {candidate_name}
Target Job Title: {job_title}
Target Company: {company}
Tone: {tone} (professional, enthusiastic, or conversational)
Additional Candidate Notes/Context: {additional_notes}

Candidate Tailored Resume Sections (for experience & skills context):
{resume_sections}

Target Job Description:
{job_description}

Guidelines:
1. Contact Information Block: Do not add placeholder contact info blocks (like "[Street Address]", "[Phone Number]"). Simply start with the date, followed by a professional greeting (e.g. "Dear Hiring Team at {company}," or "Dear Hiring Manager,").
2. Introduction: Hook the reader by stating the role they are applying for, their enthusiasm, and a brief statement summarizing why they are a perfect fit.
3. Body Paragraphs (2-3): Connect the candidate's actual projects, achievements, and technical stack (from the resume) directly to the core challenges mentioned in the JD. Focus on results and value addition.
4. Call to Action: Reiterate interest, suggest a meeting/call, and sign off professionally (e.g., "Sincerely,\n{candidate_name}").
5. Length: Keep the entire cover letter around 250-350 words, fitting on a single page.
6. Tone Alignment: Match the selected tone ({tone}) closely:
   - "professional": Formal, elegant, highly authoritative.
   - "enthusiastic": High-energy, passionate about the company's mission.
   - "conversational": Warm, accessible, storytelling-focused.

Respond in the following JSON format:
{{
    "cover_letter": "The full text of the generated cover letter"
}}
"""
