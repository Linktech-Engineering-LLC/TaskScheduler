# Remote Operations — Secure Remote Execution Model
Deterministic, operator‑grade rules for remote execution, authentication, transport, and subsystem orchestration across SSH‑based TaskScheduler environments.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Remote Connection Model](#2-remote-connection-model)
3. [Authentication Sources](#3-authentication-sources)
4. [Remote Subsystem Execution](#4-remote-subsystem-execution)
5. [Transport & Security Rules](#5-transport--security-rules)
6. [Configuration](#6-configuration)
7. [Developer Notes](#7-developer-notes)
8. [Future Work](#8-future-work)

---

## 1. Overview
TaskScheduler supports remote execution for cron, systemd, environment management, and host‑level inspection. Remote operations are performed exclusively over SSH using deterministic, operator‑grade rules. All remote actions follow strict invariants: no plaintext transmission, no silent privilege escalation, and no deviation from the local execution model except where remote constraints require it.

This document defines how remote hosts are contacted, authenticated, and controlled within the TaskScheduler execution pipeline.

---

## 2. Remote Connection Model
Remote operations use a single, unified SSH execution pipeline.

### 2.1 Connection Establishment
* SSH connections are created on demand
* No persistent background sessions
* Connection parameters are derived from host configuration
* Host fingerprints must be trusted by the underlying SSH client

### 2.2 Host Metadata
Each remote host defines:
* hostname or IP
* port (default 22)
* user
* authentication source
* optional sudo requirements

### 2.3 Session Lifecycle
* Sessions are created only when needed
* Commands are executed synchronously
* Sessions are closed immediately after command completion
* No remote state is retained between operations

---

## 3. Authentication Sources
Remote authentication follows the same deterministic model as local password handling.

### 3.1 Password‑Based Authentication
* Passwords may be retrieved from Vault
* Passwords may be retrieved from Encrypton
* Passwords may be entered interactively
* Passwords are never logged
* Passwords are never written to disk

### 3.2 SSH Key Authentication
* Key paths may be provided via environment variables
* Keys may be encrypted; decryption handled by SSH client
* Keys are never transmitted over the network
* Keys are never copied to remote hosts

### 3.3 Multi‑Source Resolution
If multiple authentication sources exist:
1. SSH key is preferred
2. Vault password
3. Encrypton password
4. Interactive password

---

## 4. Remote Subsystem Execution
Remote execution mirrors local subsystem behavior with remote‑specific constraints.

### 4.1 Remote Cron
* Remote crontab is read via SSH
* Edits are applied using remote `crontab` binary
* Cron logs are retrieved via remote file read or journalctl

### 4.2 Remote Systemd
* Remote units are listed using remote `systemctl`
* Status queries use remote `systemctl status`
* Unit edits require sudo if configured

### 4.3 Remote Environment Management
* Environment files are read via SSH
* Writes require sudo if file permissions demand it
* No remote environment variables are exported automatically

### 4.4 Remote File Access
* Only explicit paths are accessed
* No directory traversal outside configured paths
* No wildcard expansion unless performed by remote shell

---

## 5. Transport & Security Rules
Remote operations follow strict transport invariants.

### 5.1 Transport Guarantees
* All remote communication uses SSH
* No HTTP/HTTPS transport
* No plaintext sockets
* No fallback to insecure protocols

### 5.2 Command Execution Rules
* Commands are executed with explicit arguments
* No shell injection
* No dynamic command construction without sanitization
* Sudo prompts are handled deterministically

### 5.3 Logging Rules
* Remote commands may be logged
* Remote passwords are never logged
* Remote output is sanitized before logging

### 5.4 Failure Handling
* Connection failures produce deterministic error messages
* Authentication failures never reveal password content
* Subsystem failures include remote stderr output

---

## 6. Configuration
Example configuration block:

```yaml
remote:
  hosts:
    prod-server:
      host: prod.example.com
      port: 22
      user: deploy
      auth: vault
      require_sudo: true

    staging:
      host: staging.example.com
      user: ops
      auth: ssh_key
```

### 6.1 Required Keys
* `remote.hosts.*.host`
* `remote.hosts.*.user`
* `remote.hosts.*.auth`

### 6.2 Optional Keys
* `remote.hosts.*.port`
* `remote.hosts.*.require_sudo`
* `remote.hosts.*.ssh_keyfile_env`

---

## 7. Developer Notes
* All remote execution must use the RemoteManager API
* Raw SSH commands must never be constructed manually
* Unit tests must cover:
    * SSH connection lifecycle
    * Authentication resolution
    * Remote cron/systemd operations
    * Logging sanitization
* Remote operations must never bypass local security policy
* Any new subsystem must integrate with the remote execution pipeline

---

## 8. Future Work
* Add multiplexed SSH sessions for performance
* Add remote host capability detection
* Add remote environment diffing
* Add remote audit logging
* Add multi‑host batch operations