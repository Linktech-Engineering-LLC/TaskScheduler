# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-11
 Modified: 2026-10-11
 File: TaskScheduler/helpers/privilege.py
 Version: 1.0.0
 Description: Description of this module
"""

def can_edit_cron(security: dict, cron_cfg: dict) -> bool:
    return (
        security.get("privilege_escalation", {}).get("allow", False)
        and security.get("privilege_escalation", {}).get("allow_cron_edit", False)
        and cron_cfg.get("editable", False)
    )

def can_edit_systemd(security: dict, systemd_cfg: dict) -> bool:
    return (
        security.get("privilege_escalation", {}).get("allow", False)
        and security.get("privilege_escalation", {}).get("allow_systemd_edit", False)
        and systemd_cfg.get("editable", False)
    )

def can_edit_env(security: dict, env_cfg: dict) -> bool:
    return (
        security.get("privilege_escalation", {}).get("allow", False)
        and security.get("privilege_escalation", {}).get("allow_env_edit", False)
        and env_cfg.get("editable", False)
    )
