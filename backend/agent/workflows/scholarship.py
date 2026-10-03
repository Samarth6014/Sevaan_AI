"""Scholarship workflow: Observe -> Plan -> Act (one tool at a time) -> Check -> Re-plan / Ask."""
from sqlmodel import Session, select
from backend.agent import tools as T  # noqa: F401  (registers tools)
from backend.agent.tools.extract_profile import missing_fields
from backend.agent.guardrails import looks_like_injection
from backend.agent.llm import get_llm
from backend.agent.prompts.base import load as load_prompts
from backend.agent.tools.base import ToolContext, call, plain_profile
from backend.agent import trace
from backend.connectors import get_connector
from backend.core.errors import GuardrailViolation
from backend.models import Case, Document
from backend.rules import load_all
from .base import QUESTION_ORDER, DONT_KNOW, is_yes, is_no


def _ctx(session: Session, case: Case) -> ToolContext:
    return ToolContext(session=session, case=case, connector=get_connector(), llm=get_llm())


def _state(case: Case) -> dict:
    return dict((case.profile or {}).get("__state__", {}))


def _set_state(ctx: ToolContext, **kw) -> None:
    prof = dict(ctx.case.profile or {})
    st = dict(prof.get("__state__", {}))
    st.update(kw)
    prof["__state__"] = st
    ctx.case.profile = prof
    ctx.save()


def _out(ctx, reply, **extra) -> dict:
    conv = list(ctx.case.conversation or [])
    conv.append({"role": "agent", "text": reply})
    ctx.case.conversation = conv
    ctx.save()
    return {"reply": reply, "stage": ctx.case.stage, "needs_confirmation": ctx.case.stage == "REVIEW_CONFIRM",
            "summary": extra.get("summary"), "options": extra.get("options", [])}


def _ask_next(ctx, P) -> dict:
    missing = missing_fields(ctx)
    todo = [f for f in QUESTION_ORDER if f in missing] + [f for f in missing if f not in QUESTION_ORDER]
    if todo:
        f = todo[0]
        _set_state(ctx, expecting=f)
        return _out(ctx, P.get(f"q_{f}", f"Please tell me your {f}."))
    return _do_match(ctx, P)


def _do_match(ctx, P) -> dict:
    ctx.case.stage = "MATCH"
    ranked = call(ctx, "rank_schemes")
    schemes = load_all()
    lines, options = [P["matched_header"]], []
    for i, e in enumerate(ranked["eligible"], 1):
        options.append(e["scheme_id"])
        if e["verified"]:
            lines.append(f"{i}. " + P["eligible_line"].format(name=e["name"]))
        else:
            lines.append(f"{i}. Potential match for {e['name']}; rules are not yet human-verified.")
        met = [r for r in e.get("reasons", []) if r.get("outcome") == "met"]
        if met:
            rule_ids = ", ".join(r["rule_id"] for r in met if r.get("rule_id"))
            if rule_ids:
                lines.append(f"   Rules met: {rule_ids}")
        if e.get("source"):
            lines.append(f"   Source: {e['source']}")
    for n in ranked["not_eligible"]:
        why = "; ".join(r["text"] for r in n["reasons"]) or "-"
        lines.append(P["not_eligible_line"].format(name=n["name"], why=why))
        rule_ids = ", ".join(r["rule_id"] for r in n.get("reasons", []) if r.get("rule_id"))
        if rule_ids:
            lines.append(f"   Rules checked: {rule_ids}")
        if n.get("source"):
            lines.append(f"   Source: {n['source']}")
    drafted_unknown = [u for u in ranked["unknown"] if u["drafted"]]
    for u in drafted_unknown:
        lines.append(P["unknown_line"].format(name=u["name"], why="missing " + ", ".join(u["missing_fields"])))
        if u.get("source"):
            lines.append(f"   Source: {u['source']}")
    undrafted = [u for u in ranked["unknown"] if not u["drafted"]]
    if undrafted:
        lines.append(f"{len(undrafted)} other schemes are not checked yet because their rules are not drafted. A human helper can check them.")
    if ranked["conflicts"]:
        names = ", ".join(schemes[s].name for grp in ranked["conflicts"] for s in grp)
        lines.append(P["conflict"].format(names=names))
    if not options:
        lines.append(P["no_scheme"])
        ctx.case.recommended_scheme_ids = []
        ctx.save()
        return _out(ctx, "\n".join(lines))
    ctx.case.recommended_scheme_ids = ranked["recommended"]
    ctx.case.schemes_considered = [{"scheme_id": e["scheme_id"], "result": "eligible"} for e in ranked["eligible"]]
    ctx.save()
    _set_state(ctx, options=options)
    lines.append(P["choose"])
    return _out(ctx, "\n".join(lines), options=options)


def _do_plan(ctx, P, scheme_id) -> dict:
    s = load_all()[scheme_id]
    ctx.case.chosen_scheme_id = scheme_id
    ctx.case.stage = "PLAN"
    ctx.save()
    plan = call(ctx, "plan_documents", scheme_id=scheme_id)
    lines = [P["plan_header"].format(name=s.name)]
    for m in plan["missing"]:
        lines.append(P["plan_missing"].format(label=m["label"], where=m["where_to_get"]))
    if not plan["missing"]:
        lines.append(P["plan_ok"])
    else:
        lines.append(P["plan_next"])
        call(ctx, "schedule_reminder", date=s.deadline.date, message=f"Missing documents for {s.name}: " + ", ".join(m["label"] for m in plan["missing"]))
    lines.append(P["deadline"].format(deadline=s.deadline.date or s.deadline.note))
    ctx.case.stage = "COLLECT"
    ctx.save()
    return _out(ctx, "\n".join(lines))


def _do_fill(ctx, P) -> dict:
    ctx.case.stage = "FILL"
    ctx.save()
    sid = ctx.case.chosen_scheme_id
    call(ctx, "prefill_form", scheme_id=sid)
    errs = call(ctx, "validate_form")["errors"]
    if errs:
        ctx.case.stage = "COLLECT"
        ctx.save()
        return _out(ctx, P["fill_errors"].format(errors=" ".join(errs)))
    ctx.case.stage = "REVIEW_CONFIRM"
    ctx.save()
    summary = {k: v["value"] for k, v in ctx.case.form.items()}
    sources = {k: v["source"] for k, v in ctx.case.form.items()}
    lines = [P["review_header"]] + [f"- {k}: {v} (from {sources[k]})" for k, v in summary.items()]
    return _out(ctx, "\n".join(lines), summary=summary)


def _do_submit(ctx, P) -> dict:
    ctx.case.stage = "SUBMIT"
    ctx.save()
    try:
        res = call(ctx, "submit_application")
    except GuardrailViolation:
        ctx.case.stage = "REVIEW_CONFIRM"
        ctx.save()
        return _out(ctx, P["refused"])
    ctx.case.stage = "TRACK"
    ctx.save()
    return _out(ctx, P["submitted"].format(app_id=res["application_id"], status=res["status"]))


def confirm(session: Session, case: Case, decision: bool) -> dict:
    ctx, P = _ctx(session, case), load_prompts(case.language)
    if case.stage != "REVIEW_CONFIRM":
        return _out(ctx, P["refused"])
    call(ctx, "request_confirmation", decision=decision)
    if not decision:
        return _out(ctx, P["declined"])
    return _do_submit(ctx, P)


def on_document_uploaded(session: Session, case: Case, doc: Document) -> dict:
    ctx, P = _ctx(session, case), load_prompts(case.language)
    res = call(ctx, "read_document", doc_id=doc.id)
    msg = f"Read {doc.doc_type}: " + ", ".join(f"{k}={v}" for k, v in res["fields"].items())
    if res["needs_check"]:
        msg += " (low confidence: a human should check this document)"
    plan = call(ctx, "plan_documents", scheme_id=case.chosen_scheme_id) if case.chosen_scheme_id else {"missing": []}
    msg += ". " + (P["plan_ok"] if not plan["missing"] else "Still missing: " + ", ".join(m["label"] for m in plan["missing"]) + ".")
    return _out(ctx, msg)


def handle_message(session: Session, case: Case, text: str) -> dict:
    ctx, P = _ctx(session, case), load_prompts(case.language)
    first = not case.conversation
    conv = list(case.conversation or [])
    conv.append({"role": "user", "text": text})
    case.conversation = conv
    ctx.save()

    if looks_like_injection(text):  # treated as data: no state change, no tool run
        trace.log(session, case.id, "guardrail", {"text": text}, {"blocked": "injection"}, ok=False)
        return _out(ctx, P["refused"])

    t = text.strip().lower()
    st = _state(case)
    stage = case.stage

    if stage == "INTAKE":
        pre = P["greet"] + "\n" if first else ""
        pending = st.get("pending")
        if pending:
            if is_yes(t):
                prof = dict(case.profile); prof[pending["field"]] = {"value": pending["value"], "source": "spoken", "confidence": 1.0}
                case.profile = prof; ctx.save()
            _set_state(ctx, pending=None)
            r = _ask_next(ctx, P)
            r["reply"] = pre + r["reply"]
            return r
        if any(p in t for p in DONT_KNOW) and st.get("expecting"):
            prof = dict(case.profile)
            prof["__skipped__"] = list(prof.get("__skipped__", [])) + [st["expecting"]]
            case.profile = prof; ctx.save()
            r = _ask_next(ctx, P)
            r["reply"] = pre + P["unknown_noted"] + "\n" + r["reply"]
            return r
        res = call(ctx, "extract_profile", text=text, expecting=st.get("expecting"))
        if res["needs_confirmation"]:
            f, v = next(iter(res["needs_confirmation"].items()))
            _set_state(ctx, pending={"field": f, "value": v})
            return _out(ctx, pre + P["heard"].format(field=f, value=v))
        r = _ask_next(ctx, P)
        r["reply"] = pre + r["reply"]
        return r

    if stage == "MATCH":
        options = st.get("options", [])
        schemes = load_all()
        pick = None
        if t.isdigit() and 1 <= int(t) <= len(options):
            pick = options[int(t) - 1]
        else:
            pick = next((o for o in options if o in t or schemes[o].name.lower() in t), None)
        if pick:
            return _do_plan(ctx, P, pick)
        call(ctx, "extract_profile", text=text)  # citizen may be correcting a fact: re-plan
        return _do_match(ctx, P)

    if stage == "COLLECT":
        if t in ("continue", "next", "done"):
            plan = call(ctx, "plan_documents", scheme_id=case.chosen_scheme_id)
            if plan["missing"]:
                call(ctx, "schedule_reminder", date=None, message="Upload missing documents: " + ", ".join(m["label"] for m in plan["missing"]))
                return _out(ctx, "Some documents are still missing. I set a reminder. Upload them when you have them, then say 'continue'.")
            return _do_fill(ctx, P)
        return _out(ctx, P["plan_next"])

    if stage == "REVIEW_CONFIRM":
        if is_yes(t):
            return confirm(session, case, True)
        if is_no(t):
            return confirm(session, case, False)
        res = call(ctx, "extract_profile", text=text)  # changed a fact: refill, token invalidated
        if res["accepted"]:
            return _do_fill(ctx, P)
        return _out(ctx, P["review_header"])

    if stage == "TRACK":
        st2 = call(ctx, "track_status")
        return _out(ctx, P["tracking"].format(status=st2["status"]))

    return _out(ctx, P["refused"])
