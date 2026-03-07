# Accomplishments overview (master)

**Purpose:** High-level record of **all work accomplished** on HomeWorld. Use this **together with** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) and [VISION.md](VISION.md) when deciding what to do next and when **generating the next task list**. Vision = where we're going; this doc = what we've already done; task list = current block of work.

**When to update:** After major milestones, completed task-list cycles, or automation changes. Keep it high-level; link to detailed docs for depth.

**Last updated:** 2026-03-06 (thirty-second list complete, rapid prototyping: 7 impl + 2 verification + 1 buffer)

---

## How to use this when generating the next task list

1. **Read** [VISION.md](VISION.md) — theme, campaign, vertical slice gate, Act 1/2 scope.
2. **Read this doc** — what is already in place (so you don’t duplicate or assume undone).
3. **Read** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) — what the last block was; which tasks completed or remain.
4. **Read** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) — suggested phases (Harden & demo, Deferred, Act 2 prep, Steam EA).
5. **Read** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) — known manual-only steps and workarounds.
6. **Produce** the next 10 tasks in CURRENT_TASK_LIST per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md).

---

## 1. Game and content (high level)

| Area | Accomplished |
|------|----------------|
| **Act 1 core** | PCG forest (ForestIsland_PCG, create_pcg_forest.py); GAS (GA_PrimaryAttack, Dodge, Interact, Place); BuildPlacementSupport (GetPlacementHit); Week 1 playtest gate passed. |
| **Homestead** | DemoMap layout (create_demo_from_scratch, demo_map_config); harvestable trees (BP_HarvestableTree, place_resource_nodes); resource collection (TryHarvestInFront, GA_Interact); home placement (GA_Place, TryPlaceAtCursor). Agentic building **prep** (BP_BuildOrder_Wall, SO); full agentic flow deferred. |
| **Family** | Family spawn (MEC + State Tree: create_mec_family_gatherer, create_state_tree_family_gatherer, link_state_tree_to_mec); Protector (GA_ProtectorAttack); Healer (HomeWorldHealAbility); Child (ST_FamilyGatherer branch); role persistence (UHomeWorldFamilySubsystem); SaveGame hook deferred. |
| **Planetoid** | Planetoid level (ensure_planetoid_level, place_portal_placeholder, planetoid_map_config); PCG POI (Planetoid_POI_PCG); Shrine/Treasure/Yield (AHomeWorldYieldNode, create_bp_yield_nodes); visit/interact doc + PIE checklist. |
| **Spirits** | Spirit roster (UHomeWorldSpiritRosterSubsystem); assign/unassign spirit to node (SpiritAssignmentSubsystem, SetAssignedSpirit). |
| **Dungeon** | Dungeon POI (place_dungeon_entrance, dungeon_map_config); AHomeWorldDungeonEntrance (trigger + OpenLevel); boss/reward doc. |
| **Vertical slice** | One moment (Claim homestead) and one corner (Homestead compound) chosen per PROTOTYPE_SCOPE; VERTICAL_SLICE_CHECKLIST exists; first full task-list cycle ran verification (T1–T10 completed). |

---

## 2. Automation and agent company

| Area | Accomplished |
|------|----------------|
| **Loop** | RunAutomationLoop.ps1: fetch task → implement → build if C++/Build.cs changed → validate (PIE when applicable) → mark task complete; exits when no pending/in_progress in CURRENT_TASK_LIST. |
| **Watcher** | Watch-AutomationAndFix.ps1: runs loop; on failure invokes Fixer; on repeat failure invokes Guardian (loop-breaker); Editor Output Log capture (full + filtered) on failure. |
| **Start** | Start-AllAgents.ps1 (and Start-AllAgents-InNewWindow.ps1): one entry point; optional Editor auto-launch when UE_EDITOR set; Run-AutomationWithCapture.ps1 for teed output and terminal-stay-open. |
| **Refiner** | Run-RefinerAgent.ps1 / refine-rules-from-runs: update rules and strategy from agent run history. |
| **Build** | Safe-Build.ps1 with Editor close/relaunch protocol; automatic build when C++/Build.cs modified; Build-HomeWorld.bat + Build-HomeWorld.log. |
| **Logging** | automation_loop.log, automation_errors.log, automation_events.log (high-level events), agent_run_history.ndjson; Get-AutomationStatus.ps1; exit alerts and last-activity JSON. |
| **Stall** | Watch-HeartbeatStall.ps1 for stall detection and process termination. |

---

## 3. Infrastructure and quality

| Area | Accomplished |
|------|----------------|
| **Session** | SESSION_LOG.md, DAILY_STATE.md (yesterday/today/tomorrow); NEXT_SESSION_PROMPT.md; read at start and updated at end. |
| **Errors** | KNOWN_ERRORS.md (UE 5.7, MCP, PCG, etc.); AUTOMATION_GAPS.md (manual-only steps); error recurrence prevention in rules. |
| **Tests** | PythonAutomationTest (Content/Python/tests/test_*.py); pie_test_runner.py → Saved/pie_test_results.json; PIE validation in loop; level loader and PIE flow tests. |
| **CI** | validate.yml (lint, JSON schema, C++ header/source, doc freshness). |
| **MCP** | UnrealMCP; execute_python_script, console commands; agent utility scripts (mcp_harness, pie_test_runner, blueprint_inspector, layout_blueprint_nodes, capture_viewport). |
| **Task list** | 10-task schema (goal, success criteria, research_notes, steps_or_doc, status); validate_task_list.py; HOW_TO_GENERATE_TASK_LIST; CURRENT_TASK_LIST_TEMPLATE. |

---

## 4. Completed task-list cycles (summary)

| Cycle | Focus | Outcome |
|-------|--------|--------|
| **First 10-task list** | Vertical slice checklist, portal (DemoMap→planetoid), dungeon entrance, State Tree Defend/Night, polish moment+corner, demo record, deferred feature verification (Save/Load, ReportDeath, GrantBossReward), Act 2 prep (Defend at home), Steam EA prep (packaging + store checklist), buffer. | All T1–T10 **completed**. Loop exited; next step = generate new list. |
| **Second 10-task list** | Re-verification (T1–T4: vertical slice, portal, dungeon, State Tree); deferred deep-dives (T5–T8: agentic building, SaveGame, death→spirit, boss reward); T9 packaged build optional; T10 buffer. | All T1–T10 **completed** (2026-03-04 automation session; 10 rounds, loop_exited_ok). |
| **Third 10-task list** | Gap-attempt T1–T2 (LevelToOpen, State Tree Night?/Defend); re-verification T3–T5; deferred T6–T7; Act 2 prep T8; Steam EA T9; buffer T10. Policy: when a gap is addressed, note in AUTOMATION_GAPS.md. | All T1–T10 **completed** (2026-03-05). Gap 1/2 researched and documented in AUTOMATION_GAPS; vertical slice, portal, dungeon, Save/Load, ReportDeath/GrantBossReward, Act 2 prep, Steam EA checklist updated. **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run Start-AllAgents-InNewWindow.ps1. |
| **Fourth 10-task list** | Gap follow-ups T1–T2 (portal ref image, State Tree refs/GUI); harden & demo T3–T4 (vertical slice checklist, demo recording/sign-off); deferred T5–T6 (agentic building, SaveGame verification); Act 2 T7; Steam EA T8; buffer T9–T10. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run Start-AllAgents-InNewWindow.ps1. |
| **Fifth 10-task list** | Ref production T1–T3 (portal ref, State Tree refs, run set_portal_level_to_open); night encounter T4; PIE validation T5; planetoid visit T6; packaging T7; refinement T8; docs T9; buffer T10. | All T1–T10 **completed** (2026-03-05). Refs documented host-side; T3 blocked on T1; night encounter stub; PIE validation doc; planetoid flow doc; packaging deferred; refinement doc; T9 docs polish; T10 close-out. **Next:** Sixth list generated; run Start-AllAgents-InNewWindow.ps1. |
| **Sixth 10-task list** | Vertical slice checklist T1; PIE-with-validation T2; agentic building T3; SaveGame persistence T4; Act 2 Defend T5; demo recording/sign-off T6; packaged build T7; single-instance guard verify T8; docs polish T9; buffer T10. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle. |
| **Seventh 10-task list** | Re-verify slice T1; PIE validation T2; portal/State Tree gaps T3–T4; SaveGame/Act 2 T5–T6; packaged build T7; docs T8; AUTOMATION_GAPS T9; buffer T10. | Superseded by eighth list. |
| **Eighth 10-task list** | MVP-focused: T1 PIE pre-demo checklist, T2 Save/Load and Phase 2, T3 portal, T4 State Tree Defend, T5 SaveGame, T6 packaging, T7 slice sign-off, T8–T10 docs and buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read TASK_LIST_REPEATS_LOG, ACCOMPLISHMENTS_OVERVIEW §4); run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle. |
| **Ninth 10-task list** | Re-verify slice, Save/Load and Phase 2, portal/State Tree gaps, SaveGame, packaging, slice sign-off, docs, AUTOMATION_GAPS, buffer (T1–T10). | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4 to avoid duplicating completed work). Then run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle. |
| **Tenth 10-task list** | Same re-verify/gap focus (T1–T10). | All T1–T10 **completed** (2026-03-04 run; 10 rounds, each exit 0; max rounds hit when round 10 left all statuses pending—fixed post-run). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle. |
| **Eleventh 10-task list** | PIE-full validation, deferred (agentic building, death→spirit), Act 2 prep (Defend/TimeOfDay), SaveGame persistence, Steam EA, docs, AUTOMATION_GAPS, buffer. | All T1–T10 **completed**. **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle. |
| **Twelfth 10-task list** | Implement agentic building (DAY10 Option B), packaged build run, demo sign-off, Act 2 follow-up, docs, refinement, AUTOMATION_GAPS, buffer. | All T1–T10 **completed**. **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Thirteenth 10-task list** | MVP scope updated with day/night and astral rules (VISION); tasks: verify MVP doc, astral-return-on-death, no-day-death, PIE pre-demo, packaged build, docs, AUTOMATION_GAPS, buffer. | All T1–T10 **completed** (2026-03-04 run; 10 rounds, loop_exited_ok). **Next:** Generate new list; run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Fourteenth 10-task list** | PIE re-verify, implement astral return, demo/sign-off, packaged build, Act 2, docs, refinement, AUTOMATION_GAPS, buffer. | Superseded by fifteenth (rapid prototyping list). |
| **Fifteenth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (astral return, night encounter, agentic building step, AdvanceToDawn, portal, Place/Harvest, dungeon/spirit stub, SaveGame/boss test), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Sixteenth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (hw.AstralDeath, night collectible stub, agentic building step, demo recording, packaged build, spirit ability stub, physical/spiritual goods stub, pie_test_runner TimeOfDay/astral), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Seventeenth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (OnAstralDeath wire, night collectible expansion, Act 2 Defend stub, spirit ability cooldown/second, physical/spiritual tagging, night encounter spawn, pie_test_runner night check, SaveGame TimeOfDay persistence), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Eighteenth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (astral death from damage, spiritual power persistence, Act 2 Defend expansion, spirit VFX/sound stub, Physical/Spiritual HUD, night encounter config, pie_test_runner SaveGame phase check, vertical slice checklist §4), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Nineteenth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (astral health HUD, spiritual power spend stub, family Defend positions, spirit cooldown/VFX on HUD, TimeOfDay phase on HUD, night encounter wave/second type, pie_test_runner spiritual power persistence, vertical slice §4 eighteenth), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twentieth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (day restoration loop design + stub, spirit ability cost, family move to DefendPosition, night countdown HUD, night encounter wave counter, pie_test_runner SpendSpiritualPower/astral HUD check, vertical slice §4 nineteenth, packaged build smoke-test), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-first 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (day buff SaveGame persistence, HUD insufficient power message, Defend next steps/end trigger, HUD restored-today count, wave 2 difficulty stub, pie_test_runner day restoration check, vertical slice §4 twenty-first, packaged build retry/workaround), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-second 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (day buff effect at night, HUD spiritual power at night, Defend return at dawn, second spirit ability or regen stub, wave 3/config spawns, pie_test_runner day buff persistence, vertical slice §4 twenty-second, Package-AfterClose run), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-third 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (love/bond stub, meals-with-family stub, planetoid packs design/stub, SpiritShield key + HUD, key-point boss stub, pie_test_runner day buff bonus check, vertical slice §4 twenty-third, package Stage retry doc), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-fourth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (conversion design/hook, LoveLevel persistence, homestead-on-planetoid design, HUD LoveLevel, planetoid packs config, pie_test_runner love bonus check, vertical slice §4 twenty-fourth, package retry or doc), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-fifth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (conversion wire when placeholder defeated, converted foe role stub, HUD Converted count, homestead-landed stub, pie_test_runner LoveLevel/conversion check, vertical slice §4 twenty-fifth, package retry or doc, conversion flow doc), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-sixth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (defend combat stub ranged/AOE, planetoid combat stub combo/single-target, converted role on HUD/log, pie_test_runner conversion/role check, combat variety doc, vertical slice §4 twenty-sixth, package retry or doc, defenses-around-homestead), T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-05). **Next:** Generate new 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-seventh 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (LoveLevel/day-buff feedback, defeat path for conversion test, homestead-on-planetoid level trigger, pie_test_runner SaveGame round-trip, pre-demo §3 run sequence, vertical slice §4 twenty-seventh, package retry or doc, KNOWN_ERRORS/AUTOMATION_GAPS update), T9 PIE verification, T10 buffer. First of 4 runs toward polished MVP per [MVP_GAP_ANALYSIS.md](MVP_GAP_ANALYSIS.md). | All T1–T10 **completed**. **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-eighth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (console commands reference, night spawn at Phase 2, HUD metrics reference, pie_test_runner planetoid/HomesteadLandedOnPlanetoid check, demo-readiness checklist, vertical slice §4 twenty-eighth, package retry or doc, KNOWN_ERRORS/AUTOMATION_GAPS update), T9 PIE verification, T10 buffer. Run 2 of 4 toward polished MVP. | All T1–T10 **completed**. **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Twenty-ninth 10-task list** | **Rapid prototyping** (§0): T1–T8 implementation (pre-demo entry point, pie_test_results interpretation, combat stub testability, MVP polish readiness section, vertical slice date/run note, vertical slice §4 twenty-ninth, package retry or doc, KNOWN_ERRORS/AUTOMATION_GAPS update), T9 PIE verification, T10 buffer. Run 3 of 4 toward polished MVP. | All T1–T10 **completed**. **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Thirtieth 10-task list** | **Vision-aligned** (from [VISION.md](VISION.md)): T1–T8 implementation (vision–task cross-ref, sin/virtue spectrum doc, Week 1 playtest checklist, planetoid complete doc, converted role mapping, day love→night paragraph, vertical slice single source, night three-part checklist), T9 PIE pre-demo (documented deferred in VERTICAL_SLICE_CHECKLIST §3), T10 buffer. | All T1–T10 **completed**. **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Thirty-first 10-task list** | **Rapid prototyping** (§0): T1–T2 console commands (hw.Planetoid.Complete, hw.SinVirtue.Pride), T3–T4 vertical slice §4 (thirtieth + thirty-first deliverables), T5 CONSOLE_COMMANDS update, T6 packaged build or doc, T7 KNOWN_ERRORS/AUTOMATION_GAPS, T8 pie_test_runner planetoid-complete check, T9 PIE verification, T10 buffer. | All T1–T10 **completed** (2026-03-06 run; 10 rounds, max rounds reached so T10 completed manually). **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |
| **Thirty-second 10-task list** | **Rapid prototyping** (§0): T1 max rounds 11 (RunAutomationLoop.ps1), T2–T3 vertical slice §4 thirty-second deliverables + CONSOLE_COMMANDS planetoid_complete, T4 hw.SinVirtue.Greed stub, T5 packaged build or doc, T6 KNOWN_ERRORS/AUTOMATION_GAPS, T7 vertical slice §4 thirty-second outcomes, T8 PIE pre-demo verification, T9 task list/loop state verification, T10 buffer. | All T1–T10 **completed** (2026-03-06 run; 10 rounds; T10 ran in-loop thanks to max-rounds 11 cap). **Next:** Generate new list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1`. |

---

## 5. Quick reference for “what’s next”

- **Current tasks:** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md)
- **Project state and work not yet done:** [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md)
- **Where we’re heading:** [VISION.md](VISION.md)
- **Next planning window:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md)
- **Gaps (manual-only):** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md)
- **How to generate next list:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md)
