from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ClaimRequest, ClaimResponse
from app.services.gemini_service import refute_claim

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://refute.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Refute backend is live"}


@app.post("/refute", response_model=ClaimResponse)
async def refute(payload: ClaimRequest):
    return refute_claim(payload.claim)
