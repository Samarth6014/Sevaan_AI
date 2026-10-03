"""STT/TTS adapter with cache and typed fallback. Provider calls are NOT implemented here:
the Sarvam/Bhashini endpoints and payloads must be taken from their docs [U]."""
import hashlib, json
from pathlib import Path
from backend.core.config import settings, ROOT

CACHE = ROOT / "fixtures" / "cache"


class SpeechUnavailable(Exception):
    pass


def _key(prefix: str, payload: str, lang: str) -> Path:
    return CACHE / f"{prefix}_{hashlib.sha1((lang + payload).encode()).hexdigest()}.json"


def transcribe(audio_b64: str, language: str) -> dict:
    """-> {text, confidence}. Cached demo clips first; otherwise provider; otherwise typed fallback."""
    p = _key("stt", audio_b64, language)
    if settings.use_cached_demo and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    from .providers.base import get_stt
    prov = get_stt()
    if prov is None:
        raise SpeechUnavailable("Speech not configured. Please type your answer.")
    return prov.transcribe(audio_b64, language)


def synthesize(text: str, language: str) -> dict:
    """-> {audio_b64 | None, use_browser_tts}. Browser speechSynthesis is the fallback."""
    p = _key("tts", text, language)
    if settings.use_cached_demo and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"audio_b64": None, "use_browser_tts": True}
