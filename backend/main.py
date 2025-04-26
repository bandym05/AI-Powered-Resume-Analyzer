# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from services.parser import extract_text_from_file
from services.scorer import calculate_fit_score
from services.llm_service import analyze_resume
from models.schemas import ResumeAnalysisResponse

app = FastAPI()

# CORS settings so Streamlit frontend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=List[ResumeAnalysisResponse])
async def analyze_resumes(
    resumes: List[UploadFile] = File(...), 
    job_description: UploadFile = File(...)
):
    # ✅ Properly extract text from job description file (handles PDF/DOCX/TXT)
    jd_text = await extract_text_from_file(job_description)

    results = []

    for resume_file in resumes:
        # ✅ Properly extract text from each resume file
        resume_text = await extract_text_from_file(resume_file)
        
        # Analyze the resume with the job description using LLM
        analysis = await analyze_resume(resume_text, jd_text)

        # Calculate a manual fit score
        fit_score = calculate_fit_score(resume_text, jd_text)

        # Build the response for this resume
        result = ResumeAnalysisResponse(
            filename=resume_file.filename,
            fit_score=fit_score,
            missing_skills=analysis.get("missing_skills", []),
            improvement_suggestions=analysis.get("suggestions", "")
        )

        results.append(result)
    
    return results
