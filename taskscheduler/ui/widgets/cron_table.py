# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/cron_table.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

class CronTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Scheduling", "Command"])
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def populate(self, rows):
        self.setRowCount(len(rows))
        for i, (schedule, command) in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(schedule))
            self.setItem(i, 1, QTableWidgetItem(command))
