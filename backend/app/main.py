from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from app.services.gemini_service import refute_claim

load_dotenv()

app = FastAPI(
    title="Refute — Structured Reasoning API",
    description="Evaluates claims using Gemini 3 with deterministic, structured reasoning",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RefuteRequest(BaseModel):
    claim: str


class RefuteResponse(BaseModel):
    verdict: str
    argument: str
    counter_argument: str
    reasoning: list


@app.post("/refute", response_model=RefuteResponse)
def refute(request: RefuteRequest):
    """
    Evaluate a claim and return structured reasoning.
    """
    try:
        return refute_claim(request.claim)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}
