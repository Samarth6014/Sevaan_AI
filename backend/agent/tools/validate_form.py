from sqlmodel import select
from .base import tool
from backend.documents import validate
from backend.models import Document


@tool("validate_form")
def validate_form(ctx) -> dict:
    docs = ctx.session.exec(select(Document).where(Document.case_id == ctx.case.id)).all()
    errs = validate(ctx.case.form, [{"filename": d.filename, "size_kb": d.size_kb, "status": d.status} for d in docs])
    return {"errors": errs}
