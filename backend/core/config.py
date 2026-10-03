import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    demo_otp: str = os.getenv("DEMO_OTP", "123456")
    max_upload_kb: int = int(os.getenv("MAX_UPLOAD_KB", "200"))  # [A] verify against NSP
    use_cached_demo: bool = os.getenv("USE_CACHED_DEMO", "true").lower() == "true"
    connector_mode: str = os.getenv("CONNECTOR_MODE", "mock")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-demo-only")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'scholarpath.db'}")
    packs_dir: Path = ROOT / "packs"


settings = Settings()
