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

## 10. Orchestration
Cron orchestration coordinates:
- loading user cron definitions,
- applying validation,
- exposing entries to the GUI,
- exporting to target locations on operator request.

## 11. Future Extensions
Planned extensions include:
- cron safety warnings,
- “next run” simulation,
- diffing against system crontab,
- shell‑specific helpers for complex schedules.

## 12. Deterministic Guarantees
Given the same:
- shell,
- environment,
- cron definitions,
TaskScheduler’s Cron subsystem guarantees identical parsing, validation, and export