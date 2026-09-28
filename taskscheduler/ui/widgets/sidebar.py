# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-25
Modified: 2026-09-25
 File: timerdeck/ui/widgets/sidebar.py
 Version: 1.0.0
 Description: Description of this module
"""

import getpass
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QRadioButton, QComboBox,
    QLabel, QFrame, QVBoxLayout, QButtonGroup,
    QLineEdit, QCheckBox, QHBoxLayout
)
from PySide6.QtCore import Signal

from ..widgets.cards import icon

class SidebarWidget(QWidget):
    # Signals emitted upward to MainWindow
    scopeChanged = Signal(str)
    userChanged = Signal(str)
    remoteModeChanged = Signal(bool)
    hostChanged = Signal(str)
    passwordModeChanged = Signal(bool)
    newRequested = Signal()
    editRequested = Signal()
    deleteRequested = Signal()
    refreshRequested = Signal()

    def __init__(self, users: list[str], hosts: list[str]):
        super().__init__()

        self.users = users
        self.hosts = hosts
        self.current_user = getpass.getuser()

        self._build_ui()
        self._wire_signals()
        self.update_visibility()

    # ------------------------------------------------------------
    # Build UI
    # ------------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)

        # =========================================================
        # Scope Frame
        # =========================================================
        scope_frame = QFrame()
        scope_layout = QHBoxLayout(scope_frame)
        scope_layout.setContentsMargins(0, 0, 0, 0)

        self.scope_user = QRadioButton("User")
        self.scope_system = QRadioButton("System")
        self.scope_user.setChecked(True)

        scope_layout.addWidget(QLabel("Scope:"))
        scope_layout.addWidget(self.scope_user)
        scope_layout.addWidget(self.scope_system)

        layout.addWidget(scope_frame)

        # =========================================================
        # User Frame
        # =========================================================
        self.user_frame = QFrame()
        uf_layout = QHBoxLayout(self.user_frame)
        uf_layout.setContentsMargins(0, 0, 0, 0)

        self.user_label = QLabel("User:")
        self.user_selector = QComboBox()
        self.user_selector.addItems(self.users)

        uf_layout.addWidget(self.user_label)
        uf_layout.addWidget(self.user_selector)

        layout.addWidget(self.user_frame)

        # =========================================================
        # Password Frame
        # =========================================================
        self.password_frame = QFrame()
        pf_layout = QHBoxLayout(self.password_frame)
        pf_layout.setContentsMargins(0, 0, 0, 0)

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.password_toggle = QCheckBox("Show")
        self.password_toggle.toggled.connect(
            lambda checked: self.password_edit.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )

        pf_layout.addWidget(self.password_label)
        pf_layout.addWidget(self.password_edit)
        pf_layout.addWidget(self.password_toggle)

        layout.addWidget(self.password_frame)

        # =========================================================
        # Remote Frame
        # =========================================================
        remote_frame = QFrame()
        remote_layout = QHBoxLayout(remote_frame)
        remote_layout.setContentsMargins(0, 0, 0, 0)

        self.rb_local = QRadioButton("Local")
        self.rb_remote = QRadioButton("Remote")
        self.rb_local.setChecked(True)

        remote_layout.addWidget(self.rb_local)
        remote_layout.addWidget(self.rb_remote)

        layout.addWidget(remote_frame)

        # =========================================================
        # Host Frame
        # =========================================================
        self.host_frame = QFrame()
        hf_layout = QHBoxLayout(self.host_frame)
        hf_layout.setContentsMargins(0, 0, 0, 0)

        self.host_label = QLabel("Host:")
        self.host_selector = QComboBox()
        self.host_selector.addItems(self.hosts)

        hf_layout.addWidget(self.host_label)
        hf_layout.addWidget(self.host_selector)

        layout.addWidget(self.host_frame)

        # =========================================================
        # Task Controls Frame
        # =========================================================
        self.controls_frame = QFrame()
        controls_layout = QVBoxLayout(self.controls_frame)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_new = QPushButton("New")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        self.btn_refresh = QPushButton("Refresh")

        controls_layout.addWidget(self.btn_new)
        controls_layout.addWidget(self.btn_edit)
        controls_layout.addWidget(self.btn_delete)
        controls_layout.addWidget(self.btn_refresh)

        layout.addWidget(self.controls_frame)

        layout.addStretch()

    # ------------------------------------------------------------
    # Wire Signals
    # ------------------------------------------------------------
    def _wire_signals(self):
        # Scope
        self.scope_user.toggled.connect(lambda checked: checked and self.scopeChanged.emit("user"))
        self.scope_system.toggled.connect(lambda checked: checked and self.scopeChanged.emit("system"))
        self.scope_user.toggled.connect(lambda _: self.update_visibility())
        self.scope_system.toggled.connect(lambda _: self.update_visibility())

        # User
        self.user_selector.currentTextChanged.connect(self._user_changed)

        # Remote
        self.rb_local.toggled.connect(self._remote_mode_update)
        self.rb_remote.toggled.connect(self._remote_mode_update)

        # Host
        self.host_selector.currentTextChanged.connect(self.hostChanged.emit)

        # Password toggle
        self.password_toggle.toggled.connect(self.passwordModeChanged.emit)

        # Control Buttons
        self.btn_new.clicked.connect(self.newRequested.emit)
        self.btn_edit.clicked.connect(self.editRequested.emit)
        self.btn_delete.clicked.connect(self.deleteRequested.emit)
        self.btn_refresh.clicked.connect(self.refreshRequested.emit)

    # ------------------------------------------------------------
    # Visibility Logic
    # ------------------------------------------------------------
    def update_visibility(self):
        scope = "system" if self.scope_system.isChecked() else "user"
        selected_user = self.user_selector.currentText()
        remote = self.rb_remote.isChecked()

        # Password required for system OR user mismatch
        needs_password = (scope == "system") or (selected_user != self.current_user)

        # User frame only for user scope
        self.user_frame.setVisible(scope == "user")

        # Password frame
        self.password_frame.setVisible(needs_password)

        # Host frame only for remote mode
        self.host_frame.setVisible(remote)

    # ------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------
    def _user_changed(self, user):
        self.userChanged.emit(user)
        self.password_edit.clear()
        self.update_visibility()

    def _remote_mode_update(self):
        remote = self.rb_remote.isChecked()
        self.remoteModeChanged.emit(remote)
        self.update_visibility()
    # In Sidebar class
    def set_actions_visible(self, visible: bool):
        self.controls_frame.setVisible(visible)
