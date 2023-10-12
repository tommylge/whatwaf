import re

from whatwaf.lib.settings import HTTP_HEADER


__product__ = "urlscan"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    detection_schema = (
        re.compile(r"rejected.by.url.scan", re.I),
        re.compile(r"/rejected.by.url.scan", re.I)
    )
    for detection in detection_schema:
        if detection.search(content) is not None:
            return True
        if detection.search(headers.get(HTTP_HEADER.LOCATION, "")) is not None:
            return True