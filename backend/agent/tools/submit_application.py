from sqlmodel import select

from .base import tool
from backend.models import Document
from backend.agent.guardrails import require_valid_token


@tool("submit_application")
def submit_application(ctx) -> dict:
    """The ONLY code path that submits. Refuses without a valid token for the current form."""
    require_valid_token(ctx.case.id, ctx.case.form, (ctx.case.confirmation or {}).get("token"))
    otr = ctx.connector.register_otr(f"case-{ctx.case.id}")
    doc_ids = [
        d.id for d in ctx.session.exec(select(Document).where(Document.case_id == ctx.case.id)).all()
        if d.id is not None
    ]
    app_id = ctx.connector.submit_application(otr, ctx.case.chosen_scheme_id, ctx.case.form, doc_ids,
                                              ctx.case.confirmation["token"])
    ctx.case.application_id = app_id
    st = ctx.connector.get_status(app_id)
    ctx.case.status, ctx.case.status_history = st["status"], st["history"]
    ctx.save()
    return {"application_id": app_id, "status": st["status"]}
