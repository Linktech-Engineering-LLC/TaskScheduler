# TaskScheduler — Sidebar Documentation
Deterministic, operator‑grade scheduling and environment management utilities for Linux (systemd + cron).

**Suite:** Linktech Engineering Tools Suite  
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Sidebar Philosophy](#2-sidebar-philosophy)
3. [Scope Controls](#3-scope-controls)
4. [Host Selection](#4-host-selection)
5. [Action Frame](#5-action-frame)
6. [Dashboard Behavior](#6-dashboard-behavior)
7. [Deterministic Behavior](#7-deterministic-behavior)
8. [Future Expansion](#8-future-expansion)

---

## 1. Overview
The TaskScheduler sidebar is a **context controller**, not a navigation menu. It configures the execution scope (User/System), target (Local/Remote), and host selection for all operational views. It also exposes the action buttons used by Cron, Systemd, and Environment views — but only when those views are active.

The sidebar does **not** summarize system state, does **not** switch views, and does **not** contain any Cron/Systemd/Env logic. All summarization occurs in the Dashboard.

---

## 2. Sidebar Philosophy
The sidebar is designed around deterministic operator behavior:
* **Context First**
  Operators must choose scope and host before performing actions.
* **Zero Ambiguity**
  Controls never change position, never collapse, and never reorder.
* **Action Visibility Only When Valid**
  The action frame is hidden when Dashboard is active, preventing invalid operations.
* **Predictable State**
  The sidebar always reflects the current execution context, regardless of which view is active.

This ensures operators always know where actions will apply and under what scope.

---

## 3. Scope Controls
The scope controls define the execution domain:
* **User Scope**
  Actions apply to user‑level cron entries, environment variables, and user‑accessible systemd units.
* **System Scope**
  Actions apply to system‑level cron entries, environment variables, and systemd units requiring elevated permissions.

Scope selection is deterministic and immediately affects all operational views.

---

## 4. Host Selection
The sidebar provides host selection for remote or multi‑host operation:
* **Local Host**
  Default mode; actions apply to the local machine.
* **Remote Host**
  When enabled, actions target the selected remote host.

Host selection is always visible, even on Dashboard, because context is global.

---

## 5. Action Frame
The action frame contains the operational buttons:
* **New**
* **Edit**
* **Delete**
* **Refresh**

These buttons apply to the currently active view (Cron, Systemd, Environment).
They are **hidden** when Dashboard is active, because Dashboard is informational and has no actionable rows.

The entire frame is toggled as a single unit for deterministic layout behavior.

--- 

## 6. Dashboard Behavior
When Dashboard is active:
* The action frame is hidden.
* Scope and host controls remain visible.
* No operational actions are available.
* The sidebar acts purely as a context indicator.

This prevents “dead buttons” and keeps the operator’s mental model clean.

---

## 7. Deterministic Behavior
The sidebar enforces deterministic behavior:
* Scope and host controls never move or hide.
* Action frame visibility is tied strictly to view selection.
* No dynamic resizing or animation.
* No contextual guessing — the sidebar reflects exactly one state at all times.

This matches the operator‑grade philosophy of the Linktech Engineering Tools Suite.

---

## 8. Future Expansion
Potential enhancements include:
* Additional scopes (e.g., container namespaces)
* Advanced remote host profiles
* Context‑aware action sets for future tools
* Operator mode indicators
* Sidebar presets for automation workflows

### Move Button (Cron ↔ Systemd Transfer)
A future addition to the action frame will be the Move button, which transfers a schedule between cron and systemd. This operation is a structural conversion, not a simple copy, and will be performed entirely within the active view’s editor window. The sidebar will expose the Move button only when an actionable view is active and the selected schedule supports conversion.

All expansions will preserve deterministic behavior and structural stability.