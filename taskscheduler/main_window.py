# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-05-16
Modified: 2026-09-25
 File: timerdeck/ui/main_window.py
 Version: 1.0.0
 Description: Main Window Orchestrator
"""


from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter,
    QStackedWidget, QLabel, QMessageBox, 
    QDockWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from .cron_editor import CronJobEditor
from .environment import (
    EnvironmentController,
    EnvironmentTableModel,
    EnvironmentMode
)
from .logic import (
    CronManager,
    EnvManager,
    HostManager,
    SystemdManager,
    UserManager
)
from .ui.widgets import icon, make_card
from .ui.widgets import (
    CronTableWidget,
    DashboardWidget,
    SidebarWidget
)

from PythonTools.net.users import get_valid_users

class MainWindow(QMainWindow):
    request_close = Signal()

    def __init__(self):
        super().__init__()
        
        self.cron_rows = []
        # --- Icons ---
        self.icon_dashboard = icon("dashboard.svg")
        self.icon_systemd_user = icon("systemd-user.svg")
        self.icon_systemd_system = icon("systemd-system.svg")
        self.icon_cron = icon("cron.svg")
        self.icon_env = icon("env.svg")
        self.icon_logs = icon("logs.svg")  # placeholder for future
        self.icon_close = icon("exit.svg")
        self.icon_settings = icon("settings.svg")
        self.icon_reload = icon("refresh.svg")
        self.icon_help = icon("help.svg")
        self.icon_about = icon("about.svg")
        self.icon_logs = icon("logs.svg")

        # --- Managers ---
        self.cron_manager = CronManager()
        self.env_manager = EnvManager()
        self.host_manager = HostManager()
        self.user_manager = UserManager()
        self.systemd_manager = SystemdManager()
        self.env_controller = EnvironmentController()
        self.env_model = EnvironmentTableModel([])

        # --- State ---
        self.active_scope = "user"
        self.active_user = self.user_manager.get_users()[0] if self.user_manager.get_users() else ""
        self.remote_mode = False
        self.active_host = ""
        self.active_view = "dashboard"

        # --- Window Setup ---
        self.setWindowTitle("TimerDeck")
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

    # ============================================================
    # UI Construction
    # ============================================================
    def _build_ui(self):
        menubar = self.menuBar()
       # --- Top-level menus ---
        self.menu_file = menubar.addMenu("&File")
        self.menu_tasks = menubar.addMenu("&Tasks")
        self.menu_view = menubar.addMenu("&View")
        self.menu_help = menubar.addMenu("&Help")

        # --- Main Splitter ---
        splitter = QSplitter(Qt.Horizontal)

        # --- Sidebar ---
        self.sidebar = SidebarWidget(
            users=self.user_manager.get_users(),
            hosts=self.host_manager.get_hosts()
        )
        self.sidebar.controls_frame.hide()

        dock = QDockWidget("Sidebar", self)
        dock.setWidget(self.sidebar)
        dock.setTitleBarWidget(QWidget())  # hide title bar
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # --- Main Content Stack ---
        self.stack = QStackedWidget()

        # Dashboard
        self.dashboard = DashboardWidget()
        self.stack.addWidget(self.dashboard)

        # Systemd placeholder
        systemd_view = QLabel("Systemd Timers\n\nList of systemd timers will appear here.")
        systemd_view.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(systemd_view)

        # Cron Table
        self.cron_table = CronTableWidget()
        self.stack.addWidget(self.cron_table)

        splitter.addWidget(self.stack)
        self.setCentralWidget(splitter)

        self.VIEW_DASHBOARD = 0
        self.VIEW_SYSTEMD = 1
        self.VIEW_CRON = 2

    # ============================================================
    # Actions
    # ============================================================
    def _create_actions(self):

        # --- File ---
        self.act_settings = QAction(self.icon_settings, "Settings", self)
        self.act_reload = QAction(self.icon_reload, "Reload All", self)
        self.act_exit = QAction(self.icon_close, "Exit", self)
        self.menu_file.addAction(self.act_settings)
        self.menu_file.addAction(self.act_reload)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.act_exit)

        # --- Tasks ---
        self.act_view_systemd = QAction(self.icon_systemd_user, "Systemd Tasks", self)
        self.act_view_cron = QAction(self.icon_cron, "Cron Jobs", self)
        self.act_view_env = QAction(self.icon_env, "Environment Variables", self)
        self.menu_tasks.addAction(self.act_view_systemd)
        self.menu_tasks.addAction(self.act_view_cron)
        self.menu_tasks.addAction(self.act_view_env)

        # --- View ---
        self.act_view_dashboard = QAction(self.icon_dashboard, "Dashboard", self)
        self.menu_view.addAction(self.act_view_dashboard)
        # 2. Logs submenu SECOND
        self.menu_logs = self.menu_view.addMenu("Logs")
        self.action_view_ts_logs = QAction(self.icon_logs, "TaskScheduler Logs", self)
        self.action_view_cron_logs = QAction(self.icon_logs, "Cron Logs", self)
        self.action_view_systemd_logs = QAction(self.icon_logs, "Systemd Logs", self)

        self.menu_logs.addAction(self.action_view_ts_logs)
        self.menu_logs.addAction(self.action_view_cron_logs)
        self.menu_logs.addAction(self.action_view_systemd_logs)
        # --- Help ---
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
        
        # Row Signals
        self.cron_table.itemDoubleClicked.connect(self.on_cron_row_double_clicked)
        self.sidebar.newRequested.connect(self.on_new_requested)
        self.sidebar.editRequested.connect(self.on_edit_requested)
        self.sidebar.deleteRequested.connect(self.on_delete_requested)
        self.sidebar.refreshRequested.connect(self.on_refresh_requested)

    # ============================================================
    # View Switching
    # ============================================================
    def show_view(self, view: str):
        self.active_view = view

        # Sidebar button visibility logic
        if view == "dashboard":
            self.sidebar.set_actions_visible(False)
        else:
            self.sidebar.set_actions_visible(True)
        
        match view:
            case "dashboard":
                self.stack.setCurrentIndex(self.VIEW_DASHBOARD)

            case "systemd":
                self.stack.setCurrentIndex(self.VIEW_SYSTEMD)

            case "cron":
                self.stack.setCurrentIndex(self.VIEW_CRON)
                self.show_cron()

            case _:
                # Optional: fallback
                self.stack.setCurrentIndex(0)

    # ============================================================
    # Sidebar Callbacks
    # ============================================================
    def load_user_cron(self, user: str):
        self.active_user = user
        self.cron_rows = self.cron_manager.load_user_cron(user)
        self.dashboard.set_cron_tasks(self.cron_rows)

    def set_host(self, host: str):
        self.active_host = host

    def update_remote_mode(self, remote: bool):
        self.remote_mode = remote
        self.host_manager.set_remote_mode(remote)

    # ============================================================
    # Dashboard Refresh
    # ============================================================
    def refresh_dashboard(self):
        user = self.active_user
        scope = self.active_scope

        self.cron_rows = self.cron_manager.load_user_cron(user)
        self.dashboard.set_cron_tasks(self.cron_rows)

        systemd_rows = self.systemd_manager.load_timers(user, scope)
        self.dashboard.set_systemd_tasks(systemd_rows)

        entries = self.env_controller.load_environment(EnvironmentMode.USER)
        self.env_model.update_entries(entries)
        self.dashboard.set_environment_model(self.env_model)

    # ============================================================
    # Cron View
    # ============================================================
    def show_cron(self):
        scope = self.active_scope

        if scope == "user":
            self.cron_rows = self.cron_manager.load_user_cron(self.active_user)
        else:
            self.cron_rows = self.cron_manager.load_system_cron()

        self.cron_table.populate(self.cron_rows)
        self.stack.setCurrentWidget(self.cron_table)

    # ============================================================
    # Close Handling
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
            event.accept()
        else:
            event.ignore()
    def populate(self, rows):
        self.setRowCount(len(rows))
        for i, entry in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(entry.schedule_string()))
            self.setItem(i, 1, QTableWidgetItem(entry.command))
            self.setItem(i, 2, QTableWidgetItem("enabled" if entry.enabled else "disabled"))
            self.setItem(i, 3, QTableWidgetItem(entry.comment))

    # ============================================================
    # Placeholder Methods for Actions
    # ============================================================
    def open_settings_dialog(self):
        pass

    def new_timer(self):
        pass

    def edit_selected_timer(self):
        pass

    def delete_selected_timer(self):
        pass

    def show_about_dialog(self):
        pass

    def open_docs_page(self):
        pass
    def set_scope(self, scope: str):
        """Update active scope when SidebarWidget changes it."""
        self.active_scope = scope
        if scope == "user":
            self.act_view_systemd.setIcon(self.icon_systemd_user)
        else:
            self.act_view_systemd.setIcon(self.icon_systemd_system)      
        self.systemd_manager.set_scope(scope)
        self.statusBar().showMessage(f"Scope changed to: {scope.capitalize()}")
    def get_entry_from_row(self, row):
        return self.cron_rows[row]
    
    def new_cron_job(self):
        dlg = CronJobEditor(self)
        if dlg.exec():
            entry = dlg.get_cron_entry()
            self.add_entry_to_table(entry)
            self.write_crontab()
    def edit_cron_job(self):
        row = self.cron_table.currentRow()
        if row < 0:
            return

        entry = self.get_entry_from_row(row)
        dlg = CronJobEditor(self)
        dlg.set_cron_entry(entry)

        if dlg.exec():
            updated = dlg.get_cron_entry()
            self.update_row(row, updated)
            self.write_crontab()
    def on_cron_row_double_clicked(self, item):
        row = item.row()
        self.cron_table.selectRow(row)   # ⭐ This is the missing piece
        self.edit_cron_job()
    def on_new_requested(self):
        if self.active_view == "cron":
            self.new_cron_job()
        elif self.active_view == "systemd":
            self.new_systemd_task()
        elif self.active_view == "env":
            self.new_env_var()

    def on_edit_requested(self):
        if self.active_view == "cron":
            self.edit_cron_job()
        elif self.active_view == "systemd":
            self.edit_systemd_task()
        elif self.active_view == "env":
            self.edit_env_var()
    def on_delete_requested(self):
        if self.active_view == "cron":
            self.delete_cron_job()
        elif self.active_view == "systemd":
            self.delete_systemd_task()
        elif self.active_view == "env":
            self.delete_env_var()
    def delete_cron_job(self):
        print("Delete cron job requested")

    def delete_systemd_task(self):
        print("Delete systemd task requested")

    def delete_env_var(self):
        print("Delete environment variable requested")
    def on_refresh_requested(self):
        match self.active_view:
            case "cron":
                self.refresh_cron_jobs()
            case "systemd":
                self.refresh_systemd_tasks()
            case "env":
                self.refresh_env_vars()
            case _:
                pass
    def refresh_cron_jobs(self):
        print("Refreshing cron jobs")

    def refresh_systemd_tasks(self):
        print("Refreshing systemd tasks")

    def refresh_env_vars(self):
        print("Refreshing environment variables")
