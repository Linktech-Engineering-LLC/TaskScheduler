# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/user_manager.py
 Version: 1.0.0
 Description: Description of this module
"""

from PythonTools.net.users import get_valid_users

class UserManager:
    def __init__(self):
        # Cache users so we don't re-scan /etc/passwd repeatedly
        self._users = get_valid_users()

    def get_users(self):
        """Return the list of valid users."""
        return self._users

    def get_default_user(self):
        """Return the first user (current user)."""
        return self._users[0] if self._users else None

    def is_valid_user(self, user):
        """Check if a user is in the valid list."""
        return user in self._users