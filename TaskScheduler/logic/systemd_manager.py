# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-07
 File: timerdeck/logic/systemd_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import getpass

from TaskScheduler import PROJECTNAME

from PythonTools.sessions import LocalSession, SystemdRunner
from PythonTools.log_helpers import log_call
class SystemdManager:
    def __init__(self, logctx: dict | None = None):
        # Default scope is personal (user-level systemd)
        self.active_scope = "personal"
        self.logctx = logctx
        self.logfactory = None
        if logctx:
            self.logfactory = logctx.get("factory")
        if self.logfactory:
            self.logger = self.logfactory.get_logger("SYSTEMD")
        else:
            # Fallback logger: avoids crashes in test mode
            import logging
            self.logger = logging.getLogger(f"{PROJECTNAME}.SYSTEMD")
            self.logger.addHandler(logging.NullHandler())

    def set_scope(self, scope: str):
        """Set the active systemd scope."""
        if scope not in ("personal", "system"):
            scope = "system"

        self.active_scope = scope
        return scope

    def get_scope(self):
        """Return the current systemd scope."""
        return self.active_scope

    # Placeholder for future systemd timer loading
    @log_call
    def load_timers(self, user, scope, ssh_manager=None):
        session = ssh_manager.session if ssh_manager else LocalSession()

        # user=True means use --user
        if user:
            cmd = "systemctl --user list-timers --all"
        else:
            cmd = "systemctl list-timers --all"

        output = session.run(cmd)
        return self._parse_timers(output.msg)
    @log_call
    def _parse_timers(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and not l.startswith("NEXT") and not l.startswith("—")
        ]

        parsed = {}

        for line in lines:
            if "timers listed" in line.lower():
                continue                
            parts = line.split()

            unit = parts[-2]
            activates = parts[-1]
            timing = parts[:-2]

            next_run = " ".join(timing[0:4])
            last_run = " ".join(timing[5:9])

            parsed[unit] = {
                "timer": unit,
                "service": activates,
                "next": next_run,
                "last": last_run,
                "status": "active"
            }

        return list(parsed.values())
