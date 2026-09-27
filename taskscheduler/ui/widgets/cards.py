# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/cards.py
 Version: 1.0.0
 Description: Description of this module
"""

from pathlib import Path
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon

ICONS_DIR = Path(__file__).parents[1] / "icons"

def icon(name: str) -> QIcon:
    return QIcon(str(ICONS_DIR / name))


def make_card(title: str, value: str, icon_name: str) -> QFrame:
    card = QFrame()
    card.setObjectName("DashboardCard")
    card.setProperty("class", "DashboardCard")

    layout = QVBoxLayout(card)
    layout.setSpacing(6)

    icon_label = QLabel()
    icon_label.setPixmap(icon(icon_name).pixmap(32, 32))
    icon_label.setAlignment(Qt.AlignCenter)

    title_label = QLabel(title)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setObjectName("DashboardTitle")

    value_label = QLabel(value)
    value_label.setAlignment(Qt.AlignCenter)
    value_label.setObjectName("DashboardValue")

    layout.addWidget(icon_label)
    layout.addWidget(title_label)
    layout.addWidget(value_label)

    return card
