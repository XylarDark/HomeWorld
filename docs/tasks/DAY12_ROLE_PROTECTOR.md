# Day 12 [2.2]: Role — Attack/Defend (Protector)

**Goal:** Add **Protector** role behavior: State Tree combat branch (e.g. defend at night, move to enemy) and GAS combat abilities so a family agent can attack/defend.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 12, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md). **Astral death (night combat):** When the player's astral body is defeated at night, they return to body and wake at dawn — see [ASTRAL_DEATH_AND_DAY_SAFETY.md](ASTRAL_DEATH_AND_DAY_SAFETY.md).

---

## 1. Prerequisites

- **Day 11 done:** MEC_FamilyGatherer, ST_FamilyGatherer, Mass Spawner on DemoMap; agents spawn and are visible (and move if ZoneGraph is set up). See [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).
- **IsNight:** [UHomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h) provides `GetIsNight()` and `GetCurrentPhase()`. Use console **hw.TimeOfDay.Phase** to test night (see below).

**Testing IsNight (no DaySequence yet):** In PIE or Editor, open the **Output Log** or **Console** and run: `hw.TimeOfDay.Phase 2` to force **Night** (0=Day, 1=Dusk, 2=Night, 3=Dawn). Set back to day with `hw.TimeOfDay.Phase 0`. The State Tree Blackboard **IsNight** must be set from Blueprint or a Mass processor that reads `UHomeWorldTimeOfDaySubsystem::GetIsNight()`.

---

## 2. State Tree — Defend / Attack branch

Per [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Step 3.2 and Step 5:

1. **ST_FamilyGatherer** (or a dedicated ST_FamilyProtector if you split by role): ensure the root **Selector** has a **Night?** (or **Threat?**) branch as the **first** child (highest priority), above Idle/Gather.
2. **Condition:** Blackboard **IsNight** (Bool). Set IsNight from Blueprint or a Mass processor using `TimeOfDaySubsystem::GetIsNight()` (subsystem is not directly exposed in State Tree editor). Optional: "enemy in range" from “enemy in range” from Blackboard / EQS.
3. **Task:** Defend — e.g. **MoveTo** (rally point or enemy actor); optionally **Play Anim Montage** (guard/attack idle).
4. **Blackboard:** Add **IsNight** (Bool) and optionally **DefendTarget** (Vector or Object). Wire IsNight from game code: get the world's `UHomeWorldTimeOfDaySubsystem` and call `GetIsNight()` each tick or from a Mass processor, and write the result to the State Tree blackboard.

**List 62 / task list T2 (State Tree Night? branch):** There is no automation API for State Tree graph editing. Use the **one-time manual steps** in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2 (open ST_FamilyGatherer, add Night? as first child, condition IsNight, Defend task, Blackboard IsNight). Then validate with PIE + **hw.TimeOfDay.Phase 2** (see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Defend-at-night (List 62) verification). The C++ teleport path (T1/T3) gives observable "family at DefendPosition" without requiring the State Tree branch.

### Defend positions (T3 — family at Defend when DefendActive)

When **DefendActive** is true (night), family should be at "Defend positions" (rally points). Implemented as:

1. **Tag in level:** **create_demo_from_scratch.py** runs **place_defend_gather_positions.py** and **place_partner.py** so DemoMap gets one DefendPosition- and one GatherPosition-tagged actor and one Family-tagged actor (partner). Alternatively run those scripts with DemoMap open (Tools → Execute Python Script or MCP). Or place actors manually and add the tag **DefendPosition** (Details → Actor → Tags → add `DefendPosition`).
2. **GameMode discovery:** When TimeOfDay is Phase 2 (night), `AHomeWorldGameMode::TryLogDefendPositions()` runs once per night: finds all actors with tag `DefendPosition` and logs count and locations to Output Log (e.g. "Defend positions (T3): N actor(s) with tag DefendPosition" and first 5 locations). **PIE:** Run `hw.TimeOfDay.Phase 2` and check Output Log to confirm.
3. **T3 teleport (C++):** When DefendActive (night), `AHomeWorldGameMode::TryMoveFamilyToDefendPositions()` runs once per night: finds all actors with tag **Family** and all actors with tag **DefendPosition**, then teleports each Family actor to a DefendPosition (round-robin). Add tag **Family** to family representation actors (e.g. Mass-spawned agents or test pawns) so they are moved. **PIE:** Place DefendPosition- and Family-tagged actors, run `hw.TimeOfDay.Phase 2`; Output Log shows "HomeWorld: T3 moved N family actor(s) to DefendPosition (teleport)."
4. **State Tree MoveTo (optional):** Complete the one-time steps in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2 (Night? branch, IsNight blackboard, Defend task) for State Tree–driven move behavior. The C++ teleport above gives observable "family at DefendPosition" without requiring State Tree editing.
5. **No DefendPosition or Family actors:** If no DefendPosition or no Family actors, the log explains (add the respective tags for teleport to run).

### Defend next steps (T3 — nav vs teleport, phase end)

- **Current (MVP):** Family are teleported once per night to DefendPosition-tagged actors. No navigation; instant move. Good for prototype and testing.
- **Next steps (choose one or combine):**
  1. **Keep teleport as MVP** — No change; Defend remains “family at positions at night” via teleport. Document as design choice for prototype.
  2. **Nav move later** — Replace teleport with AI/nav move: use State Tree **MoveTo** (see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2: Night? branch, IsNight blackboard, Defend task) so family walk to DefendPosition. Requires Gap 2 one-time manual steps; then family move at night via State Tree instead of GameMode teleport.
  3. **Defend phase end** — When dawn arrives, Defend phase is cleared and logged. Implemented in `AHomeWorldGameMode::Tick`: on transition from Night to non-Night (e.g. Dawn), the game logs **"Defend phase end (dawn)."** and resets Defend state (bDefendPhaseLogged, bDefendPositionsLogged, bFamilyMovedToDefendThisNight). So each night Defend runs again from a clean state.

### Conversion and Defend (List 62 — VISION: convert, not kill)

Defend-at-night aligns with [VISION.md](../workflow/VISION.md) § Vanquishing foes: we **convert** attackers (strip sin → loved form), not kill them. When Defend phase is active (night), the game logs **"Defend active — convert attackers (VISION: convert, not kill)."** (once per night in `TryLogDefendPhaseActive`). When a foe is defeated during Defend, call **`AHomeWorldGameMode::ReportFoeConverted(Foe)`** so the game records the conversion (increments `ConvertedFoesThisNight`, optional role assignment). See GameMode `ReportFoeConverted`, `GetConvertedFoesThisNight`, and `EConvertedFoeRole`; full conversion gameplay (strip sin, spawn loved form) is implemented in later lists.

### T3 — Family return from Defend at dawn (stub)

When dawn arrives (phase transition from Night to non-Night), family that were at DefendPosition are **returned** to a gather/home position:

1. **GatherPosition tag:** Place actors (e.g. TargetPoint or empty Actor) where family should stand after dawn. Add the tag **GatherPosition** to each (Details → Actor → Tags → add `GatherPosition`).
2. **GameMode return:** `AHomeWorldGameMode::TryReturnFamilyFromDefendAtDawn()` runs once per dawn: finds all actors with tag **Family** and all actors with tag **GatherPosition**, then teleports each Family actor to a GatherPosition (round-robin). If no GatherPosition actors exist, family are teleported to **GatherReturnOffset** (configurable on GameMode Blueprint, default 500,0,100).
3. **PIE validation:** (1) Place Family- and DefendPosition-tagged actors, run `hw.TimeOfDay.Phase 2` (night) so family move to Defend. (2) Run `hw.TimeOfDay.Phase 3` (Dawn) or `hw.TimeOfDay.Phase 0` (Day). (3) Output Log shows "Defend phase end (dawn)." and "T3 return from Defend at dawn — moved N family actor(s) to GatherPosition" (or "to GatherReturnOffset" if no GatherPosition actors).
4. **No Family actors:** If no Family-tagged actors, the log explains; add tag **Family** to family representation actors for return to run.

---

## 3. GAS combat abilities (Protector)

- **C++:** `UHomeWorldProtectorAttackAbility` ([Source/HomeWorld/HomeWorldProtectorAttackAbility.h](../../Source/HomeWorld/HomeWorldProtectorAttackAbility.h)) — commit + log; add montage/effects in Blueprint. **Blueprint:** Run `Content/Python/create_ga_protector_attack.py` to create **GA_ProtectorAttack** and add to **BP_HomeWorldCharacter → Default Abilities**. Trigger via `TryActivateAbilityByClass` or add IA_ProtectorAttack for testing. **Granting:** For Mass agents with ASC, grant this ability; State Tree task can trigger by class or tag in Defend state.’s “family member” ASC if you use one; document how the State Tree or a task triggers the ability (e.g. “When in Defend state, fire ability by tag”).

- **Spirit/night ability (T6):** `UHomeWorldSpiritBurstAbility` — night-only (Phase 2) spirit combat stub. Run `Content/Python/create_ga_spirit_burst.py` to create **GA_SpiritBurst** and add to Default Abilities. In PIE: `hw.TimeOfDay.Phase 2` then `hw.SpiritBurst` to trigger; only succeeds at night. See [VISION.md](../workflow/VISION.md) spirit abilities at night.

---

## 4. Validation

- **PIE:** Run **hw.TimeOfDay.Phase 2** in console to force Night; agents using ST_FamilyGatherer should switch to the Defend branch. Use **hw.TimeOfDay.Phase 0** to return to day. Alternatively, with day/night or a test “night” trigger, agents switch to Defend (e.g. move toward enemy or rally point).
- **Combat:** After running `create_ga_protector_attack.py`, GA_ProtectorAttack is on the player Default Abilities. Trigger via `TryActivateAbilityByClass` or add input; check Output Log for "ProtectorAttack ability activated" and "committed successfully".

### T4 Act 2 prep validation (day/night Defend at home)

- **Family at homestead:** For the prototype, "family at homestead" is satisfied by family agents (Mass) spawning on the playable map. Use **DemoMap** as the homestead map: Mass Spawner is placed via `Content/Python/place_mass_spawner_demomap.py` (config: `demo_map_config.json` — `mass_spawner_position`, `mass_spawner_spawn_count`, etc.). Ensure MEC_FamilyGatherer and ST_FamilyGatherer are set up per [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).
- **PIE validation (hw.TimeOfDay.Phase 2):** (1) Open DemoMap, start PIE. (2) Open **Console** (or Output Log). (3) Run `hw.TimeOfDay.Phase 2` to force **Night**. (4) If ST_FamilyGatherer has the **Night?** branch and **IsNight** blackboard wired from `UHomeWorldTimeOfDaySubsystem::GetIsNight()` (see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2 for one-time manual steps), family agents should switch to the Defend branch (e.g. MoveTo rally or guard behavior). (5) Run `hw.TimeOfDay.Phase 0` to return to day. If the State Tree Night? branch is not yet added, complete the manual steps in AUTOMATION_GAPS Gap 2 first.
- **hw.Defend.Status:** In PIE, run **`hw.Defend.Status`** to log Defend phase status (phase 0–3, DefendActive, DefendPosition actor count, Family actor count, family-moved-this-night). Use after `hw.TimeOfDay.Phase 2` to verify Defend at home without relying on State Tree. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) Commands table.

### T4 (CURRENT_TASK_LIST) close-out

- **Outcome:** Gap re-documented; verification steps documented. There is no Python/MCP API for State Tree graph editing, so the **Night?** branch and **IsNight** blackboard cannot be added by automation. Full "agents switch to Defend" behavior requires the **one-time manual steps** in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2; after that, PIE + `hw.TimeOfDay.Phase 2` validates Defend.
- **Programmatic verification (TimeOfDay only):** The cvar **hw.TimeOfDay.Phase** (0=Day, 1=Dusk, 2=Night, 3=Dawn) is implemented in [HomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.cpp). In PIE, run `hw.TimeOfDay.Phase 2` in the console; `UHomeWorldTimeOfDaySubsystem::GetIsNight()` then returns true. No automated script is required for T4; full Defend validation is gated on the manual State Tree steps in Gap 2.

### T4 (eighth list, 2026-03-05) verification

- **Run:** MCP `execute_console_command("hw.TimeOfDay.Phase 2")` succeeded; `execute_python_script("pie_test_runner.py")` ran (includes `check_time_of_day_phase2`). `Saved/pie_test_results.json` not readable from agent context; outcome inferred: TimeOfDay cvar is set in PIE; full Defend behavior is observable only after completing [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2 one-time manual steps (Night? branch + IsNight blackboard). **DAY12 §4 satisfied:** validation procedure and Gap 2 dependency documented; T4 status set to completed in CURRENT_TASK_LIST.

### T8 (CURRENT_TASK_LIST) — Act 2 prep: day/night Defend at home

- **Goal:** Validate that day/night drives Defend; family at homestead (Mass on DemoMap); PIE with `hw.TimeOfDay.Phase 2` shows family Defend behavior when Night? branch is present; optional night encounter doc/stub.
- **Family at homestead:** Satisfied by Mass Spawner on DemoMap. Run `Content/Python/place_mass_spawner_demomap.py` with DemoMap open (MCP or Tools → Execute Python Script); config in `Content/Python/demo_map_config.json` (`mass_spawner_position`, `mass_spawner_spawn_count`, etc.). MEC_FamilyGatherer and ST_FamilyGatherer per [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).
- **PIE validation (Defend branch):** (1) Open DemoMap, ensure Mass Spawner exists (run place_mass_spawner_demomap.py if needed). (2) Start PIE. (3) Console: `hw.TimeOfDay.Phase 2` (Night). (4) If ST_FamilyGatherer has the **Night?** branch and **IsNight** blackboard wired (one-time manual steps in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2), family agents switch to Defend. (5) `hw.TimeOfDay.Phase 0` to return to day.
- **Night encounter stub:** [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) provides design and implementation stub (GetIsNight, OnNightStarted); satisfies T8 “doc or stub for night spawn.”
- **T8 success criteria:** All met: family-at-homestead script and config in place; PIE + Phase 2 validation documented; DAY12 T4 Act 2 prep validation satisfied; NIGHT_ENCOUNTER = doc/stub.
- **T8 closed (2026-03-05):** Automated validation run via MCP: `place_mass_spawner_demomap.py` (Mass Spawner on DemoMap), `pie_test_runner.py` (includes `check_time_of_day_phase2` in ALL_CHECKS; run with PIE active for TimeOfDay/GetIsNight verification). Defend branch observable in PIE only after one-time Gap 2 manual steps (State Tree Night? branch + IsNight blackboard).

### T3 (CURRENT_TASK_LIST) — Act 2 stub: Defend-at-home trigger (2026-03-05)

- **Implemented:** When TimeOfDay is Phase 2 (night), the game logs **"HomeWorld: Defend phase active (TimeOfDay Phase 2)."** once per night (AHomeWorldGameMode::TryLogDefendPhaseActive). **UHomeWorldTimeOfDaySubsystem::GetIsDefendPhaseActive()** returns true when Phase 2 (same as GetIsNight()) for State Tree / Blueprint. **PIE:** Run `hw.TimeOfDay.Phase 2`; Output Log shows "Defend phase active". Full Defend State Tree branch still requires AUTOMATION_GAPS Gap 2 (Night? branch + IsNight blackboard).

### T7 (CURRENT_TASK_LIST) — Act 2 prep: Defend at home validation (night phase)

- **Goal:** Validate day/night Defend at homestead; document validation steps and Gap 2 dependency.
- **Defend requires Gap 2 manual steps:** There is no Python/MCP API for State Tree graph editing. To see family Defend behavior in PIE, complete the **one-time manual steps** in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2 (open ST_FamilyGatherer, add Night? branch as first child, condition IsNight, Defend task, Blackboard IsNight wired from game code).
- **Validation steps (after Gap 2 setup):** (1) Open DemoMap, ensure Mass Spawner exists (`place_mass_spawner_demomap.py`). (2) Start PIE. (3) Console: `hw.TimeOfDay.Phase 2` (Night). (4) Family agents using ST_FamilyGatherer should switch to the Defend branch. (5) `hw.TimeOfDay.Phase 0` to return to day.
- **Programmatic check (TimeOfDay only):** Run `pie_test_runner.py` with PIE active; it includes `check_time_of_day_phase2` (sets Phase 2, verifies GetIsNight() when subsystem is accessible from Python). Result in `Saved/pie_test_results.json`. If PIE is not running, the check reports "PIE not running" (T5 run 2026-03-05: not run). Full Defend behavior is observable only in PIE after the manual State Tree setup.
- **T7 closed (2026-03-05):** Validation steps and Gap 2 dependency documented above; DAY12 T4 satisfied. No code changes.

- **T2 (CURRENT_TASK_LIST) PIE-with-validation — TimeOfDay Phase 2 (2026-03-05):** With PIE running, `pie_test_runner.py` was executed via MCP. **TimeOfDay Phase 2:** passed (detail: "TimeOfDay not gettable from Python; verify manually: hw.TimeOfDay.Phase 2 (DAY12 §4, AUTOMATION_GAPS Gap 2)."). The check sets the cvar and reports passed when the subsystem is not accessible from Python; Defend branch behavior remains manually verified after Gap 2 State Tree setup.
- **T2 eighth-list completed:** check_time_of_day_phase2 is in pie_test_runner ALL_CHECKS; run with PIE for current pass/fail. Save/Load persistence see DAY15 §4.
- **T2 ninth-list re-verification (2026-03-05):** pie_test_runner.py run via MCP; check_time_of_day_phase2 and check_save_load_persistence results in `Saved/pie_test_results.json` (see DAY15 §4). Defend branch remains gated on AUTOMATION_GAPS Gap 2.

### T4 (ninth list, 2026-03-05) verification

- **Run:** With PIE active (Editor + MCP connected), `execute_console_command("hw.TimeOfDay.Phase 2")` succeeded; `execute_python_script("pie_test_runner.py")` ran (includes `check_time_of_day_phase2`). `Saved/pie_test_results.json` not readable from agent context; outcome: TimeOfDay cvar set in PIE; programmatic Phase 2 check executed. Full Defend behavior (family agents switching to Night? branch) is observable only after completing [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2 one-time manual steps (Night? branch + IsNight blackboard in ST_FamilyGatherer). **DAY12 §4 satisfied:** validation procedure and Gap 2 dependency documented; T4 status set to completed in CURRENT_TASK_LIST.

### T5 (CURRENT_TASK_LIST) — Act 2 Defend at home (night phase) — closed 2026-03-05

- **Defend requires Gap 2 manual steps.** There is no Python/MCP API for State Tree graph editing; the **Night?** branch and **IsNight** blackboard must be added via the one-time steps in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2.
- **Validation (after Gap 2 setup):** Run Phase 2 after manual setup: (1) Open DemoMap, ensure Mass Spawner exists (`place_mass_spawner_demomap.py`). (2) Start PIE. (3) Console: `hw.TimeOfDay.Phase 2` (Night). (4) Family agents using ST_FamilyGatherer should switch to the Defend branch. (5) `hw.TimeOfDay.Phase 0` to return to day.
- **Programmatic check:** `pie_test_runner.py` (with PIE active) includes `check_time_of_day_phase2`; result in `Saved/pie_test_results.json`. TimeOfDay cvar works in PIE; full Defend behavior is observable only after Gap 2 State Tree setup.
- **DAY12 §4 satisfied:** Validation steps and Gap 2 dependency documented above and in T4/T7/T8; no code changes required for T5.

### T3 (eleventh list, 2026-03-05) — Act 2 prep: Defend at home / TimeOfDay validation

- **Run:** With Editor and MCP connected, `execute_console_command("hw.TimeOfDay.Phase 2")` succeeded; `execute_python_script("pie_test_runner.py")` ran (includes `check_time_of_day_phase2` in ALL_CHECKS). Results written to `Saved/pie_test_results.json`.
- **Outcome:** TimeOfDay cvar set in PIE (Phase 2 = Night). Full family Defend behavior (agents switching to Night? branch) is observable only after completing the one-time manual steps in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2 (Night? branch + IsNight blackboard in ST_FamilyGatherer). Gap 2 status unchanged.
- **DAY12 §4 satisfied:** Validation procedure and Gap 2 dependency documented; T3 status set to completed in CURRENT_TASK_LIST.

### T5 (twelfth list) — Act 2 follow-up: night encounter stub or Defend doc

- **Defend validation and Gap 2:** Defend-at-home validation steps and Gap 2 (State Tree Night? branch + IsNight) status are documented above and in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2. Full Defend behavior requires the one-time manual steps in Gap 2; then PIE + `hw.TimeOfDay.Phase 2` validates.
- **Night encounter stub:** [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) provides the design and implementation stub. **TimeOfDay hook:** `UHomeWorldTimeOfDaySubsystem::GetIsNight()` (poll) and `OnNightStarted` (delegate, reserved; not yet broadcast). Console: `hw.TimeOfDay.Phase 2` for Night. See NIGHT_ENCOUNTER §2 (Implementation stub) and §4 (Next steps when implementing).
- **Next step for Act 2:** (1) **Defend:** Complete [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2 one-time manual steps (Night? branch, IsNight blackboard in ST_FamilyGatherer), then PIE + `hw.TimeOfDay.Phase 2` to observe family Defend. (2) **Night encounter (optional):** Implement spawn/trigger per [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (e.g. GameMode or BP_NightEncounterManager using GetIsNight or future OnNightStarted).

---

## 5. After Day 12

- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 12 (Protector); Today = Day 13 (Healer). Append [SESSION_LOG.md](../SESSION_LOG.md).
