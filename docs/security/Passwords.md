# Password Handling — Core Security Model
Deterministic, operator‑grade authentication, credential management, and privilege‑escalation rules for local and remote TaskScheduler environments.

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. Overview
2. Password Sources
3. Password Entry UI
4. Transmission Rules
5. Security Invariants
6. Configuration
7. Developer Notes
8. Future Work

---

## 1. Overview
TaskScheduler performs privileged operations across cron, systemd, environment management, and remote hosts. These operations may require authentication depending on subsystem, scope, and host configuration. The password model is intentionally deterministic: passwords are never logged, never retained longer than necessary, and never written to disk unless explicitly configured through encrypted storage.

This document defines how passwords are collected, validated, transmitted, and protected throughout the TaskScheduler execution pipeline.

---

## 2. Password Sources
TaskScheduler supports multiple password sources, each with different security guarantees and operational constraints.

### 2.1 Plaintext (Local Only)
A simple plaintext password stored in the configuration file.
* Only permitted when `security.allow_plaintext: true`
* File permissions must be `600`
* Intended for isolated hosts or offline testing
* Never recommended for production

### 2.2 Vault (Encrypted Storage)
Passwords stored in an AES‑256 encrypted vault file.
* Requires a vault master key
* Supports multiple named entries
* Recommended for production deployments
* Vault file is never decrypted on disk

### 2.3 Encrypton (Lightweight Encrypted Format)
A compact encrypted password format stored alongside host configuration.
* Uses symmetric encryption with per‑host salt
* Suitable for remote automation
* Passwords are decrypted only in memory

### 2.4 Hashed (Planned)
Hashed password mode is planned for future releases.
* SHA‑256 or bcrypt
* Intended for non‑interactive authentication workflows
* Will not support reversible decryption

---

## 3. Password Entry UI
The password entry field appears only when required by the active subsystem and scope.

### 3.1 Display Rules
The password field is shown when:
* The selected scope is **system**
* The selected user differs from the current session user
* Remote mode requires authentication
* A subsystem explicitly requests credentials

### 3.2 UI Behavior
* Passwords are masked by default
* A visibility toggle is provided
* Inline validation indicates missing or invalid credentials
* Passwords are cleared when user, scope, or host changes
* Passwords entered in the UI are **never persisted**

### 3.3 Sidebar Integration
The sidebar updates dynamically:
* System‑scope operations enable password entry
* User‑scope operations disable password entry
* Remote operations may override local rules

---

## 4. Transmission Rules
Passwords are transmitted only when required and only through secure channels.

### 4.1 Local Operations
Used for privileged local actions:
* Passed to `sudo` via stdin
* Never written to logs
* Cleared immediately after use

### 4.2 Remote Operations
Used for SSH authentication:
* Supports password‑based login
* Supports vault‑retrieved credentials
* Supports Encrypton‑decoded credentials
* Never transmitted in plaintext
* Never stored on remote hosts

### 4.3 No Network Leakage
TaskScheduler guarantees:
* No HTTP/HTTPS password transmission
* No plaintext socket communication
* No accidental logging of credentials

---

## 5. Security Invariants
TaskScheduler enforces strict invariants across all password‑handling paths.
1. Passwords are never logged.  
   All logging paths sanitize password fields.
2. Passwords are never retained longer than necessary.  
   Cleared immediately after use.
3. Passwords are never written to disk unless encrypted.  
   Only Vault and Encrypton modes persist credentials.
4. Plaintext passwords require restrictive permissions.  
   Files must be mode 600.
5. Remote passwords are only transmitted over SSH.  
   No plaintext network transmission.
6. Password UI clears on context change.  
   Changing user, scope, or host invalidates the current password.
7. System‑scope operations always require authentication.  
   No bypasses or silent privilege escalation.
8. All password‑handling code must use the PasswordManager API.  
   Direct access to raw password strings is prohibited.

---

## 6. Configuration
Example configuration block:

```yaml
security:
  vault:
    enabled: true
    vault_path_env: {PROJECT}_VAULT_PATH
    password_file_env: {PROJECT}_VAULT_PASSWORD_FILE

  encrypton:
    enabled: true
    encrypton_path_env: {PROJECT}_ENCRYPTON_PATH
    encrypton_key_env: {PROJECT}_ENCRYPTON_KEY_FILE

  allow_plaintext: false
```

### 6.1 Required Keys
* `security.allow_plaintext`
* `security.vault.enabled`
* `security.encrypton.enabled`

### 6.2 Optional Keys
* `security.vault.file`
* `security.encrypton.salt`

---

## 7. Developer Notes
* All password handling must go through `PasswordManager`.
* Raw password strings must never be stored in attributes or globals.
* Unit tests must cover:
    * UI clearing behavior
    * Vault and Encrypton decoding
    * Transmission rules
    * Logging sanitization
* New subsystems requiring authentication must integrate with the existing password pipeline.
* Any code path that touches credentials must be reviewed for compliance with invariants.

---

## 8. Future Work
* Implement hashed password mode
* Add SSH key‑based authentication
* Add per‑host password policies
* Add audit logging for authentication attempts (without passwords)
* Add multi‑vault support for multi‑tenant environments