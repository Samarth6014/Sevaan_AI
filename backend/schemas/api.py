"""FROZEN API models (only A edits, after telling the team)."""
from typing import Any, Optional
from pydantic import BaseModel


class OtpRequest(BaseModel):
    phone: str


class VerifyRequest(BaseModel):
    phone: str
    otp: str
    role: str = "citizen"  # DEMO ONLY: real role assignment needs a real identity provider


class TokenResponse(BaseModel):
    token: str
    role: str
    demo_only: bool = True


class CaseCreate(BaseModel):
    language: str = "en"
    channel: str = "web"


class MessageIn(BaseModel):
    text: Optional[str] = None
    audio_b64: Optional[str] = None  # speech adapter turns this into text


class MessageOut(BaseModel):
    reply: str
    stage: str
    needs_confirmation: bool = False
    summary: Optional[dict] = None
    options: list[str] = []


class ConfirmIn(BaseModel):
    decision: bool


class ConsentIn(BaseModel):
    case_id: int
    purpose: str
    language: str = "en"


class FeedbackIn(BaseModel):
    rating: int
    comment: str = ""


class SchemeEdit(BaseModel):
    deadline_date: Optional[str] = None
    deadline_note: Optional[str] = None
    faqs: Optional[list[dict[str, Any]]] = None


class AdvanceIn(BaseModel):
    rejected_reason: Optional[str] = None
