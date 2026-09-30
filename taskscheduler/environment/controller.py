# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-09-30
 File: taskscheduler/environment/controller.py
 Version: 1.0.0
 Description: Description of this module
"""

from .resolver import EnvironmentResolver
from .scanner.process import ProcessScanner
from .scanner.system import SystemScanner
from .scanner.user import UserScanner
from .scanner.cron import CronScanner
from .scanner.systemd import SystemdScanner
from .modes import EnvironmentMode
from .model import ResolvedEnvEntry


class EnvironmentController:
    def __init__(self):
        self.resolver = EnvironmentResolver()
        self.scanners = [
            ProcessScanner(),
            SystemScanner(),
            UserScanner(),
            CronScanner(),
            SystemdScanner(),
        ]

    def scan_raw(self):
        raw = []
        for scanner in self.scanners:
            raw.extend(scanner.scan())
        return raw

    def load_environment(self, mode: EnvironmentMode) -> list[ResolvedEnvEntry]:
        raw = self.scan_raw()
        return self.resolver.resolve_for_mode(raw, mode)
