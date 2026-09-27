# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/ssh_manager.py
 Version: 1.0.0
 Description: Description of this module
"""

from PythonTools.sessions import SSHSession

class SSHManager:
    def __init__(self):
        self.session: SSHSession | None = None

    def connect(self, host: str, user: str):
        self.session = SSHSession(host=host, user=user)

    def run(self, command: str):
        if self.session is None:
            raise RuntimeError("SSH session not initialized")
        return self.session.run(command)
