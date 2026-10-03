import logging
from .pii import mask_text


class _MaskFilter(logging.Filter):
    def filter(self, record):
        record.msg = mask_text(str(record.msg))
        return True


def get_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        h.addFilter(_MaskFilter())
        log.addHandler(h)
        log.setLevel(logging.INFO)
    return log
