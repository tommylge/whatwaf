import re

from whatwaf.lib.settings import HTTP_HEADER


__product__ = "stingray"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    status = kwargs.get("status", 0)
    status_schema = (403, 500)
    detection_schema = (
        re.compile(r"\AX-Mapping-", re.I),
    )
    for detection in detection_schema:
        if detection.search(headers.get(HTTP_HEADER.SET_COOKIE, "")) is not None:
            if status in status_schema:
                return True