"""Thin LLM adapter. The LLM only converses/extracts/explains; it never decides eligibility."""
import re
from abc import ABC, abstractmethod
from backend.core.config import settings


class LLM(ABC):
    @abstractmethod
    def extract_profile(self, text: str, language: str, expecting: str | None = None) -> dict:
        """-> {field: {"value": v, "confidence": float}}. Must never invent values."""

    def explain(self, text: str, language: str) -> str:
        return text


_NUM = r"(\d[\d,]*(?:\.\d+)?)"


class MockLLM(LLM):
    """Rule-based extractor so the demo and tests run with no API key."""

    def extract_profile(self, text: str, language: str, expecting: str | None = None) -> dict:
        t = text.lower()
        out: dict = {}

        def put(k, v, c=0.9):
            out[k] = {"value": v, "confidence": c}

        m = re.search(_NUM + r"\s*(lakh|lakhs|lac)", t)
        if m:
            put("family_income_annual", int(float(m.group(1).replace(",", "")) * 100000))
        else:
            m = re.search(r"(income|earn\w*)[^\d]{0,25}" + _NUM, t)
            if m:
                put("family_income_annual", int(float(m.group(2).replace(",", ""))))
            elif expecting == "family_income_annual":
                m = re.search(_NUM, t)
                if m:
                    put("family_income_annual", int(float(m.group(1).replace(",", ""))), 0.7)

        m = re.search(r"class\s*(\d{1,2})", t) or re.search(r"(\d{1,2})(?:st|nd|rd|th)\s*(?:class|std|standard)", t)
        if m:
            put("current_level", int(m.group(1)))
        elif expecting == "current_level":
            m = re.search(r"\b(\d{1,2})\b", t)
            if m:
                put("current_level", int(m.group(1)), 0.7)
            elif re.search(r"\bug\b|degree|college", t):
                put("current_level", "UG")

        for cat in ("sc", "st", "obc", "ews"):
            if re.search(rf"\b{cat}\b", t):
                put("category", cat.upper())
                break
        else:
            if re.search(r"\b(general|gen)\b", t):
                put("category", "GEN")

        if re.search(r"private", t):
            put("institution_type", "private")
        elif re.search(r"\baided\b", t):
            put("institution_type", "aided")
        elif re.search(r"government|govt|sarkari", t):
            put("institution_type", "government")
        elif re.search(r"local body", t):
            put("institution_type", "local_body")
        elif re.search(r"kendriya|navodaya", t):
            put("institution_type", "central_school")

        m = re.search(_NUM + r"\s*(%|percent)", t)
        if m and expecting in (None, "marks_pct_class7"):
            put("marks_pct_class7", float(m.group(1)), 0.8)
        elif expecting == "marks_pct_class7":
            m = re.search(_NUM, t)
            if m:
                put("marks_pct_class7", float(m.group(1)), 0.7)

        m = re.search(r"(\d{1,2})\s*(years old|year old|yrs)", t)
        if m:
            put("age", int(m.group(1)))
        if re.search(r"\b(girl|female|she|daughter)\b", t):
            put("gender", "female")
        elif re.search(r"\b(boy|male|son)\b", t):
            put("gender", "male")
        return out


class ExternalLLM(LLM):
    def __init__(self):
        raise NotImplementedError(
            "Implement your provider here (tool calling + JSON-schema output), validate with Pydantic, "
            "retry once, then ask the human. Keep LLM_PROVIDER=mock until then.")


def get_llm() -> LLM:
    return MockLLM() if settings.llm_provider == "mock" else ExternalLLM()
