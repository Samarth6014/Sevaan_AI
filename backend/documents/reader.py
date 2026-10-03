"""Document reading. Demo reads synthetic text sample docs ("key: value" lines).
[later] swap in a vision/OCR provider behind the same function signature."""
import re

# document field -> form/profile field
FIELD_MAP = {
    "income_certificate": {"annual_income": "family_income_annual", "holder": "student_name"},
    "caste_certificate": {"category": "category", "holder": "student_name"},
    "mark_sheet": {"marks_pct_class7": "marks_pct_class7", "holder": "student_name"},
}
LOW_CONFIDENCE = 0.8


def _coerce(v: str):
    v = v.strip()
    if re.fullmatch(r"-?\d+", v.replace(",", "")):
        return int(v.replace(",", ""))
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def read_document(doc_type: str, text: str, filename: str = "") -> dict:
    mapping = FIELD_MAP.get(doc_type, {})
    fields, lines_ok, lines_total = {}, 0, 0
    for line in text.splitlines():
        if not line.strip():
            continue
        lines_total += 1
        m = re.match(r"\s*([\w ]+?)\s*:\s*(.+)$", line)
        if not m:
            continue
        lines_ok += 1
        key = m.group(1).strip().lower().replace(" ", "_")
        if key in mapping:
            fields[mapping[key]] = _coerce(m.group(2))
    conf = 0.95 if lines_total and lines_ok == lines_total else 0.7
    if "noisy" in filename.lower():
        conf = min(conf, 0.6)  # noisy sample: forces a human check
    return {"fields": fields, "confidence": conf, "needs_check": conf < LOW_CONFIDENCE}
