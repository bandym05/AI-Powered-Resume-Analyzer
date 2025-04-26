from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from models import SessionLocal, ResumeAnalysis
from utils import extract_text_from_pdf, analyze_resume_with_llm
import shutil
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_resumes(job_description: str = Form(...), files: list[UploadFile] = File(...)):
    db = SessionLocal()
    results = []
    
    for file in files:
        # Save uploaded file
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        resume_text = extract_text_from_pdf(file_path)
        
        # Analyze with LLM
        analysis_result = analyze_resume_with_llm(resume_text, job_description)
        
        # Parse LLM response (simplified)
        skills = analysis_result.split("1. Top 5 skills:")[1].split("2.")[0].strip()
        experience = analysis_result.split("2. Years of experience:")[1].split("3.")[0].strip()
        education = analysis_result.split("3. Education:")[1].split("4.")[0].strip()
        match_score = float(analysis_result.split("4. Match score:")[1].split("%")[0].strip())
        suggestions = analysis_result.split("5. Suggestions:")[1].strip()
        
        # Save to DB
        db_record = ResumeAnalysis(
            filename=file.filename,
            skills=skills,
            experience=experience,
            education=education,
            match_score=match_score,
            suggestions=suggestions
        )
        db.add(db_record)
        db.commit()
        
        results.append({
            "filename": file.filename,
            "skills": skills,
            "match_score": match_score,
            "suggestions": suggestions
        })
    
    return {"results": results}