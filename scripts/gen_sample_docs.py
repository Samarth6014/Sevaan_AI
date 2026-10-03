"""Writes SAMPLE synthetic documents (text) into fixtures/sample_docs/. Fake names/numbers only."""
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "fixtures" / "sample_docs"
DOCS = {
    "clean/income_certificate.txt": "SAMPLE - NOT A REAL DOCUMENT\nHolder: Sample Student\nAnnual Income: 180000\nIssuer: SAMPLE Tahsildar Office",
    "clean/mark_sheet.txt": "SAMPLE - NOT A REAL DOCUMENT\nHolder: Sample Student\nMarks Pct Class7: 72",
    "noisy/mark_sheet_noisy.txt": "SAMPLE ~~ NOT A REAL DOC\nHolder Sample Stud?nt\nMarks Pct Class7: 7#",
}
for rel, text in DOCS.items():
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")
print("written", len(DOCS))
