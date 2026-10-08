# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-08
 Modified: 2026-10-08
 File: TaskScheduler/models/environment_vm.py
 Version: 1.0.0
 Description: Description of this module
"""

class EnvironmentViewModel:
    def __init__(self, env, distro, mode):
        details = env.get("details", {})
        user = env.get("user", {})

        self.os_family = env.get("family")
        self.os_name = details.get("flavor", {}).get("name") or details.get("family")
        self.arch = details.get("arch")
        self.user = user.get("login")
        self.home = user.get("home")
        self.shell = user.get("shell")
        self.mode = mode
        self.scheduler = distro.get("scheduler")
