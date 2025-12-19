import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# -----------------------------
# LLM setup (CPU-friendly)
# -----------------------------
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
llm_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_new_tokens=300)

def run_llm(prompt: str) -> str:
    return llm_pipeline(prompt)[0]["generated_text"]

def generate_skill_recommendations(missing_skills: list) -> dict:
    """
    Adress to the user what skills they are missing and recommend the users on what initiative can be done to equip those missing skills.
    """
    if not missing_skills:
        return {}

    recommendations = {}

    for skill in missing_skills:
        prompt = f"""
You are a helpful career advisor. Provide 2-3 actionable learning steps for a user missing a skill.

Examples:
Skill: Python
Recommendations:
- Complete Python Crash Course by Eric Matthes
- Solve coding challenges on LeetCode
- Follow Python tutorials on freeCodeCamp

Skill: Docker
Recommendations:
- Follow Docker official guides
- Build and run containers locally
- Watch hands-on tutorials on YouTube

Now give recommendations for the skill: {skill}
"""

        rec_text = run_llm(prompt)

        # Split lines by newlines and remove empty lines
        rec_list = [line.strip(" -") for line in rec_text.split("\n") if line.strip()]
        recommendations[skill] = rec_list

    return recommendations
