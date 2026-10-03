"""Deterministic eligibility engine. NO LLM, agent or speech imports (dependency rule 4)."""
from typing import Any, Optional
from .schema import Scheme, Rule, Cond


def _eval_op(op: str, actual: Any, expected: Any) -> bool:
    if op == "<=":
        return actual <= expected
    if op == ">=":
        return actual >= expected
    if op == "==":
        return actual == expected
    if op == "in":
        return actual in expected
    if op == "not_in":
        return actual not in expected
    if op == "is_true":
        return bool(actual) is True
    if op == "is_false":
        return bool(actual) is False
    raise ValueError(f"unsupported op {op}")


def _cond(cond: Cond, profile: dict) -> Optional[bool]:
    v = profile.get(cond.field)
    if v is None:
        return None
    return _eval_op(cond.op, v, cond.value)


def eval_rule(rule: Rule, profile: dict) -> Optional[bool]:
    """True / False / None (unknown)."""
    v = profile.get(rule.field)
    if v is None:
        return None
    expected = rule.value
    if rule.relax and isinstance(expected, (int, float)):
        applies = _cond(rule.relax.if_, profile)
        base = _eval_op(rule.op, v, expected)
        if base:
            return True
        if applies is None:
            return None  # cannot tell whether relaxation applies
        if applies:
            shift = rule.relax.by
            if rule.op == ">=":
                expected = expected - shift
            elif rule.op == "<=":
                expected = expected + shift
    try:
        return _eval_op(rule.op, v, expected)
    except TypeError:
        return None


def check_eligibility(scheme: Scheme, profile: dict) -> dict:
    """profile: plain {field: value}. Returns result, reasons, failed_rules, missing_fields."""
    reasons, failed, missing = [], [], []
    any_false = any_unknown = False
    none_true = none_unknown = False

    if not scheme.eligibility.all_of and not scheme.eligibility.none_of:
        return {
            "scheme_id": scheme.scheme_id, "result": "unknown", "reasons": [
                {"rule_id": None, "text": "Rules for this scheme are not drafted yet. Ask a human helper.",
                 "outcome": "unknown"}],
            "failed_rules": [], "missing_fields": [], "verified": scheme.verified,
            "source": scheme.source_official_url,
        }

    for r in scheme.eligibility.all_of:
        out = eval_rule(r, profile)
        if out is True:
            reasons.append({"rule_id": r.id, "text": r.text, "outcome": "met"})
        elif out is False:
            any_false = True
            failed.append(r.id)
            reasons.append({"rule_id": r.id, "text": r.text, "outcome": "not_met"})
        else:
            any_unknown = True
            if r.field not in missing:
                missing.append(r.field)
            reasons.append({"rule_id": r.id, "text": r.text, "outcome": "unknown"})

    for r in scheme.eligibility.none_of:
        out = eval_rule(r, profile)
        if out is True:
            none_true = True
            failed.append(r.id)
            reasons.append({"rule_id": r.id, "text": r.text, "outcome": "excluded"})
        elif out is None:
            none_unknown = True
            if r.field not in missing:
                missing.append(r.field)
            reasons.append({"rule_id": r.id, "text": r.text, "outcome": "unknown"})

    if any_false or none_true:
        result = "not_eligible"
    elif any_unknown or none_unknown:
        result = "unknown"
    else:
        result = "eligible"
    return {
        "scheme_id": scheme.scheme_id, "result": result, "reasons": reasons,
        "failed_rules": failed, "missing_fields": missing, "verified": scheme.verified,
        "source": scheme.source_official_url,
    }
