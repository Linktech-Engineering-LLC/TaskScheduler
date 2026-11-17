# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-11-12
 Modified: 2026-11-17
 File: TaskScheduler/services/user_discovery.py
 Version: 1.0.0
 Description: Description of this module
"""

# services/user_discovery.py

import pwd

from PythonTools.gui import QtLoggerMixin

from TaskScheduler import PROJECTNAME


class UserDiscoveryService(QtLoggerMixin):

    def __init__(self, user_config: dict, logctx: dict | None = None):
        self._init_logger(logctx, "USERS", PROJECTNAME)
        self.user_config = user_config

    def get_users(self) -> list[str]:

        self.logger.debug("get_users: start")
        min_uid = self.user_config["min_uid"]
        home_prefix = self.user_config["required_home_prefix"]
        require_home = self.user_config.get("required_home_directory", True)
        entries = pwd.getpwall()

        self.logger.debug(f"get_users: entries={len(entries)}")

        users = sorted(
            {
                entry.pw_name
                for entry in pwd.getpwall()
                if (
                    entry.pw_uid >= min_uid
                    and entry.pw_shell
                    not in ("/sbin/nologin", "/usr/sbin/nologin", "/bin/false")
                    and (not require_home or entry.pw_dir.startswith(home_prefix))
                )
            }
        )
        self.logger.debug(f"get_users: users={len(users)}")

        return users
