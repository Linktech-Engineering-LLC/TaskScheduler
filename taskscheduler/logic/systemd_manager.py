# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/systemd_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import getpass
from PythonTools.sessions import LocalSession, SystemdRunner

class SystemdManager:
    def __init__(self):
        # Default scope is personal (user-level systemd)
        self.active_scope = "personal"

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
    def load_timers(self, user, scope, ssh_manager=None):
        current_user = getpass.getuser()

        # Enforce correct scope rules
        if user != current_user:
            scope = "system"
        else:
            scope = self.active_scope
        session = ssh_manager.session if ssh_manager else LocalSession()

        if scope == "user":
            cmd = "systemctl --user list-timers --all"
        else:
            cmd = "systemctl list-timers --all"

        output = session.run(cmd)
        return self._parse_timers(output.msg)
    def _parse_timers(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and not l.startswith("NEXT") and not l.startswith("—")
        ]

        parsed = []

        for line in lines:
            parts = line.split()
            # systemctl list-timers output looks like:
            # NEXT LEFT LAST PASSED UNIT ACTIVATES
            # We only care about UNIT and ACTIVATES
            if len(parts) >= 6:
                next_run = parts[0]
                last_run = parts[2]
                unit = parts[4]
                activates = parts[5]
            else:
                continue

            parsed.append({
                "timer": unit,
                "service": activates,
                "next": next_run,
                "last": last_run,
                "status": "active"  # placeholder
            })

        return parsed
