from setuptools import setup, find_packages

from whatwaf.lib.settings import VERSION
from whatwaf.lib.formatter import fatal, error

try:
    setup(
        name="whatwaf",
        version=VERSION,
        packages=find_packages(),
        url="https://github.com/tommylge/whatwaf",
        license="GPLv3",
        author="tommylge",
        description="Detect and bypass web application firewalls and protection systems",
        install_requires=open("requirements.txt").read().split("\n"),
        py_modules=["whatwaf"],
    )
except Exception as e:
    import sys, traceback

    sep = "-" * 30
    fatal(
        "WhatWaf has caught an unhandled exception with the error message: '{}'.".format(
            str(e)
        )
    )
    exception_data = "Traceback (most recent call):\n{}{}".format(
        "".join(traceback.format_tb(sys.exc_info()[2])), str(e)
    )
    error("\n{}\n{}\n{}".format(sep, exception_data, sep))
