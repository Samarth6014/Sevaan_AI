from fastapi import APIRouter, HTTPException
from backend.auth.session import make_token, ROLES
from backend.core.config import settings
from backend.schemas.api import OtpRequest, VerifyRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/otp")
def send_otp(body: OtpRequest):
    return {"sent": True, "demo_only": True, "hint": "Demo OTP is fixed. No SMS is sent."}


@router.post("/verify", response_model=TokenResponse)
def verify(body: VerifyRequest):
    if body.otp != settings.demo_otp:
        raise HTTPException(status_code=401, detail="Wrong OTP")
    if body.role not in ROLES:
        raise HTTPException(status_code=400, detail="Unknown role")
    return TokenResponse(token=make_token(body.phone, body.role), role=body.role)
