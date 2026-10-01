# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-01
 File: taskscheduler/systemd/__init__.py
 Version: 1.0.0
 Description: Description of this module
"""

from .models import (
    SystemdServiceUnit, 
    SystemdTask, 
    SystemdTimerUnit,
    CalendarSpec,
    WEEKDAYS
)
from .visualizer import (
    build_service_unit, 
    build_timer_unit, 
    get_timer_runtime_metadata,
    parse_systemd_unit
)
from .discovery import (
    list_systemd_timers, 
    load_service_unit, 
    load_systemd_task, 
    load_timer_unit,
    resolve_unit_path,
    run_systemd
)

__all__ = [
    "build_service_unit",
    "build_timer_unit",
    "CalendarSpec",
    "get_timer_runtime_metadata",
    "list_systemd_timers",
    "load_service_unit",
    "load_systemd_task",
    "load_timer_unit",
    "parse_systemd_unit",
    "resolve_unit_path",
    "run_systemd",
    "SystemdServiceUnit",
    "SystemdTask",
    "SystemdTimerUnit",
    "WEEKDAYS"
]