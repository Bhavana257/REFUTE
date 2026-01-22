from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ClaimRequest
from app.services.gemini_service import GeminiService

app = FastAPI()

# 🔥 CORS FIX (THIS IS REQUIRED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_service = GeminiService()


@app.post("/challenge")
def challenge_claim(request: ClaimRequest):
    return gemini_service.challenge_claim(request.claim)
