def extract_features(resume_text: str, job_desc: str) -> list:
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_desc.lower().split())

    skills_match = len(resume_words.intersection(jd_words))
    ratio = skills_match / len(jd_words) if jd_words else 0.0
    experience_match = 1 if "experience" in resume_text.lower() else 0
    education_match = 1 if any(w in resume_text.lower() for w in ["degree", "bachelor", "master", "phd"]) else 0
    keyword_overlap = len(resume_words.intersection(jd_words)) / len(resume_words.union(jd_words)) if resume_words.union(jd_words) else 0.0

    return [skills_match, ratio, experience_match, education_match, keyword_overlap]