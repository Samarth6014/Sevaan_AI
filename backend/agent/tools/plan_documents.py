from datetime import date
from sqlmodel import select
from .base import tool, plain_profile
from backend.models import Document
from backend.rules import load_all

VERIFY_TEXT = "Not verified yet. Check the official portal or ask a human helper."


def _cond_true(cond: str | None, prof: dict):
    """'category in SC,ST,OBC' -> True/False/None(unknown)."""
    if not cond:
        return True
    try:
        field, rest = cond.split(" in ", 1)
    except ValueError:
        return None
    v = prof.get(field.strip())
    return None if v is None else v in [x.strip() for x in rest.split(",")]


@tool("plan_documents")
def plan_documents(ctx, scheme_id: str) -> dict:
    s = load_all()[scheme_id]
    prof = plain_profile(ctx.case)
    have = {d.doc_type for d in ctx.session.exec(select(Document).where(Document.case_id == ctx.case.id))}
    missing, maybe = [], []
    for d in s.documents:
        c = _cond_true(d.condition, prof)
        needed = d.required and c is not False or (not d.required and c is True)
        if c is None and not d.required:
            maybe.append(d.label)
        if needed and d.id not in have:
            office = d.where_to_get.office
            missing.append({"id": d.id, "label": d.label,
                            "where_to_get": VERIFY_TEXT if office == "verify" else office,
                            "carry": d.where_to_get.carry})
    # certificates (office visits) first: they take longest
    order = sorted(missing, key=lambda m: (0 if "certificate" in m["id"] else 1))
    days = None
    if s.deadline.date:
        days = (date.fromisoformat(s.deadline.date) - date.today()).days
    return {"scheme_id": scheme_id, "missing": missing, "maybe_needed": maybe,
            "suggested_order": [m["id"] for m in order], "days_remaining": days,
            "deadline_note": s.deadline.note}
