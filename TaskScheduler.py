# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-10-05
 File: TaskScheduler.py
 Version: 1.0.0
 Description: Entry point for the TimerDeck Application
"""


import sys
from PySide6.QtWidgets import QApplication

from PythonTools.log_helpers import LoggerFactory
from taskscheduler import MainWindow

def init_logging():
    log_cfg = {
        "path": "~/logs/TaskScheduler.log",
        "log_level": "DEBUG"
    }

    logger_factory = LoggerFactory(
        log_cfg=log_cfg,
        project_name="TaskScheduler"
    )
    logger = logger_factory.get_logger("TaskScheduler")
    logger.info("TaskScheduler logging initialized.")
    return logger
def main():
    logger = init_logging()
    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
