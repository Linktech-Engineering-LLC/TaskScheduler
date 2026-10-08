# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
 Modified: 2026-10-08
 File: taskscheduler/ui/widgets/dashboard.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea,
    QTableView
)
from PySide6.QtCore import Qt

from TaskScheduler import PROJECTNAME
from ...models import SchedulerCapabilities, EnvironmentViewModel

from PythonTools.gui import QtLoggerMixin


class DashboardWidget(QWidget, QtLoggerMixin):
    def __init__(self, parent=None, config: dict | None = None, logctx: dict | None = None):
        super().__init__(parent)
        self._init_logger(logctx, "DASHBOARD", PROJECTNAME)
        self.logger.info("DashboardWidget Initialized.")

        self.config = config or {}

        self.env      = self.config.get("environment") or {}
        self.distro   = self.config.get("distro") or {}
        self.features = self.config.get("features") or {}
        self.mode     = self.config.get("mode") or "unknown"

        missing = []
        if not self.env: missing.append("environment")
        if not self.distro: missing.append("distro")
        if not self.features: missing.append("features")
        if self.mode == "unknown": missing.append("mode")

        if missing:
            self.logger.warning(f"Dashboard config missing or null keys: {missing}")
        elif self.logctx.get("level") == "DEBUG":
            self.logger.debug(f"distro: {self.distro}")
            self.logger.debug(f"features: {self.features}")
            
        self.scheduler_caps = SchedulerCapabilities(self.env, self.distro, self.features)
        self.env_vm = EnvironmentViewModel(self.env, self.distro, self.mode)

        self.apply_distro_rules()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # --- Cron Tasks ---
        self.cron_table = self._make_table(
            title="Cron Tasks",
            headers=["Schedule", "Command", "Comment"]
        )
        layout.addWidget(self.cron_table)

        # --- Systemd Tasks ---
        self.systemd_table = self._make_table(
            title="Systemd Tasks",
            headers=["Timer", "Service", "Next Run", "Last Run", "Status"]
        )
        layout.addWidget(self.systemd_table)

        # --- Environment Variables ---
        self.env_table = self._make_env_table("Environment Variables")
        layout.addWidget(self.env_table)
        self.finalize_logging_wrappers()

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
    def _make_env_table(self, title):
        group = QGroupBox(title)

        table = QTableView()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(table)

        layout = QVBoxLayout(group)
        layout.addWidget(scroll)

        group.table = table
        return group

    # ---------------------------------------------------------
    # Public API: Populate Cron Tasks
    # ---------------------------------------------------------
    def set_cron_tasks(self, tasks):
        if not self.cron_enable:
            return
        table = self.cron_table.table
        table.setRowCount(0)

        for row, t in enumerate(tasks):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(t.schedule_string()))
            table.setItem(row, 1, QTableWidgetItem(t.command))
            table.setItem(row, 2, QTableWidgetItem(t.comment))

    # ---------------------------------------------------------
    # Public API: Populate Systemd Tasks
    # ---------------------------------------------------------
    def set_systemd_tasks(self, tasks):
        if not self.systemd_enable:
            return
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
    def set_environment_model(self, model):
        if self.env_enabled:
            self.env_table.table.setModel(model)

    def apply_distro_rules(self):
        self.cron_enable = (
            self.features.get("cront", True)
            and self.distro.get("supports_cron", True)
        )
        self.systemd_enable = (
            self.features.get("systemd", True)
            and self.distro.get("supports_systemd", True)
        )
        self.env_enabled = (
            self.features.get("env_manager", False)
            and self.distro.get("supports_env", False)
        )
    def clear_environment_model(self):
        # If env_model doesn't exist yet, create an empty one
        if not hasattr(self, "env_model"):
            from TaskScheduler.environment import EnvironmentTableModel
            self.env_model = EnvironmentTableModel([])

        # Replace entries with empty list
        self.env_model.update_entries([])

        # Push empty model into the UI
        self.set_environment_model(self.env_model)
