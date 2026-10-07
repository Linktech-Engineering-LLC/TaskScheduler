# TaskScheduler
Operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite  
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Version:** 0.2.0 (In Development)  
**Packaging:** AppImage · Flatpak · DEB · RPM · TGZ · ZIP (planned)  
**PythonTools:** 0.2.0 (integration planned)  
**Last Updated:** 2026‑09‑26  

![Linktech Engineering Tools](https://img.shields.io/badge/Linktech%20Engineering-Tools%20Suite-0A66C2)
![Status: Under Construction](https://img.shields.io/badge/Status-Under_Construction-orange?style=for-the-badge)

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)
![Last Commit](https://img.shields.io/github/last-commit/Linktech-Engineering-LLC/TimerDeck)

---

## Table of Contents
1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Planned Capabilities](#3-planned-capabilities)
4. [Project Status](#4-project-status)
5. [Roadmap](#5-roadmap)
6. [Development](#6-development)
7. [Contributing](#7-contributing)
8. [License](#8-license)
9. [Related Projects](#9-related-projects)
10. [Documentation Index](#10-documentation-index)

---

## 1. Overview
**TaskScheduler** is an operator‑grade desktop GUI for inspecting, editing, and managing **systemd timers**, **cron jobs**, and **environment variables** on Linux systems.
It provides a unified interface for viewing scheduled tasks, understanding execution history, and modifying configurations without relying on command‑line tooling.

TaskScheduler is part of the **Linktech Engineering Tools Suite**, designed for deterministic, operator‑focused system management.

---

## 2. Features
* Unified dashboard for cron, systemd, environment variables, and logs
* Operator‑grade menu system:
    * **Tasks**: Systemd Tasks · Cron Jobs · Environment Variables
    * **View**: Dashboard · Logs
* Deterministic sidebar context selector:
    * Scope (User/System)
    * User selection (User scope only)
    * Password entry (System scope or user mismatch)
    * Remote/Local mode
    * Host selection (Remote only)
* Interactive column resizing with horizontal scrolling
* Systemd timer parsing (next/last run, unit linkage)
* Cron parsing with:
    * inline comments
    * preceding comments (Kcron‑style)
    * multi‑line comment accumulation
* Systemd comment support:
    * preceding comment lines in unit files
    * inline comments
    * Description= fallback
* Dedicated editor windows for:
    * Cron entries
    * Systemd timers
    * Environment variables
* Cross‑system move operations:
    * Cron ↔ Systemd
    * Env ↔ Cron/Systemd
* Deterministic parsing and refresh behavior
* Remote host support (SSH config parsing)

---

## 3. Planned Capabilities
* View systemd timers, units, and next/last run times
* Inspect associated service units and execution results
* Manage both user and system‑level timers
* View and edit cron jobs
* Unified environment variable management
* Privilege‑aware operations with on‑demand elevation
* SSH/remote host support (planned)

---

## 4. Project Status
TaskScheduler is under active development.
Current focus: **Phase‑2 architecture refactor and data integration**, including:
* Complete menu redesign (Tasks/View separation)
* Sidebar simplification (context‑only, no navigation)
* Frame‑based visibility logic for scope/user/password/remote
* Logs view integration
* Systemd/Cron/Env editor window foundations
* Deterministic refresh orchestration
* Remote host enumeration via ~/.ssh/config

---

## 5. Roadmap
### 5.1 Phase 1 — Core UI Foundation (Complete)
* Project structure and repository initialization
* Main window, sidebar navigation, stacked views
* Dashboard layout and icon system
* Initial documentation

### 5.2 Phase 2 — Data Integration (Current)
* Systemd timer enumeration (user + system)
* Cron job parsing (inline + preceding comments)
* Environment variable extraction
* Dashboard + Logs view integration
* Menu refactor (Tasks/View)
* Sidebar refactor (context selector only)
* Password logic (system scope + user mismatch)
* Remote host support (SSH config parsing)
* Orchestrator conversion

### 5.3 Phase 3 — Interaction & Management
* Timer/service detail views
* Cron/Systemd/Env editor windows
* Move operations between systems
* Start/stop/reload actions
* Privilege‑aware operations (sudo/pkexec)
* Log viewer enhancements (filtering, search, export)

#### 5.4 Phase 4 — Advanced Features
* Search and filtering across timers and units
* Failure diagnostics and log extraction
* Exportable reports (JSON/YAML)
* SSH remote host support (full)

### 5.5 Phase 5 — Polish & Release
* Dark‑mode palette and icon variants
* Hover/active states and animations
* Packaging (AppImage, Flatpak, DEB, RPM, TGZ, ZIP)
* v1.0 release

---

## 6. Development
### 6.1 Requirements
* Python 3.12+
* PySide6
* Access to `systemctl` and `journalctl`
* Linux environment (desktop or VM)

Install dependencies:

```bash
pip install -r requirements.txt
```

### 6.2 Running the Application
From the project root:

```bash
python -m timerdeck
```
Or:

```bash
python TimerDeck.py
```

### 6.3 Project Structure
```text
timerdeck/
 ├─ ui/               # Qt UI components, icons, styles
 ├─ core/             # Application logic and helpers
 ├─ data/             # systemd/cron/env parsing modules
 ├─ resources/        # stylesheets, themes
 └─ tests/            # unit tests
```

---

## 7. Contributing
Contributions are welcome once the core architecture stabilizes.
Issues and pull requests should align with the roadmap phases and maintain deterministic, operator‑grade behavior.

---

## 8. License
TimerDeck is released under the MIT License.
See the [LICENSE](LICENSE) file for full details.

---

## 9. Related Projects
TaskScheduler is part of the **Linktech Engineering Tools Suite**, a collection of deterministic, operator‑grade utilities designed for system reliability, automation, and structured tooling.

[PythonTools](https://github.com/Linktech-Engineering-LLC/PythonTools)
Deterministic Python automation utilities, including:
* structured logging
* safe file operations
* deterministic subprocess orchestration
* cross‑platform helpers

Used internally by TaskScheduler for future orchestration and packaging.

[NMS_Tools](https://github.com/Linktech-Engineering-LLC/NMS_Tools)
Network Monitoring System utilities for:
* SNMP polling
* system health checks
* structured diagnostics
* operator‑grade dashboards

Shares architectural principles with TaskScheduler (deterministic refresh, explicit state).

[CSharpTools](https://github.com/Linktech-Engineering-LLC/CSharpTools)
Cross‑platform .NET utilities built with Avalonia:
* GUI tooling
* structured editors
* operator‑grade workflows
* Provides architectural inspiration for TaskScheduler’s UI design.

**EpubPublisher** (planned)
Structured EPUB generation with:
* deterministic chapter ordering
* invariant‑based layout
* operator‑grade publishing pipeline

Will integrate with PythonTools.

**PSCleaner** (planned)
PowerShell cleanup and formatting utilities:
* whitespace normalization
* comment alignment
* deterministic formatting rules

Part of the broader Linktech tooling ecosystem.

---

## 10. Documentation Index
A structured documentation index helps operators, contributors, and maintainers navigate TaskScheduler’s architecture and behavior.

### UI Documentation
* [Menus.md](docs/ui/Menus.md)
  Tasks menu, View menu, Help menu, and operator‑grade navigation rules.
* [Sidebar.md](docs/ui/Sidebar.md)
  Scope selector, user selection, password rules, remote mode, host selection, and frame‑based visibility logic.
* [Logs.md](docs/ui/Logs.md)
  Logs view, future diagnostics, filtering, and export plans.
* [Icons.md](docs/ui/Icons.md)
  Icon system, stroke rules, design invariants, and naming conventions.

> See [docs/ui/index.md](docs/ui/index.md) for the complete UI module overview and deterministic design guarantees.

---

### Core Architecture
* [Systemd.md](docs/core/Systemd.md)
  Timer enumeration, unit linkage, next/last run parsing, comment extraction.
* [Cron.md](docs/core/Cron.md)
  Cron parsing rules, inline comments, preceding comments, multi‑line accumulation.
* [Env.md](docs/core/Env.md)
  Environment variable extraction, deterministic parsing, editor behavior.
* [Orchestrator.md](docs/core/Orchestrator.md)
  Manager orchestration model, refresh cycles, deterministic state transitions.

> See [docs/core/index.md](docs/core/index.md) for the complete architecture module overview and deterministic guarantees.

### Security & Privilege
* [Passwords.md](docs/security/Passwords.md)
  Password rules:
    * required for system scope
    * required for user mismatch
    * frame‑based visibility
    * show/hide toggle behavior
* [Remote.md](docs/security/Remote.md)
  SSH host enumeration, remote mode behavior, host selection rules.

### Development
* [Structure.md](docs/dev/Structure.md)
  Project layout, module boundaries, UI/core/data separation.
* [Testing.md](docs/dev/Testing.md)
  Unit test structure, deterministic test rules, mock environments.
* [Packaging.md](docs/dev/Packaging.md)
  Packaging plans: AppImage, Flatpak, DEB, RPM, TGZ, ZIP.

### Roadmap
* [Phase2.md](docs/roadmap/Phase2.md) — Data integration & UI stabilization
* [Phase3.md](docs/roadmap/Phase3.md) — Editors, privilege operations, move operations
* [Phase4.md](docs/roadmap/Phase4.md) — Diagnostics, search, filtering, SSH
* [Phase5.md](docs/roadmap/Phase5.md) — Polish, dark mode, packaging, v1.0 release

### [Architecture](docs/Architecture.md)
High‑level architectural overview of TaskScheduler, including:
* Application Structure
    * MainWindow
    * SidebarWidget
    * View stack (Dashboard, Systemd, Cron, Env, Logs)
    * Menu system (File, Tasks, View, Help)
* UI Architecture
    * Frame‑based sidebar design
    * Deterministic visibility rules
    * Password logic (system scope + user mismatch)
    * Remote mode and host selection
    * Icon system and design invariants
* Core Architecture
    * Systemd manager
    * Cron manager
    * Environment manager
    * Orchestrator pattern
    * Deterministic refresh cycle
    * Comment extraction rules
* Security Model
    * Privilege boundaries
    * Password requirements
    * Remote host behavior
    * Planned sudo/pkexec integration
* Data Flow
    * How views request data
    * How managers return structured results
    * How refresh cycles propagate through the UI
    * How editor windows commit changes
* Future Architectural Extensions
    * SSH remote orchestration
    * Log viewer pipeline
    * Diagnostics subsystem
    * Export/reporting pipeline
    * Packaging architecture

This document defines the invariants that keep TaskScheduler deterministic, predictable, and operator‑grade.