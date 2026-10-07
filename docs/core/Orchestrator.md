# Orchestrator — Core Execution Architecture
Deterministic, operator‑grade task coordination and subsystem orchestration for Linux automation environments.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Architectural Invariants](#2-architectural-invariants)
3. [Orchestration Model](#3-orchestration-model)
4. [Module Registration](#4-module-registration)
5. [Task Lifecycle](#5-task-lifecycle)
6. [Dependency Resolution](#6-dependency-resolution)
7. [Error Classes and Recovery](#7-error-classes-and-recovery)
8. [Logging and Diagnostics](#8-logging-and-diagnostics)
9. [Integration Points (GUI / CLI / API)](#9-integration-points-gui--cli--api)
10. [Examples](#10-examples)
11. [Future Extensions](#11-future-extensions)
12. [Deterministic Guarantees](#12-deterministic-guarantees)

---

## 1. Overview
The Orchestrator is the deterministic execution engine that coordinates all subsystems within TaskScheduler. It provides a unified, predictable mechanism for running tasks, validating environments, resolving dependencies, and isolating failures. Every module—CronManager, SystemdManager, GUI, CLI, and future extensions—executes through the Orchestrator.

The Orchestrator exists to ensure:
* **Consistency**: Every operation follows the same lifecycle.
* **Isolation**: No module can crash the system.
* **Determinism**: Results are reproducible across machines and environments.
* **Clarity**: Logs, errors, and results follow a uniform structure.

It is the “traffic controller” of the Linktech Engineering Tools Suite.

---

## 2. Architectural Invariants
The Orchestrator enforces the following invariants across all modules:
* **Invariant 1 — Deterministic Execution**
  No operation runs without a validated context and a deterministic pre‑check.
* **Invariant 2 — Structured Results**
  Every task returns a Result object containing:
  `status`, `payload`, `context`, `errors`, and `logs`.
* **Invariant 3 — Failure Isolation**
  No module may raise an unhandled exception into the Orchestrator.
  All exceptions are wrapped into structured error classes.
* **Invariant 4 — Mandatory Logging**
  Every operation logs start, end, and result using the unified logging schema.
* **Invariant 5 — No Hidden Side Effects**
  All state changes must be declared in the module metadata.
* **Invariant 6 — Reproducibility**
  The same task, with the same inputs, produces the same outputs.

These invariants define the Orchestrator’s identity and guarantee operator‑grade reliability.

---

## 3. Orchestration Model
The Orchestrator supports two execution paths:

### Synchronous Execution
Used for tasks that must complete before the next step:
* Cron parsing
* Systemd unit inspection
* GUI-triggered operations
* CLI commands

Synchronous tasks block until completion and return a structured result.

### Asynchronous Execution
Used for background or long‑running operations:
* Periodic refresh tasks
* Deferred validation
* Background diagnostics
* Future remote orchestration

Asynchronous tasks run in managed worker threads with lifecycle tracking.

### Execution Flow
1. Task request received
2. Context validation
3. Dependency resolution
4. Execution
5. Result packaging
6. Logging
7. Post‑processing hooks
8. Return to caller

This flow is identical for all modules.

---

## 4. Module Registration
Modules register themselves with the Orchestrator using a simple metadata declaration:
* **Module name**
* **Supported operations**
* **Required dependencies**
* **Optional capabilities**
* **State mutation declarations**

Example (conceptual):

```Code
Module: CronManager
Operations: load_user_cron, write_user_cron
Dependencies: system.cron, parser
Capabilities: daily detection, comment preservation
```

The Orchestrator uses this metadata to validate tasks before execution.

---

## 5. Task Lifecycle
Every task follows the same lifecycle:
1. **Request**
   The caller submits a task with parameters and context.
2. **Validation**
   The Orchestrator ensures the module and operation exist and are authorized.
3. **Dependency Resolution**
   All required subsystems are checked for availability.
4. **Execution**
   The module performs the operation inside a controlled execution wrapper.
5. **Result Packaging**
   Output is wrapped into a structured Result object.
6. **Logging**
   Start, end, and result are logged with module namespace.
7. **Post‑Processing**
   Optional hooks run (GUI refresh, state sync, etc.).
8. **Return**
   The caller receives the structured result.

This lifecycle is the backbone of deterministic behavior.

---

## 6. Dependency Resolution
Modules declare dependencies such as:
* system binaries
* configuration files
* environment variables
* Python modules
* external services

The Orchestrator resolves these dependencies before execution.

If a dependency is missing:
* the task is not executed
* a structured error is returned
* the failure is logged
* the caller receives remediation guidance

This prevents partial or undefined behavior.

---

## 7. Error Classes and Recovery
The Orchestrator defines a strict error taxonomy:

### Recoverable Errors
* Missing optional dependencies
* Temporary IO failures
* Non-critical parsing issues

### Non‑Recoverable Errors
* Missing required dependencies
* Invalid module metadata
* Corrupted configuration
* Unexpected exceptions

### Recovery Mechanisms
* Automatic retry (where safe)
* Fallback execution paths
* Structured remediation messages
* GUI prompts for operator action

No error is ever returned as raw text.

---

## 8. Logging and Diagnostics
All modules log using the unified schema:

```Code
[timestamp] [LEVEL] TaskScheduler.<MODULE>: [module=<MODULE>] <message>
```
Every operation logs:
* start
* end
* result
* context
* errors
* remediation (if applicable)

Logs are structured, deterministic, and reproducible.

---

## 9. Integration Points (GUI / CLI / API)
### GUI
The GUI calls Orchestrator tasks for:
* cron loading
* cron writing
* systemd inspection
* validation
* diagnostics

The GUI never executes modules directly.

### CLI
CLI commands map 1:1 to Orchestrator operations.

### API (Future)
Remote orchestration will expose:
* task submission
* result retrieval
* diagnostics
* state inspection

All through the same deterministic engine.

---

## 10. Examples
### Example 1 — Load Cron
```Code
Task: load_user_cron
Module: CronManager
Result: List of CronEntry objects
```
### Example 2 — Write Cron
```Code
Task: write_user_cron
Module: CronManager
Result: success/failure + diff
```
### Example 3 — Systemd Unit Inspection
```Code
Task: inspect_unit
Module: SystemdManager
Result: structured unit metadata
```

---

## 11. Future Extensions
Planned expansions include:
* GUI orchestration
* fallback prompting
* symlink selection logic
* base‑vs‑portable install handling
* remote orchestration
* module sandboxing
* distributed execution

These features will extend the Orchestrator without breaking invariants.

---

## 12. Deterministic Guarantees
The Orchestrator guarantees:
* reproducible execution
* structured results
* isolated failures
* unified logging
* predictable behavior
* operator‑grade reliability

It is the foundation of the Linktech Engineering Tools Suite.
