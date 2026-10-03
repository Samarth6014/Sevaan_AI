"""Simulated government services exposed for the demo (/mock/*)."""
from fastapi import APIRouter, File, Form, UploadFile
from backend.connectors.mock.digilocker import digilocker
from backend.connectors.mock.nsp import nsp
from backend.rules import load_all

router = APIRouter(prefix="/mock", tags=["mock-government-simulation"])


@router.post("/otr/register")
def register(student_ref: str):
    return {"otr_id": nsp.register_otr(student_ref)}


@router.get("/schemes")
def schemes():
    return [{"scheme_id": s.scheme_id, "name": s.name, "form_fields": ["student_name", "category", "family_income_annual",
             "current_level", "institution_type", "marks_pct_class7"]} for s in load_all().values()]


@router.post("/documents")
async def upload_document(doc_type: str = Form(...), file: UploadFile = File(...)):
    raw = await file.read()
    size_kb = max(1, (len(raw) + 1023) // 1024)
    return nsp.upload_document(file.filename, size_kb, doc_type)


@router.get("/applications/{app_id}")
def status(app_id: str):
    return nsp.get_status(app_id)


@router.post("/digilocker/consent")
def dl_consent(case_ref: str):
    return {"consented": digilocker.consent(case_ref), "simulated": True}


@router.get("/digilocker/doc/{doc_type}")
def dl_doc(doc_type: str):
    return digilocker.fetch(doc_type) or {"error": "not found"}
