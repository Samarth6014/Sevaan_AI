from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(index=True)
    doc_type: str
    filename: str
    size_kb: int = 0
    extracted_fields: dict = Field(default_factory=dict, sa_column=Column(JSON))
    confidence: float = 0.0
    status: str = "uploaded"  # uploaded | needs_check | accepted | rejected
    content_text: str = ""    # sample docs only (synthetic)
