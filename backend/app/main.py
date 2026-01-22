from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ClaimRequest, ClaimResponse
from app.services.gemini_service import refute_claim

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/challenge", response_model=ClaimResponse)
async def challenge_claim(payload: ClaimRequest):
    return await refute_claim(payload.claim)
