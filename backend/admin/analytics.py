from sqlmodel import Session, select
from backend.models import Case, Feedback, TraceEntry

STAGES = ["INTAKE", "MATCH", "PLAN", "COLLECT", "FILL", "REVIEW_CONFIRM", "SUBMIT", "TRACK"]


def compute(session: Session) -> dict:
    cases = session.exec(select(Case)).all()
    funnel = {s: sum(1 for c in cases if STAGES.index(c.stage) >= STAGES.index(s)) for s in STAGES}
    ratings = [f.rating for f in session.exec(select(Feedback))]
    blocked = len(session.exec(select(TraceEntry).where(TraceEntry.ok == False)).all())  # noqa: E712
    return {"label": "Numbers come from synthetic/demo runs only", "cases": len(cases), "funnel": funnel,
            "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
            "blocked_actions": blocked,
            "accessibility_scores": "see reports/a11y_walkthrough.md (fill after running axe/Lighthouse)"}
