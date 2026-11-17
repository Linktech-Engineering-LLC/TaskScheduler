# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-11-17
 File: taskscheduler/systemd/__init__.py
 Version: 1.0.0
 Description: Description of this module
"""

from .builder import (
                      build_service_unit,
                      build_timer_unit,
                      merge_file_comments,
                      merge_timer_sections,
                      parse_dropins,
                      parse_systemd_unit,
)
from .discovery import list_systemd_timers
from .loader import (
                      load_service_unit,
                      load_systemd_task,
                      load_timer_unit,
                      resolve_unit_path,
                      run_systemd,
)
from .models import (
                      MONOTONIC_KEYS,
                      WEEKDAYS,
                      CalendarSpec,
                      ParsedUnitFile,
                      ParsedUnitSection,
                      SystemdScheduleDescriptor,
                      SystemdServiceUnit,
                      SystemdTask,
                      SystemdTimerUnit,
                      build_schedule_descriptor,
)
from .visualizer import find_dropins, get_timer_runtime_metadata

__all__ = [
                      "MONOTONIC_KEYS",
                      "WEEKDAYS",
                      "CalendarSpec",
                      "ParsedUnitFile",
                      "ParsedUnitSection",
                      "SystemdScheduleDescriptor",
                      "SystemdServiceUnit",
                      "SystemdTask",
                      "SystemdTimerUnit",
                      "build_schedule_descriptor",
                      "build_service_unit",
                      "build_timer_unit",
                      "find_dropins",
                      "get_timer_runtime_metadata",
                      "list_systemd_timers",
                      "load_service_unit",
                      "load_systemd_task",
                      "load_timer_unit",
                      "parse_systemd_unit",
                      "resolve_unit_path",
                      "run_systemd",
]
