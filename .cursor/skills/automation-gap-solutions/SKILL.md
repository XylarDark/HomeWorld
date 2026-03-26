---
name: automation-gap-solutions
description: Close automation gaps (Level Streaming/portal, State Tree graph, PCG no-access). Use when the user or task asks to implement solutions for AUTOMATION_GAPS.
---

# Automation gap solutions

Use this skill when the user or task asks to **close an automation gap**, **implement a solution for AUTOMATION_GAPS**, or to automate **Level Streaming/portal**, **State Tree graph editing**, or **PCG no-access steps**.

## Steps

1. **Read** [docs/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) and the "Solution approaches" section for the relevant gap.
2. **Read** [docs/FULL_AUTOMATION_RESEARCH.md](../../docs/FULL_AUTOMATION_RESEARCH.md) §2–4 and §10 for GUI automation patterns.
3. **Portal (Gap 1):** Implement or extend script to place [AHomeWorldDungeonEntrance](../../Source/HomeWorld/HomeWorldDungeonEntrance.h) at portal position and set `LevelToOpen` from [planetoid_map_config.json](../../Content/Python/planetoid_map_config.json). The script [place_portal_placeholder.py](../../Content/Python/place_portal_placeholder.py) already does this; if it fails (e.g. property not set), add logging and document in AUTOMATION_GAPS, or add GUI automation (ref images for Details → Level To Open).
4. **State Tree (Gap 2):** Use research outcome from [docs/GAP_SOLUTIONS_RESEARCH.md](../../docs/Automation/GAP_SOLUTIONS_RESEARCH.md): no high-level Python API; use [state_tree_apply_defend_branch.py](../../Content/Python/gui_automation/state_tree_apply_defend_branch.py) with refs in [Content/Python/gui_automation/refs/state_tree/](../../Content/Python/gui_automation/refs/state_tree/), or document one-time manual per [DAY12_ROLE_PROTECTOR.md](../../docs/tasks/DAY12_ROLE_PROTECTOR.md).
5. **PCG:** Run [pcg_apply_manual_steps.py](../../Content/Python/gui_automation/pcg_apply_manual_steps.py) with Editor focused and refs present; if refs missing, run [capture_pcg_refs.py](../../Content/Python/gui_automation/capture_pcg_refs.py) per [refs/README.md](../../Content/Python/gui_automation/refs/README.md).
6. **Update** [docs/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) (Research log) or [docs/GAP_SOLUTIONS_RESEARCH.md](../../docs/Automation/GAP_SOLUTIONS_RESEARCH.md) with the result (solution implemented, API not found, or GUI path documented).

## References

- [.cursor/rules/19-automation-gaps.mdc](../../.cursor/rules/19-automation-gaps.mdc) — Rule for gap handling.
- [docs/PCG_VARIABLES_NO_ACCESS.md](../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) — PCG settings automation cannot set.
