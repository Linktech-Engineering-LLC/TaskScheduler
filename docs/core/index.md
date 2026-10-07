# Core Architecture Index
Unified index for the foundational architecture documents of the Linktech Engineering Tools Suite.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Purpose](#1-purpose)
2. [Document Set](#2-document-set)
3. [Relationships](#3-relationships)
4. [Architectural Layering](#4-architectural-layering)
5. [Deterministic Guarantees](#5-deterministic-guarantees)

---

## 1. Purpose
The `docs/core` folder contains the foundational architectural documents for TaskScheduler. These documents define the deterministic subsystems—environment, scheduling, and orchestration—that underpin the entire Linktech Engineering Tools Suite.

This index provides a unified entry point and describes how the documents relate to one another.

--- 

## 2. Document Set
[Systemd.md](Systemd.md)
Deterministic systemd unit architecture, service control, and environment isolation.

[Env.md](Env.md)
Environment model, variable resolution, configuration loading, and deterministic state management.

[Cron.md](Cron.md)
Cron architecture, parsing model, comment preservation, daily detection, and schedule normalization.

[Orchestrator.md](Orchestrator.md)
Core execution engine, task lifecycle, dependency resolution, module registration, and deterministic orchestration.

---

## 3. Relationships
The documents form a layered architecture:
* **Env** provides deterministic configuration for all modules.
* **Systemd** and **Cron** define the two primary scheduling subsystems.
* **Orchestrator** coordinates all modules and enforces architectural invariants.

Together, they define the core execution model of TaskScheduler.

---

## 4. Architectural Layering
```Code
+---------------------------+
|       Orchestrator        |
|  Deterministic Execution  |
+---------------------------+
|   Systemd   |    Cron     |
|  Scheduling |  Scheduling |
+---------------------------+
|       Env (Configuration) |
+---------------------------+
```
This layering ensures:
* reproducible execution
* isolated failures
* unified logging
* predictable behavior
* operator‑grade reliability

---

## 5. Deterministic Guarantees
The core architecture guarantees:
* consistent execution models
* structured results
* unified logging
* reproducible behavior
* strict invariants across all modules

This index serves as the authoritative map of the `docs/core` architecture module.