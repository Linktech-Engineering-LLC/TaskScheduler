# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/system_entry.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONOTONIC_KEYS = {
    "OnBootSec",
    "OnStartupSec",
    "OnUnitActiveSec",
    "OnUnitInactiveSec",
    "OnActiveSec",
    "OnFailureSec",
}
@dataclass
class ParsedUnitSection:
    name: str
    entries: dict[str, list[str]]      # key → list of values
    comments_before: list[str]         # comments before section
    comments_inline: dict[str, list[str]]  # key → comments near that key

@dataclass
class ParsedUnitFile:
    path: Path
    sections: dict[str, ParsedUnitSection]
    file_comments: list[str]

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
class CalendarSpec:
    raw: str
    years: List[str]
    months: List[str]
    days: List[str]
    weekdays: List[str]
    times: List[str]
@dataclass
class SystemdScheduleDescriptor:
    calendar: list[str]
    calendar_comments: list[str]

    monotonic: dict[str, str]
    monotonic_comments: list[str]

    accuracy_sec: str | None
    randomized_delay_sec: str | None
    persistent: bool

    unit_state: str
    load_state: str
    fragment_path: Path
    dropins: list[Path]
    source_path: Path | None
    generated_by: str | None

    comments: list[str]
    timer_section_comments: list[str]
    schedule_comments: dict[str, list[str]]
@dataclass(slots=True)
class SystemdTask:
    timer: SystemdTimerUnit
    service: SystemdServiceUnit
    schedule: SystemdScheduleDescriptor
    
    @property
    def name(self) -> str:
        return self.timer.name

    @property
    def calendar(self) -> List[str]:
        return self.timer.on_calendar

    @property
    def command(self) -> List[str]:
        return self.service.exec_start

def build_schedule_descriptor(
    merged_timer: ParsedUnitSection,
    show_output: dict[str, str],
    file_comments: list[str],
    dropins: list[Path],
    fragment_path: Path
) -> SystemdScheduleDescriptor:

    calendar = merged_timer.entries.get("OnCalendar", [])
    calendar_comments = merged_timer.comments_inline.get("OnCalendar", [])

    monotonic = {
        k: merged_timer.entries[k][0]
        for k in MONOTONIC_KEYS
        if k in merged_timer.entries
    }

    monotonic_comments = [
        c for k in MONOTONIC_KEYS
        for c in merged_timer.comments_inline.get(k, [])
    ]

    accuracy_sec = merged_timer.entries.get("AccuracySec", [None])[0]
    randomized_delay_sec = merged_timer.entries.get("RandomizedDelaySec", [None])[0]
    persistent = merged_timer.entries.get("Persistent", ["false"])[0].lower() == "true"

    return SystemdScheduleDescriptor(
        calendar=calendar,
        calendar_comments=calendar_comments,

        monotonic=monotonic,
        monotonic_comments=monotonic_comments,

        accuracy_sec=accuracy_sec,
        randomized_delay_sec=randomized_delay_sec,
        persistent=persistent,

        unit_state=show_output.get("UnitFileState", ""),
        load_state=show_output.get("LoadState", ""),
        fragment_path=fragment_path,
        dropins=dropins,
        source_path = Path(show_output["SourcePath"]) if show_output.get("SourcePath") else None,
        generated_by=show_output.get("GeneratedBy"),

        comments=file_comments,
        timer_section_comments=merged_timer.comments_before,
        schedule_comments=merged_timer.comments_inline,
    )
