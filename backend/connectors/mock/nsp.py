"""Mock National Scholarship Portal. Simulated: no external calls."""
import itertools
from backend.core.config import settings
from backend.connectors.base import PortalConnector

STATUSES = ["Submitted", "Under institute verification", "Under nodal verification", "Approved"]
ALLOWED_FORMATS = {"pdf", "jpg", "jpeg", "png", "txt"}  # txt only for synthetic sample docs


class MockNSP(PortalConnector):
    def __init__(self):
        self._otr: dict[str, str] = {}
        self._docs: dict[str, dict] = {}
        self._apps: dict[str, dict] = {}
        self._ids = itertools.count(1)

    def register_otr(self, student_ref: str) -> str:
        return self._otr.setdefault(student_ref, f"OTR{next(self._ids):06d}")

    def upload_document(self, filename: str, size_kb: int, doc_type: str) -> dict:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_FORMATS:
            return {"ok": False, "error": f"Format .{ext} not allowed. Use PDF, JPG or PNG."}
        if size_kb > settings.max_upload_kb:
            return {"ok": False, "error": f"File is {size_kb} KB; the limit is {settings.max_upload_kb} KB."}
        doc_id = f"DOC{next(self._ids):06d}"
        self._docs[doc_id] = {"filename": filename, "type": doc_type}
        return {"ok": True, "doc_id": doc_id}

    def submit_application(self, otr_id, scheme_id, form, doc_ids, confirmation_token) -> str:
        if not (otr_id and scheme_id and confirmation_token):
            raise ValueError("otr_id, scheme_id and confirmation_token are required")
        app_id = f"APP{next(self._ids):06d}"
        self._apps[app_id] = {"scheme_id": scheme_id, "index": 0, "history": [STATUSES[0]], "rejected": None}
        return app_id

    def get_status(self, application_id: str) -> dict:
        a = self._apps.get(application_id)
        if not a:
            return {"status": "Unknown", "history": []}
        status = "Rejected" if a["rejected"] else STATUSES[a["index"]]
        return {"status": status, "history": list(a["history"]), "reason": a["rejected"]}

    def advance(self, application_id: str, rejected_reason: str | None = None) -> dict:
        a = self._apps.get(application_id)
        if not a:
            return {"status": "Unknown", "history": []}
        if rejected_reason:
            a["rejected"] = rejected_reason
            a["history"].append("Rejected")
        elif a["index"] < len(STATUSES) - 1 and not a["rejected"]:
            a["index"] += 1
            a["history"].append(STATUSES[a["index"]])
        return self.get_status(application_id)


nsp = MockNSP()  # one process-wide instance for the demo
