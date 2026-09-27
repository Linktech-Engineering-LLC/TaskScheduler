# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
Modified: 2026-09-25
 File: TimerDeck.py
 Version: 1.0.0
 Description: Entry point for the TimerDeck Application
"""


import sys
from PySide6.QtWidgets import QApplication

from taskscheduler import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
