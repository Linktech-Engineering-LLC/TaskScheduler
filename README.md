# TaskScheduler — Deterministic Scheduling & Environment Management
Operator‑grade GUI for managing systemd timers, cron jobs, environment variables, and remote hosts, built with deterministic refresh cycles and strict security invariants.

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
2. [Architecture](#2-architecture)
3. [Configuration System (YAML + JSON Schema)](#3-configuration-system-yaml--json-schema)
4. [Features](#4-features)
5. [Remote Operations](#5-remote-operations)
6. [Security Model](#6-security-model)
7. [Development](#7-development)
8. [Roadmap](#8-roadmap)
9. [Related Projects](#9-related-projects)
10. [Documentation Index](#10-documentation-index)
11. [License](#11-license)

---

## 1. Overview
TaskScheduler provides a unified, deterministic interface for viewing and managing scheduled tasks across Linux systems. It integrates:
* **systemd timers**
* **cron jobs**
* **environment variables**
* **logs**
* **remote hosts (SSH)**

The application is built around operator‑grade principles: predictable behavior, explicit state transitions, deterministic refresh cycles, and strict privilege boundaries.

--- 

## 2. Architecture
TaskScheduler uses a layered architecture:

### UI Layer (PySide6)
* MainWindow
* Sidebar (scope, user, password, remote mode, host selection)
* Stacked views (Dashboard, Systemd, Cron, Env, Logs)
* Editor windows for each subsystem

### Core Layer
* Systemd Manager
* Cron Manager
* Environment Manager
* Orchestrator (deterministic refresh pipeline)
* Security & privilege model
* Remote execution model

### Data Layer
* Structured parsers for systemd, cron, and environment files
* Deterministic comment extraction
* Log viewer pipeline
* Config loaders (YAML + JSON Schema)

---

## 3. Configuration System (YAML + JSON Schema)
TaskScheduler now uses a **strict schema‑validated configuration pipeline**:

### Project.yml → Project.json
Defines:
* mode
* features
* GUI behavior
* safety rules
* install mode
* logging configuration
* paths

### distros.yml → Distros.json
Defines OS capability matrix:
* supports_cron
* supports_systemd
* supports_env
* cron/systemd paths
* binaries
* package manager

### Security.yml → Security.json
Defines:
* sudo rules
* user switching rules
* privilege escalation
* vault configuration
* password policy

### Users.yml → Users.json (planned)
Defines:
* per‑user settings
* remote host associations
* privilege overrides

All configuration files are validated at startup using JSON Schema Draft‑2020‑12.

---

## 4. Features
TaskScheduler provides:

### Unified Dashboard
* systemd timers
* cron jobs
* environment variables
* logs

### Deterministic Sidebar
* Scope (User/System)
* User selection
* Password entry (system scope or user mismatch)
* Remote mode toggle
* Host selection

### Subsystem Editors
* Cron editor
* Systemd timer editor
* Environment variable editor

### Parsing Features
* Inline + preceding comments (cron + systemd)
* Multi‑line comment accumulation
* Description fallback for systemd

### Cross‑System Operations
* Cron ↔ Systemd
* Env ↔ Cron/Systemd

### Remote Host Support
* SSH config parsing
* Remote cron/systemd/env operations
* Deterministic remote execution pipeline

---

## 5. Remote Operations
Remote operations follow the rules defined in [Remote.md](docs/security/Remote.md):
* SSH‑based execution only
* No plaintext transport
* No persistent sessions
* Deterministic command execution
* Vault / Encrypton / SSH key authentication
* Remote cron/systemd/env management

Remote mode integrates seamlessly with the sidebar and password model.

---

## 6. Security Model
Security follows the invariants defined in [Passwords.md](/docs/security/Passwords.md) and **Security.json**:
* Passwords never logged
* Passwords never retained longer than necessary
* Passwords never written to disk unless encrypted
* Vault + Encrypton support
* Plaintext only allowed with strict permissions
* System‑scope operations always require authentication
* All password handling goes through PasswordManager
* Remote passwords transmitted only over SSH

Privilege escalation is deterministic and explicit.

---

## 7. Development
### Requirements
* Python 3.12+
* PySide6
* Access to systemctl, journalctl, crontab

### Running
```bash
python -m timerdeck
```

### Project Structure
```Code
timerdeck/
 ├─ ui/
 ├─ core/
 ├─ data/
 ├─ resources/
 └─ tests/
```

---

## 8. Roadmap
### Phase 2 (Current)
* Data integration
* Sidebar refactor
* Password logic
* Remote host enumeration
* Orchestrator conversion

### Phase 3
* Editor windows
* Move operations
* Privilege‑aware actions
* Log viewer enhancements

### Phase 4
* Diagnostics
* Search/filtering
* Full SSH remote support

### Phase 5
* Dark mode
* Packaging

v1.0 release

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

---

## 11. License
TaskScheduler is released under the MIT License.
See the [LICENSE](LICENSE) file for full details.