from app.services.gemini_service import run_gemini


def refute_agent(claim: str) -> str:
    """
    Structured Gemini agent.
    MUST return deterministic JSON for frontend consumption.
    """

    prompt = f"""
You are a structured reasoning engine.

Analyze the following claim:

"{claim}"

You MUST return ONLY valid JSON in the EXACT format below.
Do NOT include markdown, explanations, or extra text.

JSON FORMAT (STRICT):

{{
  "verdict": "true | false | partially true | context-dependent",
  "confidence": 0-100,
  "argument": "Primary argument supporting the verdict",
  "counter_argument": "Strong opposing argument",
  "reasoning": [
    "Reasoning step 1",
    "Reasoning step 2",
    "Reasoning step 3"
  ]
}}

Rules:
- Do not add any fields
- Do not change field names
- Reasoning MUST be an array (not a paragraph)
- Confidence MUST be a number between 0 and 100
"""

    return run_gemini(prompt)
