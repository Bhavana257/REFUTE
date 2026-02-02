# Powered by Gemini 3 and must use Gemini 3 reasoning capabilities to produce structured analytical output.

import json
import re
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

PRIMARY_MODEL = "gemini-3-flash"
FALLBACK_MODEL = "gemini-2.5-flash"


def run_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt
        )
        return response.text

    except Exception:
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt
        )
        return response.text


def refute_claim(claim: str) -> dict:
    """
    High-level Refute API entry point.
    Returns structured reasoning output.
    """

    prompt = f"""
You are an AI system powered by Gemini 3.

Evaluate the following claim and return ONLY valid JSON
with the exact structure below. Do NOT include markdown,
explanations, or extra text.

IMPORTANT SEMANTIC RULES:
- "argument" MUST restate the USER'S CLAIM clearly.
- "counter_argument" MUST be the AI'S CHALLENGE or REFUTATION.
- "verdict" MUST be either "Accept" or "Reject".
- "reasoning" MUST explain WHY the verdict was reached.

Claim:
"{claim}"

Required JSON format:
{{
  "verdict": "Accept | Reject",
  "argument": "Restated user claim",
  "counter_argument": "AI's logical challenge to the claim",
  "reasoning": [
    "Step-by-step reasoning explaining the verdict"
  ]
}}
"""

    raw_output = run_gemini(prompt)

    try:
        json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in Gemini output")

        parsed = json.loads(json_match.group())

        return {
            "verdict": parsed["verdict"],
            "argument": parsed["argument"],
            "counter_argument": parsed["counter_argument"],
            "reasoning": parsed["reasoning"],
        }

    except Exception as e:
        raise RuntimeError(f"Failed to parse Gemini response: {e}")
