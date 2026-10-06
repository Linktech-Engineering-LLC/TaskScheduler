# Environment Subsystem — Core Behavior and Rules
Deterministic, operator‑grade environment discovery, resolution, and export modeling for Linux shell environments.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Architectural Invariants](#2-architectural-invariants)
3. [Environment Model](#3-environment-model)
4. [Discovery Rules](#4-discovery-rules)
5. [Parsing Rules](#5-parsing-rules)
6. [Shell Integration](#6-shell-integration)
7. [Validation Rules](#7-validation-rules)
8. [Editor Contract](#8-editor-contract)
9. [Export Semantics](#9-export-semantics)
10. [Orchestration](#10-orchestration)
11. [Future Extensions](#11-future-extensions)
12. [Deterministic Guarantees](#12-deterministic-guarantees)

---

## 1. Overview
TaskScheduler’s Environment subsystem provides deterministic discovery, parsing, validation, and export of environment variables across shell‑specific configuration files. It models environment definitions as structured data and ensures consistent behavior across Bash, Zsh, Sh, and other POSIX‑compatible shells.

Environment data is never modified implicitly; all changes are operator‑initiated and logged.

---

## 2. Architectural Invariants
Environment behavior follows fixed invariants:
* **Shell‑aware**: resolution rules depend on the user’s login shell (from `/etc/passwd`).
* **Non‑destructive**: TaskScheduler never rewrites shell RC files without explicit operator action.
* **Deterministic**: identical environment files produce identical parsed models.
* **Observable**: all operations are logged via `TaskScheduler.environment`.
* **Isolated**: environment parsing does not execute shell code; only static analysis is performed.

---

## 3. Environment Model
Environment variables are represented internally as:
* **name** — variable identifier
* **value** — resolved literal value
* **exported** — whether the variable is marked for export
* **source** — originating file (e.g., `.bashrc`, `.profile`, `.zshenv`)
* **enabled** — whether the variable is active
* **comment** — optional operator notes

This model ensures consistent behavior across shells and export targets.

---

## 4. Discovery Rules
Environment discovery identifies shell‑specific configuration files based on the user’s login shell:

### Bash
* `~/.bashrc`
* `~/.bash_profile`
* `~/.profile`

### Zsh
* `~/.zshrc`
* `~/.zprofile`
* `~/.zshenv`

### Sh / Dash
* `~/.profile`

Discovery is deterministic and does not rely on shell execution.

---

## 5. Parsing Rules
Environment parsing enforces:
* literal assignment only (`VAR=value`)
* safe export detection (`export VAR=value` or `export VAR`)
* rejection of dynamic constructs (`$(...)`, backticks, process substitution)
* rejection of shell functions
* preservation of comments
* preservation of ordering

Parsing is static and does not evaluate shell expressions.

---

## 6. Shell Integration
Shell integration ensures:
* correct file precedence (e.g., `.zshenv` loads before `.zshrc`)
* correct export semantics
* correct PATH merging rules
* correct alias/function exclusion
* correct handling of shell‑specific quirks (e.g., Zsh’s `typeset`)

Environment variables are resolved in the same order the shell would load them, but without executing shell code.

---

## 7. Validation Rules
Validation ensures:
* variable names are syntactically valid
* values do not contain forbidden constructs
* exported variables are properly declared
* PATH‑like variables follow safe merging rules
* duplicates are detected and surfaced
* shadowed variables are flagged

Validation is deterministic and shell‑aware.

---

## 8. Editor Contract
The Environment editor (GUI) must:
* preserve comments
* preserve ordering
* never silently drop variables
* reflect validation status in real time
* allow toggling of exported/non‑exported state
* allow enabling/disabling variables without deletion

The editor operates directly on the Environment model.

---

## 9. Export Semantics
Environment export behavior is deterministic:
* disabled variables are omitted
* comments are preserved
* export statements are normalized
* shell‑specific file targets are respected
* no destructive rewrites occur without operator confirmation

Export targets include:
* user shell RC files
* TaskScheduler’s internal environment file
* shell‑specific export bundles

---

## 10. Orchestration
Environment orchestration coordinates:
* discovery of environment files
* parsing into structured models
* validation
* GUI exposure
* export operations
* logging of all operator actions

It ensures consistent behavior across shells and environments.

---

## 11. Future Extensions
Planned enhancements include:
* environment diff viewer
* PATH conflict detection
* automatic environment repair suggestions
* shell‑specific export bundles
* environment simulation for cron/systemd commands
* environment provenance tracking

---

## 12. Deterministic Guarantees
Given the same:
* shell,
* environment files,
* variable definitions,

TaskScheduler’s Environment subsystem guarantees identical discovery, parsing, validation, and export behavior across runs and environments.