# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-10-11
 Modified: 2026-10-11
 File: TaskScheduler/helpers/table.py
 Version: 1.0.0
 Description: Description of this module
"""

from PySide6.QtWidgets import QAbstractItemView

def apply_cron_table_structure(table, cfg):
    columns = cfg.get("columns", ["Schedule", "Command", "Status", "Comment"])
    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels(columns)

def apply_cron_table_behavior(table, cfg):
    readonly = cfg.get("readonly", True)
    stretch_last = cfg.get("stretch_last", True)
    autosize = cfg.get("autosize", True)

    if readonly:
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    else:
        table.setEditTriggers(QAbstractItemView.AllEditTriggers)

    table.horizontalHeader().setStretchLastSection(stretch_last)

    if autosize:
        table.resizeColumnsToContents()