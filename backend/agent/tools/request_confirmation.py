from .base import tool
from backend.agent.guardrails import make_confirmation_token, form_hash
from datetime import datetime
from backend.core.clock import now_utc


@tool("request_confirmation")
def request_confirmation(ctx, decision: bool) -> dict:
    """Human gate. Token issued only after an explicit yes to the whole summary."""
    if not decision or not ctx.case.form:
        ctx.case.confirmation = {}
        ctx.save()
        return {"confirmed": False}
    token = make_confirmation_token(ctx.case.id, ctx.case.form)
    ctx.case.confirmation = {"confirmed_at": now_utc().isoformat(),
                             "confirmed_fields_hash": form_hash(ctx.case.form), "token": token}
    ctx.save()
    return {"confirmed": True, "confirmed_fields_hash": ctx.case.confirmation["confirmed_fields_hash"]}
