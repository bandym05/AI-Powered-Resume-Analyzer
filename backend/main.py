# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.parser import extract_text_from_file
from services.scorer import calculate_fit_score
from services.llm_service import analyze_resume
from models.schemas import ResumeAnalysisResponse

from typing import List

app = FastAPI()

# CORS settings so Streamlit can talk to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=List[ResumeAnalysisResponse])
async def analyze_resumes(resumes: List[UploadFile] = File(...), job_description: UploadFile = File(...)):
    # Extract job description text
    jd_text = await job_description.read()
    jd_text = jd_text.decode('utf-8')  # assuming it's a simple .txt upload for now

    results = []

    for resume_file in resumes:
        resume_text = await extract_text_from_file(resume_file)
        
        # LLM analyzes resume + JD
        analysis = await analyze_resume(resume_text, jd_text)

        # Calculate fit score manually
        fit_score = calculate_fit_score(resume_text, jd_text)

        result = ResumeAnalysisResponse(
            filename=resume_file.filename,
            fit_score=fit_score,
            missing_skills=analysis.get("missing_skills", []),
            improvement_suggestions=analysis.get("suggestions", "")
        )

        results.append(result)
    
    return results
