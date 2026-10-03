import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.auth.session import require_role
from backend.connectors import get_connector
from backend.core.db import get_session
from backend.models import Case, Feedback, SchemeOverride
from backend.rules import load_all
from backend.schemas.api import SchemeEdit, AdvanceIn
from .analytics import compute

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_role("admin"))])


@router.get("/cases")
def cases(session: Session = Depends(get_session)):
    # metadata only: no profile, no documents, no conversation
    return [{"id": c.id, "stage": c.stage, "status": c.status, "scheme": c.chosen_scheme_id,
             "application_id": c.application_id, "language": c.language} for c in session.exec(select(Case))]


@router.get("/analytics")
def analytics(session: Session = Depends(get_session)):
    return compute(session)


@router.put("/schemes/{scheme_id}")
def edit_scheme(scheme_id: str, body: SchemeEdit, session: Session = Depends(get_session)):
    if scheme_id not in load_all():
        raise HTTPException(404, "Scheme not found")
    ov = session.get(SchemeOverride, scheme_id) or SchemeOverride(scheme_id=scheme_id)
    if body.deadline_date is not None:
        ov.deadline_date = body.deadline_date
    if body.deadline_note is not None:
        ov.deadline_note = body.deadline_note
    if body.faqs is not None:
        ov.faqs_json = json.dumps(body.faqs, ensure_ascii=False)
    session.add(ov); session.commit()
    return {"saved": True}


@router.post("/cases/{case_id}/advance")
def advance(case_id: int, body: AdvanceIn, session: Session = Depends(get_session)):
    c = session.get(Case, case_id)
    if not c or not c.application_id:
        raise HTTPException(404, "No submitted application for this case")
    st = get_connector().advance(c.application_id, body.rejected_reason)
    c.status, c.status_history = st["status"], st["history"]
    session.add(c); session.commit()
    return st
