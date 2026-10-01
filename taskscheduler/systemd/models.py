# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-01
 File: taskscheduler/systemd/system_entry.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

@dataclass(slots=True)
class SystemdServiceUnit:
    name: str
    fragment_path: Path

    description: str | None = None
    exec_start: List[str] = field(default_factory=list)
    working_directory: Path | None = None
    environment: Dict[str, str] = field(default_factory=dict)

    type: str | None = None
    user: str | None = None
    group: str | None = None


@dataclass(slots=True)
class SystemdTimerUnit:
    name: str
    fragment_path: Path

    description: str | None = None
    on_calendar: List[str] = field(default_factory=list)
    accuracy_sec: str | None = None
    randomized_delay_sec: str | None = None
    persistent: bool = False

    unit: str | None = None  # linked service name

    next_run: str | None = None
    last_run: str | None = None

@dataclass(slots=True)
class SystemdTask:
    timer: SystemdTimerUnit
    service: SystemdServiceUnit

    @property
    def name(self) -> str:
        return self.timer.name

    @property
    def schedule(self) -> List[str]:
        return self.timer.on_calendar

    @property
    def command(self) -> List[str]:
        return self.service.exec_start

@dataclass(slots=True)
class CalendarSpec:
    raw: str
    years: List[str]
    months: List[str]
    days: List[str]
    weekdays: List[str]
    times: List[str]
