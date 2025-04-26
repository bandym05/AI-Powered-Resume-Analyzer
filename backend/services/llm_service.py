# backend/services/llm_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # You must set this in environment variables

async def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a professional HR recruiter AI.

Given the following resume and job description:

Resume:
{resume_text}

Job Description:
{job_description}

1. List missing skills from resume compared to job description.
2. Suggest improvements to the resume.
Respond in JSON format like:
{{
    "missing_skills": [...],
    "suggestions": "..."
}}
    """

    url = "https://api.groq.com/v1/chat/completions"  # Example for Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",  # You can adjust this
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=body)
    output = response.json()

    try:
        content = output['choices'][0]['message']['content']
        return eval(content)  # Since Groq returns pure text, we eval the JSON string
    except Exception as e:
        print("LLM Parsing error:", e)
        return {"missing_skills": [], "suggestions": ""}    
