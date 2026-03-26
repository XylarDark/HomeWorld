# MVP gap analysis (vision vs implemented)

**Purpose:** Compare the project **vision** (VISION.md, PROTOTYPE_SCOPE, MVP full scope) with **what is implemented** and list gaps needed to reach a **solid, marketing-ready MVP**. Includes asset creation, gameplay, content, and polish. Use this to prioritize the next work.

**Sources:** [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md), [VisionBoard/Core/PROTOTYPE_SCOPE.md](../VisionBoard/Core/PROTOTYPE_SCOPE.md), [VisionBoard/Core/STACK_PLAN.md](../VisionBoard/Core/STACK_PLAN.md), [VisionBoard/MVP/MVP_TUTORIAL_PLAN.md](../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md), ACCOMPLISHMENTS_OVERVIEW §4, PROJECT_STATE_AND_TASK_LIST, CONTENT_LAYOUT, ASSET_WORKFLOW_AND_STEAM_DEMO, AssetCreation/.

---

## 1. MVP definition (from vision)

- **Theme:** Love as Epic Quest; day = physical/nurture, night = astral/combat.
- **MVP deliverable:** **Marketing-ready** slice: one playable loop, **one moment** (Claim homestead), **one beautiful corner** (Homestead compound), and **good-looking marketing material** (screenshots, capsule, short video). **Assets and visuals are mandatory.**
- **MVP tutorial gate:** One full day + night ending in “family taken”: wake → breakfast → love task → game with child → gather → lunch → dinner → bed → spectral combat → boss → wake to family taken.
- **Week 1 playtest gate:** Crash → scout → boss → claim home.
- **MVP full scope (vision):** Main menu (Play, Character, Options, Quit); full agentic building (family agents complete build orders); astral-by-day (stub or unlock); bed actor in-world; in-world meal/love/game triggers; assets and visuals for marketing.

---

## 2. What is implemented (summary)

| Area | Status | Notes |
|------|--------|--------|
| **C++ / systems** | Implemented | Character, GameMode, GAS (PrimaryAttack, Dodge, Interact, Place), BuildPlacementSupport, TimeOfDay, SaveGame, Family/Spirit/Inventory/SpiritRoster/SpiritAssignment, MealTrigger, GoToBed, DungeonEntrance, YieldNode, BuildOrder, ResourcePile, ProtectorAttack, Heal, SpiritBurst, SpiritShield, MainMenuWidget, CharacterCustomizeWidget, HUD, conversion (ReportFoeConverted). |
| **Console commands** | Implemented | hw.Meal.*, hw.LoveTask.Complete, hw.GameWithChild.Complete, hw.GoToBed, hw.TimeOfDay.Phase, hw.SpiritBurst, hw.GrantBossReward, hw.AstralDeath, hw.TutorialEnd, hw.PlaceWall, hw.Conversion.Test, etc. |
| **Main menu flow** | Implemented | C++ flow (Play → DemoMap, Character → character screen, Options stub, Quit). WBP_MainMenu and WBP_CharacterCreate require manual button binding per CHARACTER_GENERATION_AND_CUSTOMIZATION. |
| **DemoMap / PCG** | Implemented | DemoMap, ForestIsland_PCG, create_demo_from_scratch, place_resource_nodes; PCG mesh list / Get Landscape Data often need one-time manual setup (PCG_VARIABLES_NO_ACCESS). |
| **Placement / build** | Implemented | GetPlacementHit, GA_Place, TryPlaceAtCursor; BP_BuildOrder_Wall, BP_Bed, BP_MealTrigger_*, place_bed, place_resource_nodes. |
| **Night / conversion** | Implemented | TimeOfDay phases, SpiritBurst/SpiritShield, night encounter placeholder (ReportFoeConverted), HUD Converted count, boss reward. |
| **Asset pipeline** | Documented + script | AssetCreation/ layout, STYLE_GUIDE, batch_import_asset_creation.py, CONTENT_LAYOUT paths. |
| **Packaged build** | Attempted | Phase 3: build run documented; smoke test deferred (no exe or build failure). |

---

## 3. Gaps to solid MVP

### 3.1 Asset creation and visuals (critical)

Vision: *“Assets and visuals are mandatory for the MVP deliverable.”* Marketing-ready = screenshots, capsule, trailer.

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **No exported assets in pipeline** | `AssetCreation/Exports/` has only `.gitkeep` in Harvestables, Homestead, Dungeon, Biomes, Characters. No FBX/GLB in Exports. | Populate Exports (or use marketplace/FAB/Quixel): harvestables (trees, rocks, flowers), homestead buildings/props, dungeon kit, biome props. Run batch_import_asset_creation.py to get meshes into `/Game/HomeWorld/`. |
| **PCG / environment look** | ForestIsland_PCG exists; mesh list and landscape tag often manual. Trees/rocks may be placeholder or from a pack. | Lock PCG setup (Get Landscape Data By Tag, Static Mesh Spawner mesh list) so “beautiful corner” (homestead compound + forest) looks intentional. Use Quixel or POLYGON/Medieval Village per STACK_PLAN. |
| **Character / family look** | BP_HomeWorldCharacter; FAB or Man ref in CONTENT_LAYOUT. Family (partner, child) may be placeholder. | One recognizable player character; partner and child with clear read (Primitive Characters or POLYGON per PROTOTYPE_SCOPE asset list). |
| **Homestead “beautiful corner”** | place_homestead_placeholders, Homestead map; DemoMap compound. | Placed buildings, resource nodes, and PCG so one framed shot is screenshot-ready (lighting, no holes, no floating meshes). |
| **Capsule / key art** | Not in scope for Phase 4 (skipped). | Before calling MVP “done”: at least one capsule (616×353) and 2–5 key screenshots for store or pitch. |
| **Enemies / boss** | Night encounter placeholder; key-point boss spawn stub. | One or more enemy types for “scout/boss” beat; one boss for “claim home” moment (placeholder art OK if readable). |

**Action:** Prioritize (1) getting real meshes into Exports and importing (harvestables + homestead or environment pack), (2) one polished “beautiful corner” shot, (3) capsule/screenshots plan.

---

### 3.2 Gameplay and flow verification

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **Tutorial loop not consistently verified** | MVP_TUTORIAL_PLAN checklist has all steps; many session logs say “deferred (Editor/MCP not connected).” No recent single-session pass with all 13 steps green. | Run full tutorial loop in one PIE session (CONSOLE_COMMANDS § List 63 integration): wake → meals → love task → game with child → gather → bed → spectral → combat → boss → wake to family taken. Document pass/fail per step; fix broken steps. |
| **Week 1 playtest not signed off** | Crash → scout → boss → claim home: deferred in recent lists. | Run Week 1 playtest (CONSOLE_COMMANDS § Pre-demo, DAY5_PLAYTEST_SIGNOFF): start, move, harvest (E), trigger or reach boss, place (P) to claim home. Sign off in DAY5_PLAYTEST_SIGNOFF or SESSION_LOG. |
| **Pre-demo checklist often deferred** | VERTICAL_SLICE_CHECKLIST §3 (Level, Character, Moment, Corner, Stability) often unchecked or deferred. | With Editor and level open: complete §3 once, document result; fix any red (e.g. missing input, broken placement, crash). |
| **Child-creation mini-game** | Vision: “press sequence of keys in song-like pattern; child spawns.” No C++ or Blueprint implementation found. | Implement simple MVP: short key sequence (e.g. 4–6 keys with timing); on success, spawn child NPC and join household. Or document as post-MVP and keep hw.GameWithChild.Complete as console-only for tutorial. |

**Action:** (1) One full tutorial run + one Week 1 playtest run with results documented; (2) decide and implement or defer child-creation mini-game.

---

### 3.3 Content and level design

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **DemoMap as “moment + corner”** | DemoMap exists; resource nodes and PCG placeables. Homestead compound = chosen corner. | Ensure compound has placed buildings (or placeholders), lit and framed; “claim homestead” (P) works and feels like the moment. |
| **Planetoid (Pride)** | ensure_planetoid_level, place_portal_placeholder, Planetoid_POI_PCG; design in PLANETOID_DESIGN / PLANETOID_BIOMES. | For MVP: either one playable planetoid slice (portal from DemoMap → Pride with one biome/POI) or explicitly defer and keep Act 1 on DemoMap only. |
| **Dungeon** | BP_DungeonEntrance, dungeon_map_config; interior sublevel optional. | For “boss” beat: either dungeon entrance + interior or key-point boss in open world; one path must be playable. |
| **Family in level** | Partner and child for love task / game with child. | Partner and child actors in DemoMap (or tutorial level) with correct tags; in-world triggers for love task and game with child (BP_MealTrigger_* style). |

**Action:** Lock “one moment, one corner” on DemoMap (or one level); ensure partner/child and triggers exist where required by tutorial.

---

### 3.4 Agentic building (MVP full scope)

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **Path 1 (console/simulated)** | hw.PlaceWall, hw.CompleteBuildOrder, hw.SimulateBuildOrderActivation. | Verified via CONSOLE_COMMANDS; keep as MVP path if Path 2 not done. |
| **Path 2 (family agent BUILD)** | State Tree BUILD branch has no automation; manual graph editing. Agent claims SO, completes build order. | Either complete BUILD branch (manual steps in AGENTIC_BUILDING) and verify one full flow, or document as post-MVP and rely on Path 1 for MVP. |

**Action:** Decide: Path 2 required for MVP (then do manual State Tree + verification) or Path 1 sufficient (document and move on).

---

### 3.5 Polish and UX

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **Main menu / character UI** | C++ and widget class paths exist; WBP_MainMenu / WBP_CharacterCreate need buttons and bindings (manual per CHARACTER_GENERATION). | Confirm MainMenu → Play → DemoMap and Character → character screen work; bind Options (stub OK) and Quit. |
| **First-launch flow** | GameDefaultMap = MainMenu; ensure_main_menu_map. | Verify cold start → MainMenu → Play → in-game; no missing map or widget. |
| **HUD and feedback** | TimeOfDay phase, Spiritual/Physical, Converted, Love, Restored today, etc. | Enough for player to understand phase and key resources; no need for full polish if readable. |
| **Stability** | Many PIE/verification runs deferred. | One 2–5 min stable PIE session with no crash during tutorial or playtest; fix blocking errors. |

**Action:** One pass on main menu + first launch + one stable playthrough; log and fix blockers.

---

### 3.6 Packaged build and distributable

| Gap | Current state | Needed for MVP |
|-----|----------------|----------------|
| **Packaged exe** | Phase 3: packaged build run; smoke test deferred (no exe). | Optional for “MVP deliverable” (vision: marketing-ready does not require Steam). If you want a runnable build: fix Stage/build, produce exe, smoke-test once. |
| **Smoke test** | Documented as deferred. | If exe exists: launch, load level, move, confirm no critical errors. |

**Action:** Optional; only if MVP definition includes “runnable build.” Otherwise leave as deferred.

---

## 4. What to do next (prioritized order)

Use this list when you want to know **what to implement or fix next** for a solid MVP. Work in order; each item is one concrete focus.

1. **Assets and “beautiful corner”** — Get at least harvestables (or one environment pack) into Exports, import, assign to PCG/BP. One framed homestead compound shot that looks intentional.
2. **One full verification pass** — Tutorial loop + Week 1 playtest + pre-demo §3 in one or two sessions; document pass/fail; fix broken steps.
3. **Child-creation mini-game** — Implement simple key-sequence MVP or explicitly defer and document; align tutorial checklist.
4. **Main menu and first launch** — Confirm MainMenu → Play → DemoMap and Character screen; bind buttons if missing.
5. **Agentic building** — Decide Path 1 vs Path 2 for MVP; if Path 2, complete BUILD branch and verify.
6. **Capsule and screenshots** — At least one capsule and 2–5 screenshots for marketing (can be late in MVP).
7. **Packaged build** — Only if you need a runnable build for MVP; otherwise post-MVP.

---

## 5. References

- **Vision and scope:** [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md), [VisionBoard/Core/PROTOTYPE_SCOPE.md](../VisionBoard/Core/PROTOTYPE_SCOPE.md).
- **Asset workflow:** [ASSET_WORKFLOW_AND_STEAM_DEMO.md](ASSET_WORKFLOW_AND_STEAM_DEMO.md), [AssetCreation/README.md](../AssetCreation/README.md), [AssetCreation/STYLE_GUIDE.md](../AssetCreation/STYLE_GUIDE.md).
- **Verification:** [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) § Pre-demo and § List 63 integration, [VERTICAL_SLICE_CHECKLIST.md](../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md) §3, [MVP_TUTORIAL_PLAN.md](../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md), [DAY5_PLAYTEST_SIGNOFF.md](TaskLists/TaskSpecs/DAY5_PLAYTEST_SIGNOFF.md).
- **Content paths:** [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md).
- **Task lists:** [TaskLists/HOW_TO_GENERATE_TASK_LIST.md](TaskLists/HOW_TO_GENERATE_TASK_LIST.md), [TaskLists/NEXT_30_DAY_WINDOW.md](TaskLists/NEXT_30_DAY_WINDOW.md).
