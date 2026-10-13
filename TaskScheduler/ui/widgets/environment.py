# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-13
 Modified: 2026-10-13
 File: TaskScheduler/ui/widgets/environment.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QLabel
)
from PySide6.QtCore import Qt


class EnvironmentWidget(QWidget):
    """
    Simple environment variable viewer.
    Uses EnvironmentTableModel provided by MainWindow.
    """

    def __init__(self, env_model, logctx=None, parent=None):
        super().__init__(parent)

        self.logctx = logctx
        self.env_model = env_model

        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Environment Variables")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Table
        self.table = QTableView()
        self.table.setModel(self.env_model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        layout.addWidget(self.table)

    def refresh(self):
        """Refresh table view after model updates."""
        self.table.reset()
