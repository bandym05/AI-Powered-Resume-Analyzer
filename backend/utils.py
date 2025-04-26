from pdfminer.high_level import extract_text
from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set your Groq API key
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def analyze_resume_with_llm(resume_text, job_description):
    prompt = f"""
    Analyze this resume against the job description below:
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Extract:
    1. Top 5 skills (comma-separated)
    2. Years of experience (e.g., "5 years")
    3. Education (e.g., "MS in Computer Science")
    4. Match score (0-100%) based on skills/experience fit
    5. 3 suggestions to improve the resume for this job
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
        temperature=0.3
    )
    return response.choices[0].message.content