from datetime import datetime
from backend.core.clock import now_utc
from typing import Optional
from sqlmodel import SQLModel, Field


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_phone: str = Field(index=True)
    case_id: Optional[int] = None
    message: str
    due_date: Optional[str] = None
    read: bool = False
    created_at: datetime = Field(default_factory=now_utc)


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(index=True)
    rating: int
    comment: str = ""
    created_at: datetime = Field(default_factory=now_utc)


class SchemeOverride(SQLModel, table=True):
    """Admin edits (deadline, FAQs) stored separately so pack files stay untouched."""
    scheme_id: str = Field(primary_key=True)
    deadline_date: Optional[str] = None
    deadline_note: Optional[str] = None
    faqs_json: Optional[str] = None
