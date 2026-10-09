# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-09
 File: taskscheduler/ui/widgets/cron_table.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QAbstractItemView,
)
from TaskScheduler import PROJECTNAME
from PythonTools.gui import QtLoggerMixin

class CronTableWidget(QTableWidget, QtLoggerMixin):
    def __init__(self, config: dict | None = None, logctx: dict | None = None):
        super().__init__()
        self._init_logger(logctx, "CRON", PROJECTNAME)
        self.apply_config(config)
        self.logger.info("CronTableWidget Structure Initialized.")
    def populate(self, rows):
        labels = {}
        if self.config:
            labels = self.config.get("status_labels", {"enabled": "enabled", "disabled": "disabled"})

        self.setRowCount(len(rows))
        for i, t in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(t.schedule_string()))
            self.setItem(i, 1, QTableWidgetItem(t.command))

            status = labels["enabled"] if t.enabled else labels["disabled"]
            self.setItem(i, 2, QTableWidgetItem(status))

            self.setItem(i, 3, QTableWidgetItem(t.comment))
    def apply_config(self, config: dict | None = None):
        """Apply TaskScheduler.yml cron config to the widget."""
        self.config = config or {}
        # --- Structure ---------------------------------------------------------
        columns = self.config.get(
            "columns",
            ["Schedule", "Command", "Status", "Comment"]
        )
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # --- Behavior ----------------------------------------------------------
        # readonly
        if self.config.get("readonly", True):
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.AllEditTriggers)

        # stretch last column
        self.horizontalHeader().setStretchLastSection(
            self.config.get("stretch_last", True)
        )

        # autosize columns
        if self.config.get("autosize", True):
            self.resizeColumnsToContents()
            
