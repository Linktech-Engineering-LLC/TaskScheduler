# TaskScheduler — Menu System Documentation
Deterministic, operator‑grade scheduling and environment management utilities for Linux (systemd + cron).
 
**Suite:** Linktech Engineering Tools Suite  
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. Overview
2. Menu Philosophy
3. File Menu
4. Tasks Menu
5. View Menu
6. Help Menu
7. Deterministic Behavior
8. Future Expansion

---

## 1. Overview
TaskScheduler uses a menu‑driven navigation model, replacing the older sidebar navigation pattern.
Menus provide deterministic, operator‑grade access to all major subsystems:
* systemd timers
* cron jobs
* environment variables
* dashboard
* logs
* settings
* documentation

Menus are intentionally simple, predictable, and stable across all views.

---

## 2. Menu Philosophy
TaskScheduler follows three UI invariants:

### 2.1 Menus are the primary navigation mechanism
The sidebar is a **context selector**, not a navigation panel.
All system navigation happens through the menu bar.

### 2.2 Menus must remain stable
Menu items do not appear or disappear based on state.
Operators must always know where actions live.

### 2.3 Menus must reflect operator workflows
Each menu corresponds to a clear operational category:
* **File** → application‑level actions
* **Tasks** → system‑level scheduling subsystems
* **View** → UI views
* **Help** → meta‑information

---

## 3. File Menu
The File menu contains application‑level actions that affect TaskScheduler itself.

### File → Settings
Opens the settings dialog (future).
Will include:
* theme selection
* refresh interval
* remote host defaults
* logging preferences

### File → Reload All
Triggers a full refresh cycle:

```Code
CronManager.load()
SystemdManager.load()
EnvManager.load()
Dashboard.update()
Logs.update()
```
This is deterministic and always refreshes all subsystems.

### File → Exit
Closes TaskScheduler using the unified closeEvent() path.
This ensures:
* confirmation dialog
* safe shutdown
* no partial state writes

---

## 4. Tasks Menu
The Tasks menu provides access to the three scheduling subsystems.

### Tasks → Systemd Tasks
Switches the active system to systemd and opens the systemd task view.

### Tasks → Cron Jobs
Switches the active system to cron and opens the cron job view.

### Tasks → Environment Variables
Switches the active system to environment and opens the environment variable view.

### Behavior
Selecting a system:
* updates active_system
* updates the dashboard
* determines which editor window opens
* determines which manager receives save/delete/move operations

This menu replaces the old toolbar system selector.

---

## 5. View Menu
The View menu controls which UI view is displayed.

### View → Dashboard
Shows the unified dashboard containing:
* cron entries
* systemd timers
* environment variables

Dashboard is read‑only and supports double‑click → editor.

### View → Logs
Shows the logs view.

Logs view is:
* read‑only
* scrollable
* future‑filterable
* future‑exportable

---

## 6. Help Menu
The Help menu provides meta‑information.

### Help → About
Shows application metadata:
* version
* suite identity
* maintainer
* license
* build information

### Help → Documentation
Opens the documentation index.

This links to:
* README
* Architecture.md
* UI documentation
* parsing documentation
* security documentation

---

## 7. Deterministic Behavior
The menu system follows strict deterministic rules:
* Menu items never hide or change dynamically
* Menu actions always route through MainWindow
* Menu actions never perform system operations directly
* Menu actions always trigger orchestrator‑level behavior
* Menu actions never bypass the sidebar context selector
* Menus are stable, predictable, and operator‑grade.

---

## 8. Future Expansion
Planned menu additions:

### File
* Export report (JSON/YAML)
* Import configuration

### Tasks
* Remote systemd tasks (Phase 4)
* Remote cron jobs (Phase 4)

### View
* Diagnostics
* Search/filter panel

### Help
* Keyboard shortcuts
* Release notes