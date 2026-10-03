from backend.core.config import settings
from .base import PortalConnector


def get_connector() -> PortalConnector:
    if settings.connector_mode == "real":
        raise NotImplementedError("Real connectors are roadmap items: add connectors/real/<x>.py")
    from .mock.nsp import nsp
    return nsp
