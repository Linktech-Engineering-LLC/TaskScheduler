# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-01
 File: taskscheduler/systemd/discovery.py
 Version: 1.0.0
 Description: Description of this module
"""

from typing import List
from pathlib import Path

from .models import SystemdTimerUnit, SystemdServiceUnit, SystemdTask
from .visualizer import (
    build_timer_unit, 
    build_service_unit, 
    parse_systemd_unit,
    get_timer_runtime_metadata
)

from PythonTools.net import local_command, sudo_run

def list_systemd_timers(user: bool = True, sudo_password: str | None = None, logger=None) -> list[str]:
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += "list-timers --all --no-pager --plain"

    out, code, err = run_systemd(cmd, user, sudo_password, logger)

    timers: list[str] = []
    for line in out.splitlines():
        parts = line.split()
        if parts and parts[0].endswith(".timer"):
            timers.append(parts[0])

    return timers

def resolve_unit_path(name: str, user: bool, sudo_password: str | None, logger=None) -> Path | None:
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += f"show {name} -p FragmentPath"

    out, code, err = run_systemd(cmd, user, sudo_password, logger)

    if "=" not in out:
        return None

    _, path = out.split("=", 1)
    path = path.strip()

    return Path(path) if path else None

def load_timer_unit(name: str, user: bool, sudo_password: str | None, logger=None) -> SystemdTimerUnit | None:
    timer_path = resolve_unit_path(name, user, sudo_password, logger)
    if not timer_path or not timer_path.exists():
        return None

    parsed = parse_systemd_unit(timer_path)
    return build_timer_unit(name, parsed, timer_path)

def load_service_unit(name: str, user: bool, sudo_password: str | None, logger=None) -> SystemdServiceUnit | None:
    svc_path = resolve_unit_path(name, user, sudo_password, logger)
    if not svc_path or not svc_path.exists():
        return None

    parsed = parse_systemd_unit(svc_path)
    return build_service_unit(name, parsed, svc_path)

def load_systemd_task(timer: SystemdTimerUnit, user: bool, sudo_password: str | None, logger=None) -> SystemdTask | None:
    svc_name = timer.unit or timer.name.replace(".timer", ".service")
    service = load_service_unit(svc_name, user, sudo_password, logger)

    if not service:
        return None

    return SystemdTask(timer=timer, service=service)

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

def run_systemd(cmd: str, user: bool, sudo_password: str | None, logger=None):
    """
    Unified runner for systemd commands.
    - user=True  → always local_command
    - user=False → sudo_run if sudo_password is provided
    """
    if user:
        out, code, err = local_command(cmd, logger=logger)
        return out, code, err

    # system-level
    result = sudo_run(cmd, sudo_password, logger=logger)
    return result.msg, result.code, result.err