# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TimerDeck
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-09-30
 File: taskscheduler/environment/resolver.py
 Version: 1.0.0
 Description: Description of this module
"""

from dataclasses import dataclass
from typing import List

from .raw import Source, RawEnvEntry
from .modes import EnvironmentMode
from .model import ResolvedEnvEntry, Status, DiagnosticEntry

class EnvironmentResolver:
    def __init__(self):
        self.precedence_order = {
            Source.PROCESS: 1,
            Source.SYSTEM: 2,
            Source.USER: 3,
            Source.CRON: 4,
            Source.SYSTEMD_FILE: 5,
            Source.SYSTEMD_UNIT: 6,
            Source.SYSTEMD_DROPIN: 7,
        }

    def resolve(self, raw_entries: List[RawEnvEntry]) -> List[ResolvedEnvEntry]:
        grouped: dict[str, List[RawEnvEntry]] = {}

        for entry in raw_entries:
            grouped.setdefault(entry.variable, []).append(entry)

        resolved: List[ResolvedEnvEntry] = []

        for variable, entries in grouped.items():
            sorted_entries = sorted(
                entries,
                key=lambda e: self.precedence_order[e.source],
                reverse=True
            )

            winner = sorted_entries[0]
            winner_status = (
                Status.INHERITED if winner.source == Source.PROCESS else Status.DEFINED
            )

            diagnostics: list[DiagnosticEntry] = []

            for losing in sorted_entries[1:]:
                if self._is_masked(winner, losing):
                    losing_status = Status.MASKED
                    losing_comment = self._auto_comment_mask(winner, losing)
                elif self._same_precedence(winner, losing):
                    losing_status = Status.SHADOWED
                    losing_comment = self._auto_comment_shadow(winner, losing)
                else:
                    losing_status = Status.OVERRIDDEN
                    losing_comment = self._auto_comment_override(winner, losing)

                diagnostics.append(
                    DiagnosticEntry(
                        source=losing.source,
                        location=losing.location,
                        value=losing.value,
                        status=losing_status,
                        comment=losing_comment
                    )
                )

            resolved.append(
                ResolvedEnvEntry(
                    variable=variable,
                    value=winner.value,
                    status=winner_status,
                    source=winner.source,
                    comment=self._auto_comment_winner(winner, diagnostics),
                    diagnostics=diagnostics
                )
            )

        return resolved

    def _same_precedence(self, a: RawEnvEntry, b: RawEnvEntry) -> bool:
        return self.precedence_order[a.source] == self.precedence_order[b.source]

    def _is_masked(self, winner: RawEnvEntry, losing: RawEnvEntry) -> bool:
        if winner.source == Source.SYSTEMD_DROPIN and losing.source in {
            Source.SYSTEMD_UNIT,
            Source.SYSTEMD_FILE,
        }:
            return True
        if winner.source == Source.SYSTEMD_UNIT and losing.source == Source.SYSTEMD_FILE:
            return True
        return False

    # --- auto comments ---

    def _auto_comment_mask(self, winner: RawEnvEntry, losing: RawEnvEntry) -> str:
        return f"Masked by {winner.source.name.lower()} at {winner.location or 'unknown'}"

    def _auto_comment_shadow(self, winner: RawEnvEntry, losing: RawEnvEntry) -> str:
        return f"Shadowed by equal-precedence {winner.source.name.lower()}"

    def _auto_comment_override(self, winner: RawEnvEntry, losing: RawEnvEntry) -> str:
        return f"Overridden by higher-precedence {winner.source.name.lower()}"

    def _auto_comment_winner(
        self,
        winner: RawEnvEntry,
        diagnostics: list[DiagnosticEntry],
    ) -> str | None:
        if not diagnostics:
            return None
        return f"Effective value from {winner.source.name.lower()} ({winner.location or 'unknown'}); {len(diagnostics)} competing definitions"

    def resolve_for_mode(
        self,
        raw_entries: list[RawEnvEntry],
        mode: EnvironmentMode,
    ) -> list[ResolvedEnvEntry]:
        filtered = [
            e for e in raw_entries
            if self._include_in_mode(e.source, mode)
        ]
        return self.resolve(filtered)

    def _include_in_mode(self, source: Source, mode: EnvironmentMode) -> bool:
        if mode == EnvironmentMode.USER:
            return source in {
                Source.PROCESS,
                Source.USER,
                Source.CRON,
            }
        if mode == EnvironmentMode.SYSTEM:
            return source in {
                Source.SYSTEM,
                Source.SYSTEMD_FILE,
                Source.SYSTEMD_UNIT,
                Source.SYSTEMD_DROPIN,
                Source.CRON,
            }
        return True
