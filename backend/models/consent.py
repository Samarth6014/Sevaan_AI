from datetime import datetime
from backend.core.clock import now_utc
from typing import Optional
from sqlmodel import SQLModel, Field


class Consent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(index=True)
    purpose: str            # per-purpose, never bundled
    language: str = "en"
    status: str = "granted"  # granted | revoked
    created_at: datetime = Field(default_factory=now_utc)
    revoked_at: Optional[datetime] = None
