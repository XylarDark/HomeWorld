# 10/10 door execution

Main when started: `d249d2b`

- [x] `AGENTS.md` already pointed at the door and already held the 60k line. Not pasted.
- [x] `CLAUDE.md` is `@AGENTS.md` only.
- [x] No always-apply Cursor rule. `AGENTS.md` already forbids `alwaysApply: true`, and Cursor loads `AGENTS.md`.
- [x] No SessionStart hook. Native load plus the import is the boot.
- [x] Door is 56 lines. Mode table and rules 1–5 are in `DOOR_RULES.md`, opened with the task.
- [x] Metrics sheet is named, not a start read.
- [x] Close order stayed in the door. The check fails if the door exceeds 100 lines, the sheet returns to the start read, or the Claude import is missing.
