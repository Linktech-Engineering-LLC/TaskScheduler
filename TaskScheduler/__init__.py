# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-07
 File: timerdeck/__init__.py
 Version: 1.0.0
 Description: Description of this module
"""
from importlib.metadata import metadata, PackageNotFoundError

from PythonTools.utils import read_toml

try:
    PROGMETA = metadata(__name__)
    PROJECTNAME = PROGMETA.get("name")
    VERSION = PROGMETA.get("version")
except PackageNotFoundError:
    from PythonTools.utils import read_toml
    proj = read_toml("pyproject.toml")["project"]
    PROJECTNAME = proj["name"]
    VERSION = proj["version"]

__all__ = [
    "PROJECTNAME",
    "VERSION"
]