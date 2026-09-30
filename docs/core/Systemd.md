# Systemd — Core Architecture
Deterministic, operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Architectural Invariants](#2-architectural-invariants)
3. [Systemd Unit Model](#3-systemd-unit-model)
4. [Unit Discovery](#4-unit-discovery)
5. [Parsing Rules](#5-parsing-rules)
6. [Environment Resolution](#6-environment-resolution)
7. [Timer Semantics](#7-timer-semantics)
8. [Modification Rules](#8-modification-rules)
9. [Editor Contract](#9-editor-contract)
10. [Orchestration](#10-orchestration)
11. [Future Extensions](#11-future-extensions)
12. [Deterministic Guarantees](#12-deterministic-guarantees)

---

## 1. Overview
TaskScheduler’s systemd subsystem provides deterministic discovery, parsing, environment resolution, and safe modification of systemd units and timers.
It does not implement or interact with the full init system — only the components required for scheduling and environment management:
* Timer units
* Service units
* Drop‑ins
* Environment sources
* Reload semantics

The subsystem is designed to be reproducible, predictable, and safe for operators.
All write‑back operations occur through drop‑ins, never through modification of system units.

---

## 2. Architectural Invariants
These invariants define the behavior of the systemd subsystem.
They do not change across versions.
* **Timer → Service Mapping**
  Every timer unit maps to exactly one service unit.
* **Drop‑in Override Model**
  Drop‑ins override base units but never replace them.
* **Environment Precedence**
  `EnvironmentFile=` overrides `Environment=`.
  Drop‑ins override both.
* **Write‑back Safety**
  TaskScheduler never writes to system units directly.
  Only drop‑ins are generated.
* **Comment Preservation**
  All comments and ordering in unit files must be preserved.
* **Reload Requirement**
  Any modification requires a deterministic reload sequence.
* **Deterministic Discovery**
  Unit discovery must produce identical results across runs.

---

## 3. Systemd Unit Model
TaskScheduler defines a strict internal model for systemd units.

### SystemdUnit
Represents any unit file.

Fields include:
* `name`
* `path`
* `type` (service, timer, etc.)
* `sections`
* `directives`
* `comments`
* `dropins`

### SystemdService
Specialization of SystemdUnit for service units.

Additional fields:
* `exec_start`
* `environment`
* `environment_files`
* `dropins`

### SystemdTimer
Specialization of SystemdUnit for timer units.

Additional fields:
* `on_calendar`
* `accuracy_sec`
* `randomized_delay_sec`
* `persistent`
* `unit_target`

### SystemdDropIn
Represents a drop‑in override file.

Fields:
* `path`
* `sections`
* `directives`
* `comments`

### SystemdEnvironmentSource
Represents any environment source:
* `Environment=`
* `EnvironmentFile=`
* drop‑ins
* resolved file contents

---

## 4. Unit Discovery
TaskScheduler performs deterministic discovery of systemd units.

### Search Paths
* `/etc/systemd/system`
* `/usr/lib/systemd/system`
* `/run/systemd/system`
* Drop‑ins under `*.d/` directories

### Discovery Rules
* Timer units are paired with their corresponding service units.
* Drop‑ins are attached to their parent units.
* Environment files referenced by units are resolved.
* All discovered units are normalized into the internal model.

### Reproducibility
Discovery must produce identical results across runs unless the underlying filesystem changes.

---

## 5. Parsing Rules
Parsing is deterministic and comment‑preserving.

### Unit File Parsing
* Sections are parsed in order.
* Directives are parsed exactly as written.
* Comments are preserved with positional fidelity.
* Duplicate directives are allowed and preserved.

### Environment Parsing
* `Environment=` lines are parsed into key/value pairs.
* `EnvironmentFile=` paths are resolved and parsed.
* Drop‑ins override base unit values.

### Drop‑in Parsing
* Drop‑ins are parsed identically to unit files.
* Drop‑ins override base unit directives.
* Ordering is preserved.

---

## 6. Environment Resolution
TaskScheduler resolves environment variables from all systemd sources.

### Sources
* `Environment=`
* `EnvironmentFile=`
* Drop‑ins
* Resolved file contents

### Precedence
1. Drop‑ins
2. EnvironmentFile
3. Environment

### Status Classification
Each variable is classified as:
* active
* inherited
* overridden
* shadowed
* masked

These statuses feed directly into the Environment Table.

---

## 7. Timer Semantics
TaskScheduler interprets systemd timer directives into its internal schedule model.

### Core Directives
* `OnCalendar=`
* `AccuracySec=`
* `RandomizedDelaySec=`
* `Persistent=`

### Mapping Rules
* `OnCalendar=` → canonical schedule expression
* `AccuracySec=` → schedule tolerance
* `RandomizedDelaySec=` → jitter model
* `Persistent=` → missed‑run behavior

### Activation
Timer activation is mapped to the corresponding service unit.

---

## 8. Modification Rules
Modification is performed exclusively through drop‑ins.

### Editable Fields
* `Environment=`
* `EnvironmentFile=`
* Timer directives
* Service directives
* Any overrideable directive

### Read‑only Fields
* Unit type
* Unit name
* Unit path
* System‑provided directives

### Write‑back Rules
* Drop‑ins are generated deterministically.
* Comments and ordering are preserved.
* Only modified fields are written.
* Reload is triggered after write‑back.

---

## 9. Editor Contract
Defines how the systemd editor behaves.

### Field Layout
* Timer fields
* Service fields
* Environment fields
* Drop‑in fields

### Validation
* Directive validation
* Environment key/value validation
* File path validation

### Save Semantics
* Only changed fields generate drop‑ins.
* Write‑back is atomic.
* Reload is deterministic.

### Error Reporting
* Parse errors
* Write‑back errors
* Reload errors

---

## 10. Orchestration
Defines how systemd integrates with the rest of TaskScheduler.

### Dashboard Integration
* Timer table
* Service table
* Environment table

### Orchestrator Integration
* Editor routing
* Refresh cycles
* Environment propagation

### Cron Migration
Defines how cron schedules can be migrated into systemd timers.

---

## 11. Future Extensions
Reserved for future development:
* systemd‑user units
* transient units
* advanced environment layering
* unit templating
* multi‑instance services

---

### 12. Deterministic Guarantees
TaskScheduler provides the following guarantees:
* deterministic parsing
* deterministic write‑back
* deterministic environment resolution
* deterministic override behavior
* deterministic reload semantics
* deterministic discovery

These guarantees define the reliability and reproducibility of the systemd subsystem.
