"""FROZEN: rule-file schema (only A edits, after telling the team). Pure data, no LLM imports."""
from typing import Any, Optional
from pydantic import BaseModel, Field

PROFILE_FIELDS = [
    "age", "gender", "state", "category", "minority_community", "disability_percent",
    "family_income_annual", "current_level", "institution_type", "institution_recognized",
    "study_mode", "marks_pct_class7", "marks_pct_class10", "marks_pct_class12",
    "class12_board_percentile", "receiving_other_scholarship", "orphan",
    "parent_in_armed_or_police_services", "domicile_state",
]
OPS = ["<=", ">=", "==", "in", "not_in", "is_true", "is_false"]


class Cond(BaseModel):
    field: str
    op: str
    value: Any = None


class Relax(BaseModel):
    if_: Cond = Field(alias="if")
    by: float
    model_config = {"populate_by_name": True}


class Rule(BaseModel):
    id: str
    field: str
    op: str
    value: Any = None
    text: str = ""
    needs_verification: bool = False
    relax: Optional[Relax] = None


class Eligibility(BaseModel):
    all_of: list[Rule] = []
    none_of: list[Rule] = []


class DocWhere(BaseModel):
    office: str = "verify"
    carry: list[str] = []
    note: str = "verify"


class DocSpec(BaseModel):
    id: str
    label: str
    required: bool = True
    condition: Optional[str] = None  # e.g. "category in SC,ST,OBC"
    where_to_get: DocWhere = DocWhere()


class Benefit(BaseModel):
    text: str = ""
    amount_per_year: Optional[float] = None


class Deadline(BaseModel):
    date: Optional[str] = None
    note: str = "verify on official portal"


class FAQ(BaseModel):
    q: str
    a: str


class Scheme(BaseModel):
    scheme_id: str
    name: str
    ministry: str = ""
    level: str = "central"
    portal: str = "scholarships.gov.in"
    source_dataset_slug: str = ""
    source_official_url: str = ""
    verified: bool = False
    verified_by: Optional[str] = None
    exclusive_group: Optional[str] = None
    eligibility: Eligibility = Eligibility()
    benefit: Benefit = Benefit()
    documents: list[DocSpec] = []
    faqs: list[FAQ] = []
    deadline: Deadline = Deadline()
    categories: list[str] = []
    drafted: bool = False  # True once human/LLM-drafted rules exist
