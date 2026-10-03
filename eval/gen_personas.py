"""Synthetic personas. Ground truth comes from the rule engine, so it is only as good as the verified rule files.
Hand-check >= 30 personas against official pages (blueprint 10.8)."""
import json, random
from pathlib import Path
from backend.rules import load_all, check_eligibility

random.seed(7)
OUT = Path(__file__).parent / "personas.json"


def make(n=150):
    schemes = load_all()
    personas = []
    for i in range(n):
        prof = {
            "family_income_annual": random.choice([120000, 180000, 300000, 349000, 351000, 500000, 900000]),
            "current_level": random.choice([8, 9, 10, 11, "UG"]),
            "institution_type": random.choice(["government", "aided", "private", "central_school", "local_body"]),
            "marks_pct_class7": random.choice([45, 50, 55, 60, 80]),
            "category": random.choice(["GEN", "SC", "ST", "OBC", "EWS"]),
        }
        for k in list(prof):
            if random.random() < 0.15:  # missing facts must give unknown
                prof.pop(k)
        expected = {sid: check_eligibility(s, prof)["result"] for sid, s in schemes.items()}
        personas.append({"persona_id": f"p{i:03d}", "profile": prof, "expected": expected, "preferred_language": random.choice(["en", "hi", "te"])})
    OUT.write_text(json.dumps(personas, indent=1))
    return personas


if __name__ == "__main__":
    print(len(make()), "personas ->", OUT)
