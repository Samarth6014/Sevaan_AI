from datetime import datetime
from backend.core.clock import now_utc
from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON


class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_phone: str = Field(index=True)
    language: str = "en"
    channel: str = "web"
    stage: str = "INTAKE"
    created_at: datetime = Field(default_factory=now_utc)
    profile: dict = Field(default_factory=dict, sa_column=Column(JSON))          # field -> {value, source, confidence}
    schemes_considered: list = Field(default_factory=list, sa_column=Column(JSON))
    recommended_scheme_ids: list = Field(default_factory=list, sa_column=Column(JSON))
    chosen_scheme_id: Optional[str] = None
    form: dict = Field(default_factory=dict, sa_column=Column(JSON))             # field -> {value, source, confidence}
    confirmation: dict = Field(default_factory=dict, sa_column=Column(JSON))
    application_id: Optional[str] = None
    status: str = "Draft"
    status_history: list = Field(default_factory=list, sa_column=Column(JSON))
    granted_helpers: list = Field(default_factory=list, sa_column=Column(JSON))  # helper phones allowed
    conversation: list = Field(default_factory=list, sa_column=Column(JSON))
