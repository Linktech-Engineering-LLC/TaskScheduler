# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon McClatchey, Linktech Engineering LLC

"""
 Package: TaskScheduler
 Author: Leon McClatchey
 Company: Linktech Engineering LLC
 Created: 2026-09-30
 Modified: 2026-10-05
 File: taskscheduler/environment/diff.py
 Version: 1.0.0
 Description: Description of this module
"""

from .modes import EnvDiffEntry
from .model import ResolvedEnvEntry

class EnvironmentDiffEngine:
    def diff(
        self,
        left: list[ResolvedEnvEntry],
        right: list[ResolvedEnvEntry],
    ) -> list[EnvDiffEntry]:
        left_map = {e.variable: e for e in left}
        right_map = {e.variable: e for e in right}

        all_vars = set(left_map.keys()) | set(right_map.keys())
        diffs: list[EnvDiffEntry] = []

        for var in sorted(all_vars):
            l = left_map.get(var)
            r = right_map.get(var)

            lv = l.value if l else None
            rv = r.value if r else None
            ls = l.status if l else None
            rs = r.status if r else None

            if lv != rv or ls != rs:
                diffs.append(
                    EnvDiffEntry(
                        variable=var,
                        left_value=lv,
                        right_value=rv,
                        left_status=ls,
                        right_status=rs,
                    )
                )

        return diffs

