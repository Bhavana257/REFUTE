from google import genai
import json
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_gemini(prompt: str) -> dict:
    """
    Executes a Gemini 3 call and enforces JSON-only output.
    """
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned non-JSON output")


def initial_analysis_agent(claim: str) -> dict:
    prompt = f"""
You are an analytical reasoning agent.

Task:
Given a user claim, construct the strongest possible argument supporting the claim.

Rules:
- Assume the claim is true unless proven otherwise
- Explicitly list assumptions
- Avoid emotional language
- Do not consider counterarguments yet

Output strictly in JSON with keys:
- argument
- assumptions
- initial_confidence (0–100)

Claim:
\"{claim}\"
"""
    return call_gemini(prompt)


def critic_agent(claim: str, argument: str, assumptions: list) -> dict:
    prompt = f"""
You are an adversarial critic agent.

Your job is to challenge the reasoning produced by another agent.

Rules:
- Identify logical gaps and unstated assumptions
- Provide counterexamples when possible
- Do NOT propose fixes

Output strictly in JSON with keys:
- critiques (array)
- counter_argument
- confidence_reduction_reason

Claim:
\"{claim}\"

Argument:
{argument}

Assumptions:
{assumptions}
"""
    return call_gemini(prompt)


def revision_agent(claim: str, argument: str, critiques: list, counter_argument: str) -> dict:
    prompt = f"""
You are a revision agent.

Revise the original argument after receiving adversarial critiques.

Rules:
- You may weaken or reject the claim
- Acknowledge uncertainty
- Update confidence

Output strictly in JSON with keys:
- revised_argument
- revised_verdict (True / False / Inconclusive)
- revised_confidence (0–100)
- unresolved_uncertainties

Claim:
\"{claim}\"

Original Argument:
{argument}

Critiques:
{critiques}

Counter Argument:
{counter_argument}
"""
    return call_gemini(prompt)


def stability_agent(revised_argument: str, revised_verdict: str,
                    revised_confidence: int, uncertainties: list) -> dict:
    prompt = f"""
You are a stability evaluator.

Determine whether the reasoning process has stabilized.

Rules:
- If confidence < 60 OR uncertainties are critical, mark unstable
- Otherwise finalize

Output strictly in JSON with keys:
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
