import re

from whatwaf.lib.settings import HTTP_HEADER


__product__ = "denyall"


def detect(content, **kwargs):
    content = str(content)
    headers = kwargs.get("headers", {})
    detection_schema = (
        re.compile(r"\Acondition.intercepted", re.I),
        re.compile(r"\Asessioncookie=", re.I)
    )
    for detection in detection_schema:
        if detection.search(content) is not None:
            return True
        if detection.search(headers.get(HTTP_HEADER.SET_COOKIE, "")) is not None:
            return True
