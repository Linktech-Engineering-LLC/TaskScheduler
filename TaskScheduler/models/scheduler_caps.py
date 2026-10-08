# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-08
 Modified: 2026-10-08
 File: TaskScheduler/models/scheduler_caps.py
 Version: 1.0.0
 Description: Description of this module
"""

class SchedulerCapabilities:
    def __init__(self, env, distro, features):
        family = env.get("family")
        scheduler = distro.get("scheduler")

        self.supports_cron = scheduler == "cron"
        self.supports_systemd = scheduler == "systemd"
        self.supports_launchd = scheduler == "launchd"
        self.supports_windows = scheduler == "windows"

        self.default_scheduler = scheduler
        self.features = features
