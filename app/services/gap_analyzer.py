def analyze_gap(required_skills, user_skills):
    required_set = set([s.strip() for s in required_skills])
    user_set = set([s.strip() for s in user_skills])
    missing = list(required_set - user_set)
    matched = list(required_set & user_set)
    return {
        "missing_skills": missing,
        "matched_skills": matched
    }
