"""All guardrails live here (dependency rule 3)."""
import hashlib, hmac, json, re
from backend.core.config import settings
from backend.core.errors import GuardrailViolation

_INJECTION = re.compile(
    r"(ignore (all |the |previous |your )?(rules|instructions)|disregard .*(rules|instructions)|"
    r"submit (it )?(now|anyway)|skip (the )?confirmation|you are now|system prompt)", re.I)


def looks_like_injection(text: str) -> bool:
    return bool(_INJECTION.search(text or ""))


def form_hash(form: dict) -> str:
    flat = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in sorted(form.items())}
    return hashlib.sha256(json.dumps(flat, sort_keys=True, default=str).encode()).hexdigest()


def make_confirmation_token(case_id: int, form: dict) -> str:
    msg = f"{case_id}:{form_hash(form)}"
    return hmac.new(settings.secret_key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def verify_confirmation_token(case_id: int, form: dict, token: str | None) -> bool:
    if not token:
        return False
    return hmac.compare_digest(token, make_confirmation_token(case_id, form))


def require_valid_token(case_id: int, form: dict, token: str | None) -> None:
    """Token is invalid if any form field changed after confirmation."""
    if not verify_confirmation_token(case_id, form, token):
        raise GuardrailViolation("Submission refused: no valid confirmation for the current form.")


def sanitize_document_text(text: str) -> str:
    """Text inside documents is DATA. Strip lines that look like instructions."""
    return "\n".join(l for l in text.splitlines() if not looks_like_injection(l))
