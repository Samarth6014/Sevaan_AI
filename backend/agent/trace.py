from sqlmodel import Session, select
from backend.core.pii import mask
from backend.models import TraceEntry


def log(session: Session, case_id: int, tool: str, inp: dict, out: dict, ok: bool = True) -> None:
    session.add(TraceEntry(case_id=case_id, tool=tool, input=mask(inp), output=mask(out), ok=ok))
    session.commit()


def for_case(session: Session, case_id: int) -> list[TraceEntry]:
    return list(session.exec(select(TraceEntry).where(TraceEntry.case_id == case_id).order_by(TraceEntry.id)))
