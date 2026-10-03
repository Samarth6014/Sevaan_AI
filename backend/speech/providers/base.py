from backend.core.config import settings


class STTProvider:
    def transcribe(self, audio_b64: str, language: str) -> dict:
        raise NotImplementedError


def get_stt():
    if not settings.sarvam_api_key:
        return None
    raise NotImplementedError(
        "Add speech/providers/sarvam.py using docs.sarvam.ai (REST clips under 30 s). "
        "Return {'text': str, 'confidence': float}. Do not guess the payload shape.")
