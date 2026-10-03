"""Mock DigiLocker: simulated consent screen + synthetic sample documents. No Aadhaar flows."""
from backend.connectors.base import DocumentVault

SAMPLES = {
    "income_certificate": {"holder": "Sample Student", "annual_income": 180000, "issuer": "SAMPLE Tahsildar Office"},
    "caste_certificate": {"holder": "Sample Student", "category": "SC", "issuer": "SAMPLE Tahsildar Office"},
    "mark_sheet": {"holder": "Sample Student", "marks_pct_class7": 72, "school": "SAMPLE Govt High School"},
}


class MockDigiLocker(DocumentVault):
    def __init__(self):
        self._consented: set[str] = set()

    def consent(self, case_ref: str) -> bool:
        self._consented.add(case_ref)
        return True

    def fetch(self, doc_type: str) -> dict | None:
        return SAMPLES.get(doc_type)


digilocker = MockDigiLocker()
