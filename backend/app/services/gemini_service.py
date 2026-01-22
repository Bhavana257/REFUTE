import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def refute_claim(claim: str) -> dict:
    """
    Uses Gemini 3 to analyze and refute a claim.
    Always returns all required fields to match ClaimResponse schema.
    """

    prompt = f"""
You are a critical reasoning assistant.

Analyze the following claim and respond in STRICT JSON with the keys:
verdict, argument, reasoning, counter_argument.

Claim:
"{claim}"

Rules:
- verdict must be a short statement (True / False / Misleading)
- argument must challenge the claim directly
- reasoning must explain logically
- counter_argument must rebut a possible defense
- Output ONLY valid JSON
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=prompt
        )

        text = response.text.strip()

        import json
        data = json.loads(text)

        return {
            "verdict": data.get("verdict", "Unclear"),
            "argument": data.get("argument", "No argument generated."),
            "reasoning": data.get("reasoning", "No reasoning provided."),
            "counter_argument": data.get("counter_argument", "No counter-argument generated.")
        }

    except Exception as e:

        return {
            "verdict": "Error",
            "argument": "The system failed to analyze the claim.",
            "reasoning": str(e),
            "counter_argument": "Please try again later."
        }
