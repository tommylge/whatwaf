import re

from whatwaf.lib.settings import HTTP_HEADER


__product__ = "dosarrest"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    detection_schema = (
        re.compile(r"dosarrest", re.I),
        re.compile(r"x.dis.request.id", re.I)
    )
    for detection in detection_schema:
        if detection.search(headers.get(HTTP_HEADER.SERVER, "")) is not None:
            return True
        if len(headers) != 0:
            for header in headers.keys():
                if detection.search(headers[header]) is not None:
                    return True
                if detection.search(header) is not None:
                    return True
