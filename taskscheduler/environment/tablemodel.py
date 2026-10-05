# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-10-05
 File: taskscheduler/environment/tablemodel.py
 Version: 1.0.0
 Description: Description of this module
"""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtGui import QColor

from .model import ResolvedEnvEntry, Status

class EnvironmentTableModel(QAbstractTableModel):
    COLUMN_VARIABLE = 0
    COLUMN_VALUE = 1
    COLUMN_STATUS = 2
    COLUMN_SOURCE = 3
    COLUMN_COMMENT = 4

    HEADERS = [
        "Variable",
        "Value",
        "Status",
        "Source",
        "Comment",
    ]

    def __init__(self, entries: list[ResolvedEnvEntry], parent=None):
        super().__init__(parent)
        self.entries = entries

    # ------------------------------------------------------------
    # Required Qt model methods
    # ------------------------------------------------------------

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.entries)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return None

    # ------------------------------------------------------------
    # Data retrieval
    # ------------------------------------------------------------

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        entry = self.entries[index.row()]
        col = index.column()

        # --- Text display ---
        if role in (Qt.DisplayRole, Qt.EditRole):
            if col == self.COLUMN_VARIABLE:
                return entry.variable
            elif col == self.COLUMN_VALUE:
                return entry.value
            elif col == self.COLUMN_STATUS:
                return entry.status.value
            elif col == self.COLUMN_SOURCE:
                return entry.source.name.lower()
            elif col == self.COLUMN_COMMENT:
                return entry.comment

        # --- Color coding for status ---
        if role == Qt.ForegroundRole and col == self.COLUMN_STATUS:
            if entry.status == Status.MASKED:
                return QColor("#c0392b")  # red
            if entry.status == Status.OVERRIDDEN:
                return QColor("#e67e22")  # orange
            if entry.status == Status.SHADOWED:
                return QColor("#7f8c8d")  # gray

        return None

    # ------------------------------------------------------------
    # Editing support
    # ------------------------------------------------------------

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if index.column() == self.COLUMN_COMMENT:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if role == Qt.EditRole and index.column() == self.COLUMN_COMMENT:
            self.entries[index.row()].comment = value
            self.dataChanged.emit(index, index)
            return True
        return False

    # ------------------------------------------------------------
    # Refresh model
    # ------------------------------------------------------------

    def update_entries(self, new_entries: list[ResolvedEnvEntry]):
        self.beginResetModel()
        self.entries = new_entries
        self.endResetModel()