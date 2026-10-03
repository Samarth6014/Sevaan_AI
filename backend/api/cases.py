from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session, select
from backend.agent import loop, trace
from backend.auth.access import get_case_for
from backend.auth.session import current_user, require_role
from backend.connectors import get_connector
from backend.core.db import get_session
from backend.core.errors import forbidden
from backend.models import Case, Document, Consent, Feedback, Notification
from backend.schemas.api import CaseCreate, MessageIn, MessageOut, ConfirmIn
from backend.speech.adapter import transcribe, SpeechUnavailable

router = APIRouter(prefix="/api/cases", tags=["cases"])


def _meta(c: Case) -> dict:
    return {"id": c.id, "language": c.language, "stage": c.stage, "status": c.status,
            "chosen_scheme_id": c.chosen_scheme_id, "application_id": c.application_id,
            "created_at": c.created_at.isoformat()}


@router.post("")
def create_case(body: CaseCreate, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = Case(owner_phone=user["phone"], language=body.language, channel=body.channel)
    session.add(c); session.commit(); session.refresh(c)
    return _meta(c)


@router.get("")
def list_cases(user=Depends(current_user), session: Session = Depends(get_session)):
    cases = session.exec(select(Case)).all()
    if user["role"] == "citizen":
        cases = [c for c in cases if c.owner_phone == user["phone"]]
    elif user["role"] == "helper":
        cases = [c for c in cases if user["phone"] in (c.granted_helpers or [])]
    return [_meta(c) for c in cases]  # admin sees metadata only


@router.get("/{case_id}")
def get_case(case_id: int, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user)
    return {**_meta(c), "conversation": c.conversation, "form": c.form}


@router.delete("/{case_id}")
def delete_case(case_id: int, user=Depends(require_role("citizen")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user)
    for model in (Document, Consent, Feedback, Notification):
        for row in session.exec(select(model).where(model.case_id == case_id)):
            session.delete(row)
    for t in trace.for_case(session, case_id):
        session.delete(t)
    session.delete(c); session.commit()
    return {"deleted": True}


@router.post("/{case_id}/grant")
def grant_helper(case_id: int, helper_phone: str, user=Depends(require_role("citizen")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user)
    c.granted_helpers = list(c.granted_helpers or []) + [helper_phone]
    session.add(c); session.commit()
    return {"granted": helper_phone}


@router.post("/{case_id}/message", response_model=MessageOut)
def message(case_id: int, body: MessageIn, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user)
    if not session.exec(select(Consent).where(Consent.case_id == case_id, Consent.status == "granted")).first():
        raise forbidden("Consent notice must be accepted before any data is collected")
    text = body.text or ""
    if body.audio_b64:
        try:
            stt = transcribe(body.audio_b64, c.language)
        except SpeechUnavailable as e:
            return MessageOut(reply=str(e), stage=c.stage)
        text = stt["text"]
    return MessageOut(**loop.handle_message(session, c, text))


@router.post("/{case_id}/confirm", response_model=MessageOut)
def confirm(case_id: int, body: ConfirmIn, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user)
    return MessageOut(**loop.confirm(session, c, body.decision))


@router.get("/{case_id}/trace")
def get_trace(case_id: int, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    get_case_for(session, case_id, user)
    return [{"ts": t.ts.isoformat(), "tool": t.tool, "input": t.input, "output": t.output, "ok": t.ok}
            for t in trace.for_case(session, case_id)]


@router.post("/{case_id}/documents")
async def upload_document(case_id: int, doc_type: str = Form(...), file: UploadFile = File(...),
                          user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    c = get_case_for(session, case_id, user, documents=True)
    raw = await file.read()
    size_kb = max(1, (len(raw) + 1023) // 1024)
    res = get_connector().upload_document(file.filename, size_kb, doc_type)
    if not res["ok"]:
        return {"ok": False, "error": res["error"]}
    d = Document(case_id=case_id, doc_type=doc_type, filename=file.filename, size_kb=size_kb,
                 content_text=raw.decode("utf-8", errors="ignore") if file.filename.endswith(".txt") else "")
    session.add(d); session.commit(); session.refresh(d)
    return {"ok": True, "doc_id": d.id, **loop.on_document_uploaded(session, c, d)}


@router.get("/{case_id}/documents")
def list_documents(case_id: int, user=Depends(require_role("citizen", "helper")), session: Session = Depends(get_session)):
    get_case_for(session, case_id, user, documents=True)
    return [{"id": d.id, "doc_type": d.doc_type, "filename": d.filename, "status": d.status, "confidence": d.confidence}
            for d in session.exec(select(Document).where(Document.case_id == case_id))]


@router.delete("/{case_id}/documents/{doc_id}")
def delete_document(case_id: int, doc_id: int, user=Depends(require_role("citizen")), session: Session = Depends(get_session)):
    get_case_for(session, case_id, user, documents=True)
    d = session.get(Document, doc_id)
    if d and d.case_id == case_id:
        session.delete(d); session.commit()
    return {"deleted": True}
