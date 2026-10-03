"""Mock OTP login. SIMULATION ONLY: the UI shows a 'demo only' banner."""
import base64, hashlib, hmac, json
from fastapi import Depends, Header, HTTPException
from backend.core.config import settings

ROLES = {"citizen", "helper", "admin"}


def _sig(payload: str) -> str:
    return hmac.new(settings.secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()


def make_token(phone: str, role: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"phone": phone, "role": role}).encode()).decode()
    return f"{payload}.{_sig(payload)}"


def parse_token(token: str) -> dict:
    try:
        payload, sig = token.split(".", 1)
        if not hmac.compare_digest(sig, _sig(payload)):
            raise ValueError
        return json.loads(base64.urlsafe_b64decode(payload.encode()))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")


def current_user(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Login required")
    return parse_token(authorization[7:])


def require_role(*roles: str):
    def dep(user: dict = Depends(current_user)) -> dict:
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Role not allowed")
        return user
    return dep
