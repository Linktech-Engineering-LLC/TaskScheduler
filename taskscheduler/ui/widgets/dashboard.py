# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/dashboard.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea
)
from PySide6.QtCore import Qt


class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # --- Cron Tasks ---
        self.cron_table = self._make_table(
            title="Cron Tasks",
            headers=["Schedule", "Command", "Status", "Comment"]
        )
        layout.addWidget(self.cron_table)

        # --- Systemd Tasks ---
        self.systemd_table = self._make_table(
            title="Systemd Tasks",
            headers=["Timer", "Service", "Next Run", "Last Run", "Status"]
        )
        layout.addWidget(self.systemd_table)

        # --- Environment Variables ---
        self.env_table = self._make_table(
            title="Environment Variables",
            headers=["Variable", "Value", "Status", "Comment", "Source"]
        )
        layout.addWidget(self.env_table)

    # ---------------------------------------------------------
    # Helper: Create a titled table inside a scrollable QGroupBox
    # ---------------------------------------------------------
    def _make_table(self, title, headers):
        group = QGroupBox(title)

        # Table
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(table)

        # Layout inside group
        layout = QVBoxLayout(group)
        layout.addWidget(scroll)

        group.table = table
        return group

    # ---------------------------------------------------------
    # Public API: Populate Cron Tasks
    # ---------------------------------------------------------
    def set_cron_tasks(self, tasks):
        table = self.cron_table.table
        table.setRowCount(0)

        for row, t in enumerate(tasks):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(t.get("schedule", "")))
            table.setItem(row, 1, QTableWidgetItem(t.get("command", "")))
            table.setItem(row, 2, QTableWidgetItem(t.get("status", "")))
            table.setItem(row, 3, QTableWidgetItem(t.get("comment", "")))

    # ---------------------------------------------------------
    # Public API: Populate Systemd Tasks
    # ---------------------------------------------------------
    def set_systemd_tasks(self, tasks):
        table = self.systemd_table.table
        table.setRowCount(0)

        for row, t in enumerate(tasks):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(t.get("timer", "")))
            table.setItem(row, 1, QTableWidgetItem(t.get("service", "")))
            table.setItem(row, 2, QTableWidgetItem(t.get("next", "")))
            table.setItem(row, 3, QTableWidgetItem(t.get("last", "")))
            table.setItem(row, 4, QTableWidgetItem(t.get("status", "")))

    # ---------------------------------------------------------
    # Public API: Populate Environment Variables
    # ---------------------------------------------------------
    def set_environment_variables(self, env_vars):
        table = self.env_table.table
        table.setRowCount(0)

        for row, v in enumerate(env_vars):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(v.get("name", "")))
            table.setItem(row, 1, QTableWidgetItem(v.get("value", "")))
            table.setItem(row, 2, QTableWidgetItem(v.get("status", "")))
            table.setItem(row, 3, QTableWidgetItem(v.get("comment", "")))
            table.setItem(row, 4, QTableWidgetItem(v.get("source", "")))
