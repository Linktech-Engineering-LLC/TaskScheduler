# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/__init__.py
 Version: 1.0.0
 Description: Description of this module
"""

from .builder import (
    build_service_unit, build_timer_unit, parse_systemd_unit,
    merge_file_comments, merge_timer_sections, parse_dropins
)
from .models import (
    SystemdServiceUnit, SystemdTask, SystemdTimerUnit,
    CalendarSpec, WEEKDAYS, MONOTONIC_KEYS,
    SystemdScheduleDescriptor, build_schedule_descriptor,
    ParsedUnitFile, ParsedUnitSection
)
from .visualizer import (
    get_timer_runtime_metadata, find_dropins,
)
from .discovery import (
    list_systemd_timers, 
)
from .loader import (
    load_systemd_task, load_timer_unit, load_service_unit,
    resolve_unit_path, run_systemd, 
)
__all__ = [
    "build_service_unit", "build_timer_unit", "build_schedule_descriptor",
    "CalendarSpec", "get_timer_runtime_metadata", "list_systemd_timers",
    "load_service_unit", "load_systemd_task", "load_timer_unit",
    "parse_systemd_unit", "resolve_unit_path", "run_systemd",
    "SystemdServiceUnit", "SystemdTask", "SystemdTimerUnit",
    "WEEKDAYS", "MONOTONIC_KEYS", "find_dropins",
    "SystemdScheduleDescriptor", "ParsedUnitSection", "ParsedUnitFile"
]