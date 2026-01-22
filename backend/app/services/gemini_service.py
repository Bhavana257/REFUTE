"""
gemini_service.py

NOTE:
This file is intentionally kept as a compatibility layer.
All core reasoning is delegated to the Marathon Agent orchestrator.
"""

from orchestrator import run_marathon_refutation


def refute_statement(statement: str) -> dict:
    """
    Legacy-compatible entry point.
    Internally delegates to the Marathon Agent.
    """

    result = run_marathon_refutation(statement)

    return {
        "verdict": result["final_verdict"],
        "confidence": result["final_confidence"],
        "reasoning": result["thought_state"]
    }
