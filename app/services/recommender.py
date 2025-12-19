def recommend(skills):
    return [
        {
            "skill": skill,
            "recommendation": f"Build a project using {skill}"
        }
        for skill in skills
    ]
