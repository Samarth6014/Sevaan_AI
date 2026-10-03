from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.core.db import get_session
from backend.models import SchemeOverride
from backend.rules import load_all
import json

router = APIRouter(prefix="/api/schemes", tags=["catalogue"])


def _public(s, ov: SchemeOverride | None):
    d = s.model_dump()
    if ov:
        if ov.deadline_date is not None:
            d["deadline"]["date"] = ov.deadline_date
        if ov.deadline_note is not None:
            d["deadline"]["note"] = ov.deadline_note
        if ov.faqs_json:
            d["faqs"] = json.loads(ov.faqs_json)
    return d


@router.get("")
def list_schemes(q: str = "", level: str = "", category: str = "", ministry: str = "",
                 session: Session = Depends(get_session)):
    out = []
    for s in load_all().values():
        hay = f"{s.name} {s.ministry}".lower()
        if q and q.lower() not in hay:
            continue
        if level and s.level != level:
            continue
        if category and category not in s.categories:
            continue
        if ministry and ministry.lower() not in s.ministry.lower():
            continue
        out.append({"scheme_id": s.scheme_id, "name": s.name, "ministry": s.ministry, "level": s.level,
                    "verified": s.verified, "drafted": s.drafted, "categories": s.categories})
    return out


@router.get("/{scheme_id}")
def get_scheme(scheme_id: str, session: Session = Depends(get_session)):
    s = load_all().get(scheme_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return _public(s, session.get(SchemeOverride, scheme_id))
