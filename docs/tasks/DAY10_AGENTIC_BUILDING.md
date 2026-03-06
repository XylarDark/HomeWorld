# Day 10 [1.5]: Optional agentic building

**Goal:** Family agents fulfill player-placed build orders (SO_WallBuilder, State Tree BUILD). Day 10 is **optional** and can be done after Phase 2; this doc covers both prep-only and full implementation.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 10, [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md), [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY9_HOME_PLACEMENT.md](DAY9_HOME_PLACEMENT.md).

---

## 1. Options

| Option | Description |
|--------|-------------|
| **A. Defer** | Skip Day 10; proceed to Day 11 (Family spawn). Do agentic building later (e.g. after Day 15). |
| **B. Full Day 10** | Implement Family Agents base (FAMILY_AGENTS Steps 1–4) then Agentic Building (AGENTIC_BUILDING Steps 1–5). Requires Mass/State Tree/ZoneGraph/Smart Objects setup. |
| **C. Prep only** | Create BP_BuildOrder_Wall (and optional SO_WallBuilder shell), set PlaceActorClass on character. No Mass/State Tree work; full agentic building after Phase 2. |

---

## 2. Prep only (Option C) — steps

1. **Folders** — Run `Content/Python/ensure_week2_folders.py` in Editor so `/Game/HomeWorld/Building/` (and Mass/AI/SmartObjects) exist.
2. **BP_BuildOrder_Wall** — Run `Content/Python/create_bp_build_order_wall.py` in Editor (Tools → Execute Python Script or MCP when connected). This ensures Week 2 folders, creates the Blueprint from `AHomeWorldBuildOrder`, sets Build Definition ID to `Wall`, and sets **Place Actor Class** on BP_HomeWorldCharacter to BP_BuildOrder_Wall. Then in Editor add a Static Mesh component (wall or cube) and a translucent blue material for the hologram; set collision to Overlap only; ensure actor tag **BuildOrder** (C++ may already add it).
3. **PlaceActorClass** — Set automatically by the script above; if you ran it, verify in BP_HomeWorldCharacter Details that **Place Actor Class** = BP_BuildOrder_Wall.
4. **Optional:** Create SO_WallBuilder: Run `Content/Python/create_so_wall_builder.py` in Editor (Tools → Execute Python Script or MCP). This creates SO_WallBuilder and **DA_SO_WallBuilder_Behavior** in `/Game/HomeWorld/Building/` and assigns the behavior to SO_WallBuilder (fixes validation; no experimental plugin). Add interaction **BuildWall**, **Slots** = 2 if needed. Add Smart Object component to BP_BuildOrder_Wall and assign SO_WallBuilder; implementation can be stubbed until family agents exist. See [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) Step 2 and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) (SO_WallBuilder).

**Validation:** PIE, press P while aiming at ground; BP_BuildOrder_Wall spawns at cursor. No family agents required.

### T5 (CURRENT_TASK_LIST) verification — agentic building flow

- **Automated:** Run `create_bp_build_order_wall.py` (Editor or MCP) to ensure BP_BuildOrder_Wall exists and **Place Actor Class** is set on BP_HomeWorldCharacter. Run `pie_test_runner.py`; the **PlaceActorClass set** check verifies the character is configured for placement.
- **In PIE:** Press **P** while aiming at ground; BP_BuildOrder_Wall (or assigned placeholder) spawns at cursor. Full agentic flow (family agents building) is deferred per NEXT_30_DAY_WINDOW N2.

**T5 verification (2026-03-05):** Ran `create_bp_build_order_wall.py` and `pie_test_runner.py` via MCP; both executed successfully. **What works:** Script creates/reuses BP_BuildOrder_Wall, sets BuildDefinitionID and PlaceActorClass on BP_HomeWorldCharacter; pie_test_runner includes `check_place_actor_class_set`. In PIE, key **P** spawns the place actor at cursor. **What remains manual/deferred:** Full agentic flow (family agents fulfilling build orders via SO_WallBuilder, State Tree BUILD branch, MP_WoodInventory) remains deferred per NEXT_30_DAY_WINDOW N2; no console command to place wall from outside PIE — placement is in-PIE only via GA_Place (key P).

### T3 (CURRENT_TASK_LIST) verification — place wall via agent/console

- **Goal:** Place wall (or BP_BuildOrder_Wall) via agent/console so automation or testing can place structures.
- **What works (2026-03-05):**
  - **In-PIE:** Key **P** (GA_Place) spawns PlaceActorClass (e.g. BP_BuildOrder_Wall) at cursor. Run `create_bp_build_order_wall.py` first so PlaceActorClass is set on BP_HomeWorldCharacter.
  - **Console:** **hw.PlaceWall** — in PIE, open console (~) and run `hw.PlaceWall` to place one instance at current cursor/aim (same as key P). Requires PIE; uses character's PlaceActorClass and TryPlaceAtCursor().
  - **Automation:** Run `create_bp_build_order_wall.py` (Editor or MCP) to ensure BP_BuildOrder_Wall exists and PlaceActorClass is set; `pie_test_runner.py` has `check_place_actor_class_set`.
- **What remains manual/deferred:** Full agentic flow (family agents fulfilling build orders via SO_WallBuilder, State Tree BUILD branch) is deferred. Placing from **outside** PIE (e.g. Editor-only automation) would require GUI automation to simulate P or hw.PlaceWall inside a PIE session; no Editor-time spawn of build orders is implemented.
- **Success:** Place wall executable via console (hw.PlaceWall) and in-PIE flow (key P); verification and gaps documented here and in AUTOMATION_GAPS only if a new gap is identified.

**T2 (CURRENT_TASK_LIST, eleventh list 2026-03-05):** Verified/document outcome: (a) **Full agentic building** — still deferred; prep done (BP_BuildOrder_Wall, PlaceActorClass, SO prep); full flow (family agents fulfilling build orders per Option B) not implemented. (b) **Death-to-spirit** — implemented; `hw.ReportDeath` (HomeWorld.cpp) calls ReportDeathAndAddSpirit; `pie_test_runner.check_report_death` runs when PIE is active. PROJECT_STATE §2 Deferred features table updated (Last list/date = eleventh 2026-03-05) so next list does not re-add this verify task.

**T2 (CURRENT_TASK_LIST, twelfth list 2026-03-05):** Implement full agentic building flow (Option B) — **partial progress, outcome still deferred.** (1) **Added** `Content/Python/create_bp_wood_pile.py`: creates BP_WoodPile from AHomeWorldResourcePile with ResourceType=Wood, AmountPerHarvest=10 (idempotent). (2) **Already in place:** BP_BuildOrder_Wall, PlaceActorClass, SO_WallBuilder shell (create_bp_build_order_wall.py, create_so_wall_builder.py). (3) **Remaining (no automation API):** BUILD branch in ST_FamilyGatherer (EQS BuildOrder nearby, MoveTo SO, Claim, Play montage, Release) — State Tree graph editing has no Python API (AUTOMATION_GAPS Gap 2); SO_WallBuilder OnActivated/OnDeactivated wiring on BP_BuildOrder_Wall; MP_WoodInventory Mass Processor; HarvestWood SO on BP_WoodPile. Full flow requires manual or GUI-automation steps per AGENTIC_BUILDING.md and FAMILY_AGENTS_MASS_STATETREE.md. PROJECT_STATE §2 Deferred features table updated (Last list/date = twelfth 2026-03-05).

**T3 (CURRENT_TASK_LIST, fifteenth list 2026-03-05):** One concrete step implemented. (1) **AHomeWorldBuildOrder::CompleteBuildOrder()** — BlueprintCallable; sets `bBuildCompleted` and logs; SO_WallBuilder OnActivated (or agent BUILD branch) can call this when build finishes. (2) **Console command hw.CompleteBuildOrder** — In PIE, completes the nearest incomplete build order to the player (e.g. after placing with hw.PlaceWall or key P). **PIE test:** Place wall (P or hw.PlaceWall), then run `hw.CompleteBuildOrder`; log shows "Build order completed" and actor's `bBuildCompleted` is true (Blueprint can hide hologram / show final mesh). Full BUILD branch and SO behavior wiring still deferred.

**T3 (CURRENT_TASK_LIST, sixteenth list 2026-03-05):** SO_WallBuilder activation made **triggerable and observable** in PIE. **hw.SimulateBuildOrderActivation** — In PIE, simulates SO activation on the nearest incomplete build order: logs "SO_WallBuilder activation (simulated). Completing build order on &lt;actor&gt;" and calls CompleteBuildOrder(). **PIE test:** Place wall (P or hw.PlaceWall), then run `hw.SimulateBuildOrderActivation`; Output Log shows the SO activation message and "Build order completed"; `bBuildCompleted` is true. Full agent flow (family agents claiming and completing via State Tree BUILD branch) remains deferred (no API for State Tree graph editing); this command satisfies "SO activation is triggered and observable" for testing.

---

## 3. Full Day 10 (Option B) — step order

**Prerequisite:** [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Steps 1–4 done (MEC_FamilyGatherer, ST_FamilyGatherer, Mass spawner, ZoneGraph, Smart Objects for gather/sleep).

Then follow [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md): BP_BuildOrder_Wall, SO_WallBuilder, BP_WoodPile (for agents), ST_FamilyGatherer BUILD branch, MP_WoodInventory, PIE validation.

---

## 4. After Day 10

- **If deferred:** Update DAILY_STATE (Yesterday = Day 10 defer; Today = Day 11); append SESSION_LOG. Day 10 optional item in 30_DAY_SCHEDULE can stay unchecked or marked deferred.
- **If prep only:** Same; SESSION_LOG notes asset prep done, agentic building deferred to after Phase 2.
- **If full:** Check off Day 10 in 30_DAY_SCHEDULE; DAILY_STATE Today = Day 11; SESSION_LOG with commit reference.
