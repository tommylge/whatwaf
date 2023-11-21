import os
import importlib
from . import plugins

import whatwaf.lib.formatter as formatter

from whatwaf.lib.timeout import timeout

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

loaded_plugins = ScriptQueue().load_scripts()

@timeout(seconds=8)
def detection_main(response):
    """
    main detection function
    """
    formatter.info("gathering HTTP responses")
    detected_protections = set()

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

    return list(detected_protections)
