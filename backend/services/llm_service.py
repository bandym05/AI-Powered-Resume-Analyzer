import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert AI recruiter.

Based on the following:

=== Resume ===
{resume_text}

=== Job Description ===
{job_description}

Please:
1. List missing skills from the resume compared to job description (bullet points).
2. Suggest improvements to make the resume a better fit (short paragraph).

Format your output strictly in JSON:
{{
    "missing_skills": ["Skill 1", "Skill 2", ...],
    "suggestions": "One paragraph suggestion here."
}}
"""

    url = "https://api.groq.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=body)
    output = response.json()

    try:
        content = output['choices'][0]['message']['content']
        return json.loads(content)  
    except Exception as e:
        print("Parsing error from LLM:", e)
        return {"missing_skills": [], "suggestions": "No suggestion available."}
