from typing import Dict, Any

from gemini_agents import (
    initial_analysis_agent,
    critic_agent,
    revision_agent,
    stability_agent
)


def run_marathon_refutation(claim: str) -> Dict[str, Any]:
    """
    Marathon Agent Orchestrator:
    Executes multi-step reasoning with self-critique and revision.
    """

    thought_state = {
        "claim": claim,
        "iterations": []
    }

    # STEP 1 — Initial Analysis
    analysis = initial_analysis_agent(claim)

    # STEP 2 — Adversarial Critique
    critique = critic_agent(
        claim=claim,
        argument=analysis["argument"],
        assumptions=analysis["assumptions"]
    )

    # STEP 3 — Revision
    revision = revision_agent(
        claim=claim,
        argument=analysis["argument"],
        critiques=critique["critiques"],
        counter_argument=critique["counter_argument"]
    )

    # STEP 4 — Stability Evaluation
    stability = stability_agent(
        revised_argument=revision["revised_argument"],
        revised_verdict=revision["revised_verdict"],
        revised_confidence=revision["revised_confidence"],
        uncertainties=revision["unresolved_uncertainties"]
    )

    thought_state["iterations"].append({
        "analysis": analysis,
        "critique": critique,
        "revision": revision,
        "stability": stability
    })

    return {
        "status": "completed",
        "final_verdict": stability["final_verdict"],
        "final_confidence": stability["final_confidence"],
        "thought_state": thought_state
    }
