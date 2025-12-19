import uvicorn
from fastapi.testclient import TestClient
from app.main import app
from app.services.rag_service import add_user_skills

# -----------------------------
# Create FastAPI test client
# -----------------------------
client = TestClient(app)

# -----------------------------
# Setup: add sample user skills
# -----------------------------
user_id = "user123"
add_user_skills(user_id, ["Python", "FastAPI", "Docker", "PostgreSQL"])

# -----------------------------
# Job description input
# -----------------------------
job_description = """
Looking for backend engineer with Python, FastAPI, Docker, Kubernetes, and PostgreSQL experience.
"""

# -----------------------------
# Make POST request to /analyze
# -----------------------------
response = client.post(
    "/analyze/",
    json={"user_id": user_id, "job_description": job_description}
)

# -----------------------------
# Print output
# -----------------------------
if response.status_code == 200:
    data = response.json()
    print("Required skills:", data["required_skills"])
    print("Existing skills:", data["existing_skills"])
    print("Missing skills:", data["missing_skills"])
    print("Recommendations:", data["recommendations"])
else:
    print("Error:", response.status_code, response.text)
