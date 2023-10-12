import os
import importlib
from . import plugins

import whatwaf.lib.formatter as formatter
import whatwaf.lib.settings as settings

from types import ModuleType


class ScriptQueue(object):

    """
    This is where we will load all the scripts that we need to identify the firewall
    or to identify the possible bypass
    """
    skip_schema = ("__init__.py", ".pyc", "__")

    def load_scripts(self):
        retval: list[ModuleType] = []
        file_list: list[str] = [
            f
            for f in os.listdir(path=str(plugins.__path__[0]))
            if not any(s in f for s in self.skip_schema)
        ]
        for script in file_list:
            script = script[:-3]
            try:
                script = importlib.import_module(
                    f".plugins.{script}", "whatwaf.content"
                )
                retval.append(script)
            except Exception:
                formatter.warn(
                    "failed to load tamper '{}', pretending it doesn't exist".format(
                        script
                    )
                )
        return retval


def detection_main(response):
    """
    main detection function
    """
    formatter.info("gathering HTTP responses")

    amount_of_products = 0
    detected_protections = set()

    formatter.info("loading firewall detection scripts")
    loaded_plugins = ScriptQueue().load_scripts()

    formatter.info("running firewall detection checks")
    for detection in loaded_plugins:
        try:
            if (
                detection.detect(
                    str(response.body), status=response.status, headers=response.headers
                )
                is True
            ):
                detected_protections.add(detection.__product__)
        except Exception:
            pass

    if len(detected_protections) > 0:
        if settings.UNKNOWN_FIREWALL_NAME not in detected_protections:
            amount_of_products += 1
        if len(detected_protections) > 1:
            for i, _ in enumerate(list(detected_protections)):
                amount_of_products += 1

    if amount_of_products == 1:
        detected_protections = list(detected_protections)[0]
        formatter.discover(
            "detected website protection identified as '{}'".format(
                detected_protections
            )
        )
        if isinstance(detected_protections, str):
            detected_protections = [detected_protections]
    elif amount_of_products == 0:
        formatter.success("no protection identified on target")
    else:
        detected_protections = [
            item
            for item in list(detected_protections)
            if item != settings.UNKNOWN_FIREWALL_NAME
        ]
        for protection in sorted(detected_protections):
            if not protection == settings.UNKNOWN_FIREWALL_NAME:
                formatter.discover("{}".format(protection))

    return detected_protections
