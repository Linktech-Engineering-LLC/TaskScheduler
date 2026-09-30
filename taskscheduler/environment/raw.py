# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC
"""
 Package: PythonTools
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
Created: 2026-09-30
Modified: 2026-09-30
 File: ~/projects/Python/TaskScheduler/taskscheduler/environment/raw.py
 Version: 1.0.0
 Description: Module description here
"""

from dataclasses import dataclass
from enum import Enum

class Source(Enum):
    PROCESS = 1
    SYSTEM = 2
    USER = 3
    CRON = 4
    SYSTEMD_FILE = 5
    SYSTEMD_UNIT = 6
    SYSTEMD_DROPIN = 7

@dataclass
class RawEnvEntry:
    variable: str
    value: str
    source: Source
    location: str | None = None
