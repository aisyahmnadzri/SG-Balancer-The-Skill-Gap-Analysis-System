from app.services.skill_extractor import extract_required_skills

job_desc = "Looking for backend engineer with FastAPI, Docker, Kubernetes, and PostgreSQL experience."

skills = extract_required_skills(job_desc)
print(skills)
