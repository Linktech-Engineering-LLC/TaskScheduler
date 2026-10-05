# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-29
 Modified: 2026-10-05
 File: taskscheduler/cron_entry.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass

@dataclass
class CronEntry:
    minute: str
    hour: str
    dom: str
    month: str
    dow: str
    command: str
    comment: str = ""       # ← add this line
    enabled: bool = True
    daily: bool = False
    boot: bool = False
    source: str = "user"

    def schedule_string(self):
        return f"{self.minute} {self.hour} {self.dom} {self.month} {self.dow}"

