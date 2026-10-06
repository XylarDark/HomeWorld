# SESSION_START optimization

Status: done.
Before (`30df6df`): door 1139 words; route-context 838; HOMEWORLD_ROUTE 706; WORLD_METRICS 1132.
After: door 1017 words; route-context 838; HOMEWORLD_ROUTE 706; WORLD_METRICS 1132. HANDBACK 150. LEVEL_RULES 117.

Phase 1 moved the six hand-back fields to `Docs/context/HANDBACK.md`.
Phase 2 moved the old rules 6–9 to `Docs/context/LEVEL_RULES.md`.
The three start reads were not edited. Open the new files only when that job starts.
