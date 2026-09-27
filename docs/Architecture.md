# TaskScheduler — Architectural Overview
Deterministic, operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite  
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Purpose](#1-purpose)
2. [High‑Level Architecture](#2-highlevel-architecture)
3. [UI Layer](#3-ui-layer)
4. [Manager Layer](#4-manager-layer)
5. [Orchestrator Layer](#5-orchestrator-layer)
6. [Data Flow](#6-data-flow)
7. [Comment Model](#7-comment-model)
8. [Future Expansion](#8-future-expansion)
9. [Architectural Guarantees](#9-architectural-guarantees)

---

## 1. Purpose
This document defines the architectural structure of **TaskScheduler**, including its UI footprint, subsystem boundaries, data‑flow model, and orchestration patterns.
It serves as the authoritative reference for contributors, maintainers, and future development phases.

TaskScheduler’s architecture is built around:
* deterministic behavior
* strict separation of concerns
* predictable UI/UX
* operator‑grade reliability
* extensibility for future systems (SSH, remote hosts, etc.)

---

## 2. High‑Level Architecture
TaskScheduler is composed of three primary layers:
1. UI Layer
2. Manager Layer
3. Orchestrator Layer

Each layer has strict responsibilities and must not leak logic into adjacent layers.

```Code
+---------------------------+
|        MainWindow         |  ← Orchestrator
+---------------------------+
| Sidebar | Menus | Views |  ← UI Layer
+---------------------------+
| CronManager | SystemdManager | EnvManager |  ← Manager Layer
+---------------------------+
| Systemd | Cron | Environment |  ← External Systems
+---------------------------+
```

---

## 3. UI Layer
The UI layer contains all Qt/PySide6 components.
It must not contain business logic, parsing logic, or system calls.

### 3.1 MainWindow
MainWindow is the **orchestrator**, not a logic container.

Responsibilities:
* Build UI structure
* Wire signals
* Maintain active system selection
* Launch editor windows
* Refresh dashboard
* Coordinate managers
* Enforce deterministic refresh cycles

Must not:
* parse cron/systemd/env data
* read/write files
* call systemctl or crontab
* contain business logic

### 3.2 Menu System (Tasks / View / File / Help)
TaskScheduler uses a **menu‑driven navigation model**, replacing the old sidebar navigation.

#### Tasks Menu
* Systemd Tasks
* Cron Jobs
* Environment Variables

#### View Menu
* Dashboard
* Logs

#### File Menu
* Settings
* Reload All
* Exit

#### Help Menu
* About
* Documentation

Menus are the **primary navigation mechanism**.

### 3.3 Sidebar (Context Selector)
The sidebar is no longer a navigation panel.
It is a **context selector**, controlling:
* Scope (User / System)
* User selection (User scope only)
* Password entry
    * required for system scope
    * required for user mismatch
* Remote mode (Local / Remote)
* Host selection (Remote only)

The sidebar uses **frame‑based visibility**, ensuring deterministic layout:
* User frame
* Password frame
* Host frame

Sidebar must not:
* perform system operations
* modify data
* contain parsing logic

### 3.4 Dashboard
Dashboard is a **summary view** only.

Responsibilities:
* Display cron entries
* Display systemd timers
* Display environment variables
* Support double‑click → open editor
* Support column resizing and scrolling

Must not:
* modify data
* perform system operations
* contain parsing logic

### 3.5 Logs View
The Logs view provides:
* structured log display
* future filtering/search
* future export capabilities
* integration with systemd journal

Must not:
* modify logs
* perform system operations
* contain parsing logic

### 3.6 Editor Windows
Each system has its own editor window:
* CronEditWindow
* SystemdEditWindow
* EnvEditWindow

Responsibilities:
* Display full editable fields
* Save changes via managers
* Delete entries via managers
* Migrate entries between systems
* Refresh dashboard after operations

Must not:
* parse cron/systemd/env data
* perform system calls directly

---

## 4. Manager Layer
Managers contain all business logic, parsing, and system interactions.

### 4.1 CronManager
Responsibilities:
* Load cron entries
* Parse inline and preceding comments
* Write updated crontabs
* Delete entries
* Convert cron → systemd (migration)

### 4.2 SystemdManager
Responsibilities:
* Enumerate timers (user + system)
* Parse unit files
* Extract next/last run times
* Extract comments:
    * preceding comment lines
    * inline comments
    * Description= fallback
* Write updated unit files
* Convert systemd → cron (migration)

### 4.3 EnvManager
Responsibilities:
* Extract environment variables
* Determine source (cron/systemd)
* Write updated environment definitions
* Migrate env → cron/systemd

---

## 5. Orchestrator Layer
MainWindow orchestrates all interactions between UI and managers.

Responsibilities:
* Maintain `active_system`
* Launch editor windows
* Refresh dashboard
* Coordinate save/delete/move operations
* Route operations to correct manager

Must not:
* contain parsing logic
* perform system calls
* modify files directly

---

## 6. Data Flow
### 6.1 Loading Data
```Code
MainWindow.refresh_dashboard()
    → CronManager.load()
    → SystemdManager.load()
    → EnvManager.load()
    → Dashboard.update_tables()
```

### 6.2 Editing Data
```Code
Dashboard.double_click(row)
    → MainWindow.open_editor(active_system)
        → EditorWindow.load(entry)
```

### 6.3 Saving Data
```Code
EditorWindow.save()
    → Manager.save(entry)
    → MainWindow.refresh_dashboard()
```

### 6.4 Migration
```Code
EditorWindow.move_to(target_system)
    → SourceManager.delete(entry)
    → TargetManager.save(converted_entry)
    → MainWindow.refresh_dashboard()
```

---

## 7. Comment Model
TaskScheduler supports comments for both cron and systemd.

### 7.1 Cron Comments
Supported:
* preceding comment lines
* inline comments
* multi‑line comment accumulation

### 7.2 Systemd Comments
Supported:
* preceding comment lines
* inline comments
* Description= fallback

Comments are displayed in:
* Dashboard
* Editor windows

---

## 8. Future Expansion
Planned architectural extensions:
* SSH remote host support
* Multi‑host dashboard
* User‑scope switching
* Privilege elevation (sudo/pkexec)
* Search/filter subsystem
* Exportable reports (JSON/YAML)
* Plugin architecture for additional schedulers

---

## 9. Architectural Guarantees
TaskScheduler guarantees:
* deterministic behavior
* reproducible parsing
* strict separation of concerns
* predictable UI footprint
* operator‑grade reliability
* extensibility without architectural drift