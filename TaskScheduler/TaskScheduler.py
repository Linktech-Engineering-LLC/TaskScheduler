# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-10-08
 File: TaskScheduler.py
 Version: 1.0.0
 Description: Entry point for the TimerDeck Application
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from PythonTools.ansible import (
    load_yaml, GenericInventoryLoader
)
from PythonTools.log_helpers import LoggerFactory
from PythonTools.system.env import get_environment

from .main_window import MainWindow
from TaskScheduler import PROJECTNAME, VERSION


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def init_config(logctx):
    config = {}
    logger = logctx.get("logger")
    logger.info("Reading Configuration and Host information")
    yaml = load_yaml(Path("etc/TaskScheduler.yml"))
    distros = GenericInventoryLoader(Path("etc/hosts.yml"),Path("etc/hosts.schema.yml")).load()
    project = yaml.get(PROJECTNAME, {})
    config["mode"] = project["mode"]
    config["environment"] = get_environment()
    for f in ["features", "gui", "safety", "install"]:
        config[f] = project.get(f, {})
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
    logger.info(f"Ready to process Distro: {config['distro']}")
    return config


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def init_logging():
    cfg = load_yaml(Path("etc/TaskScheduler.yml")).get("logs", {})
    log_cfg = {
        "path": Path(cfg.get("path")) / f"{PROJECTNAME}.log",
        "log_level": cfg.get("level", "INFO"),
        "log_max_mb": cfg.get("rotation").get("max_size_mb"),
        "archive_mode": cfg.get("rotation").get("archive_type"),
        "backup_count": cfg.get("rotation").get("max_files"),
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
# Main entry point
# ---------------------------------------------------------------------------

def main():
    logctx = init_logging()
    config = init_config(logctx)

    app = QApplication([])
    window = MainWindow(config, logctx)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
