# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/parsers.py
 Version: 1.0.0
 Description: Description of this module
"""

import re

from pathlib import Path
from typing import Dict, List

from .models import (
    CalendarSpec,
    SystemdServiceUnit, 
    SystemdTimerUnit,
    WEEKDAYS
)
from PythonTools.net import local_command, sudo_run

def get_timer_runtime_metadata(user: bool = True, sudo_password: str | None = None, logger=None) -> Dict[str, Dict[str, str]]:
    """
    Returns:
    {
        "logrotate.timer": {
            "next": "Thu 2026-10-01 03:00:00",
            "last": "Thu 2026-09-30 03:00:00",
            "service": "logrotate.service",
            "state": "loaded active waiting"
        },
        ...
    }
    """
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += "list-timers --all --no-pager --plain"

    out, code, err = (
        local_command(cmd, logger=logger)
        if user or sudo_password is None
        else sudo_run(cmd, sudo_password, logger=logger).as_tuple
    )
    if logger:
        logger.debug(f"[DEBUG]get_timer_runtime_metadata Results={out}")
    metadata: Dict[str, Dict[str, str]] = {}

    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 6:
            continue

        timer = parts[0]
        if not timer.endswith(".timer"):
            continue

        next_run = " ".join(parts[1:3])     # date + time
        last_run = " ".join(parts[3:5])     # date + time
        service = parts[5]
        state = " ".join(parts[6:]) if len(parts) > 6 else ""

        metadata[timer] = {
            "next": next_run,
            "last": last_run,
            "service": service,
            "state": state
        }

    return metadata

def parse_oncalendar(expr: str) -> CalendarSpec:
    raw = expr.strip()

    # Split date/time
    if " " in raw:
        date_part, time_part = raw.split(" ", 1)
    else:
        date_part, time_part = raw, None

    years, months, days, weekdays = [], [], [], []
    times = []

    # Handle keywords
    if raw == "daily":
        weekdays = WEEKDAYS
        times = ["00:00"]
        return CalendarSpec(raw, ["*"], ["*"], ["*"], weekdays, times)

    if raw == "weekly":
        weekdays = WEEKDAYS
        times = ["00:00"]
        return CalendarSpec(raw, ["*"], ["*"], ["*"], weekdays, times)

    if raw == "monthly":
        days = ["1"]
        times = ["00:00"]
        return CalendarSpec(raw, ["*"], ["*"], days, [], times)

    # Parse date part
    if "-" in date_part:
        parts = date_part.split("-")
        years = expand_field(parts[0])
        months = expand_field(parts[1])
        days = expand_field(parts[2])
    else:
        # weekday-only expression
        weekdays = expand_field(date_part)

    # Parse time part
    if time_part:
        times = expand_field(time_part)

    return CalendarSpec(raw, years, months, days, weekdays, times)

def expand_field(field: str) -> List[str]:
    field = field.strip()

    if field == "*":
        return ["*"]

    # Range: Mon..Fri or 1..5 or 03:00..05:00
    if ".." in field:
        start, end = field.split("..", 1)
        return expand_range(start, end)

    # List: Mon,Wed,Fri
    if "," in field:
        return [f.strip() for f in field.split(",")]

    return [field]

def expand_range(start: str, end: str) -> List[str]:
    # Weekday range
    if start in WEEKDAYS and end in WEEKDAYS:
        s = WEEKDAYS.index(start)
        e = WEEKDAYS.index(end)
        return WEEKDAYS[s:e+1]

    # Numeric range
    if start.isdigit() and end.isdigit():
        return [str(i) for i in range(int(start), int(end) + 1)]

    # Time range (hour only)
    if re.match(r"\d{2}:\d{2}", start) and re.match(r"\d{2}:\d{2}", end):
        sh, sm = map(int, start.split(":"))
        eh, em = map(int, end.split(":"))
        return [f"{h:02d}:{sm:02d}" for h in range(sh, eh + 1)]

    return [start, end]

def summarize_calendar(spec: CalendarSpec) -> str:
    parts = []

    if spec.weekdays:
        parts.append(f"Weekdays: {' '.join(spec.weekdays)}")

    if spec.days and spec.days != ["*"]:
        parts.append(f"Days: {' '.join(spec.days)}")

    if spec.months and spec.months != ["*"]:
        parts.append(f"Months: {' '.join(spec.months)}")

    if spec.years and spec.years != ["*"]:
        parts.append(f"Years: {' '.join(spec.years)}")

    if spec.times:
        parts.append(f"Times: {' '.join(spec.times)}")

    return "\n".join(parts)

def find_dropins(name: str, logger=None) -> list[Path]:
    """
    Locate all drop-in configuration files for a systemd unit.
    """
    dirs = [
        Path("/etc/systemd/user") / f"{name}.d",
        Path("/run/systemd/user") / f"{name}.d",
        Path("/usr/lib/systemd/user") / f"{name}.d",
    ]

    dropins = []
    for d in dirs:
        if d.exists():
            dropins.extend(sorted(d.glob("*.conf")))

    if logger:
        logger.debug(f"dropins for {name}: {dropins}")

    return dropins
