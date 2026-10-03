"""Entry points used by the API. The loop is the scholarship workflow (more packs: agent/workflows/<id>.py)."""
from backend.agent.workflows.scholarship import handle_message, confirm, on_document_uploaded  # noqa: F401
