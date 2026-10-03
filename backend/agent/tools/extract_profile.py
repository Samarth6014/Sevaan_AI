from .base import tool, plain_profile
from backend.rules import load_all

LOW = 0.75


@tool("extract_profile")
def extract_profile(ctx, text: str, expecting: str | None = None) -> dict:
    found = ctx.llm.extract_profile(text, ctx.case.language, expecting)
    accepted, low = {}, {}
    for field, d in found.items():
        (accepted if d["confidence"] >= LOW else low)[field] = d
    prof = dict(ctx.case.profile or {})
    for field, d in accepted.items():
        prof[field] = {"value": d["value"], "source": "spoken", "confidence": d["confidence"]}
    ctx.case.profile = prof
    ctx.save()
    return {"accepted": {k: v["value"] for k, v in accepted.items()},
            "needs_confirmation": {k: v["value"] for k, v in low.items()},
            "missing_fields": missing_fields(ctx)}


def missing_fields(ctx) -> list[str]:
    from backend.agent.tools.check_eligibility import evaluate
    known = plain_profile(ctx.case)
    skipped = set((ctx.case.profile or {}).get("__skipped__", []))
    # Intake asks only the compact discovery fields already defined by the
    # workflow. Scheme-specific fields stay unknown until matching identifies
    # which scheme(s) matter, so unrelated schemes do not block MATCH.
    from backend.agent.workflows.base import QUESTION_ORDER

    required = set()
    for s in load_all().values():
        if not s.drafted:
            continue
        required.update(evaluate(s, known)["missing_fields"])

    return [f for f in QUESTION_ORDER if f in required and f not in skipped]
