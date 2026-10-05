# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-05
 Modified: 2026-10-05
 File: taskscheduler/systemd/gui/monotonic_visualizer_widget.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MonotonicVisualizerWidget(QWidget):
    def __init__(self, monotonic: dict[str, str], parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        if not monotonic:
            layout.addWidget(QLabel("—"))
            return

        # Show each monotonic trigger
        for key, value in monotonic.items():
            layout.addWidget(QLabel(f"<b>{key}</b>: {value}"))
