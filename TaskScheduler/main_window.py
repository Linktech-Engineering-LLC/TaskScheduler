# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
 Modified: 2026-10-13
 File: taskscheduler/ui/main_window.py
 Version: 1.0.1
 Description: Main Window Orchestrator (Cleaned)
"""

import getpass

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter,
    QStackedWidget, QLabel, QMessageBox,
    QDockWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from TaskScheduler import PROJECTNAME, VERSION
from .cron import CronJobEditor
from .environment import (
    EnvironmentController,
    EnvironmentTableModel,
    EnvironmentMode
)
from .helpers import distro
from .logic import (
    CronManager,
    EnvManager,
    HostManager,
    SystemdManager,
    UserManager
)
from .systemd.gui.systemd_tasks_window import SystemdTasksWindow
from .ui.widgets import icon
from .ui.widgets import (
    CronTableWidget,
    DashboardWidget,
    SidebarWidget,
    EnvironmentWidget  # ⭐ You will need this widget
)
from PythonTools.gui import QtLoggerMixin
from PythonTools.sessions import LocalSession, SSHSession


class MainWindow(QMainWindow, QtLoggerMixin):
    request_close = Signal()

    def __init__(self, config: dict, logctx: dict | None = None):
        super().__init__()

        self._init_logger(logctx, "GUI", PROJECTNAME)
        self.logger.info("MainWindow Initialized.")

        # --- State ---
        self.cron_rows = []
        self.active_editor = None
        self.active_view = "dashboard"
        self.remote_mode = False
        self.active_host = ""

        # --- Config ---
        self.config = config or {}
        self.mode = config.get("mode")
        self.features = config.get("features", {})
        self.distro = config.get("distro", {})
        self.cron_config = self.features.get("cron", {}).copy

        # --- Capability Flags ---
        self.can_view_cron = (
            self.features.get("cron", {}).get("enabled", False)
            and distro.supports_cron(self.distro)
        )
        self.can_view_systemd = (
            self.features.get("systemd", {}).get("enabled", False)
            and distro.supports_systemd(self.distro)
        )
        self.can_view_env = (
            self.features.get("env_manager", {}).get("enabled", False)
            and distro.supports_env(self.distro)
        )

        # --- Managers ---
        self.cron_manager = CronManager(
            config=self.cron_config,
            logctx=self.logctx
        )
        self.env_manager = EnvManager()
        self.host_manager = HostManager()
        self.user_manager = UserManager()
        self.systemd_manager = SystemdManager(logctx=self.logctx)
        self.env_controller = EnvironmentController()
        self.env_model = EnvironmentTableModel([])

        # --- Active User ---
        users = self.user_manager.get_users()
        self.active_user = users[0] if users else getpass.getuser()
        self.active_scope = "user"

        # --- Icons ---
        self.icon_dashboard = icon("dashboard.svg")
        self.icon_systemd_user = icon("systemd-user.svg")
        self.icon_systemd_system = icon("systemd-system.svg")
        self.icon_cron = icon("cron.svg")
        self.icon_env = icon("env.svg")
        self.icon_close = icon("exit.svg")
        self.icon_settings = icon("settings.svg")
        self.icon_reload = icon("refresh.svg")
        self.icon_help = icon("help.svg")
        self.icon_about = icon("about.svg")
        self.icon_logs = icon("logs.svg")

        # --- Window Setup ---
        title = f"{PROJECTNAME} v{VERSION}"
        if self.mode != "production":
            title += f" — {self.mode}"
        self.setWindowTitle(title)
        self.resize(1100, 700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.statusBar().showMessage("Ready")
        self.request_close.connect(self.handle_close_request)

        # --- Build UI ---
        self._build_ui()

        # --- Actions + Signals ---
        self._create_actions()
        self._wire_signals()

        # --- Initial Dashboard Refresh ---
        self.refresh_dashboard()
        self.logger.info("MainWindow UI constructed Successfully.")

    # ============================================================
    # UI Construction
    # ============================================================
    def _build_ui(self):
        menubar = self.menuBar()

        # Menus
        self.menu_file = menubar.addMenu("&File")
        self.menu_tasks = menubar.addMenu("&Tasks")
        self.menu_view = menubar.addMenu("&View")
        self.menu_help = menubar.addMenu("&Help")

        splitter = QSplitter(Qt.Horizontal)

        # Sidebar
        self.sidebar = SidebarWidget(
            users=self.user_manager.get_users(),
            hosts=self.host_manager.get_hosts(),
            config=self.config,
            logctx=self.logctx
        )
        self.sidebar.controls_frame.hide()

        dock = QDockWidget("Sidebar", self)
        dock.setWidget(self.sidebar)
        dock.setTitleBarWidget(QWidget())
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # Main Stack
        self.stack = QStackedWidget()

        # Dashboard
        self.dashboard = DashboardWidget(self, config=self.config, logctx=self.logctx)
        self.dashboard.set_capabilities(
            cron=self.can_view_cron,
            systemd=self.can_view_systemd,
            env=self.can_view_env
        )
        self.stack.addWidget(self.dashboard)

        # Systemd placeholder
        self.systemd_placeholder = QLabel("Systemd Tasks\n\nSystemd task management will appear here.")
        self.systemd_placeholder.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(self.systemd_placeholder)

        # Cron Table
        self.cron_table = CronTableWidget(config=self.features.get("cron", {}), logctx=self.logctx)
        self.stack.addWidget(self.cron_table)

        # Environment View ⭐
        self.env_view = EnvironmentWidget(self.env_model, logctx=self.logctx)
        self.stack.addWidget(self.env_view)

        splitter.addWidget(self.stack)
        self.setCentralWidget(splitter)

        # View Indexes
        self.VIEW_DASHBOARD = 0
        self.VIEW_SYSTEMD = 1
        self.VIEW_CRON = 2
        self.VIEW_ENV = 3

        self.logger.info("MainWindow UI built successfully.")

    # ============================================================
    # Actions
    # ============================================================
    def _create_actions(self):
        # File
        self.act_settings = QAction(self.icon_settings, "Settings", self)
        self.act_reload = QAction(self.icon_reload, "Reload All", self)
        self.act_exit = QAction(self.icon_close, "Exit", self)
        self.menu_file.addAction(self.act_settings)
        self.menu_file.addAction(self.act_reload)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.act_exit)

        # Tasks
        self.act_view_systemd = QAction(self.icon_systemd_user, "Systemd Tasks", self)
        self.menu_tasks.addAction(self.act_view_systemd)
        self.act_view_systemd.setEnabled(self.can_view_systemd)

        self.act_view_cron = QAction(self.icon_cron, "Cron Jobs", self)
        self.menu_tasks.addAction(self.act_view_cron)
        self.act_view_cron.setEnabled(self.can_view_cron)

        self.act_view_env = QAction(self.icon_env, "Environment Variables", self)
        self.menu_tasks.addAction(self.act_view_env)
        self.act_view_env.setEnabled(self.can_view_env)

        # View
        self.act_view_dashboard = QAction(self.icon_dashboard, "Dashboard", self)
        self.menu_view.addAction(self.act_view_dashboard)

        # Logs submenu
        self.menu_logs = self.menu_view.addMenu("Logs")
        self.menu_logs.addAction(QAction(self.icon_logs, "TaskScheduler Logs", self))
        self.menu_logs.addAction(QAction(self.icon_logs, "Cron Logs", self))
        self.menu_logs.addAction(QAction(self.icon_logs, "Systemd Logs", self))

        # Help
        self.act_about = QAction(self.icon_about, "About", self)
        self.act_docs = QAction(self.icon_help, "Documentation", self)
        self.menu_help.addAction(self.act_about)
        self.menu_help.addAction(self.act_docs)

    # ============================================================
    # Signals
    # ============================================================
    def _wire_signals(self):
        # File
        self.act_exit.triggered.connect(self.close)
        self.act_reload.triggered.connect(self.refresh_dashboard)
        self.act_settings.triggered.connect(self.open_settings_dialog)

        # Tasks
        self.act_view_systemd.triggered.connect(lambda: self.show_view("systemd"))
        self.act_view_cron.triggered.connect(lambda: self.show_view("cron"))
        self.act_view_env.triggered.connect(lambda: self.show_view("env"))

        # View
        self.act_view_dashboard.triggered.connect(lambda: self.show_view("dashboard"))

        # Help
        self.act_about.triggered.connect(self.show_about_dialog)
        self.act_docs.triggered.connect(self.open_docs_page)

        # Sidebar
        self.sidebar.newRequested.connect(self.on_new_requested)
        self.sidebar.editRequested.connect(self.on_edit_requested)
        self.sidebar.deleteRequested.connect(self.on_delete_requested)
        self.sidebar.refreshRequested.connect(self.on_refresh_requested)

        # Cron table
        self.cron_table.itemDoubleClicked.connect(self.on_cron_row_double_clicked)

    # ============================================================
    # View Switching
    # ============================================================
    def show_view(self, view: str):
        self.active_view = view

        self.sidebar.set_actions_visible(view != "dashboard")

        match view:
            case "dashboard":
                self.refresh_dashboard()
                self.stack.setCurrentIndex(self.VIEW_DASHBOARD)

            case "systemd":
                self.open_systemd_tasks()

            case "cron":
                self.show_cron()

            case "env":
                self.stack.setCurrentIndex(self.VIEW_ENV)
                self.active_editor = "env"
                self._update_sidebar_editability()

    # ============================================================
    # Cron View
    # ============================================================
    def show_cron(self):
        scope = self.active_scope

        if scope == "user":
            self.cron_rows = self.cron_manager.load_user_cron(
                user=getpass.getuser(),
                session=LocalSession(logger=self.logger),
                needs_sudo=(self.sidebar.user_selector.currentText() != getpass.getuser())
            )
        else:
            self.cron_rows = self.cron_manager.load_system_cron()

        self.cron_table.populate(self.cron_rows)
        self.stack.setCurrentIndex(self.VIEW_CRON)
        self.active_editor = "cron"
        self._update_sidebar_editability()

    # ============================================================
    # Dashboard Refresh
    # ============================================================
    def refresh_dashboard(self):
        user = self.active_user
        needs_sudo = (self.sidebar.user_selector.currentText() != getpass.getuser())

        self.cron_rows = self.cron_manager.load_user_cron(
            user=user,
            session=LocalSession(logger=self.logger),
            needs_sudo=needs_sudo
        )
        self.dashboard.set_cron_tasks(self.cron_rows)

        systemd_rows = self.systemd_manager.load_timers(user, self.active_scope)
        self.dashboard.set_systemd_tasks(systemd_rows)

        entries = self.env_controller.load_environment(EnvironmentMode.USER)
        self.env_model.update_entries(entries)
        self.dashboard.set_environment_model(self.env_model)

    # ============================================================
    # Sidebar Callbacks
    # ============================================================
    def on_cron_row_double_clicked(self, item):
        row = item.row()
        self.cron_table.selectRow(row)
        self.edit_cron_job()

    def on_new_requested(self):
        match self.active_view:
            case "cron":
                self.new_cron_job()
            case "systemd":
                self.new_systemd_task()
            case "env":
                self.new_env_var()

    def on_edit_requested(self):
        match self.active_view:
            case "cron":
                self.edit_cron_job()
            case "systemd":
                self.edit_systemd_task()
            case "env":
                self.edit_env_var()

    def on_delete_requested(self):
        match self.active_view:
            case "cron":
                self.delete_cron_job()
            case "systemd":
                self.delete_systemd_task()
            case "env":
                self.delete_env_var()

    def on_refresh_requested(self):
        match self.active_view:
            case "cron":
                self.refresh_cron_jobs()
            case "systemd":
                self.refresh_systemd_tasks()
            case "env":
                self.refresh_env_vars()

    # ============================================================
    # Cron CRUD (stubs)
    # ============================================================
    def new_cron_job(self):
        dlg = CronJobEditor(self)
        if dlg.exec():
            entry = dlg.get_cron_entry()
            self.cron_rows.append(entry)
            self.cron_table.populate(self.cron_rows)
            self.write_crontab()

    def edit_cron_job(self):
        row = self.cron_table.currentRow()
        if row < 0:
            return

        entry = self.cron_rows[row]
        dlg = CronJobEditor(self)
        dlg.set_cron_entry(entry)

        if dlg.exec():
            updated = dlg.get_cron_entry()
            self.cron_rows[row] = updated
            self.cron_table.populate(self.cron_rows)
            self.write_crontab()

    def delete_cron_job(self):
        row = self.cron_table.currentRow()
        if row < 0:
            return
        del self.cron_rows[row]
        self.cron_table.populate(self.cron_rows)
        self.write_crontab()

    def refresh_cron_jobs(self):
        self.show_cron()

    def write_crontab(self):
        """⭐ Placeholder for temp-file → validate → save logic."""
        self.logger.info("write_crontab() called — implement cron saving workflow here.")

    # ============================================================
    # Systemd CRUD (stubs)
    # ============================================================
    def new_systemd_task(self):
        self.logger.info("new_systemd_task() placeholder")

    def edit_systemd_task(self):
        self.logger.info("edit_systemd_task() placeholder")

    def delete_systemd_task(self):
        self.logger.info("delete_systemd_task() placeholder")

    def refresh_systemd_tasks(self):
        self.logger.info("refresh_systemd_tasks() placeholder")

    # ============================================================
    # Env CRUD (stubs)
    # ============================================================
    def new_env_var(self):
        self.logger.info("new_env_var() placeholder")

    def edit_env_var(self):
        self.logger.info("edit_env_var() placeholder")

    def delete_env_var(self):
        self.logger.info("delete_env_var() placeholder")

    def refresh_env_vars(self):
        self.logger.info("refresh_env_vars() placeholder")

    # ============================================================
    # Systemd View
    # ============================================================
    def open_systemd_tasks(self):
        if not hasattr(self, "systemd_window"):
            self.systemd_window = SystemdTasksWindow(parent=self, logctx=self.logctx)
            self.stack.addWidget(self.systemd_window)

        self.stack.setCurrentWidget(self.systemd_window)
        self.active_editor = "systemd"
        self._update_sidebar_editability()

    # ============================================================
    # Misc
    # ============================================================
    def handle_close_request(self):
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit TimerDeck",
            "Are you sure you want to exit TimerDeck?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.logger.info("Closed Main Window")
            event.accept()
        else:
            event.ignore()

    def open_settings_dialog(self):
        self.logger.info("Settings dialog placeholder")

    def show_about_dialog(self):
        self.logger.info("About dialog placeholder")

    def open_docs_page(self):
        self.logger.info("Docs page placeholder")

    def set_scope(self, scope: str):
        self.active_scope = scope
        self.systemd_manager.set_scope(scope)
        icon = self.icon_systemd_user if scope == "user" else self.icon_systemd_system
        self.act_view_systemd.setIcon(icon)
        self.statusBar().showMessage(f"Scope changed to: {scope.capitalize()}")

    def _update_sidebar_editability(self):
        editor = self.active_editor

        match editor:
            case "cron":
                editable = self.features.get("cron", {}).get("editable", True)
                self.sidebar.set_actions_enabled(editable)
                move_enabled = (
                    self.features.get("systemd", {}).get("enabled", False)
                    and self.distro.get("supports_systemd", True)
                )
                self.sidebar.set_move_enabled(move_enabled)
                self.sidebar.set_move_visible(True)
                self.sidebar.set_move_label("Move to Systemd")

            case "systemd":
                editable = self.features.get("systemd", {}).get("editable", True)
                self.sidebar.set_actions_enabled(editable)
                move_enabled = (
                    self.features.get("cron", {}).get("enabled", False)
                    and self.distro.get("supports_cron", True)
                )
                self.sidebar.set_move_enabled(move_enabled)
                self.sidebar.set_move_visible(True)
                self.sidebar.set_move_label("Move to Cron")

            case "env":
                editable = self.features.get("env_manager", {}).get("editable", True)
                self.sidebar.set_actions_enabled(editable)
                self.sidebar.set_move_enabled(False)
                self.sidebar.set_move_visible(False)

            case _:
                self.sidebar.set_actions_enabled(False)
                self.sidebar.set_move_enabled(False)
