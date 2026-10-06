# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-05
 Modified: 2026-10-05
 File: taskscheduler/systemd/builder.py
 Version: 1.0.0
 Description: Description of this module
"""

from pathlib import Path

from .models import (
    ParsedUnitFile, ParsedUnitSection, SystemdTimerUnit,
    SystemdServiceUnit
)

def build_timer_unit(name: str, parsed: ParsedUnitFile, merged_timer: ParsedUnitSection) -> SystemdTimerUnit:
    unit = SystemdTimerUnit(name=name, fragment_path=parsed.path)

    # Description from [Unit]
    unit_section = parsed.sections.get("Unit")
    if unit_section:
        unit.description = unit_section.entries.get("Description", [None])[0]

    # Calendar schedule
    unit.on_calendar = merged_timer.entries.get("OnCalendar", [])

    # Accuracy / jitter
    unit.accuracy_sec = merged_timer.entries.get("AccuracySec", [None])[0]
    unit.randomized_delay_sec = merged_timer.entries.get("RandomizedDelaySec", [None])[0]

    # Persistent flag
    unit.persistent = merged_timer.entries.get("Persistent", ["false"])[0].lower() == "true"

    # Linked service name (if present)
    if unit_section:
        unit.unit = unit_section.entries.get("Unit", [None])[0]

    return unit

def build_service_unit(name: str, parsed: ParsedUnitFile, merged_service: ParsedUnitSection) -> SystemdServiceUnit:
    svc = SystemdServiceUnit(name=name, fragment_path=parsed.path)

    unit_section = parsed.sections.get("Unit")
    service_section = merged_service  # <-- use merged section

    # Description from [Unit]
    if unit_section:
        svc.description = unit_section.entries.get("Description", [None])[0]

    # ExecStart
    if service_section:
        svc.exec_start = service_section.entries.get("ExecStart", [])

        # WorkingDirectory
        wd = service_section.entries.get("WorkingDirectory", [None])[0]
        svc.working_directory = Path(wd) if wd else None

        # Type
        svc.type = service_section.entries.get("Type", [None])[0]

        # User / Group
        svc.user = service_section.entries.get("User", [None])[0]
        svc.group = service_section.entries.get("Group", [None])[0]

        # Environment variables
        for env in service_section.entries.get("Environment", []):
            if "=" in env:
                key, val = env.split("=", 1)
                svc.environment[key.strip()] = val.strip().strip('"')

    return svc
def parse_systemd_unit(path: Path) -> ParsedUnitFile:
    sections: dict[str, ParsedUnitSection] = {}
    file_comments: list[str] = []

    current_section: ParsedUnitSection | None = None
    pending_comments: list[str] = []

    for raw in path.read_text().splitlines():
        line = raw.strip()

        # Comment line
        if line.startswith("#"):
            pending_comments.append(line)
            continue

        # Section header
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            current_section = ParsedUnitSection(
                name=name,
                entries={},
                comments_before=pending_comments.copy(),
                comments_inline={}
            )
            sections[name] = current_section
            pending_comments.clear()
            continue

        # Key/value entry
        if "=" in line and current_section:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            current_section.entries.setdefault(key, []).append(value)

            if pending_comments:
                current_section.comments_inline.setdefault(key, []).extend(pending_comments)
                pending_comments.clear()

            continue

        # Non-comment, non-section, non-entry lines
        if pending_comments:
            file_comments.extend(pending_comments)
            pending_comments.clear()

    return ParsedUnitFile(path=path, sections=sections, file_comments=file_comments)
def parse_dropins(paths: list[Path], logger=None) -> list[ParsedUnitFile]:
    parsed = []
    for p in paths:
        try:
            parsed.append(parse_systemd_unit(p))
        except Exception as e:
            if logger:
                logger.error(f"Failed to parse drop-in {p}: {e}")
    return parsed
def merge_timer_sections(base: ParsedUnitSection, dropins: list[ParsedUnitFile]) -> ParsedUnitSection:
    """
    Merge base [Timer] section with drop-in [Timer] sections.
    Drop-ins override keys but comments are merged.
    """
    merged = ParsedUnitSection(
        name="Timer",
        entries={k: v.copy() for k, v in base.entries.items()},
        comments_before=base.comments_before.copy(),
        comments_inline={k: v.copy() for k, v in base.comments_inline.items()}
    )

    for dropin in dropins:
        sec = dropin.sections.get("Timer")
        if not sec:
            continue

        # Override entries
        for key, values in sec.entries.items():
            merged.entries[key] = values.copy()

        # Merge comments
        merged.comments_before.extend(sec.comments_before)

        for key, comments in sec.comments_inline.items():
            merged.comments_inline.setdefault(key, []).extend(comments)

    return merged
def merge_file_comments(base: ParsedUnitFile, dropins: list[ParsedUnitFile]) -> list[str]:
    comments = base.file_comments.copy()
    for d in dropins:
        comments.extend(d.file_comments)
    return comments

