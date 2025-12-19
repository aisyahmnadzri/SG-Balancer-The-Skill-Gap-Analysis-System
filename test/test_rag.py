from app.services.rag_service import add_user_skills, retrieve_user_skills

# Add sample user skills
add_user_skills("user123", ["Python", "FastAPI", "Docker", "Kubernetes", "PostgreSQL"])

# Retrieve top skills for a job
job_desc = "Looking for backend engineer with FastAPI, Docker, Kubernetes, and PostgreSQL experience."
skills = retrieve_user_skills("user123", job_desc)
print(skills)
