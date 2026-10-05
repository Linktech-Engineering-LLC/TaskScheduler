# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-10-05
 File: taskscheduler/environment/scanner/process.py
 Version: 1.0.0
 Description: Description of this module
"""

import os
from ..raw import RawEnvEntry, Source

class ProcessScanner:
    def scan(self):
        entries = []

        for key, value in os.environ.items():
            entries.append(
                RawEnvEntry(
                    variable=key,
                    value=value,
                    source=Source.PROCESS,
                    location="process"
                )
            )

        return entries