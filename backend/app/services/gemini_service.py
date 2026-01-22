import os
import json
import re
from typing import Dict

from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment")

        self.client = genai.Client(api_key=api_key)
        self.model = "models/gemini-2.5-flash"

    def _parse_gemini_json(self, text: str) -> Dict:
        """
        Gemini often returns JSON wrapped in ```json ... ```
        This function safely extracts and parses it.
        """
        try:
            # Remove code fences if present
            cleaned = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

            # Parse JSON
            parsed = json.loads(cleaned)

            return {
                "verdict": str(parsed.get("verdict", "ERROR")).upper(),
                "argument": parsed.get("argument", ""),
                "counter_argument": parsed.get("counter_argument", ""),
                "reasoning": parsed.get("reasoning", ""),
            }

        except Exception as e:
            # Fallback if parsing fails
            return {
                "verdict": "ERROR",
                "argument": "",
                "counter_argument": "",
                "reasoning": f"Failed to parse Gemini response: {str(e)}",
            }

    def challenge_claim(self, claim: str) -> Dict:
        prompt = f"""
You are an expert critical thinker.

Analyze the following claim and return ONLY valid JSON
(no markdown, no explanation outside JSON).

JSON format:
{{
  "verdict": "TRUE | FALSE | DEBATABLE",
  "argument": "Argument supporting the claim",
  "counter_argument": "Argument against the claim",
  "reasoning": "Final reasoning summary"
}}

Claim:
"{claim}"
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            raw_text = response.text.strip()
            return self._parse_gemini_json(raw_text)

        except Exception as e:
            error_msg = str(e)

            # Handle quota / API errors cleanly
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                return {
                    "verdict": "ERROR",
                    "argument": "",
                    "counter_argument": "",
                    "reasoning": "Gemini API quota exceeded. Please wait or upgrade plan.",
                }

            return {
                "verdict": "ERROR",
                "argument": "",
                "counter_argument": "",
                "reasoning": f"Gemini API error: {error_msg}",
            }


gemini_service = GeminiService()
