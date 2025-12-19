# Simple skill extractor using regex / keyword matching
import re

def extract_skills(job_description: str):
    """
    Extract technical skills from job description (very simple version).
    Can be improved with LLM if needed.
    """
    # Lowercase for simple keyword matching
    jd = job_description.lower()

    # Example skill list (expand as needed)
    skill_list = [
        "python", "fastapi", "docker", "kubernetes",
        "postgresql", "graphql", "git", "aws"
    ]

    extracted = [skill for skill in skill_list if skill in jd]
    return extracted
