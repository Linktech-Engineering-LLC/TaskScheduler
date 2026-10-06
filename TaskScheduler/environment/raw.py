# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-05
 Modified: 2026-10-05
 File: taskscheduler/environment/raw.py
 Version: 1.0.0
 Description: Description of this module
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
