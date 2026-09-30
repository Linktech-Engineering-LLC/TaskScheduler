# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-09-30
 File: taskscheduler/environment/model.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass
from enum import Enum

from .raw import Source

class Status(Enum):
    INHERITED = "inherited"
    DEFINED = "defined"
    OVERRIDDEN = "overridden"
    SHADOWED = "shadowed"
    MASKED = "masked"
    DEFAULT = "default"
    INVALID = "invalid"

@dataclass
class ResolvedEnvEntry:
    variable: str
    value: str
    status: Status
    source: Source
    comment: str | None = None
    diagnostics: list["DiagnosticEntry"] | None = None

@dataclass
class DiagnosticEntry:
    source: Source
    location: str | None
    value: str
    status: Status
    comment: str | None = None


