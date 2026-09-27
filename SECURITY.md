# Security Policy

## Supported Versions
Security updates apply to the latest development branch and the most recent tagged release. Older versions may not receive patches.

## Reporting a Vulnerability
If you discover a security issue, please report it privately:

[security@linktechengineering.net](mailto::security@linktechengineering.net)

Do not open a public GitHub issue for security‑related topics.

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Security Expectations
TaskScheduler interacts with systemd, cron, and system‑level metadata. To maintain a secure environment:

* No unvalidated input is passed to system commands.
* No external code is executed beyond systemd, journalctl, or other standard Linux utilities.
* No sensitive data (credentials, tokens, passwords) is logged.
* All privilege‑elevated operations must be explicit and user‑approved.
* TaskScheduler must fail closed on unexpected errors.
* Editing unit files must include validation and safety checks.
* Future packaging (AppImage, Flatpak, DEB) must not introduce additional attack surface.

## Privilege Model

TaskScheduler uses a deterministic privilege model:

* System scope always requires authentication.
* User-scope operations require authentication when the selected user differs from the active user.
* Remote mode requires explicit operator intent and never performs implicit SSH elevation.
* No automatic privilege escalation is performed under any circumstances.

All privileged operations must be explicitly initiated by the operator.

## Remote Host Security

Remote mode uses explicit SSH host selection based on ~/.ssh/config.
Wildcard hosts are ignored for safety.
No background probing or implicit credential usage occurs.
Future remote editing features will follow the same explicit-approval model.

## Responsible Disclosure
We request that researchers follow responsible disclosure practices and allow maintainers time to address issues before public release.

Thank you for helping keep TaskScheduler and the Linktech Engineering Tools Suite secure.
