# TaskScheduler — Contribution Guidelines
Deterministic, operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite  
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Code of Conduct](#2-code-of-conduct)
3. [How to Contribute](#3-how-to-contribute)
4. [Development Standards](#4-development-standards)
5. [Testing](#5-testing)
6. [Documentation](#6-documentation)
7. [Roadmap Alignment](#7-roadmap-alignment)
8. [Licensing](#8-licensing)
9. [Contact](#9-contact)

---

## 1. Overview
Thank you for your interest in contributing to **TaskScheduler**.
This project is part of the Linktech Engineering Tools Suite and follows strict standards for determinism, clarity, and operator‑grade reliability.

Contributions should align with:
*  the project roadmap
* deterministic behavior
* reproducible builds
* predictable UI/UX patterns
* clean separation between UI, managers, and orchestrator logic

TaskScheduler is currently in **Phase 2**, and contributions should respect the architectural direction defined in the README.

---

## 2. Code of Conduct
All contributors must follow the Linktech Engineering Code of Conduct:
* Be respectful and constructive
* Maintain professional communication
* Avoid disruptive or adversarial behavior
* Focus on clarity, correctness, and maintainability

---

## 3. How to Contribute
### 3.1 Reporting Issues
Use GitHub Issues for:
* bugs
* UI inconsistencies
* parsing errors
* incorrect systemd/cron behavior
* environment variable handling issues
* feature requests aligned with the roadmap

Please include:
* reproduction steps
* environment details
* logs or screenshots (if applicable)
* expected vs actual behavior

### 3.2 Submitting Pull Requests
Pull requests should:
* target the development branch
* follow the architectural structure (UI → Managers → Orchestrator)
* avoid introducing nondeterministic behavior
* include clear commit messages
* include tests when applicable
* update documentation if behavior changes

Before submitting:
1. Run linting
2. Run unit tests
3. Ensure UI components follow the established footprint
4. Ensure managers expose deterministic, high‑level methods
5. Ensure no business logic leaks into MainWindow or Sidebar

---

## 4. Development Standards
### 4.1 Python Style
TaskScheduler follows:
* PEP 8
* deterministic imports
* explicit typing
* no wildcard imports
* no hidden side effects

### 4.2 Qt / PySide6 Style
UI components must:
* use explicit widget construction
* avoid implicit behavior
* follow the Sidebar/MainWindow footprint
* avoid business logic
* use signals for communication
* avoid direct system calls

### 4.3 Managers
Managers must:
* expose simple, high‑level methods
* avoid UI dependencies
* avoid global state
* handle all parsing and system interactions
* return deterministic results

### 4.4 Orchestrator
MainWindow orchestrates:
* dashboard refresh
* editor window launching
* toolbar system selection
* manager coordination

It must not contain:
* parsing logic
* system calls
* direct file manipulation

---

## 5. Testing
TaskScheduler uses:
* pytest
* deterministic test fixtures
* isolated environment mocks
* no reliance on live systemd/cron state

Tests should cover:
* cron parsing
* systemd parsing
* environment variable extraction
* editor window logic
* dashboard refresh behavior

---

## 6. Documentation
Contributors should update:
* [README.md](README.md)
* CONTRIBUTING.md
* [Architecture.md](docs/Architecture.md) (if structural changes occur)
* docs/core/systemd.md (if systemd parsing changes)
* docs/cron.md (if cron parsing changes)

Documentation must remain:
* clear
* operator‑grade
* deterministic
* consistent with suite identity

---

## 7. Roadmap Alignment
All contributions must align with the TaskScheduler roadmap:
* Phase 2: Data Integration
* Phase 3: Interaction & Management
* Phase 4: Advanced Features
* Phase 5: Polish & Release

Features outside the roadmap will be deferred.

---

## 8. Licensing
By contributing, you agree that:
* all source contributions are licensed under MIT
* binary distributions may be proprietary
* contributions may be modified for consistency with suite standards

---

## 9. Contact
For questions or architectural discussions:

Maintainer:  
[Leon McClatchey](mailto:ldmcclatchey@linktechengineering.net)
[Linktech Engineering LLC](https://www.linktechengineering.net)