FORM_FIELDS = ["student_name", "category", "family_income_annual", "current_level",
               "institution_type", "marks_pct_class7"]


def _same(a, b) -> bool:
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return str(a).strip().lower() == str(b).strip().lower()


def prefill(profile: dict, doc_fields: list[dict]) -> dict:
    """profile: {field: {value, source, confidence}}; doc_fields: [{doc_type, fields}].
    Conflicts are surfaced, never resolved silently."""
    form: dict = {}
    for f in FORM_FIELDS:
        p = profile.get(f)
        candidates = [(d["doc_type"], d["fields"][f]) for d in doc_fields if f in d["fields"]]
        entry = None
        if p is not None:
            entry = {"value": p["value"], "source": p.get("source", "spoken"), "confidence": p.get("confidence", 0.9)}
        for doc_type, val in candidates:
            if entry is None:
                entry = {"value": val, "source": f"document:{doc_type}", "confidence": 0.95}
            elif not _same(entry["value"], val):
                entry["conflict"] = {"profile": entry["value"], f"document:{doc_type}": val}
        if entry is not None:
            form[f] = entry
    return form
