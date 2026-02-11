from fastapi import FastAPI
from pydantic import BaseModel
from fraud_app.modules.email_analyzer.service import analyze_email

app = FastAPI(title="Fraud Email Analyzer MVP")

class EmailIn(BaseModel):
    subject: str
    body: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze/email")
def analyze(payload: EmailIn):
    return analyze_email(payload.subject, payload.body)
