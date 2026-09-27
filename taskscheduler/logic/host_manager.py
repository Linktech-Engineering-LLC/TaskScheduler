# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/logic/host_manager.py
 Version: 1.0.0
 Description: Description of this module
"""
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon

import socket
import fnmatch
from pathlib import Path

from PythonTools.net.ssh import is_ssh_reachable


class HostManager:
    def __init__(self):
        self.remote_mode = False

    def set_remote_mode(self, enabled: bool):
        self.remote_mode = enabled
        return enabled

    # ------------------------------------------------------------
    # Stage 1: Primary host discovery from /etc/hosts
    # ------------------------------------------------------------
    def _load_hosts_from_etc(self):
        hosts = []
        current_host = socket.gethostname()

        with open("/etc/hosts") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue

                raw = raw.split("#", 1)[0].strip()
                parts = raw.split()
                if len(parts) < 2:
                    continue

                ip = parts[0]
                names = parts[1:]
                hostname = names[0]

                # Skip IPv6
                if ":" in ip:
                    continue

                # Skip loopback
                if ip.startswith("127."):
                    continue

                # Skip localhost aliases
                if any("localhost" in n for n in names):
                    continue

                # Skip current host
                if any(current_host == n for n in names):
                    continue

                hosts.append(hostname)

        return sorted(set(hosts))

    # ------------------------------------------------------------
    # Stage 2: Load SSH host patterns from ~/.ssh/config
    # ------------------------------------------------------------
    def _load_ssh_patterns(self):
        config_path = Path.home() / ".ssh" / "config"
        patterns = []

        if not config_path.exists():
            return patterns

        for line in config_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("host "):
                parts = line.split()[1:]
                for p in parts:
                    patterns.append(p)

        return patterns

    # ------------------------------------------------------------
    # Public API: two-stage filtering
    # ------------------------------------------------------------
    def get_hosts(self):
        """
        Stage 1: Filter /etc/hosts
        Stage 2: Filter those results using ~/.ssh/config patterns
        """
        base_hosts = self._load_hosts_from_etc()
        patterns = self._load_ssh_patterns()

        # Normalize everything to lowercase for case-insensitive matching
        base_hosts = [h.lower() for h in base_hosts]
        patterns = [p.lower() for p in patterns]
    
        # No SSH config → return base hosts unchanged
        if not patterns:
            return base_hosts

        filtered = []

        for host in base_hosts:
            for pattern in patterns:
                if fnmatch.fnmatch(host, pattern):
                    filtered.append(host)
                    break

        # If SSH filtering removed everything → fall back to base hosts
        return filtered or base_hosts
