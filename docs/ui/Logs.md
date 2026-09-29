# Logs - Logging Systgm Documentation

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Log Categories](#2-log-categories)
3. [Log Sources](#3-log-sources)
4. [Log Loading Flow](#4-log-loading-flow)
5. [UI Behavior](#5-ui-behavior)
6. [Error Handling](#6-error-handling)
7. [Future Enhancements](#7-future-enhancements)

## 1. Overview
The TimerDeck log system provides a unified interface for viewing logs from multiple subsystems: TaskScheduler, Cron, and Systemd. Each log category is exposed through the View → Logs submenu and routed to the appropriate backend loader. The log viewer is designed to be deterministic, predictable, and consistent with the architectural invariants of the broader tool suite.

## 2. Log Categories
TimerDeck currently supports three distinct log categories:

### 2.1 TaskScheduler Logs
TaskScheduler logs originate from the PythonTools TaskScheduler backend. These logs capture task execution, scheduling decisions, error states, and runtime diagnostics.

### 2.2 Cron Logs
Cron logs reflect user‑level or system‑level cron activity. They include execution timestamps, command output, and failure states when available.

### 2.3 Systemd Logs
Systemd timer logs are retrieved from the system journal. They include activation events, unit failures, and timer metadata.

## 3. Log Sources
Each log category maps to a specific backend:

### 3.1 TaskScheduler Source
Logs are retrieved from the PythonTools TaskScheduler logging subsystem. The backend exposes structured log entries with timestamp, severity, and message fields.

### 3.2 Cron Source
Cron logs are sourced from:
- `/var/log/syslog` (Debian‑based)
- `/var/log/cron` (RHEL‑based)
- journalctl filters when available

### 3.3 Systemd Source
Systemd logs are retrieved using:
- `journalctl --user-unit <unit>`
- `journalctl --unit <unit>` for system scope

## 4. Log Loading Flow
The log viewer follows a deterministic loading sequence:

### 4.1 User Selection
The user selects a log category from the View → Logs submenu.

### 4.2 Backend Dispatch
The MainWindow dispatches the request to the appropriate manager:
- `TaskSchedulerManager`
- `CronManager`
- `SystemdManager`

### 4.3 Normalization
Each backend normalizes its log entries into a unified structure:
- timestamp
- category
- message
- metadata (optional)

### 4.4 UI Population
The log viewer widget receives the normalized entries and populates the table.

## 5. UI Behavior
The log viewer adheres to the following UI rules:

### 5.1 Deterministic Ordering
Logs are sorted by timestamp descending.

### 5.2 Non‑blocking Loads
Log retrieval is performed synchronously but must not block the UI thread.

### 5.3 Consistent Columns
All log categories use the same column layout:
- Timestamp
- Category
- Message

## 6. Error Handling
The log viewer implements the following error behaviors:

### 6.1 Missing Log Source
If a log source is unavailable, the viewer displays a structured error card.

### 6.2 Permission Errors
Permission failures are surfaced with a clear message and recommended remediation.

### 6.3 Parse Errors
Malformed log entries are skipped but counted and reported.

## 7. Future Enhancements
Planned improvements include:

### 7.1 Search and Filtering
Regex, case sensitivity, and highlight support.

### 7.2 Export Support
Exporting logs to structured formats.

### 7.3 Live Streaming
Real‑time log updates using journalctl follow mode.
