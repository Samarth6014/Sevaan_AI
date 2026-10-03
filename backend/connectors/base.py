"""Connector interface. The agent only ever uses this (dependency rule 5)."""
from abc import ABC, abstractmethod


class PortalConnector(ABC):
    @abstractmethod
    def register_otr(self, student_ref: str) -> str: ...

    @abstractmethod
    def upload_document(self, filename: str, size_kb: int, doc_type: str) -> dict:
        """Returns {"ok": True, "doc_id": ...} or {"ok": False, "error": ...}."""

    @abstractmethod
    def submit_application(self, otr_id: str, scheme_id: str, form: dict, doc_ids: list, confirmation_token: str) -> str: ...

    @abstractmethod
    def get_status(self, application_id: str) -> dict: ...

    @abstractmethod
    def advance(self, application_id: str, rejected_reason: str | None = None) -> dict: ...


class DocumentVault(ABC):
    @abstractmethod
    def consent(self, case_ref: str) -> bool: ...

    @abstractmethod
    def fetch(self, doc_type: str) -> dict | None: ...
