# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/gui/systemd_tasks_window.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QSizePolicy
)
from ..discovery import discover_systemd_tasks
from .visualizer_widget import CalendarVisualizerWidget
from .monotonic_visualizer_widget import MonotonicVisualizerWidget

class SystemdTasksWindow(QWidget):
    def __init__(self, parent=None, logger=None):
        super().__init__(parent)
        self.setWindowTitle("Systemd Tasks")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.logger = logger
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("<b>Systemd Tasks</b>")
        header.setTextFormat(Qt.RichText)
        layout.addWidget(header)

        # Table of tasks
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Timer", "Service", "Command", "Next Run", "Last Run", "Status", "Comments"
        ])
        layout.addWidget(self.table)

        # Load data
        self._populate_table()

    def _populate_table(self):
        tasks = discover_systemd_tasks(user=True, logger=self.logger)
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            if self.logger:
                self.logger.debug(f"_populate_table row={row}]=\ntask={task}")
                print(f"row={row}\ntask={task}")

            # Timer name only
            self.table.setItem(row, 0, QTableWidgetItem(task.timer.name))
            self.table.setItem(row, 1, QTableWidgetItem(task.service.name))
            self.table.setItem(row, 2, QTableWidgetItem(task.timer.next_run or "—"))
            self.table.setItem(row, 3, QTableWidgetItem(task.timer.last_run or "—"))
            self.table.setItem(row, 4, QTableWidgetItem(task.timer.description or "active"))
            self.table.setItem(row, 5, QTableWidgetItem(", ".join(task.schedule.comments)))
