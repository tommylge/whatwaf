__product__ = "gladius"


def detect(content, **kwargs):
    headers = kwargs.get("headers", {})
    if headers:
        if headers.get("gladius_blockchain_driven_cyber_protection_network_session", "") != "":
            return True
