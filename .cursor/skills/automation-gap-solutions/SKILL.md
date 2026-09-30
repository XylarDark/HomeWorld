---
name: automation-gap-solutions
description: Close automation gaps (Level Streaming/portal, State Tree graph, PCG no-access). Use when the user or task asks to implement solutions for AUTOMATION_GAPS.
---

# Automation gap solutions

Use this skill when the user or task asks to **close an automation gap**, **implement a solution for AUTOMATION_GAPS**, or to automate **Level Streaming/portal**, **State Tree graph editing**, or **PCG no-access steps**.

## Steps

1. **Read** [docs/Automation/AUTOMATION_GAPS.md](../../../docs/Automation/AUTOMATION_GAPS.md) and the "Solution approaches" section for the relevant gap.
2. **Read** [docs/Automation/FULL_AUTOMATION_RESEARCH.md](../../../docs/Automation/FULL_AUTOMATION_RESEARCH.md) §2–4 and §10 for GUI automation patterns.
3. **Portal (Gap 1):** Implement or extend script to place [AHomeWorldDungeonEntrance](../../../Source/HomeWorld/HomeWorldDungeonEntrance.h) at portal position and set `LevelToOpen` from [planetoid_map_config.json](../../../Content/Python/planetoid_map_config.json). The script [place_portal_placeholder.py](../../../Content/Python/place_portal_placeholder.py) already does this; if it fails (e.g. property not set), add logging and document in AUTOMATION_GAPS, or add GUI automation (ref images for Details → Level To Open).
4. **State Tree (Gap 2):** No high-level Python API — see [docs/Automation/GAP_SOLUTIONS_RESEARCH.md](../../../docs/Automation/GAP_SOLUTIONS_RESEARCH.md). The former `state_tree_apply_defend_branch.py` GUI-automation script was **removed WAVE F** and does not exist. Enumerate what the API actually exposes with [state_tree_api_introspect.py](../../../Content/Python/state_tree_api_introspect.py), then either drive the exposed API, or document the GUI path per [DAY12_ROLE_PROTECTOR.md](../../../docs/TaskLists/TaskSpecs/DAY12_ROLE_PROTECTOR.md).
5. **PCG:** The former `pcg_apply_manual_steps.py` / `capture_pcg_refs.py` GUI-automation scripts were **removed WAVE F** and do not exist. Use [pcg_settings_introspect.py](../../../Content/Python/pcg_settings_introspect.py) to find settable properties and [create_pcg_forest.py](../../../Content/Python/create_pcg_forest.py) for graph work; see [docs/PCG/PCG_VARIABLES_NO_ACCESS.md](../../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) for what no API can set.
6. **Update** [docs/Automation/AUTOMATION_GAPS.md](../../../docs/Automation/AUTOMATION_GAPS.md) (Research log) or [docs/Automation/GAP_SOLUTIONS_RESEARCH.md](../../../docs/Automation/GAP_SOLUTIONS_RESEARCH.md) with the result (solution implemented, API not found, or GUI path documented). If a step is still not automatable, log it — do **not** instruct the user to click it (see `.cursor/rules/20-full-automation-no-manual-steps.mdc`).

## References

- [.cursor/rules/19-automation-gaps.mdc](../../rules/19-automation-gaps.mdc) — Rule for gap handling (from `.cursor/skills/automation-gap-solutions/`, the rules dir is two levels up).
- [docs/PCG_VARIABLES_NO_ACCESS.md](../../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) — PCG settings automation cannot set.
