from sqlmodel import Session, select

from backend.core.db import engine, init_db
from backend.models import Case
from scripts.validate_rules import main as validate_rules


DEMO_CASES = (
    {"owner_phone": "9000000011", "language": "te", "channel": "web"},
    {"owner_phone": "9000000012", "language": "en", "channel": "web"},
    {"owner_phone": "9000000013", "language": "en", "channel": "web"},
)


def seed_cases() -> int:
    created = 0
    with Session(engine) as session:
        existing_phones = {
            phone for phone in session.exec(select(Case.owner_phone)).all()
        }
        for data in DEMO_CASES:
            if data["owner_phone"] in existing_phones:
                continue
            session.add(Case(**data))
            created += 1
        if created:
            session.commit()
    return created


if __name__ == "__main__":
    init_db()
    created = seed_cases()
    print(f"DB ready. Seeded {created} demo case(s).")
    raise SystemExit(validate_rules())
