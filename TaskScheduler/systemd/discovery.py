# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/discovery.py
 Version: 1.0.0
 Description: Description of this module
"""

from typing import List
from pathlib import Path

from .loader import (
    run_systemd, load_timer_unit, load_systemd_task
)
from .models import (
    SystemdTask,
)
from .visualizer import (
    get_timer_runtime_metadata,
)

def list_systemd_timers(user: bool = True, sudo_password: str | None = None, logger=None) -> list[str]:
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += "list-timers --all --no-pager --plain"

    out, code, err = run_systemd(cmd, user, sudo_password, logger)
    timers: list[str] = []
    for line in out.splitlines():
        for part in line.split():
            if part.endswith(".timer"):
                timers.append(part)
                break
    if logger:
        logger.debug(f"list_systemd_timers timers={timers}")

    return timers



def discover_systemd_tasks(user: bool = True, sudo_password: str | None = None, logger=None) -> list[SystemdTask]:
    tasks: list[SystemdTask] = []

    runtime = get_timer_runtime_metadata(user, sudo_password, logger)

    for timer_name in list_systemd_timers(user, sudo_password, logger):
        timer = load_timer_unit(timer_name, user, sudo_password, logger)
        if not timer:
            continue

        # Attach runtime metadata if available
        if timer_name in runtime:
            timer.next_run = runtime[timer_name]["next"]
            timer.last_run = runtime[timer_name]["last"]

        task = load_systemd_task(timer, user, sudo_password, logger)
        if task:
            tasks.append(task)

    return tasks
