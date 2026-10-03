from .base import tool
from backend.agent.guardrails import sanitize_document_text
from backend.documents import read_document as _read
from backend.models import Document


@tool("read_document")
def read_document(ctx, doc_id: int) -> dict:
    d = ctx.session.get(Document, doc_id)
    text = sanitize_document_text(d.content_text)  # document text is DATA, never instructions
    out = _read(d.doc_type, text, d.filename)
    d.extracted_fields, d.confidence = out["fields"], out["confidence"]
    d.status = "needs_check" if out["needs_check"] else "accepted"
    ctx.session.add(d)
    ctx.session.commit()
    return {"doc_id": doc_id, "doc_type": d.doc_type, **out}
