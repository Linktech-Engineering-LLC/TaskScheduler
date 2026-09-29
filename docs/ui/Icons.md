# Icons - Icon Definitions

**Suite:** Linktech Engineering Tools Suite  
**Project:** TaskScheduler
**Maintainer:** Leon McClatchey, Linktech Engineering LLC  
**License:** MIT (source) · Proprietary (binaries, if distributed)  
**Requires:** Python 3.12+  
**Status:** Active Development (Phase 2)  

## Table of Contents
1. [Overview](#1-overview)
2. [Icon Directory Structure](#2-icon-directory-structure)
3. [Icon Naming Conventions](#3-icon-naming-conventions)
4. [Icon Mappings](#4-icon-mappings)
5. [UI Integration Rules](#5-ui-integration-rules)
6. [Future Enhancements](#6-future-enhancements)

## 1. Overview
TimerDeck uses a deterministic icon mapping system to ensure visual consistency across menus, actions, and widgets. Icons are loaded through the `icon()` helper and cached at MainWindow initialization.

## 2. Icon Directory Structure
Icons reside in the following directory:
`taskscheduler/ui/icons`


All icons must be SVG format to ensure crisp rendering across DPI scales.

## 3. Icon Naming Conventions
Icons follow a strict naming convention:

### 3.1 Lowercase Filenames
All filenames are lowercase with hyphens separating words.

### 3.2 Semantic Names
Icon names must reflect their functional meaning:
- `dashboard.svg`
- `cron.svg`
- `systemd-user.svg`
- `systemd-system.svg`
- `env.svg`
- `logs.svg`
- `settings.svg`
- `refresh.svg`
- `exit.svg`
- `help.svg`
- `about.svg`

## 4. Icon Mappings
The following mappings are used in MainWindow:

### 4.1 Dashboard
`dashboard.svg` → Dashboard view

### 4.2 Cron
`cron.svg` → Cron Jobs view

### 4.3 Systemd
`systemd-user.svg` → User scope  
`systemd-system.svg` → System scope

### 4.4 Environment Variables
`env.svg` → Environment Variables view

### 4.5 Logs
`logs.svg` → Logs submenu and log viewer actions

### 4.6 Settings
`settings.svg` → Settings dialog

### 4.7 Reload
`refresh.svg` → Reload All

### 4.8 Exit
`exit.svg` → Application exit

### 4.9 Help
`help.svg` → Documentation

### 4.10 About
`about.svg` → About dialog

## 5. UI Integration Rules
Icons follow these integration rules:

### 5.1 Load Once
Icons are loaded once in `__init__()` and reused.

### 5.2 No Runtime Lookup
Icons must not be loaded dynamically during view switches.

### 5.3 Consistent Sizing
Icons must be rendered at Qt’s default action size unless overridden.

## 6. Future Enhancements
Planned improvements include:

### 6.1 Dark Mode Variants
Alternate icon sets for dark themes.

### 6.2 Animated Icons
Optional animated icons for refresh and loading states.

### 6.3 Accessibility Review
Ensuring icon contrast meets accessibility guidelines.
