import re


from whatwaf.lib.settings import HTTP_HEADER


__product__ = "blockdos"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    detection_schema = (
        re.compile(r"blockdos\.net", re.I),
    )
    for detection in detection_schema:
        if detection.search(headers.get(HTTP_HEADER.SERVER, "")) is not None:
            return True
