# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-10-05
 File: taskscheduler/environment/modes.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass
from enum import Enum

from .model import Status

@dataclass
class EnvDiffEntry:
    variable: str
    left_value: str | None
    right_value: str | None
    left_status: Status | None
    right_status: Status | None

class EnvironmentMode(Enum):
    USER = "user"
    SYSTEM = "system"
