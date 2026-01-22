from google import genai
import json
import os

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_gemini(prompt: str) -> dict:
    """
    Executes a Gemini 3 Pro call and enforces JSON-only output.
    """
    response = client.models.generate_content(
        model="models/gemini-3-pro-preview",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(f"Gemini returned non-JSON output:\n{response.text}")


def initial_analysis_agent(claim: str) -> dict:
    prompt = f"""
You are an analytical reasoning agent.

Task:
Construct the strongest possible argument supporting the claim.

Rules:
- Assume the claim is true initially
- Explicitly list assumptions
- Do not include counterarguments

Output JSON with:
- argument
- assumptions
- initial_confidence (0-100)

Claim:
{claim}
"""
    return call_gemini(prompt)


def critic_agent(claim: str, argument: str, assumptions: list) -> dict:
    prompt = f"""
You are an adversarial critic agent.

Task:
Rigorously challenge the reasoning.

Rules:
- Identify logical gaps
- Challenge assumptions
- Provide counterexamples
- Do not suggest fixes

Output JSON with:
- critiques (array)
- counter_argument
- confidence_reduction_reason

Claim:
{claim}

Argument:
{argument}

Assumptions:
{assumptions}
"""
    return call_gemini(prompt)


def revision_agent(claim: str, argument: str, critiques: list, counter_argument: str) -> dict:
    prompt = f"""
You are a revision agent.

Task:
Revise the argument after critique.

Rules:
- You may weaken or reject the claim
- Explicitly acknowledge uncertainty

Output JSON with:
- revised_argument
- revised_verdict (True / False / Inconclusive)
- revised_confidence (0-100)
- unresolved_uncertainties

Claim:
{claim}

Original Argument:
{argument}

Critiques:
{critiques}

Counter Argument:
{counter_argument}
"""
    return call_gemini(prompt)


def stability_agent(
    revised_argument: str,
    revised_verdict: str,
    revised_confidence: int,
    uncertainties: list
) -> dict:
    prompt = f"""
You are a stability evaluator.

Determine whether reasoning has stabilized.

Rules:
- If confidence < 60 OR uncertainties are critical → unstable
- Else → stable

Output JSON with:
- is_stable (true/false)
- final_verdict
- final_confidence
- explanation

Revised Argument:
{revised_argument}

Verdict:
{revised_verdict}

Confidence:
{revised_confidence}

Uncertainties:
{uncertainties}
"""
    return call_gemini(prompt)
