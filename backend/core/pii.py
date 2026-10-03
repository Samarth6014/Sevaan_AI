"""Masks personal data before it reaches logs or the trace."""
import re

_PATTERNS = [
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"), "[AADHAAR]"),
    (re.compile(r"\b\d{10}\b"), "[PHONE]"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "[PAN]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
]
_SENSITIVE_KEYS = {"name", "phone", "aadhaar", "account_number", "bank_account", "ifsc", "address"}


def mask_text(s: str) -> str:
    for pat, repl in _PATTERNS:
        s = pat.sub(repl, s)
    return s


def mask(obj):
    if isinstance(obj, str):
        return mask_text(obj)
    if isinstance(obj, dict):
        return {k: ("[MASKED]" if k in _SENSITIVE_KEYS else mask(v)) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [mask(v) for v in obj]
    return obj
