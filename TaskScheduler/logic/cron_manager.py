# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-09
 File: timerdeck/logic/cron_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import getpass
import inspect

from ..cron import CronEntry
from TaskScheduler import PROJECTNAME
from PythonTools.gui import LoggerMixin
from PythonTools.sessions import LocalSession, SSHSession

class CronManager(LoggerMixin):
    def __init__(self, config: dict | None=None, logctx: dict | None=None):
        self._init_logger(logctx, "CRONMANAGER", PROJECTNAME)
        self.finalize_logging_wrappers()
        self.logger.info("Initializing CronManager")
    def load_user_cron(self, user: str, ssh_manager=None):
        # Determine session type
        session = ssh_manager.session if ssh_manager else LocalSession()

        # Determine current user (local or remote)
        current_user = getpass.getuser() if ssh_manager is None else ssh_manager.session.user

        # Build correct command
        if user == current_user:
            cmd = "crontab -l"
        else:
            cmd = f"sudo crontab -u {user} -l"
        if self.logctx and self.logctx.get("level") == "DEBUG":
            fname = inspect.stack()[0].function
            self.logger.debug(f"{fname} command = {cmd}")
        # Run command
        output = session.run(cmd)
        # Parse cron lines
        return self._parse_cron(output.msg)

    def _parse_cron(self, output: str):
        lines = [l.rstrip() for l in output.splitlines()]
        parsed = []
        pending_comment = ""

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            enabled = True
            inline_comment = ""
            schedule = ""
            command = ""

            # ───────────────────────────────────────────────
            # 1. Disabled or preceding comment
            # ───────────────────────────────────────────────
            if stripped.startswith("#"):
                enabled = False
                body = stripped[1:].lstrip()

                # Handle escaped disabled entries (#\0 ...)
                if body.startswith("\\"):
                    body = body[1:].lstrip()

                parts = body.split(maxsplit=5)

                # Disabled cron entry
                if len(parts) >= 6 and parts[0].isdigit():
                    schedule = " ".join(parts[:5])
                    command = parts[5].strip()
                else:
                    # Preceding comment
                    pending_comment = (pending_comment + " " + body).strip() if pending_comment else body
                    continue

            else:
                # ───────────────────────────────────────────────
                # 2. Enabled entry with optional inline comment
                # ───────────────────────────────────────────────
                if "#" in stripped:
                    stripped, inline_comment = stripped.split("#", 1)
                    inline_comment = inline_comment.strip()

                parts = stripped.split(maxsplit=5)
                if len(parts) >= 6:
                    schedule = " ".join(parts[:5])
                    command = parts[5].strip()
                else:
                    schedule = stripped
                    command = ""

            # ───────────────────────────────────────────────
            # 3. Build CronEntry (single unified path)
            # ───────────────────────────────────────────────
            minute, hour, dom, month, dow = schedule.split(maxsplit=4)
            comment = inline_comment or pending_comment or ""
            entry = CronEntry(
                minute=minute,
                hour=hour,
                dom=dom,
                month=month,
                dow=dow,
                command=command,
                comment=comment,
                enabled=enabled,
                source="user"
            )
            entry.daily = (entry.dom == "*" and entry.month == "*" and entry.dow == "*")
            entry.boot = stripped.startswith("@reboot")

            #if self.logctx and self.logctx.get("level") == "DEBUG":
            #    fname = inspect.stack()[0].function
            #    self.logger.debug(f"{fname} entry = {entry}")

            parsed.append(entry)
            pending_comment = ""

        return parsed
    def parse_schedule(self, schedule: str):
        """
        Convert a cron schedule string into a CronEntry object.
        Example: '*/5 * * * *' → CronEntry(minute='*/5', hour='*', dom='*', month='*', dow='*')
        """

        parts = schedule.split()

        if len(parts) < 5:
            raise ValueError(f"Invalid cron schedule: {schedule}")

        minute, hour, dom, month, dow = parts[:5]

        return CronEntry(
            minute=minute,
            hour=hour,
            dom=dom,
            month=month,
            dow=dow,
            command=""  # command will be filled in later
        )
        