import google.genai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(resume_text, job_desc):
    prompt = f"""
    Analyze resume vs job description. Be extremely concise.

    Resume:
    {resume_text}

    Job:
    {job_desc}

    Respond strictly in this exact format (no extra text):
    MATCH_SCORE: <number 0-100>

    MISSING KEYWORDS:
    - <keyword or short phrase>
    - <keyword or short phrase>
    (max 5 items, 1-4 words each)

    SUGGESTIONS:
    - <one short actionable tip>
    - <one short actionable tip>
    (max 5 items, one line each)
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text

    score_match = re.search(r'MATCH_SCORE:\s*(\d+)', text)
    score = int(score_match.group(1)) if score_match else None
    analysis = re.sub(r'MATCH_SCORE:\s*\d+\n?', '', text).strip()

    return {"score": score, "analysis": analysis}