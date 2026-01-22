from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

from orchestrator import run_marathon_refutation

app = FastAPI(
    title="Refute — Marathon Agent API",
    description="Multi-step autonomous reasoning using Gemini agents",
    version="2.0"
)


class MarathonRequest(BaseModel):
    statement: str


class MarathonResponse(BaseModel):
    final_verdict: str
    final_confidence: int
    thought_state: dict


@app.post("/refute-marathon", response_model=MarathonResponse)
def refute_marathon(request: MarathonRequest):
    """
    Executes the Marathon Agent reasoning loop for a given claim.
    """

    try:
        result = run_marathon_refutation(request.statement)

        return {
            "final_verdict": result["final_verdict"],
            "final_confidence": result["final_confidence"],
            "thought_state": result["thought_state"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}
