# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-10-06
 File: TaskScheduler.py
 Version: 1.0.0
 Description: Entry point for the TimerDeck Application
"""

import pwd, getpass
import sys
from importlib.metadata import metadata
from pathlib import Path
from PySide6.QtWidgets import QApplication

from PythonTools.log_helpers import LoggerFactory
from PythonTools.ansible import load_yaml
from PythonTools.utils import read_toml

from .main_window import MainWindow
from TaskScheduler import __project_name__

ProjectName = __project_name__
ProjectMeta = metadata(ProjectName)

def init_logging(cfg):
    log_cfg = {
        "path": Path(cfg.get("path")) / f"{ProjectName}.log",
        "log_level": cfg.get("level"),
        "log_max_mb": cfg.get("rotation").get("max_size_mb"),
        "archive_mode": cfg.get("rotation").get("archive_type"),
        "backup_count": cfg.get("rotation").get("max_files"),
        "console_stream": sys.stderr,
        "console_enabled": cfg.get("console_enabled", False),
        "color": cfg.get("color_enabled", False),
        "include_stack_traces": cfg.get("include_stack_traces", False)
    }
    logger_factory = LoggerFactory(
        log_cfg=log_cfg,
        project_name=ProjectName
    )
    logger = logger_factory.get_logger(None)
    logger.info(f"{ProjectName} logging initialized.")
    return logger
def main():
    config = load_yaml(Path("etc/TaskScheduler.yml"))
    user = getpass.getuser()
    config[ProjectName]["shell"]["default"] = pwd.getpwnam(user).pw_shell

    logger = init_logging(config.get("logs", {}))

    app = QApplication(sys.argv)

    window = MainWindow(config, logger)

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
