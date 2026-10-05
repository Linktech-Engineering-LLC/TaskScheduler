# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-28
 Modified: 2026-10-05
 File: taskscheduler/cron_editor.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QComboBox,
    QGroupBox, QFormLayout, QWidget, QSizePolicy
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

        # Command
        top_layout.addWidget(QLabel("Command:"), 0, 0)
        self.command_edit = QLineEdit()
        top_layout.addWidget(self.command_edit, 0, 1)

        # Comment
        top_layout.addWidget(QLabel("Comment:"), 1, 0)
        self.comment_edit = QLineEdit()
        top_layout.addWidget(self.comment_edit, 1, 1)

        # Options
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
        self.months_group = self._make_months_group()
        middle.addWidget(self.months_group, 0, 0)

        # Middle column: Days of Month + Days of Week
        self.days_group = self._make_days_group()
        self.weekdays_group = self._make_weekdays_group()

        mid_col = QVBoxLayout()
        mid_col.addWidget(self.days_group)
        mid_col.addWidget(self.weekdays_group)

        mid_widget = QWidget()
        mid_widget.setLayout(mid_col)
        middle.addWidget(mid_widget, 0, 1)

        # Right column: Hours + Minutes
        self.hours_group = self._make_hours_group()
        self.minutes_group = self._make_minutes_group()

        right_col = QVBoxLayout()
        right_col.addWidget(self.hours_group)
        right_col.addWidget(self.minutes_group)

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

            if str(label).isdigit():
                btn.setFixedWidth(32)
                btn.setFixedHeight(26)
            else:
                btn.setMinimumWidth(70)
                btn.setFixedHeight(28)

            layout.addWidget(btn, i // columns, i % columns)
            buttons.append(btn)

        set_all = QPushButton("Set All")
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

        # ⭐ Store the grid so set_cron_entry() can access it
        group.minute_grid = grid

        return group

    def set_cron_entry(self, entry):
        self.entry = entry
        # Command + comment
        self.command_edit.setText(entry.command)
        self.comment_edit.setText(entry.comment)

        # KCron-style defaults
        self.enable_box.setChecked(entry.enabled)
        self.daily_box.setChecked(entry.daily)
        self.boot_box.setChecked(entry.boot)

        # --- Months ---
        for btn in self.months_group.buttons:
            btn.setChecked(entry.month == "*" or btn.text() in entry.month.split(","))

        # --- Days of Month ---
        for btn in self.days_group.buttons:
            btn.setChecked(entry.dom == "*" or btn.text() in entry.dom.split(","))

        # --- Days of Week ---
        for btn in self.weekdays_group.buttons:
            btn.setChecked(entry.dow == "*" or btn.text() in entry.dow.split(","))

        # --- Hours ---
        for btn in self.hours_group.buttons:
            btn.setChecked(str(btn.text()) in entry.hour.split(","))

        # --- Minutes ---
        minute_buttons = self.minutes_group.minute_grid.buttons
        for btn in minute_buttons:
            btn.setChecked(str(btn.text()) in entry.minute.split(","))
