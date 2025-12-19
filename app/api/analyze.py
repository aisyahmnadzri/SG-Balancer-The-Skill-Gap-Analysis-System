from fastapi import APIRouter
from pydantic import BaseModel
from app.services.skill_extractor import extract_skills
from app.services.rag_service import retrieve_user_skills
from app.services.llm_service import generate_skill_recommendations

router = APIRouter()

class AnalyzeRequest(BaseModel):
    user_id: str
    job_description: str

@router.post("/analyze/")
def analyze_job(req: AnalyzeRequest):
    required_skills = extract_skills(req.job_description)
    existing_skills = retrieve_user_skills(req.user_id, req.job_description)
    missing_skills = list(set(required_skills) - set(existing_skills))
    recommendations = generate_skill_recommendations(missing_skills)
    return {
        "required_skills": required_skills,
        "existing_skills": existing_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }
