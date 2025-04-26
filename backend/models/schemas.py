# backend/models/schemas.py
from pydantic import BaseModel
from typing import List

class ResumeAnalysisResponse(BaseModel):
    filename: str
    fit_score: float
    missing_skills: List[str]
    improvement_suggestions: str
