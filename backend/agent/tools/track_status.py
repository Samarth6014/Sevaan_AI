from .base import tool


@tool("track_status")
def track_status(ctx) -> dict:
    st = ctx.connector.get_status(ctx.case.application_id)
    ctx.case.status, ctx.case.status_history = st["status"], st["history"]
    ctx.save()
    return st
