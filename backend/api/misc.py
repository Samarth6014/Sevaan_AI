from datetime import datetime
from backend.core.clock import now_utc
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.auth.access import get_case_for
from backend.auth.session import current_user, require_role
from backend.core.db import get_session
from backend.models import Consent, Feedback, Notification
from backend.schemas.api import ConsentIn, FeedbackIn

router = APIRouter(tags=["misc"])

NOTICE = {"data": "name, income, class, category, school type, marks, documents",
          "why": "to find schemes you qualify for and fill your application",
          "how_long": "until you delete your case", "withdraw": "Revoke consent or delete your case any time",
          "complain": "Contact the (simulated) grievance officer", "demo_only": True}


@router.get("/api/consent/notice")
def notice():
    return NOTICE


@router.post("/api/consent")
def grant(body: ConsentIn, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    get_case_for(session, body.case_id, user)
    c = Consent(case_id=body.case_id, purpose=body.purpose, language=body.language)
    session.add(c); session.commit(); session.refresh(c)
    return {"id": c.id, "purpose": c.purpose, "status": c.status}


@router.get("/api/consent/{case_id}")
def ledger(case_id: int, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    get_case_for(session, case_id, user)
    return [{"id": c.id, "purpose": c.purpose, "language": c.language, "status": c.status,
             "created_at": c.created_at.isoformat(), "revoked_at": c.revoked_at.isoformat() if c.revoked_at else None}
            for c in session.exec(select(Consent).where(Consent.case_id == case_id))]


@router.post("/api/consent/{consent_id}/revoke")
def revoke(consent_id: int, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = session.get(Consent, consent_id)
    if not c:
        raise HTTPException(404, "Consent not found")
    get_case_for(session, c.case_id, user)
    c.status, c.revoked_at = "revoked", now_utc()
    session.add(c); session.commit()
    return {"status": "revoked"}


@router.post("/api/cases/{case_id}/feedback")
def feedback(case_id: int, body: FeedbackIn, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    get_case_for(session, case_id, user)
    if not 1 <= body.rating <= 5:
        raise HTTPException(400, "Rating must be 1 to 5")
    session.add(Feedback(case_id=case_id, rating=body.rating, comment=body.comment)); session.commit()
    return {"saved": True}


@router.get("/api/notifications")
def notifications(user=Depends(current_user), session: Session = Depends(get_session)):
    rows = session.exec(select(Notification).where(Notification.owner_phone == user["phone"]).order_by(Notification.id.desc()))
    return [{"id": n.id, "case_id": n.case_id, "message": n.message, "due_date": n.due_date, "read": n.read} for n in rows]
