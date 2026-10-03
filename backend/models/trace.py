from datetime import datetime
from backend.core.clock import now_utc
from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON


class TraceEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(index=True)
    ts: datetime = Field(default_factory=now_utc)
    tool: str
    input: dict = Field(default_factory=dict, sa_column=Column(JSON))
    output: dict = Field(default_factory=dict, sa_column=Column(JSON))
    ok: bool = True
