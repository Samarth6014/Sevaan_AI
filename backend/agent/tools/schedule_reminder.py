from .base import tool
from backend.models import Notification


@tool("schedule_reminder")
def schedule_reminder(ctx, date: str | None, message: str) -> dict:
    n = Notification(owner_phone=ctx.case.owner_phone, case_id=ctx.case.id, message=message, due_date=date)
    ctx.session.add(n)
    ctx.session.commit()
    return {"reminder_id": n.id}  # in-app only; WhatsApp is roadmap
