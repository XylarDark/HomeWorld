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
4. **Optional:** Create SO_WallBuilder Smart Object definition in Editor (Right-click in Building or SmartObjects → Smart Object) and add Smart Object component to BP_BuildOrder_Wall; implementation can be stubbed until family agents exist. See [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) Step 2.

**Validation:** PIE, press P while aiming at ground; BP_BuildOrder_Wall spawns at cursor. No family agents required.

---

## 3. Full Day 10 (Option B) — step order

**Prerequisite:** [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Steps 1–4 done (MEC_FamilyGatherer, ST_FamilyGatherer, Mass spawner, ZoneGraph, Smart Objects for gather/sleep).

Then follow [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md): BP_BuildOrder_Wall, SO_WallBuilder, BP_WoodPile (for agents), ST_FamilyGatherer BUILD branch, MP_WoodInventory, PIE validation.

---

## 4. After Day 10

- **If deferred:** Update DAILY_STATE (Yesterday = Day 10 defer; Today = Day 11); append SESSION_LOG. Day 10 optional item in 30_DAY_SCHEDULE can stay unchecked or marked deferred.
- **If prep only:** Same; SESSION_LOG notes asset prep done, agentic building deferred to after Phase 2.
- **If full:** Check off Day 10 in 30_DAY_SCHEDULE; DAILY_STATE Today = Day 11; SESSION_LOG with commit reference.
