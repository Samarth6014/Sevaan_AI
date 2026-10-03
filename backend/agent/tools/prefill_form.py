from sqlmodel import select
from .base import tool
from backend.documents import prefill
from backend.models import Document


@tool("prefill_form")
def prefill_form(ctx, scheme_id: str) -> dict:
    docs = ctx.session.exec(select(Document).where(Document.case_id == ctx.case.id)).all()
    form = prefill(ctx.case.profile, [{"doc_type": d.doc_type, "fields": d.extracted_fields} for d in docs])
    ctx.case.form = form
    ctx.case.confirmation = {}  # any change invalidates earlier confirmation
    ctx.save()
    return {"scheme_id": scheme_id, "form": form}
