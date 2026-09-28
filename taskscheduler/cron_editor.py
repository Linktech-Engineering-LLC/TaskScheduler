# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-28
 Modified: 2026-09-28
 File: taskscheduler/cron_editor.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QComboBox,
    QGroupBox, QScrollArea, QWidget, QSizePolicy
)
from PySide6.QtCore import Qt

class CronJobEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add or Modify Scheduled Task")
        self.setModal(True)
        self.resize(750, 500)

        main = QVBoxLayout(self)

        # --- Top section: command + comment + options ---
        top_group = QGroupBox("Task Details")
        top_layout = QGridLayout(top_group)
        top_layout.addWidget(QLabel("Command:"), 0, 0)
        self.command_edit = QLineEdit()
        top_layout.addWidget(self.command_edit, 0, 1)
        top_layout.addWidget(QLabel("Comment:"), 1, 0)
        self.comment_edit = QLineEdit()
        top_layout.addWidget(self.comment_edit, 1, 1)

        opt_layout = QHBoxLayout()
        self.enable_box = QCheckBox("Enable this task")
        self.boot_box = QCheckBox("Run at system bootup")
        self.daily_box = QCheckBox("Run every day")
        opt_layout.addWidget(self.enable_box)
        opt_layout.addWidget(self.boot_box)
        opt_layout.addWidget(self.daily_box)
        top_layout.addLayout(opt_layout, 2, 0, 1, 2)
        main.addWidget(top_group)

        # --- Middle section: 3-column grid ---
        middle = QGridLayout()

        # Left column: Months
        months_group = self._make_months_group()
        middle.addWidget(months_group, 0, 0)

        # Middle column: Days of Month + Days of Week stacked vertically
        mid_col = QVBoxLayout()
        mid_col.addWidget(self._make_days_group())
        mid_col.addWidget(self._make_weekdays_group())
        mid_widget = QWidget()
        mid_widget.setLayout(mid_col)
        middle.addWidget(mid_widget, 0, 1)

        # Right column: Hours + Minutes stacked vertically
        right_col = QVBoxLayout()
        right_col.addWidget(self._make_hours_group())
        right_col.addWidget(self._make_minutes_group())
        right_widget = QWidget()
        right_widget.setLayout(right_col)
        middle.addWidget(right_widget, 0, 2)

        main.addLayout(middle)

        # --- OK / Cancel ---
        btns = QHBoxLayout()
        btns.addStretch()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        btns.addWidget(ok)
        btns.addWidget(cancel)
        main.addLayout(btns)

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    # Helper methods for compact grids
    def _make_grid_group(self, title, labels, columns):
        group = QGroupBox(title)
        layout = QGridLayout(group)
        buttons = []

        for i, label in enumerate(labels):
            btn = QPushButton(str(label))
            btn.setCheckable(True)

            # Compact numeric buttons, flexible text buttons
            if str(label).isdigit():
                btn.setFixedWidth(32)
                btn.setFixedHeight(26)
            else:
                btn.setMinimumWidth(70)
                btn.setFixedHeight(28)

            layout.addWidget(btn, i // columns, i % columns)
            buttons.append(btn)

        # “Set All” stretches to fill width
        set_all = QPushButton("Set All")
        set_all.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(set_all, (len(labels) // columns) + 1, 0, 1, columns)
        set_all.clicked.connect(lambda: [b.setChecked(True) for b in buttons])

        group.buttons = buttons
        return group

    def _make_months_group(self):
        months = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"]
        return self._make_grid_group("Months", months, columns=2)

    def _make_days_group(self):
        days = list(range(1, 32))
        return self._make_grid_group("Days of Month", days, columns=7)

    def _make_weekdays_group(self):
        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        return self._make_grid_group("Days of Week", weekdays, columns=4)

    def _make_hours_group(self):
        hours = list(range(0, 24))
        return self._make_grid_group("Hours", hours, columns=12)

    def _make_minutes_group(self):
        group = QGroupBox("Minutes")
        layout = QVBoxLayout(group)
        grid = self._make_grid_group("Minute Selection", list(range(0, 60, 5)), columns=6)
        layout.addWidget(grid)
        preset = QComboBox()
        preset.addItems([
            "Custom selection",
            "Each minute",
            "Every 2 minutes",
            "Every 5 minutes",
            "Every 10 minutes",
            "Every 15 minutes",
            "Every 30 minutes"
        ])
        layout.addWidget(QLabel("Preselection:"))
        layout.addWidget(preset)
        return group
