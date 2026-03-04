# Days 16–30: Planetoid, Spirits, Dungeon, Buffer

Task index for Phase 3 (Planetoid), Phase 4 (Spirits), Phase 5 (Dungeon), and buffer days. Each section gives the goal and links; use placeholder assets and engine defaults where needed.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md), [VISION.md](../workflow/VISION.md), [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md).

---

## Day 16 [3.1] — Planetoid level / sublevel

**Goal:** One planetoid level; travel from homestead (DemoMap) via portal or sublevel.

**Implementation (scripts + manual):**

- **Config:** [Content/Python/planetoid_map_config.json](../../Content/Python/planetoid_map_config.json) — `planetoid_level_path` (e.g. `/Game/HomeWorld/Maps/Planetoid_Pride`), optional `template_level_path`, `portal_position` (x,y,z on DemoMap), `portal_placeholder_label`.
- **Scripts:** Run in Editor (Tools → Execute Python Script or MCP `execute_python_script`):
  1. **ensure_planetoid_level.py** — Idempotent: ensures planetoid level exists; if missing, creates from template when `template_level_path` is set, else logs manual steps (File → New Level → Empty Open World → Save As Planetoid_Pride).
  2. **ensure_demo_portal.py** — Opens DemoMap and runs **place_portal_placeholder.py**: places a cube at `portal_position` with tag `Portal_To_Planetoid`; idempotent. Alternatively run **place_portal_placeholder.py** with DemoMap already open.
  3. **setup_planetoid_pcg.py** — One-shot: ensures planetoid level, POI BPs, Planetoid_POI_PCG graph; opens planetoid level, tags Landscape, places PCG Volume, assigns graph, sets Get Landscape Data, triggers Generate, saves. See [PCG_SETUP.md](../PCG_SETUP.md).
- **Automation gap (logged):** Level Streaming or Open Level from DemoMap to planetoid is not automated; see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md). Add Level Streaming Volume or Blueprint trigger at portal when automation exists.
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

- **C++ (UHomeWorldSpiritRosterSubsystem):** Game instance subsystem in `Source/HomeWorld/HomeWorldSpiritRosterSubsystem.h/.cpp`: `AddSpirit(FName SpiritId)`, `GetSpirits()`, `RemoveSpirit(FName)` (for Day 23), `GetSpiritCount()`. Stores `TArray<FName>`. Logs when spirit added/removed.
- **Death → spirit:** When a character dies (e.g. Health 0 via GAS or custom event), game code must call `GetGameInstance()->GetSubsystem<UHomeWorldSpiritRosterSubsystem>()->AddSpirit(UniqueId)`. No death hook added in C++ for Day 21—integrate when damage/death pipeline exists (e.g. attribute change listener or Blueprint event).
- **Validation:** From Blueprint or console: get subsystem, call AddSpirit with test ID, call GetSpirits/GetSpiritCount; confirm log and count. Optional: console command to list spirits.

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

- **Script (optional):** Run in Editor with target level open (DemoMap or planetoid): **place_dungeon_entrance.py**. Idempotent: places a cube actor at `dungeon_entrance_position` from [Content/Python/dungeon_map_config.json](../../Content/Python/dungeon_map_config.json) with tag **Dungeon_POI**. Use this actor as the entrance; add Level Streaming or Open Level (see below).
- **C++ trigger (recommended):** **AHomeWorldDungeonEntrance** ([Source/HomeWorld/HomeWorldDungeonEntrance.h](../../Source/HomeWorld/HomeWorldDungeonEntrance.h)) opens a level when the player overlaps its box. Create a Blueprint (e.g. **BP_DungeonEntrance**) from it, set **Level To Open** to the dungeon map name (e.g. `Dungeon_Interior` for `/Game/HomeWorld/Maps/Dungeon_Interior`), and place it at the entrance (same position as the cube, or replace the cube). Optionally set **Require Pawn Tag** (e.g. `Player`) so only the player triggers the load.
- **Dungeon level streaming — steps:**
  1. **Create dungeon level:** File → New Level → Empty Open World (or Basic); Save As → e.g. `Dungeon_Interior` under `/Game/HomeWorld/Maps/`. Add placeholder geometry, lights, boss arena as needed.
  2. **Option A (Open Level on overlap):** Place **BP_DungeonEntrance** in DemoMap at the dungeon entrance; set **Level To Open** = `Dungeon_Interior` (the map’s asset name). PIE: walk into the trigger → level loads.
  3. **Option B (Level Streaming Volume):** In DemoMap, Window → Levels → Level Streaming; add a streaming level and assign the dungeon map; add a **Level Streaming Volume** in the level and set its bounds so the dungeon streams when the player enters the volume. Use when you want the dungeon as a sublevel in the same world.
  4. **Option C (Blueprint only):** Add a **Trigger Box** (or Box component) at the entrance; in Event Graph use **On Actor Begin Overlap** → **Get Player Pawn** (optional check) → **Open Level** (node from Gameplay Statics), Level Name = your dungeon map name.
- **Validation:** Run place_dungeon_entrance.py with level open; confirm actor with tag Dungeon_POI exists. Place BP_DungeonEntrance (or Option B/C); set level name; PIE and trigger to confirm dungeon level loads.

---

## Day 25 [5.3] [5.4] — Boss actor, Dungeon complete / reward

**Goal:** Boss pawn with GAS (health, abilities); on death drop loot; dungeon complete grants reward.

**Implementation:** Boss: Pawn or Character Blueprint with GAS (reuse or extend existing attribute set/abilities); spawn in dungeon arena; placeholder mesh. Reward: on death (or kill event) call `UHomeWorldInventorySubsystem::AddResource` or custom reward struct; optional story flag. Manual/Blueprint setup; no new C++ required unless custom boss behavior needed.

---

## Days 26–30 — Buffer

**Goal:** Catch-up, Milady pipeline, 7-sins prep, polish, documentation.

- **Day 26:** Catch-up, [MILADY_IMPORT_ROADMAP.md](MILADY_IMPORT_ROADMAP.md), or 7-sins/moral-system prep per [VISION.md](../workflow/VISION.md).
- **Day 27:** Continue buffer; performance, LODs, onboarding.
- **Day 28:** Buffer or post-alpha prep (Steam EA scope).
- **Day 29:** Buffer; documentation updates.
- **Day 30:** Final catch-up; sign-off 30-day block; plan next 30-day window.
