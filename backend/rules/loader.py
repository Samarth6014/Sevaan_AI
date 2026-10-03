import json
from functools import lru_cache
from pathlib import Path
from .schema import Scheme

SCHEMES_DIR = Path(__file__).resolve().parents[2] / "packs" / "scholarships" / "schemes"


@lru_cache(maxsize=1)
def load_all(directory: str = str(SCHEMES_DIR)) -> dict[str, Scheme]:
    out: dict[str, Scheme] = {}
    for p in sorted(Path(directory).glob("*.json")):
        s = Scheme.model_validate(json.loads(p.read_text(encoding="utf-8")))
        out[s.scheme_id] = s
    return out


def get(scheme_id: str) -> Scheme | None:
    return load_all().get(scheme_id)


def reload() -> None:
    load_all.cache_clear()
