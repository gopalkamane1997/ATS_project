from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.parser import extract_text_from_pdf
from utils.features import extract_features
from utils.ml_model import predict_ml_score
from utils.gemini import get_gemini_response
import re
import uvicorn

app = FastAPI(title="ATS Resume Analyzer API")
templates = Jinja2Templates(directory="templates")


# ----------- CLEAN TEXT -----------

def clean_text(text: str):
    return re.sub(r'[^a-zA-Z ]', ' ', text).lower()


# ----------- HEALTH CHECK -----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ----------- MAIN ENDPOINT -----------

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        # Step 1: Extract resume text
        resume_text = extract_text_from_pdf(file.file)

        # Step 2: Clean text
        resume_text_clean = clean_text(resume_text)
        job_desc_clean = clean_text(job_description)

        # Step 3: Feature Engineering
        features = extract_features(resume_text_clean, job_desc_clean)

        # Step 4: ML Score
        ml_score = predict_ml_score(features)

        # Step 5: Gemini Analysis
        gemini_output = get_gemini_response(resume_text, job_description)

        return {
            "status": "success",
            "ml_match_score": ml_score,
            "gemini_match_score": gemini_output["score"],
            "gemini_analysis": gemini_output["analysis"]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)