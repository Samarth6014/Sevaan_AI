from fastapi import HTTPException


class GuardrailViolation(Exception):
    """Raised when an action would break a non-negotiable rule."""


def forbidden(msg: str = "Not allowed") -> HTTPException:
    return HTTPException(status_code=403, detail=msg)


def not_found(msg: str = "Not found") -> HTTPException:
    return HTTPException(status_code=404, detail=msg)
