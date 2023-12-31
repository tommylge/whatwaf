import re

from whatwaf.lib.settings import HTTP_HEADER


__product__ = "airlock"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    detection_schema = (
        re.compile(r"\Aal[.-]?(sess|lb)=?", re.I),
    )

    for detection in detection_schema:
        if detection.search(headers.get(HTTP_HEADER.SET_COOKIE, "")) is not None:
            return True
