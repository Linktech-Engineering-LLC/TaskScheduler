# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-05
 Modified: 2026-10-05
 File: taskscheduler/systemd/loader.py
 Version: 1.0.0
 Description: Description of this module
"""
from pathlib import Path

from PythonTools.net import local_command, sudo_run
from .builder import (
    build_timer_unit, build_service_unit, parse_systemd_unit,
    parse_dropins, merge_timer_sections, merge_file_comments
)
from .models import (
    SystemdTimerUnit, SystemdTask, SystemdServiceUnit, 
    build_schedule_descriptor, ParsedUnitSection, ParsedUnitFile
)
from .visualizer import (
    find_dropins
)

def load_timer_unit(name: str, user: bool, sudo_password: str | None, logger=None) -> SystemdTimerUnit | None:
    timer_path = resolve_unit_path(name, user, sudo_password, logger)
    if logger:
        logger.debug(f"load_timer_unit timer_path={timer_path}")

    if not timer_path or not timer_path.exists():
        return None

    # Parse base unit file
    parsed_base = parse_systemd_unit(timer_path)

    # Find and parse drop-ins
    dropin_paths = find_dropins(name, logger)
    parsed_dropins = parse_dropins(dropin_paths, logger)

    # Extract base [Timer] section
    base_timer_section = parsed_base.sections.get("Timer")
    if not base_timer_section:
        base_timer_section = ParsedUnitSection(
            name="Timer",
            entries={},
            comments_before=[],
            comments_inline={}
        )

    # Merge timer sections
    merged_timer = merge_timer_sections(base_timer_section, parsed_dropins)

    # Build SystemdTimerUnit using merged timer section
    return build_timer_unit(name, parsed_base, merged_timer)
def resolve_unit_path(name: str, user: bool, sudo_password: str | None, logger=None) -> Path | None:
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += f"show {name} -p FragmentPath"

    out, code, err = run_systemd(cmd, user, sudo_password, logger)
    if logger:
        logger.debug(f"resolve_unit_path out={out}")
    if "=" not in out:
        return None

    _, path = out.split("=", 1)
    path = path.strip()

    return Path(path) if path else None
def load_systemd_task(timer: SystemdTimerUnit, user: bool, sudo_password: str | None, logger=None) -> SystemdTask | None:
    # Determine service name
    svc_name = timer.unit or timer.name.replace(".timer", ".service")
    service = load_service_unit(svc_name, user, sudo_password, logger)
    if not service:
        return None

    # Parse base unit file
    parsed_base = parse_systemd_unit(timer.fragment_path)

    # Find and parse drop-ins
    dropin_paths = find_dropins(timer.name, logger)
    parsed_dropins = parse_dropins(dropin_paths, logger)

    # Merge timer sections
    base_timer_section = parsed_base.sections.get("Timer")
    if not base_timer_section:
        # No [Timer] section at all — create an empty one
        base_timer_section = ParsedUnitSection(
            name="Timer",
            entries={},
            comments_before=[],
            comments_inline={}
        )

    merged_timer = merge_timer_sections(base_timer_section, parsed_dropins)

    # Merge file-level comments
    merged_file_comments = merge_file_comments(parsed_base, parsed_dropins)

    # Get systemctl show metadata
    show_output = get_systemctl_show(timer.name, user, sudo_password, logger)

    # Build unified schedule descriptor
    schedule = build_schedule_descriptor(
        merged_timer=merged_timer,
        show_output=show_output,
        file_comments=merged_file_comments,
        dropins=dropin_paths,
        fragment_path=timer.fragment_path
    )

    # Build final SystemdTask
    return SystemdTask(
        timer=timer,
        service=service,
        schedule=schedule
    )
def run_systemd(cmd: str, user: bool, sudo_password: str | None, logger=None):
    """
    Unified runner for systemd commands.
    - user=True  → always local_command
    - user=False → sudo_run if sudo_password is provided
    """
    if user:
        out, code, err = local_command(cmd, logger=logger)
        if logger:
            logger.debug(f"run_systemd out={out}\ncode={code}\nerr={err}")
        return out, code, err

    # system-level
    result = sudo_run(cmd, sudo_password, logger=logger)
    return result.msg, result.code, result.err
def get_systemctl_show(name: str, user: bool, sudo_password: str | None, logger=None) -> dict[str, str]:
    """
    Run `systemctl show` and return a dict of key/value pairs.
    """
    cmd = "systemctl "
    if user:
        cmd += "--user "
    cmd += f"show {name}"

    out, code, err = run_systemd(cmd, user, sudo_password, logger)

    if code != 0:
        if logger:
            logger.error(f"systemctl show {name} failed: {err}")
        return {}

    result: dict[str, str] = {}

    for raw in out.splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        result[key.strip()] = value.strip()

    if logger:
        logger.debug(f"systemctl show {name}: {result}")

    return result
def load_service_unit(name: str, user: bool, sudo_password: str | None, logger=None) -> SystemdServiceUnit | None:
    svc_path = resolve_unit_path(name, user, sudo_password, logger)
    if logger:
        logger.debug(f"load_service_unit svc_path={svc_path}")

    if not svc_path or not svc_path.exists():
        return None

    # Parse base unit file
    parsed_base = parse_systemd_unit(svc_path)

    # Find and parse drop-ins
    dropin_paths = find_dropins(name, logger)
    parsed_dropins = parse_dropins(dropin_paths, logger)

    # Extract base [Service] section
    base_service_section = parsed_base.sections.get("Service")
    if not base_service_section:
        base_service_section = ParsedUnitSection(
            name="Service",
            entries={},
            comments_before=[],
            comments_inline={}
        )

    # Merge service sections
    merged_service = merge_timer_sections(base_service_section, parsed_dropins)

    # Build SystemdServiceUnit using merged service section
    return build_service_unit(name, parsed_base, merged_service)

