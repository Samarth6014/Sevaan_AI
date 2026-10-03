from backend.core.config import settings


def validate(form: dict, documents: list[dict]) -> list[str]:
    errors = []
    for k, v in form.items():
        if v.get("conflict"):
            errors.append(f"{k}: what you said and what the document says do not match. Please decide which is right.")
        if v.get("confidence", 1) < 0.75:
            errors.append(f"{k}: low confidence, please confirm this value.")
    for d in documents:
        if d.get("size_kb", 0) > settings.max_upload_kb:
            errors.append(f"{d.get('filename')}: larger than {settings.max_upload_kb} KB.")
        if d.get("status") == "needs_check":
            errors.append(f"{d.get('filename')}: could not be read clearly; a human should check it.")
    return errors
