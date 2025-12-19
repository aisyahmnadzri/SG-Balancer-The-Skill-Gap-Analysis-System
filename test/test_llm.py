from app.services.llm_service import run_llm

print("Starting LLM test...")

output = run_llm(
    "Extract technical skills from this job description: "
    "Looking for backend engineer with FastAPI, Docker, and PostgreSQL"
)

print("LLM response:")
print(output)
