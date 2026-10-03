"""FROZEN tool contracts (only A edits). Every call is traced with masked data."""
from dataclasses import dataclass
from typing import Any, Callable
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import Session
from backend.agent import trace
from backend.agent.llm import LLM
from backend.connectors.base import PortalConnector
from backend.models import Case

REGISTRY: dict[str, Callable[..., dict]] = {}
JSON_COLS = ["profile", "schemes_considered", "recommended_scheme_ids", "form", "confirmation",
             "status_history", "granted_helpers", "conversation"]


@dataclass
class ToolContext:
    session: Session
    case: Case
    connector: PortalConnector
    llm: LLM

    def save(self) -> None:
        for c in JSON_COLS:
            getattr(self.case, c)  # load if expired by an earlier commit
            flag_modified(self.case, c)
        self.session.add(self.case)
        self.session.commit()
        self.session.refresh(self.case)


def tool(name: str):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


def plain_profile(case: Case) -> dict:
    return {k: v["value"] for k, v in (case.profile or {}).items() if not k.startswith("__") and isinstance(v, dict)}


def call(ctx: ToolContext, name: str, **kwargs) -> dict:
    try:
        out = REGISTRY[name](ctx, **kwargs)
        trace.log(ctx.session, ctx.case.id, name, kwargs, out, ok=True)
        return out
    except Exception as e:  # guardrail refusals are logged too
        trace.log(ctx.session, ctx.case.id, name, kwargs, {"error": str(e)}, ok=False)
        raise
