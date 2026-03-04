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

---

## 3. Full Day 10 (Option B) — step order

**Prerequisite:** [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Steps 1–4 done (MEC_FamilyGatherer, ST_FamilyGatherer, Mass spawner, ZoneGraph, Smart Objects for gather/sleep).

Then follow [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md): BP_BuildOrder_Wall, SO_WallBuilder, BP_WoodPile (for agents), ST_FamilyGatherer BUILD branch, MP_WoodInventory, PIE validation.

---

## 4. After Day 10

- **If deferred:** Update DAILY_STATE (Yesterday = Day 10 defer; Today = Day 11); append SESSION_LOG. Day 10 optional item in 30_DAY_SCHEDULE can stay unchecked or marked deferred.
- **If prep only:** Same; SESSION_LOG notes asset prep done, agentic building deferred to after Phase 2.
- **If full:** Check off Day 10 in 30_DAY_SCHEDULE; DAILY_STATE Today = Day 11; SESSION_LOG with commit reference.
