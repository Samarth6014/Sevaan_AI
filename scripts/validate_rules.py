"""Schema-check every rule file and list unverified ones. Exit 1 on schema errors."""
import json, sys
from pathlib import Path
from backend.rules.schema import Scheme, OPS, PROFILE_FIELDS

DIR = Path(__file__).resolve().parents[1] / "packs" / "scholarships" / "schemes"


def main() -> int:
    bad = 0
    for p in sorted(DIR.glob("*.json")):
        try:
            s = Scheme.model_validate(json.loads(p.read_text(encoding="utf-8")))
            for r in s.eligibility.all_of + s.eligibility.none_of:
                assert r.op in OPS, f"{r.id}: bad op {r.op}"
                assert r.field in PROFILE_FIELDS, f"{r.id}: unknown field {r.field}"
        except Exception as e:
            print(f"ERROR {p.name}: {e}"); bad += 1; continue
        flag = "verified" if s.verified else "UNVERIFIED"
        state = "drafted" if s.drafted else "stub"
        print(f"{flag:10} {state:8} {s.scheme_id}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
