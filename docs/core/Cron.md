# Cron Subsystem — Core Behavior and Rules
Deterministic, operator‑grade scheduling, validation, and command‑execution modeling for Linux cron environments.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Architectural Invariants](#2-architectural-invariants)
3. [CronEntry Model](#3-cronentry-model)
4. [Schedule Parsing](#4-schedule-parsing)
5. [Command Resolution](#5-command-resolution)
6. [Environment Integration](#6-environment-integration)
7. [Validation Rules](#7-validation-rules)
8. [Editor Contract](#8-editor-contract)
9. [Export Semantics](#9-export-semantics)
10. [Orchestration](#10-orchestration)
11. [Future Extensions](#11-future-extensions)
12. [Deterministic Guarantees](#12-deterministic-guarantees)

---

## 1. Overview
TaskScheduler’s Cron subsystem models cron entries as structured data, providing deterministic parsing, validation, and export behavior. It does not directly modify system crontabs; instead, it operates on user‑level definitions and controlled export targets.

## 2. Architectural Invariants
Cron behavior is governed by fixed invariants:
- **Shell‑aware:** all parsing and validation are driven by the user’s login shell.
- **Non‑destructive:** system crontabs are never modified implicitly.
- **Deterministic:** identical inputs always produce identical schedules and exports.
- **Observable:** all operations are logged via `TaskScheduler.cron`.

## 3. CronEntry Model
Each cron entry is represented as a `CronEntry`:
- **schedule:** minute, hour, day, month, weekday fields.
- **command:** resolved executable or script.
- **comment:** optional metadata and operator notes.
- **enabled:** boolean toggle.
- **source:** origin (user file, imported, generated).

A `CronEntry` may*represent either a*traditional five*field cron schedule or a special s*hedule*such as `@reboot`.*Editor modes*(Custom* Daily, and Boot) are*normalized into a deterministic `C*onEntry`*representation prior to validation*and export.

The boolean fields `enabled`, `daily`, and `boot` influence schedule generation and export behavior.

- `enabled=False` results in a commented cron entry.
- `daily=True` normalizes day, month, and weekday fields to `*`.
- `boot=True` generates an `@reboot` schedule and suppresses standard cron time fields.

CronEntry is the authoritative representation of a schedule.

All editor modes (Custom, Daily, and Boot) are normalized into a
CronEntry instance prior to validation.

Validation is performed against the normalized CronEntry rather
than the state of individual user-interface controls.

### Disabled Entry Normalization

Disabled schedules are represented internally using the `enabled`
boolean property and are not stored with embedded comment markers.

During import, TaskScheduler recognizes both standard cron disabled
entries and KDE/KCron disabled entries. Any leading disable markers
are removed before populating the schedule fields.

A disabled schedule is identified by locating the first valid schedule
character:

- `@` for special schedules such as `@reboot`,
- `*` for wildcard schedules,
- `0-9` for numeric schedules.

Examples:

```cron
# 0 22 * * * /path/script
#\0 22 * * * /path/script
```

## 4. Schedule Parsing
Schedules are parsed from standard cron syntax into structured fields. Parsing enforces:
- numeric bounds,
- valid ranges and steps,
- valid lists and wildcards,
- rejection of malformed expressions.

## 5. Command Resolution
Commands are resolved against the active shell and environment:
- executable path resolution,
- alias and function detection,
- rejection of non‑file commands when required,
- logging of resolution decisions.

## 6. Environment Integration
Cron commands may depend on environment variables. Integration includes:
- discovery of environment files,
- shell‑specific export semantics,
- validation of referenced variables,
- optional injection of environment at export time.

## 7. Validation Rules
Validation combines schedule, command, and environment checks:
- schedule validity,
- command existence and accessibility,
- environment completeness,
- shell compatibility.

## 8. Editor Contract
The Cron editor (GUI) operates against `CronEntry` and must:
- preserve comments,
- preserve enabled/disabled state,
- never silently drop entries,
- reflect validation status in the UI.

## 9. Export Semantics
Exports are deterministic:
- disabled entries are omitted,
- comments are preserved where supported,
- environment injection is explicit,
- output format follows POSIX cron conventions.

TaskScheduler recognizes both standard commented cron entries (`#`)
and KDE/KCron disabled entries (`#\`) during import.

Internally, disabled state is normalized to the `enabled` property
of `CronEntry`.

Exports always use the standard commented cron format:

# 0 22 * * * /path/to/script

This behavior provides deterministic output while maintaining
compatibility with imported KCron schedules.

## 10. Orchestration
Cron orchestration coordinates:
- loading user cron definitions,
- applying validation,
- exposing entries to the GUI,
- exporting to target locations on operator request.

## 11. Future Extensions

Planned e*tensions*include:

- cron safety warnings,
* "next run" simulation,
- diffing *gainst system*crontab,
- shell-specific helpers *or complex*schedules,
- native support for cr*n step expressions (`*/N`, `M/N`*,
- support for range expressions*(`A-B`),
- support for range-step*expressions (`A-B/N`),
- preservat*on and*editing of imported advanced cron *xpressions.


## 12. Deterministic Guarantees
Given the same:
- shell,
- environment,
- cron definitions,
TaskScheduler’s Cron subsystem guarantees identical parsing, validation, and export