from typing import Dict, Any
import json
import re

from gemini_agents import (
    initial_analysis_agent,
    critic_agent,
    revision_agent,
    stability_agent
)


def safe_agent_output(output: Any) -> Dict[str, Any]:
    """
    Extracts and parses the first valid JSON object from LLM output.
    Handles prose, markdown, and escaped newlines robustly.
    """
    if isinstance(output, dict):
        return output

    if isinstance(output, str):

        text = re.sub(r"```json|```", "", output).strip()

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in agent output")

        json_text = match.group(0)

        return json.loads(json_text)

    raise ValueError("Unsupported agent output format")


def run_marathon_refutation(claim: str) -> Dict[str, Any]:
    """
    Marathon Agent Orchestrator:
    Executes multi-step reasoning with self-critique and revision.
    """

    thought_state = {
        "claim": claim,
        "iterations": []
    }

    analysis = safe_agent_output(
        initial_analysis_agent(claim)
    )

    critique = safe_agent_output(
        critic_agent(
            claim=claim,
            argument=analysis["argument"],
            assumptions=analysis["assumptions"]
        )
    )

    revision = safe_agent_output(
        revision_agent(
            claim=claim,
            argument=analysis["argument"],
            critiques=critique["critiques"],
            counter_argument=critique["counter_argument"]
        )
    )

    stability = safe_agent_output(
        stability_agent(
            revised_argument=revision["revised_argument"],
            revised_verdict=revision["revised_verdict"],
            revised_confidence=revision["revised_confidence"],
            uncertainties=revision["unresolved_uncertainties"]
        )
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
