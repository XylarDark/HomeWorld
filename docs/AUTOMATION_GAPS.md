# Automation gaps (log only — no manual steps)

When the agent cannot automate a step (MCP, Python, GUI automation, commandlets), it **logs an entry here** instead of documenting "manual steps" for the user. The user runs separate chat sessions to design and implement automatic solutions for these gaps.

**Format per entry:** Date | Feature/task | What is needed | Why automation didn't cover it | Suggested approach for future automation

---

(Entries appended below by the agent when a step cannot be automated.)

---

2026-03-03 | Day 16 / T3 — DemoMap level streaming or trigger to planetoid | DemoMap needs Level Streaming Volume referencing planetoid level, or a Blueprint trigger at the portal placeholder that on overlap calls Open Level (Planetoid_Pride) so the player can travel to the planetoid. | No MCP or Python API used in-session for adding Level Streaming Volumes or wiring Blueprint overlap → Open Level. Scripts place the portal placeholder (ensure_demo_portal.py) and set up planetoid PCG (setup_planetoid_pcg.py). | GUI automation: capture ref images for Level Editor (Add Level Streaming Volume, set level reference) or Blueprint (trigger volume + Open Level node); or research UE 5.7 LevelEditorSubsystem / LevelStreaming Python API for adding streaming volumes programmatically.

2026-03-03 | T4 / Day 11–12 — State Tree Night? branch and Defend behavior | ST_FamilyGatherer needs a first-priority Night? branch (condition: IsNight from blackboard), Defend task (e.g. MoveTo rally/enemy), and IsNight set from TimeOfDaySubsystem. PIE with hw.TimeOfDay.Phase 2 should validate Defend. | No MCP or Python API for editing State Tree graph (add Selector children, conditions, tasks, blackboard). create_state_tree_family_gatherer.py creates an empty asset only; 09-mcp-workflow notes AnimGraph visual graph API not exposed; State Tree is analogous. | Research UE 5.7 State Tree Python/Editor API for adding nodes and blackboard keys; or GUI automation (ref images for State Tree editor: add branch, set condition, add task). See DAY12_ROLE_PROTECTOR.md, FAMILY_AGENTS_MASS_STATETREE.md.

---

## Solution approaches (per gap)

### Gap 1: Level Streaming / portal (DemoMap → planetoid)

- **A. Programmatic (preferred):** Use existing [AHomeWorldDungeonEntrance](Source/HomeWorld/HomeWorldDungeonEntrance.h): spawn it (or a Blueprint child) at portal position via Python, set `LevelToOpen` to planetoid map name (e.g. from [planetoid_map_config.json](Content/Python/planetoid_map_config.json)). Requires: Python spawn by class (e.g. `EditorLevelLibrary.spawn_actor_from_class` with C++ class or BP), and setting `LevelToOpen` (inherited C++ UPROPERTY — may need Python `set_editor_property`; MCP often cannot set inherited C++ props per [09-mcp-workflow.mdc](.cursor/rules/09-mcp-workflow.mdc)).
- **B. API research:** LevelEditorSubsystem / LevelStreaming Python API (UE 5.7) for adding Level Streaming Volumes and setting level reference.
- **C. GUI automation:** Ref images for Level Editor (Add Level Streaming Volume, set level) or Blueprint (trigger + Open Level node); run host-side PyAutoGUI script (same pattern as [pcg_apply_manual_steps.py](Content/Python/gui_automation/pcg_apply_manual_steps.py)).

### Gap 2: State Tree Night? / Defend branch

- **A. API research:** UE 5.7 State Tree Python/Editor API for creating nodes, Selector children, conditions, tasks, blackboard keys (Epic docs, plugin source).
- **B. GUI automation:** Ref images for State Tree editor (add branch, set condition, add task); host-side script in `Content/Python/gui_automation/` (e.g. `state_tree_apply_defend_branch.py`).
- **C. C++ commandlet:** If engine exposes State Tree asset editing, implement a commandlet that builds the Defend/Night branch programmatically.

---

## Research log

Findings from deep research are recorded in [docs/GAP_SOLUTIONS_RESEARCH.md](GAP_SOLUTIONS_RESEARCH.md). Summary updates may be added below with date.

- **2026-03-03:** Gap 1 (portal): Research completed. Programmatic solution implemented: [place_portal_placeholder.py](Content/Python/place_portal_placeholder.py) now prefers spawning AHomeWorldDungeonEntrance and setting LevelToOpen from [planetoid_map_config.json](Content/Python/planetoid_map_config.json) (`portal_level_to_open`). Falls back to cube placeholder if C++ class unavailable. See GAP_SOLUTIONS_RESEARCH.md.
- **2026-03-03:** Gap 2 (State Tree): No high-level Python API for building graph nodes; GUI automation or one-time manual. Stub script and refs README added under `Content/Python/gui_automation/`.
