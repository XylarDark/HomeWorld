# Days 16–30: Planetoid, Spirits, Dungeon, Buffer

Task index for Phase 3 (Planetoid), Phase 4 (Spirits), Phase 5 (Dungeon), and buffer days. Each section gives the goal and links; use placeholder assets and engine defaults where needed.

**See also:** [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md), [VISION.md](../../../VisionBoard/Core/VISION.md), [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md).

---

## Day 16 [3.1] — Planetoid level / sublevel

**Goal:** One planetoid level; travel from homestead (DemoMap) via portal or sublevel.

**Implementation (scripts + manual):**

- **Config:** [Content/Python/planetoid_map_config.json](../../Content/Python/planetoid_map_config.json) — `planetoid_level_path` (e.g. `/Game/HomeWorld/Maps/Planetoid_Pride`), optional `template_level_path`, `portal_position` (x,y,z on DemoMap), `portal_placeholder_label`.
- **Single entry point:** Run **assemble_planetoid_from_config.py** in Editor. It runs: ensure_demo_portal (DemoMap + portal) → setup_planetoid_pcg (planetoid level + PCG). Then do manual steps in [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](../PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md) §6.3 (Get Landscape Data By Tag, Actor Spawner Template, terrain, plateau).
- **Scripts (individual):** Run in Editor (Tools → Execute Python Script or MCP `execute_python_script`):
  1. **ensure_planetoid_level.py** — Idempotent: ensures planetoid level exists; if missing, creates from template when `template_level_path` is set, else logs manual steps (File → New Level → Empty Open World → Save As Planetoid_Pride).
  2. **ensure_demo_portal.py** — Opens DemoMap and runs **place_portal_placeholder.py**: places **AHomeWorldDungeonEntrance** at `portal_position` with `LevelToOpen` from config (`portal_level_to_open`, e.g. Planetoid_Pride) and tag `Portal_To_Planetoid`; idempotent. Falls back to cube if C++ class unavailable. Alternatively run **place_portal_placeholder.py** with DemoMap already open.
  3. **setup_planetoid_pcg.py** — One-shot: ensures planetoid level, POI BPs, Planetoid_POI_PCG graph; opens planetoid level, tags Landscape, places PCG Volume, assigns graph, sets Get Landscape Data, triggers Generate, saves. See [PCG_SETUP.md](../PCG_SETUP.md).
- **T2 (CURRENT_TASK_LIST) verification:** After running ensure_demo_portal (or place_portal_placeholder with DemoMap open), set **LevelToOpen** to **Planetoid_Pride** in the portal actor’s Details panel (Python cannot set this C++ UPROPERTY; see AUTOMATION_GAPS). Run ensure_planetoid_level.py so the planetoid map exists. Start PIE on DemoMap, walk to (800,0,100) and into the portal trigger; the level should change to Planetoid_Pride. pie_test_runner includes a “Portal configured” check (Editor-time: portal actor with tag and LevelToOpen set); full E2E is PIE walk. If a cube placeholder was placed instead, add a Blueprint overlap → Open Level on that actor per AUTOMATION_GAPS Gap 1.
- **T4 (CURRENT_TASK_LIST) verification:** Portal placement verified: ensure_demo_portal/place_portal_placeholder run; cube placeholder removed and AHomeWorldDungeonEntrance placed when C++ class is available. Run pie_test_runner for "Portal configured" (actor with tag Portal_To_Planetoid and LevelToOpen). If LevelToOpen is not set (Gap 1), set in Editor Details or run gui_automation/set_portal_level_to_open.py (ref image). E2E: PIE on DemoMap, walk to (800,0,100) → planetoid level loads when LevelToOpen is set.
- **T3 (CURRENT_TASK_LIST) verification — Portal LevelToOpen (DemoMap → planetoid):** Verified/documented 2026-03-05. Run **place_portal_placeholder.py** with DemoMap open (MCP or Tools → Execute Python Script); script places AHomeWorldDungeonEntrance at (800,0,100) with tag Portal_To_Planetoid and attempts to set LevelToOpen from Python (often fails per Gap 1). **Verification:** (1) Editor-time: run **pie_test_runner.py** (no PIE) for "Portal configured" (actor with tag + LevelToOpen when readable). (2) Full E2E: set **LevelToOpen** to **Planetoid_Pride** in Editor Details or run gui_automation/set_portal_level_to_open.py (ref image); PIE on DemoMap, walk to (800,0,100), enter trigger → planetoid level loads. AUTOMATION_GAPS Gap 1 is current.
- **T3 (ninth list, 2026-03-05) re-verification:** MCP get_actors_in_level confirmed **HomeWorldDungeonEntrance** at (800,0,100) on current level. Ran place_portal_placeholder.py and pie_test_runner.py via MCP (success). Portal placement and tag verified; LevelToOpen status from pie_test_runner is in Saved/pie_test_results.json. Full E2E (walk to portal → planetoid load) requires LevelToOpen set per Gap 1 (Details or set_portal_level_to_open.py). No doc or AUTOMATION_GAPS change needed; Gap 1 remains current.
- **T6 (CURRENT_TASK_LIST) verification — Planetoid visit flow:** Prerequisite: **LevelToOpen** must be set on the portal actor (AHomeWorldDungeonEntrance). Python cannot set this C++ UPROPERTY (see AUTOMATION_GAPS Gap 1). To set it: (1) run capture_portal_refs.py host-side (Editor open, portal selected, PyAutoGUI), then set_portal_level_to_open.py; or (2) in Editor, select the portal actor in DemoMap, in Details set **LevelToOpen** to **Planetoid_Pride**. Ensure planetoid level exists (run ensure_planetoid_level.py). **Manual test steps:** (1) Open DemoMap in Editor; (2) Start PIE; (3) Walk to portal at config position (800, 0, 100); (4) Enter trigger volume; (5) Level should transition to Planetoid_Pride (UGameplayStatics::OpenLevel). Optional: run pie_test_runner with PIE not running for Editor-time "Portal configured" check (actor with tag Portal_To_Planetoid; LevelToOpen set is reported when readable). Full E2E requires PIE + walk to portal.
- **T5 (fifteenth list, 2026-03-05) — Portal LevelToOpen set via Blueprint default:** Run **ensure_portal_blueprint.py** then **ensure_demo_portal.py** (or ensure_demo_portal alone; it calls ensure_portal_blueprint). This creates **BP_PortalToPlanetoid** (child of AHomeWorldDungeonEntrance) with CDO **LevelToOpen = Planetoid_Pride** and places that Blueprint at the portal position. No Editor Details or GUI automation needed. **Verify:** PIE on DemoMap, walk to (800,0,100), enter trigger → planetoid level loads.
- **Automation gap (logged):** Level Streaming Volume setup is not automated; portal uses AHomeWorldDungeonEntrance + OpenLevel so no Level Streaming Volume required. See [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) for alternatives.
- See [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md). Use placeholder mesh for portal if needed.

---

## Day 17 [3.2] — PCG POI placement

**Goal:** PCG graph that places POI actors (Shrine, Treasure, CultivationNode, MiningNode).

**Implementation (scripts + manual):**

- **Scripts (run in Editor):**
  1. **create_bp_poi_placeholders.py** — Creates BP_Shrine_POI and BP_Treasure_POI (Actor) in /Game/HomeWorld/. Idempotent.
  2. **create_planetoid_poi_pcg.py** — Creates Planetoid_POI_PCG graph (Get Landscape Data → Surface Sampler → Transform → Actor Spawner). Idempotent. Config: planetoid_map_config.json (`poi_points_per_squared_meter`, optional `poi_actor_blueprint_path`).
- **Automated:** Run **setup_planetoid_pcg.py** (opens planetoid level, tags Landscape, places PCG Volume, assigns Planetoid_POI_PCG, sets Get Landscape Data By Tag, triggers Generate). If any step fails (engine API limits), open planetoid level and: ensure Landscape has tag **PCG_Landscape**; assign graph **Planetoid_POI_PCG** to the volume; set Get Landscape Data **By Tag** + **PCG_Landscape** and Actor Spawner **Template** in the graph; **Generate**. See [PCG_VARIABLES_NO_ACCESS.md](../PCG_VARIABLES_NO_ACCESS.md), [PCG_SETUP.md](../PCG_SETUP.md).
- See [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) (placement philosophy). Mesh/list can be placeholder cubes.

---

## Day 18 [3.3] [3.4] — Shrine POI, Treasure POI

**Goal:** Shrine actor (interaction/GAS); Treasure actor (loot on interact).

**Implementation:**

- **C++ (HomeWorldCharacter):** Extended `TryHarvestInFront()`: same trace; if hit actor has tag **Treasure_POI**, call `UHomeWorldInventorySubsystem::AddResource(Wood, 25)` and destroy actor; if tag **Shrine_POI**, log "Shrine activated" (placeholder for future GAS buff). Same E/Interact key as harvest.
- **Blueprint tags:** `create_bp_poi_placeholders.py` sets default actor tag **Shrine_POI** on BP_Shrine_POI and **Treasure_POI** on BP_Treasure_POI (run script to apply; add tags manually in Editor if script cannot set CDO).
- **Validation:** PIE on level with POI placed; face Shrine or Treasure, press E; confirm log and (Treasure) inventory Wood +25 and actor removed.
- **Shrine:** Placeholder only; add GAS buff in Blueprint or C++ later. **Treasure:** Uses existing [UHomeWorldInventorySubsystem](../../Source/HomeWorld/HomeWorldInventorySubsystem.h).

---

## Day 19 [3.5] [3.6] — Cultivation, Mining

**Goal:** Cultivation and Mining nodes/zones; workable by spirits (Phase 4); yield resources over time.

**Implementation:**

- **C++ (AHomeWorldYieldNode):** Base actor in `Source/HomeWorld/HomeWorldYieldNode.h/.cpp`: `ResourceType`, `YieldRate`, `YieldIntervalSeconds`, `bIsProducing`. Timer adds yield to `UHomeWorldInventorySubsystem` every interval (stub: always producing; Day 22 will gate on assigned spirit). Box overlap component for placement.
- **Blueprints:** Run in Editor: **create_bp_yield_nodes.py** — creates BP_Cultivation_POI (tag `CultivationNode`, ResourceType=Wood, YieldRate=5, 10s) and BP_Mining_POI (tag `MiningNode`, ResourceType=Ore, YieldRate=5, 10s). Idempotent. Add Static Mesh in Editor if desired.
- **Validation:** Close Editor, run **Build-HomeWorld.bat**. Open Editor, run script, place one of each node in level; PIE and wait for interval (or reduce in Details for testing); confirm Output Log "YieldNode ... produced ... +N" and inventory increases.
- **Spirit assignment:** Day 22 will use tags CultivationNode/MiningNode and optional worker reference on the node.

---

## Day 20 [3.7] — Visit and interact

**Goal:** Player can travel to planetoid, reach POIs, interact (harvest treasure, activate shrine, etc.).

**Implementation:**

- **Dependencies:** Day 16 (portal placeholder, level streaming or Open Level); Day 18 (TryHarvestInFront handles Shrine_POI and Treasure_POI; same E/Interact). No new C++ or Blueprint required—same GameMode and character on both levels; GA_Interact and trace work on planetoid POIs.
- **Manual (Day 16):** In DemoMap, add Level Streaming Volume referencing planetoid level, or a Blueprint trigger at the portal placeholder that on overlap calls **Open Level** (planetoid map) or streams the sublevel. Place portal trigger so player can "travel" to planetoid.
- **Validation:** (1) PIE on DemoMap; go to portal and trigger travel to planetoid. (2) On planetoid, move to a Shrine or Treasure POI; press E. Confirm Shrine logs "Shrine activated" and Treasure grants Wood +25 and removes actor. (3) Optional: set project default map to planetoid map temporarily to test POI interaction without travel.
- **Success:** Document in this section that visit = portal/streaming (Day 16) and interact = existing GA_Interact (Day 18); PIE checklist above suffices for Day 20 sign-off.

---

## Day 21 [4.1] [4.2] — Death → spirit, Spirit roster

**Goal:** On death, character becomes spirit; spirit roster in GameState or subsystem.

**Implementation:**

- **C++ (UHomeWorldSpiritRosterSubsystem):** Game instance subsystem: `AddSpirit(FName SpiritId)`, `GetSpirits()`, `RemoveSpirit(FName)` (Day 23), `GetSpiritCount()`. Serializes to **UHomeWorldSaveGame** via **SerializeToSaveGame** / **DeserializeFromSaveGame** for persistence.
- **Death → spirit hook:** **AHomeWorldCharacter::ReportDeathAndAddSpirit()** — call from Blueprint or game code when Health reaches 0 (e.g. GAS effect or damage handler). Gets SpiritRosterSubsystem from GameInstance, calls **AddSpirit(GetSpiritIdForDeath())**. **GetSpiritIdForDeath()** returns a unique FName (actor name + UniqueID). Logs when spirit is added.
- **Validation:** (1) Blueprint: get character, call Report Death And Add Spirit; confirm Output Log "Character '...' reported death and added as spirit: ...". (2) Get subsystem, call AddSpirit with test ID, GetSpirits/GetSpiritCount; confirm log and count.
- **T5 verification:** In PIE, open console (~) and run `hw.ReportDeath` — adds player to spirit roster; confirm Output Log "Character '...' reported death and added as spirit: ..." and (optional) GetSpiritCount via subsystem.
- **T7 (CURRENT_TASK_LIST) verification:** (1) Start PIE on a map with the player (e.g. DemoMap). (2) Open in-game console (~), run `hw.ReportDeath`. (3) In Output Log expect: `HomeWorld: Character '...' reported death and added as spirit: <Name>_<UniqueID>` and `HomeWorld: Spirit added to roster: <id> (count=1)`. Same character reported again is idempotent (duplicate ID not added). Spirit roster is updated via `UHomeWorldSpiritRosterSubsystem::AddSpirit`; use Blueprint/C++ Get Spirit Count to confirm count if needed. **Automated:** Run `pie_test_runner.py` with PIE active; the **ReportDeath** check runs `hw.ReportDeath` and, if SpiritRosterSubsystem is accessible from Python, verifies spirit count; otherwise reports "executed; confirm in Output Log". For boss reward use **GrantBossReward** check (Day 25).

---

## Day 22 [4.3] [4.4] — Assign spirit to node, Node progress/yield

**Goal:** Player assigns spirit to Cultivation/Mining node; node produces resources when worked.

**Implementation:**

- **C++ (AHomeWorldYieldNode):** `SetAssignedSpirit(FName)`, `ClearAssignment()`, `GetAssignedSpirit()`; `AssignedSpiritId`; setting a spirit sets `bIsProducing = true`, clear sets false. Yield timer runs in BeginPlay; `ProduceYield()` gates on `bIsProducing`.
- **C++ (UHomeWorldSpiritAssignmentSubsystem):** `AssignSpiritToNode(SpiritId, Node)` (clears previous node if spirit was elsewhere), `UnassignSpirit(SpiritId)`, `GetNodeForSpirit(SpiritId)`. Game instance subsystem.
- **Flow:** Call `GetGameInstance()->GetSubsystem<UHomeWorldSpiritAssignmentSubsystem>()->AssignSpiritToNode(SpiritId, YieldNode)` from UI or interaction; node then produces each interval. Player inventory receives yield via existing `ProduceYield()` → `UHomeWorldInventorySubsystem::AddResource`.

---

## Day 23 [4.5] — Unassign / reclaim spirit

**Goal:** Player can unassign spirit from a node; spirit becomes idle for reassignment.

- UHomeWorldSpiritAssignmentSubsystem::UnassignSpirit(SpiritId) clears the node’s **Implementation:** UHomeWorldSpiritAssignmentSubsystem::UnassignSpirit(SpiritId) clears the node assignment; node stops producing. Spirit remains in roster (Day 21); call from UI or interaction.

---

## Day 24 [5.1] [5.2] — Dungeon POI, Dungeon interior

**Goal:** Dungeon as POI; on interact load interior; interior layout with boss arena.

**Implementation:**

- **Scripts (run in Editor with target level open):** (1) **ensure_dungeon_entrance_blueprint.py** — Creates or reuses **BP_DungeonEntrance** (child of AHomeWorldDungeonEntrance) with CDO **LevelToOpen** from config (e.g. `Dungeon_Interior`). (2) **place_dungeon_entrance.py** — Idempotent: prefers **BP_DungeonEntrance**, then AHomeWorldDungeonEntrance, then cube; places at `dungeon_entrance_position` from [dungeon_map_config.json](../../Content/Python/dungeon_map_config.json) with tag **Dungeon_POI**. Overlap in PIE opens the configured level.
- **C++ trigger:** **AHomeWorldDungeonEntrance** ([Source/HomeWorld/HomeWorldDungeonEntrance.h](../../Source/HomeWorld/HomeWorldDungeonEntrance.h)) opens a level when the player overlaps its box. Run ensure_dungeon_entrance_blueprint first so LevelToOpen is set via Blueprint default; optionally set **Require Pawn Tag** (e.g. `Player`) in Editor on BP_DungeonEntrance.
- **Dungeon level streaming — steps:**
  1. **Create dungeon level:** File → New Level → Empty Open World (or Basic); Save As → e.g. `Dungeon_Interior` under `/Game/HomeWorld/Maps/`. Add placeholder geometry, lights, boss arena as needed. If the level does not exist, OpenLevel at runtime will fail until the map is created.
  2. **Option A (script default):** Run place_dungeon_entrance.py with DemoMap open; script places AHomeWorldDungeonEntrance with LevelToOpen = dungeon_level_name from config. PIE: walk into the trigger → dungeon level loads.
  3. **Option B (Level Streaming Volume):** In DemoMap, Window → Levels → Level Streaming; add a streaming level and assign the dungeon map; add a **Level Streaming Volume** so the dungeon streams when the player enters the volume.
  4. **Option C (Blueprint only):** If script placed a cube fallback, add **On Actor Begin Overlap** → **Open Level** (Level Name = dungeon map name).
- **T3 (CURRENT_TASK_LIST) verification:** After running place_dungeon_entrance.py with DemoMap open, create the dungeon map if missing (File → New Level → Save As Dungeon_Interior). If **LevelToOpen** is not set (same Python limitation as portal—see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 1), set it in Editor Details to the dungeon map name (e.g. `Dungeon_Interior`). Start PIE on DemoMap, walk into the dungeon entrance trigger; the level should change to the dungeon. If a cube placeholder was placed, add a Blueprint overlap → Open Level on that actor.
- **Validation:** Run place_dungeon_entrance.py with level open; run pie_test_runner.py for **Dungeon entrance configured** check (actor with tag Dungeon_POI). PIE and walk into trigger to confirm dungeon level loads.
- **T7 (CURRENT_TASK_LIST) — Dungeon entrance opens level in PIE:** Run **ensure_dungeon_entrance_blueprint.py** then **place_dungeon_entrance.py** with DemoMap open (MCP or Tools → Execute Python Script). This creates **BP_DungeonEntrance** (child of AHomeWorldDungeonEntrance) with CDO **LevelToOpen** from dungeon_map_config.json (e.g. `Dungeon_Interior`) and places that Blueprint at (-800,0,100). No Editor Details or Gap 1 workaround needed. **Verify:** Create dungeon map if missing (File → New Level → Save As Dungeon_Interior). PIE on DemoMap, walk to (-800,0,100), enter trigger → dungeon level loads.

- **T5 (CURRENT_TASK_LIST) verification:** (1) **Dungeon entrance:** Run `place_dungeon_entrance.py` with DemoMap open (MCP or Tools → Execute Python Script); script places **AHomeWorldDungeonEntrance** at config position (-800,0,100) with tag **Dungeon_POI**. LevelToOpen may not be settable from Python (same as portal—see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 1); if so, set **Level To Open** in Editor Details to `Dungeon_Interior`. Create the dungeon map if missing (File → New Level → Save As Dungeon_Interior under /Game/HomeWorld/Maps/). Run `pie_test_runner.py` for **Dungeon entrance configured** check. PIE on DemoMap, walk to (-800,0,100) and into the trigger → dungeon level loads when LevelToOpen is set. (2) **State Tree Defend:** T2 attempted Gap 2; no Python API for State Tree graph editing. Full Defend (hw.TimeOfDay.Phase 2 → agents switch to Defend) requires one-time manual steps in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) §Gap 2 (Night? branch, IsNight blackboard, Defend task in ST_FamilyGatherer). `pie_test_runner.py` includes **TimeOfDay Phase 2** check (validates GetIsNight() when Phase 2); observable Defend behavior requires the manual State Tree setup. Status documented in DAY12_ROLE_PROTECTOR §4 and AUTOMATION_GAPS.

---

## Day 25 [5.3] [5.4] — Boss actor, Dungeon complete / reward

**Goal:** Boss pawn with GAS (health, abilities); on death drop loot; dungeon complete grants reward.

**Implementation:** Boss: Pawn or Character Blueprint with GAS (reuse or extend existing attribute set/abilities); spawn in dungeon arena; placeholder mesh. Reward: on death (or kill event) call `UHomeWorldInventorySubsystem::AddResource` or custom reward struct; optional story flag. Manual/Blueprint setup; no new C++ required unless custom boss behavior needed.

**T5 verification (boss reward):** In PIE, open console (~) and run `hw.GrantBossReward` (or `hw.GrantBossReward 150` for amount). Grants Wood to player inventory; **HUD shows "Boss reward: +N Wood"** (yellow toast for 4s); confirm log "HomeWorld: hw.GrantBossReward granted Wood +N". A real boss Blueprint would call the same InventorySubsystem AddResource on death.

**T8 (CURRENT_TASK_LIST) verification:** Automated: run `pie_test_runner.py` with PIE active; the **GrantBossReward** check executes `hw.GrantBossReward 50` in the PIE world and, if InventorySubsystem is accessible from Python, asserts Wood increased; otherwise reports "executed; confirm in Output Log". Manual: same as T5 above.

---

## Days 26–30 — Buffer

**Goal:** Catch-up, Milady pipeline, 7-sins prep, polish, documentation.

- **Day 26:** Catch-up, [MILADY_IMPORT_ROADMAP.md](MILADY_IMPORT_ROADMAP.md), or 7-sins/moral-system prep per [VISION.md](../../../VisionBoard/Core/VISION.md).
- **Day 27:** Continue buffer; performance, LODs, onboarding.
- **Day 28:** Buffer or post-alpha prep (Steam EA scope).
- **Day 29:** Buffer; documentation updates.
- **Day 30:** Final catch-up; sign-off 30-day block; plan next 30-day window.
