# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/cron_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
import getpass
import subprocess

from PythonTools.sessions import LocalSession, SSHSession

class CronManager:
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

            # Skip empty lines
            if not stripped:
                continue

            # Preceding comment (Kcron style)
            if stripped.startswith("#"):
                # Accumulate multi-line comments
                comment_text = stripped[1:].strip()
                if pending_comment:
                    pending_comment += " " + comment_text
                else:
                    pending_comment = comment_text
                continue

            # Inline comment
            inline_comment = ""
            if "#" in stripped:
                stripped, inline_comment = stripped.split("#", 1)
                inline_comment = inline_comment.strip()

            # Parse schedule + command
            parts = stripped.split(maxsplit=5)

            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = parts[5].strip()
            else:
                schedule = stripped
                command = ""

            # Choose comment priority:
            # 1. Inline comment
            # 2. Preceding comment
            comment = inline_comment if inline_comment else pending_comment

            parsed.append({
                "schedule": schedule,
                "command": command,
                "status": "enabled",
                "comment": comment
            })

            # Reset preceding comment after attaching it
            pending_comment = ""

        return parsed
