# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-10-13
 File: TaskScheduler.py
 Version: 1.0.0
 Description: Entry point for the TimerDeck Application
"""

import os, sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from PythonTools.ansible import (
    load_yaml, GenericInventoryLoader, 
    VaultLoader, VaultPathError, VaultPasswordError,
)
from PythonTools.log_helpers import LoggerFactory
from PythonTools.parsing import load_yaml_with_substitution
from PythonTools.system.env import get_environment, resolve_xdg
from PythonTools.system.schemas import validate_config

from .main_window import MainWindow
from TaskScheduler import PROJECTNAME, VERSION


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def init_config(prjcfg, logctx: dict) -> dict:
    config = {}
    factory = logctx.get("factory", "")
    logger = factory.get_logger("Config")
    logger.info("Reading Configuration and Host information")
    distros = load_yaml(Path("etc/distros.yml"))
    distros = validate_config(PROJECTNAME.lower() if PROJECTNAME else "taskscheduler", "Distros", distros)
    project = prjcfg.get(PROJECTNAME, {})
    config["mode"] = project["mode"]
    config["environment"] = get_environment()
    for f in ["features", "gui", "safety", "install"]:
        block = project.get(f)
        config[f] = block if isinstance(block, dict) else {}
    features = config["features"]

    # Ensure subsystem blocks exist
    for subsystem in ["cron", "systemd", "env_manager"]:
        features[subsystem] = features.get(subsystem) or {}


    env = config.get("environment", {})
    family = env.get("family")
    flavor = env.get("details", {}).get("flavor", {})

    flavor_id = flavor.get("id")                  # opensuse-leap
    id_like = flavor.get("id_like", "")           # "suse opensuse"
    like_tokens = id_like.split()                 # ["suse", "opensuse"]

    family_block = distros.get(family, {})        # distros["linux"]
    logger.info("Determining OS and Distro")
    # 1. Direct match
    if flavor_id in family_block:
        distro_key = flavor_id
    else:
        # 2. ID_LIKE match
        distro_key = next((t for t in like_tokens if t in family_block), None)

    # 3. Fallback
    if not distro_key:
        distro_key = "default" if "default" in family_block else None

    config["distro"] = family_block.get(distro_key, {})
    if not isinstance(config["distro"], dict):
        config["distro"] = {}
    logger.info(f"Ready to process Distro: {config['distro']}")
    # ---------------------------------------------------------------------------
    # Normalize Distro Configuration
    # ---------------------------------------------------------------------------

    d = config.get("distro", {})

    # Normalize paths
    paths = {
        "cron_tab": d.get("cron_tab_path"),
        "cron_log": d.get("cron_log_path"),
        "systemd_units": d.get("systemd_unit_path"),
        "env_files": d.get("env_files", [])
    }

    # Normalize binaries
    binaries = {
        "crontab": d.get("cron_binaries", {}).get("crontab"),
        "cron_daemon": d.get("cron_binaries", {}).get("cron_daemon"),
        "cron_service": d.get("cron_binaries", {}).get("cron_service"),
        "systemctl": d.get("systemd_binaries", {}).get("systemctl"),
        "journalctl": d.get("systemd_binaries", {}).get("journalctl")
    }

    # Normalize distro block
    config["distro"] = {
        "supports_cron": d.get("supports_cron", False),
        "supports_systemd": d.get("supports_systemd", False),
        "supports_env": d.get("supports_env", False),

        "paths": paths,
        "binaries": binaries,

        "package_manager": d.get("package_manager")
    }

    logger.info(f"Distro normalized: {config['distro']}")
    return config


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def init_logging(cfg: dict) -> dict:
    log_cfg = {
        "path": Path(cfg.get("path", "")) / f"{PROJECTNAME}.log",
        "log_level": cfg.get("level", "INFO"),
        "log_max_mb": cfg.get("rotation", {}).get("max_size_mb"),
        "archive_mode": cfg.get("rotation", {}).get("archive_type"),
        "backup_count": cfg.get("rotation", {}).get("max_files"),
        "console_stream": sys.stderr,
        "console_enabled": cfg.get("console_enabled", False),
        "color": cfg.get("color_enabled", False),
        "include_stack_traces": cfg.get("include_stack_traces", False)
    }

    logger_factory = LoggerFactory(log_cfg=log_cfg, project_name=PROJECTNAME)
    logger = logger_factory.get_logger(None)
    logger.info(f"{PROJECTNAME} logging initialized.")

    return {
        "factory": logger_factory,
        "logger": logger,
        "level": log_cfg.get("log_level"),
        "highlights": cfg.get("highlight_patterns", {}),
        "subsystems": cfg.get("subsystems", {}),
        "gui": cfg.get("gui", {})
    }

# ---------------------------------------------------------------------------
# Load Security
# ---------------------------------------------------------------------------
def load_security(logctx: dict):
    factory = logctx.get("factory", {})
    logger = factory.get_logger("Security")
    cfg = load_yaml_with_substitution("etc/security.yml")
    cfg = validate_config(PROJECTNAME.lower() if PROJECTNAME else "taskscheduler", "Security", cfg)
    security = cfg.get("security", {})
    vault_cfg = security.get("vault", {})
    logger.info("Security File Successfully loaded")
    # These are now the *actual* environment variable names
    vault_path_env = vault_cfg.get("vault_path_env").upper()
    password_file_env = vault_cfg.get("password_file_env").upper()

    # Resolve environment variables
    vault_path = os.getenv(vault_path_env)
    password_file = os.getenv(password_file_env)
    logger.info("Security File Successfully Parsed")
    if not vault_path:
        raise VaultPathError(f"Environment variable {vault_path_env} not set")

    if not password_file:
        raise VaultPasswordError(f"Environment variable {password_file_env} not set")

    # Now pass the resolved values directly
    loader = VaultLoader(
        vault_file=os.path.expanduser(vault_path),
        password_source=os.path.expanduser(password_file),
        program_name=PROJECTNAME
    )
    secrets = loader.decrypt_yaml()
    policy = {
        "sudo": security.get("sudo", {}),
        "user_switching": security.get("user_switching", {}),
        "privilege_escalation": security.get("privilege_escalation", {}),
        "password_policy": security.get("password_policy", {})
    }
    logger.info("Config loaded with Security Policy and Secrets")
    return {
        "security": policy,
        "secrets": secrets
    }
# ---------------------------------------------------------------------------
# Load Users
# ---------------------------------------------------------------------------
def load_users_cfg(config: dict, logctx: dict):
    factory = logctx.get("factory", {})
    logger = factory.get_logger("USER_CFG")

    paths = config.get("paths", {})

    # Resolve XDG roots
    data_root = resolve_xdg("XDG_DATA_HOME",
                            paths.get("data_root"),
                            "~/.local/share/taskscheduler")

    cache_root = resolve_xdg("XDG_CACHE_HOME",
                             paths.get("temp_root"),
                             "~/.cache/taskscheduler")

    config_home = resolve_xdg("XDG_CONFIG_HOME",
                              paths.get("config_root"),
                              "~/.config/taskscheduler")

    # Users file location
    users_file = Path(config_home) / "users.yml"

    if not users_file.exists():
        logger.info(f"No users.yml found at {users_file}, skipping user config.")
        return {
            "users": {},
            "paths": {
                "data_root": data_root,
                "cache_root": cache_root,
                "config_home": config_home
            }
        }

    logger.info(f"Loading users.yml from {users_file}")

    # Load YAML
    users_cfg = load_yaml(users_file)

    # Optional: validate against a Users.json schema if you create one
    try:
        users_cfg = validate_config(
            PROJECTNAME.lower() if PROJECTNAME else "taskscheduler",
            "Users",
            users_cfg
        )
        logger.info("Users.yml validated successfully.")
    except Exception as e:
        logger.error(f"Users.yml validation failed: {e}")
        # Fail-safe: still load raw config
        # (You can choose to raise instead)
        pass

    # Normalize user config
    users = users_cfg.get("users", {}) if isinstance(users_cfg, dict) else {}

    logger.info(f"Users loaded: {list(users.keys())}")

    return {
        "users": users,
        "paths": {
            "data_root": data_root,
            "cache_root": cache_root,
            "config_home": config_home
        }
    }
# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    cfg = load_yaml(Path("etc/Project.yml"))
    cfg = validate_config(PROJECTNAME.lower() if PROJECTNAME else "taskscheduler", "Project", cfg)
    logctx = init_logging(cfg.get("logs", {}))
    config = init_config(cfg, logctx)
    policy = load_security(logctx=logctx)
    config["security"] = policy.get("security", {})
    config["secrets"] = policy.get("secrets", {})
    config["users"] = load_users_cfg(config=config, logctx=logctx)
    app = QApplication([])
    window = MainWindow(config, logctx)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
