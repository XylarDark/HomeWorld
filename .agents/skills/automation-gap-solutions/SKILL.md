---
name: automation-gap-solutions
description: Close automation gaps (Level Streaming/portal, State Tree graph, PCG no-access). Use when the user or task asks to implement solutions for AUTOMATION_GAPS.
---

# Automation gap solutions

Use this skill when the user or task asks to **close an automation gap**, **implement a solution for AUTOMATION_GAPS**, or to automate **Level Streaming/portal**, **State Tree graph editing**, or **PCG no-access steps**.

## Steps

1. **Read** [docs/Automation/AUTOMATION_GAPS.md](../../../docs/Automation/AUTOMATION_GAPS.md) and the "Solution approaches" section for the relevant gap.
2. **Read** [docs/Automation/FULL_AUTOMATION_RESEARCH.md](../../../docs/Automation/FULL_AUTOMATION_RESEARCH.md) §2–4 and §10 for GUI automation patterns.
3. **Portal (Gap 1):** [place_portal_placeholder.py](../../../Content/Python/place_portal_placeholder.py) sets `LevelToOpen` from [planetoid_map_config.json](../../../Content/Python/planetoid_map_config.json). When that write fails it logs `editor_ui: NEED_SLATE panel=portal-level`. Open [.agents/skills/ue-editor-ui/SKILL.md](../ue-editor-ui/SKILL.md). Do not add a PyAutoGUI clicker.
4. **State Tree (Gap 2):** There is no Python API for the graph. [state_tree_api_introspect.py](../../../Content/Python/state_tree_api_introspect.py) logs `editor_ui: NEED_SLATE panel=state-tree` when it finds none. Open the editor-UI skill. Do not document a click path for the user.
5. **PCG:** Use [pcg_settings_introspect.py](../../../Content/Python/pcg_settings_introspect.py) and [create_pcg_forest.py](../../../Content/Python/create_pcg_forest.py). When By Tag or the Static Mesh Spawner mesh list cannot be set, the script logs `editor_ui: NEED_SLATE panel=pcg-details`. Open the editor-UI skill. See [docs/PCG/PCG_VARIABLES_NO_ACCESS.md](../../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md).
6. **Update** [docs/Automation/AUTOMATION_GAPS.md](../../../docs/Automation/AUTOMATION_GAPS.md) (Research log) or [docs/Automation/GAP_SOLUTIONS_RESEARCH.md](../../../docs/Automation/GAP_SOLUTIONS_RESEARCH.md) with the result (solution implemented, API not found, or GUI path documented). If a step is still not automatable, log it — do **not** instruct the user to click it (see `.cursor/rules/20-full-automation-no-manual-steps.mdc`).

## References

- [.cursor/rules/19-automation-gaps.mdc](../../../.cursor/rules/19-automation-gaps.mdc) — Rule for gap handling.
- [docs/PCG_VARIABLES_NO_ACCESS.md](../../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) — PCG settings automation cannot set.
