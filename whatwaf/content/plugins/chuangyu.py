import re


__product__ = "chuangyu"


def detect(content, **kwargs):
    content = str(content)
    detection_schema = (
        re.compile(r"(http(s)?.//(www.)?)?365cyd.(com|net)", re.I),
    )
    for detection in detection_schema:
        if detection.search(content) is not None:
            return True
