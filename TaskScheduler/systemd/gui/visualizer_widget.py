# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-01
 Modified: 2026-10-05
 File: taskscheduler/systemd/gui/visualizer_widget.py
 Version: 1.0.0
 Description: Description of this module
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QSizePolicy
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from ..visualizer import parse_oncalendar, summarize_calendar
from ..models import CalendarSpec


class CalendarVisualizerWidget(QWidget):
    def __init__(self, oncalendar_expr: str, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spec: CalendarSpec = parse_oncalendar(oncalendar_expr)
        self.summary_text: str = summarize_calendar(self.spec)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Raw expression
        raw_label = QLabel(f"<b>OnCalendar:</b> {self.spec.raw}")
        raw_label.setTextFormat(Qt.RichText)
        layout.addWidget(raw_label)

        # Human summary
        summary_label = QLabel(self.summary_text)
        summary_label.setWordWrap(True)
        layout.addWidget(summary_label)

        # KCron-style grid
        grid = self._create_grid()
        layout.addLayout(grid)

    def _create_grid(self) -> QGridLayout:
        grid = QGridLayout()
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Header row
        for i, day in enumerate(weekdays):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, 0, i)

        # Highlight active days
        active_days = set(self.spec.weekdays)
        for i, day in enumerate(weekdays):
            cell = QLabel("●" if day in active_days else "")
            cell.setAlignment(Qt.AlignCenter)
            palette = cell.palette()
            if day in active_days:
                palette.setColor(QPalette.WindowText, QColor("#00AA00"))
            else:
                palette.setColor(QPalette.WindowText, QColor("#555555"))
            cell.setPalette(palette)
            grid.addWidget(cell, 1, i)

        return grid
