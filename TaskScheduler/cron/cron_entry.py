# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-29
 Modified: 2026-11-18
 File: taskscheduler/cron_entry.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass


@dataclass
class CronEntry:
    minute: str
    hour: str
    dom: str
    month: str
    dow: str

    command: str
    comment: str = ""

    enabled: bool = True
    daily: bool = False
    boot: bool = False

    source: str = "user"

    def schedule_string(self) -> str:
        """
        Return only the schedule portion.
        """

        if self.boot:
            return "@reboot"

        return (
            f"{self.minute} "
            f"{self.hour} "
            f"{self.dom} "
            f"{self.month} "
            f"{self.dow}"
        )

    def crontab_line(self) -> str:
        """
        Return full crontab line.
        """

        line = f"{self.schedule_string()} {self.command}"

        if not self.enabled:
            return f"# {line}"

        return line

    def validate(self) -> tuple[bool, str]:
        """
        Validate CronEntry contents.
        """

        if not self.command.strip():
            return False, "Command is required."

        if self.boot:
            return True, ""

        required = [
            ("minute", self.minute),
            ("hour", self.hour),
            ("day of month", self.dom),
            ("month", self.month),
            ("day of week", self.dow),
        ]

        for name, value in required:
            if not value:
                return False, f"{name} is required."

        return True, ""

    @classmethod
    def from_crontab_line(cls, line: str):
        """
        Parse a cron line into a CronEntry.
        """

        enabled = True

        line = line.rstrip()

        if line.startswith("#"):
            enabled = False

            for idx, ch in enumerate(line):
                if ch == "@" or ch == "*" or ch.isdigit():
                    line = line[idx:]
                    break

        if line.startswith("@reboot"):
            parts = line.split(maxsplit=1)

            return cls(
                minute="@reboot",
                hour="",
                dom="",
                month="",
                dow="",
                command=parts[1] if len(parts) > 1 else "",
                enabled=enabled,
                boot=True,
            )

        parts = line.split(maxsplit=5)

        return cls(
            minute=parts[0],
            hour=parts[1],
            dom=parts[2],
            month=parts[3],
            dow=parts[4],
            command=parts[5],
            enabled=enabled,
        )

@dataclass(frozen=True)
class MinutePreset:
    name: str
    interval: int
    tooltip: str

    def applies(self, minute: int) -> bool:
        if self.interval == 0:
            return False

        return minute % self.interval == 0


PRESETS = [
    MinutePreset("Custom Selection", 0, "Leave minute selections unchanged"),
    MinutePreset("All Minutes", 1, "Selects every Minute"),
    MinutePreset(
        "Every 2 Minutes", 2, f"Select {', '.join(str(i) for i in range(0, 60, 2))}"
    ),
    MinutePreset(
        "Every 3 Minutes", 3, f"Select {', '.join(str(i) for i in range(0, 60, 3))}"
    ),
    MinutePreset(
        "Every 4 Minutes", 4, f"Select {', '.join(str(i) for i in range(0, 60, 4))}"
    ),
    MinutePreset(
        "Every 5 Minutes", 5, f"Select {', '.join(str(i) for i in range(0, 60, 5))}"
    ),
    MinutePreset(
        "Every 10 Minutes", 10, f"Select {', '.join(str(i) for i in range(0, 60, 10))}"
    ),
    MinutePreset(
        "Every 15 Minutes", 15, f"Select {', '.join(str(i) for i in range(0, 60, 15))}"
    ),
    MinutePreset(
        "Every 30 Minutes", 30, f"Select {', '.join(str(i) for i in range(0, 60, 30))}"
    ),
]


@dataclass(frozen=True)
class CronField:
    name: str
    labels: list[str]
    values: list[str]
    columns: int
    button_width: int | None = None
    button_height: int = 28
    expanding: bool = False


MONTHS = CronField(
    name="Months",
    labels=[
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    values=[str(i) for i in range(1, 13)],
    columns=4,
    expanding=True,
)
WEEKDAYS = CronField(
    name="Days of Week",
    labels=[
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ],
    values=[str(i) for i in range(7)],
    columns=3,
    expanding=True,
)
HOURS = CronField(
    name="Hours",
    labels=[str(i) for i in range(24)],
    values=[str(i) for i in range(24)],
    columns=12,
    button_width=40,
)

MINUTES = CronField(
    name="Minutes Selection",
    labels=[str(i) for i in range(60)],
    values=[str(i) for i in range(60)],
    columns=6,
    button_width=40,
)
DAYS = CronField(
    name="Days of Month",
    labels=[str(i) for i in range(1, 32)],
    values=[str(i) for i in range(1, 32)],
    columns=7,
    button_width=40,
)
