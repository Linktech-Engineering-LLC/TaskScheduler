# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-28
 Modified: 2026-11-18
 File: taskscheduler/cron_editor.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .cron_entry import (
    DAYS,
    HOURS,
    MINUTES,
    MONTHS,
    PRESETS,
    WEEKDAYS,
    CronEntry,
    CronField,
)


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
        self.command_edit.setToolTip("Command to be executed per schedule")
        top_layout.addWidget(self.command_edit, 0, 1)

        # Comment
        top_layout.addWidget(QLabel("Comment:"), 1, 0)
        self.comment_edit = QLineEdit()
        self.comment_edit.setToolTip("Description of this Task")
        top_layout.addWidget(self.comment_edit, 1, 1)

        # Options
        opt_layout = QHBoxLayout()
        self.enable_box = QCheckBox("Enable this task")
        self.enable_box.setToolTip("Check to Enable this Task")
        self.boot_box = QCheckBox("Run at system bootup")
        self.boot_box.setToolTip("Check to run at system bootup")
        self.daily_box = QCheckBox("Run every day")
        self.daily_box.setToolTip("Check to run every day")
        opt_layout.addWidget(self.enable_box)
        opt_layout.addWidget(self.boot_box)
        opt_layout.addWidget(self.daily_box)

        top_layout.addLayout(opt_layout, 2, 0, 1, 2)
        main.addWidget(top_group)

        # ------------------------------------------------------------
        # Schedule Layout
        # ------------------------------------------------------------
        middle = QGridLayout()

        # Left Column
        self.months_group = self._make_months_group()
        self.days_group = self._make_days_group()
        self.weekdays_group = self._make_weekdays_group()

        middle.addWidget(self.months_group, 0, 0)
        middle.addWidget(self.days_group, 1, 0)
        middle.addWidget(self.weekdays_group, 2, 0)

        # ------------------------------------------------------------
        # Right Column - Time
        # ------------------------------------------------------------
        time_group = QGroupBox("Time")
        time_layout = QVBoxLayout(time_group)

        self.hours_group = self._make_hours_group()
        self.minutes_group = self._make_minutes_group()

        time_layout.addWidget(self.hours_group)
        time_layout.addWidget(self.minutes_group)

        middle.addWidget(time_group, 0, 1, 3, 1)  # row, column  # rowspan, colspan

        # Give more room to Time
        middle.setColumnStretch(0, 2)
        middle.setColumnStretch(1, 3)

        main.addLayout(middle)

        # --- OK / Cancel ---
        btns = QHBoxLayout()
        btns.addStretch()
        ok = QPushButton("OK")
        ok.setToolTip("Click to Save Changes")
        cancel = QPushButton("Cancel")
        cancel.setToolTip("Click to Abort Changes and Close Form")
        btns.addWidget(ok)
        btns.addWidget(cancel)
        main.addLayout(btns)

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        self.daily_box.toggled.connect(self._daily_changed)
        self.boot_box.toggled.connect(self._boot_changed)
        self.update_controls()

    # Helper methods for compact grids
    def _make_grid_group(self, field: CronField, show_title: bool = True):
        if show_title:
            group = QGroupBox(field.name)
        else:
            group = QWidget()

        layout = QGridLayout(group)
        buttons = []

        for i, label in enumerate(field.labels):
            btn = QPushButton(str(label))
            btn.cron_value = field.values[i]
            btn.setCheckable(True)
            if field.expanding:
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif field.button_width:
                btn.setFixedWidth(field.button_width)
            btn.setFixedHeight(field.button_height)
            btn.setToolTip(f"Cron Value: {btn.cron_value}")
            layout.addWidget(btn, i // field.columns, i % field.columns)
            buttons.append(btn)

        set_all = QPushButton("Set All")
        set_all.setToolTip("Click to set all in group")
        set_all.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(
            set_all, (len(field.labels) // field.columns) + 1, 0, 1, field.columns
        )

        layout.setRowStretch((len(field.labels) // field.columns) + 2, 1)
        set_all.clicked.connect(lambda: [b.setChecked(True) for b in buttons])

        group.buttons = buttons
        return group

    def _make_months_group(self):
        group = self._make_grid_group(MONTHS)
        return group

    def _make_days_group(self):
        return self._make_grid_group(DAYS)

    def _make_weekdays_group(self):
        return self._make_grid_group(WEEKDAYS)

    def _make_hours_group(self):
        return self._make_grid_group(HOURS)

    def _make_minutes_group(self):
        group = QGroupBox("Minutes")
        layout = QVBoxLayout(group)

        grid = self._make_grid_group(MINUTES, show_title=False)

        layout.addWidget(grid)

        layout.addWidget(QLabel("Preselection:"))

        combo = QComboBox()
        for index, preset in enumerate(PRESETS):
            combo.addItem(preset.name, preset)

            combo.setItemData(index, preset.tooltip, Qt.ToolTipRole)
        combo.setToolTip("Quickly select common minute intervals")

        layout.addWidget(combo)

        combo.currentIndexChanged.connect(self._preset_changed)

        group.minute_grid = grid
        group.minute_preset = combo

        return group

    def _preset_changed(self, index: int):
        preset = self.minutes_group.minute_preset.currentData()

        if preset.interval == 0:
            return

        for btn in self.minutes_group.minute_grid.buttons:
            value = int(btn.cron_value)
            btn.setChecked(preset.applies(value))

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
            btn.setChecked(
                entry.month == "*" or btn.cron_value in entry.month.split(",")
            )

        # --- Days of Month ---
        for btn in self.days_group.buttons:
            btn.setChecked(entry.dom == "*" or btn.text() in entry.dom.split(","))

        # --- Days of Week ---
        for btn in self.weekdays_group.buttons:
            btn.setChecked(entry.dow == "*" or btn.cron_value in entry.dow.split(","))

        # --- Hours ---
        for btn in self.hours_group.buttons:
            btn.setChecked(entry.hour == "*" or btn.cron_value in entry.hour.split(","))

        # --- Minutes ---
        minute_buttons = self.minutes_group.minute_grid.buttons
        for btn in minute_buttons:
            btn.setChecked(
                entry.minute == "*" or btn.cron_value in entry.minute.split(",")
            )

    def _selected_values(self, buttons):
        values = [btn.cron_value for btn in buttons if btn.isChecked()]

        if len(values) == len(buttons):
            return "*"

        return ",".join(values)

    def accept(self):

        if not self.command_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Command is required.")
            self.command_edit.setFocus()
            return

        if not self.comment_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Comment is required.")
            self.comment_edit.setFocus()
            return

        self.entry = self.get_cron_entry()

        if not self.validate_entry(self.entry):
            return

        super().accept()

    def get_cron_entry(self) -> CronEntry:
        reboot = self.boot_box.isChecked()
        daily = self.daily_box.isChecked()

        return CronEntry(
            minute="@reboot"
            if reboot
            else self._selected_values(self.minutes_group.minute_grid.buttons),

            hour=""
            if reboot
            else self._selected_values(self.hours_group.buttons),

            dom=""
            if reboot
            else "*" if daily
            else self._selected_values(self.days_group.buttons),

            month=""
            if reboot
            else "*" if daily
            else self._selected_values(self.months_group.buttons),

            dow=""
            if reboot
            else "*" if daily
            else self._selected_values(self.weekdays_group.buttons),

            command=self.command_edit.text().strip(),
            comment=self.comment_edit.text().strip(),
            enabled=self.enable_box.isChecked(),
            daily=daily,
            boot=reboot,
        )
    
    def _daily_changed(self, checked):
        if checked:
            self.boot_box.setChecked(False)
        self.update_controls()

    def _boot_changed(self, checked):
        if checked:
            self.daily_box.setChecked(False)
        self.update_controls()

    def update_controls(self):
        daily = self.daily_box.isChecked()
        boot = self.boot_box.isChecked()

        # Daily mode
        self.months_group.setEnabled(not daily and not boot)
        self.days_group.setEnabled(not daily and not boot)
        self.weekdays_group.setEnabled(not daily and not boot)

        # Boot mode
        self.hours_group.setEnabled(not boot)
        self.minutes_group.setEnabled(not boot)

    def validate_entry(self, entry: CronEntry) -> bool:
        valid, message = entry.validate()

        if not valid:
            QMessageBox.warning(
                self,
                "Validation Error",
                message,
            )

        return valid
