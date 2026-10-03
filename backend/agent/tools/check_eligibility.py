from .base import tool, plain_profile
from backend.rules import load_all, check_eligibility as _check


def evaluate(scheme, profile: dict) -> dict:
    return _check(scheme, profile)


@tool("check_eligibility")
def check_eligibility(ctx, scheme_id: str) -> dict:
    s = load_all()[scheme_id]
    return _check(s, plain_profile(ctx.case))  # pure Python, no LLM
