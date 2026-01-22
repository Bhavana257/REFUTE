import os
import google.generativeai as genai
from fastapi import HTTPException

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


async def refute_claim(claim: str):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    try:
        prompt = f"""
You are a critical thinking assistant.

Analyze the following claim and respond with:
- verdict (True / False / Misleading)
- argument
- counter_argument
- reasoning

Claim: "{claim}"
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        return {
            "verdict": "Refuted",
            "argument": text,
            "counter_argument": text,
            "reasoning": text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
