"""Least privilege: citizens see own cases; helpers only granted cases; admins metadata only."""
from backend.core.errors import forbidden, not_found
from backend.models import Case


def get_case_for(session, case_id: int, user: dict, *, documents: bool = False) -> Case:
    case = session.get(Case, case_id)
    if not case:
        raise not_found("Case not found")
    role, phone = user["role"], user["phone"]
    if role == "citizen" and case.owner_phone == phone:
        return case
    if role == "helper" and phone in (case.granted_helpers or []):
        return case
    if role == "admin" and not documents:
        return case  # metadata routes only
    raise forbidden("You do not have access to this case")
