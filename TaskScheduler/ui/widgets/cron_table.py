# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-07
 File: taskscheduler/ui/widgets/cron_table.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView
)
from TaskScheduler import PROJECTNAME
from PythonTools.gui import QtLoggerMixin

class CronTableWidget(QTableWidget, QtLoggerMixin):
    def __init__(self, logctx: dict | None = None):
        super().__init__()
        self._init_logger(logctx, "CRON", PROJECTNAME)
        self.logger.info("CronTableWidget Initialized.")
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Schedule", "Command", "Status", "Comment"])
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    def populate(self, rows):
        self.setRowCount(len(rows))
        for i, t in enumerate(rows):
            
            self.setItem(i, 0, QTableWidgetItem(t.schedule_string()))
            self.setItem(i, 1, QTableWidgetItem(t.command))
            self.setItem(i, 2, QTableWidgetItem("enabled" if t.enabled else "disabled"))
            self.setItem(i, 3, QTableWidgetItem(t.comment))

