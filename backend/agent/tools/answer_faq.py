from .base import tool
from backend.rules import load_all


@tool("answer_faq")
def answer_faq(ctx, scheme_id: str, question: str) -> dict:
    """Only verified FAQ text; no invention."""
    s = load_all()[scheme_id]
    words = set(question.lower().split())
    best, score = None, 0
    for f in s.faqs:
        sc = len(words & set(f.q.lower().split()))
        if sc > score:
            best, score = f, sc
    return {"answer": best.a if best else "not found"}
