# Manual Editor tutorial — Work that tools cannot do

**Purpose:** One place for **every task you must do in the Unreal Editor by hand**, because scripts, MCP, and Python cannot do them (or cannot do them reliably). Run your automation first, then follow this tutorial to complete setup. Each section is ordered so you can do them in sequence or jump to what you need.

**When to use:** After running scripts such as `create_demo_from_scratch.py`, `assemble_planetoid_from_config.py`, `ensure_wbp_main_menu.py`, or `ensure_demo_portal.py`. If something still does not work (e.g. PCG generates nothing, portal does not load the planetoid, main menu has no buttons), use the matching section below.

**Policy — GUI automation is default when available:** When we have the ability to interact with the Editor UI automatically (e.g. GUI scripts in `Content/Python/gui_automation/`), that is the **default method**. Use the clicker script first; use this manual tutorial only as **fallback** when GUI automation is unavailable (refs not captured, script not runnable) or has failed. For steps with no clicker (e.g. WBP_MainMenu, BUILD branch, terrain), manual is the only path. See [GUI_AUTOMATION_WHY_AND_WHEN.md](GUI_AUTOMATION_WHY_AND_WHEN.md) and [.cursor/rules/automation-standards.mdc](.cursor/rules/automation-standards.mdc).

**References:** [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md), [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md).

---

## Before you start

1. **Run the relevant scripts first** (Tools → Execute Python Script or MCP `execute_python_script`). Scripts create levels, place actors, tag landscapes, assign graphs, and trigger Generate where possible.
2. **Check Output Log** after each script. Messages like "Could not set..." or "set in Editor" mean you must do that step here.
3. **One-time vs repeat:** Most steps below are **one-time**. Once done, re-running scripts will reuse your work (create-if-missing, update-in-place).

---

## 1. PCG — Forest (DemoMap)

**When:** After running `create_demo_from_scratch.py` (or `create_pcg_forest.py`) and trees/rocks do not appear, or Generate produces nothing.

**Why manual:** Python cannot set Get Landscape Data (By Tag + tag name), Actor Spawner Template, or Static Mesh Spawner mesh list in UE 5.7.

### Steps

1. **Open the PCG graph**  
   Content Browser → **Content → HomeWorld → PCG** → double‑click **ForestIsland_PCG**.

2. **Get Landscape Data**  
   - Select the **Get Landscape Data** node.  
   - In **Details**:  
     - **Actor** → **By Tag** (or Actor Selector Settings → By Tag).  
     - **Tag** (or Tag Name): **`PCG_Landscape`**.  
     - If available: **Component** → **By Class** → **Landscape Component**.

3. **Tree branch (Actor Spawner)**  
   - Select the **Actor Spawner** node used for trees.  
   - In **Details** set **Template Actor** (or **Actor Class**) to **BP_HarvestableTree**: `/Game/HomeWorld/Building/BP_HarvestableTree`.  
   - If the tree branch is a **Static Mesh Spawner** instead, set **Mesh Selector** / mesh list to the mesh(es) from `Content/Python/pcg_forest_config.json` → `static_mesh_spawner_meshes`.

4. **Rocks branch (if present)**  
   - Select the **Static Mesh Spawner** for rocks.  
   - In **Details** set **Mesh Selector** / mesh list from `pcg_forest_config.json` → `static_mesh_spawner_meshes_rocks`.

5. **Assign graph to volume**  
   - Close the graph. In the **level** (e.g. DemoMap), select **PCG_Forest** in the Outliner.  
   - In **Details** → **Graph** assign **ForestIsland_PCG**.

6. **Generate**  
   - With **PCG_Forest** still selected, in **Details** find the **PCG** section and click **Generate** (or **Ctrl+Click** for full regeneration).  
   - Check **Output Log** for `LogPCG`; if none, the correct Generate was not used.

**Save the level** (Ctrl+S) so instances persist. See [PCG_SETUP.md](PCG_SETUP.md) and [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) for more.

---

## 2. PCG — Planetoid POI (Planetoid_Pride)

**When:** After running `assemble_planetoid_from_config.py` or `setup_planetoid_pcg.py` and the planetoid PCG generates no POIs.

**Why manual:** Same as §1 — Get Landscape Data and Actor Spawner Template are not settable from Python.

### Steps

1. **Open the planetoid level**  
   File → Open Level → **Planetoid_Pride** (`/Game/HomeWorld/Maps/Planetoid_Pride`), or leave it open after the assembly script.

2. **Open the PCG graph**  
   Content Browser → **Content → HomeWorld → PCG** → **Planetoid_POI_PCG**.

3. **Get Landscape Data**  
   - Select **Get Landscape Data**.  
   - In **Details**: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component** if available.

4. **Actor Spawner (POI)**  
   - Select the **Actor Spawner** node.  
   - In **Details** set **Template Actor** (or **Actor Class**) to **BP_Shrine_POI**: `/Game/HomeWorld/BP_Shrine_POI` (or the POI Blueprint you want).

5. **Assign graph to volume**  
   - In the level, select the **PCG Volume** (e.g. labeled **PCG_Planetoid_POI**).  
   - **Details** → **Graph** → **Planetoid_POI_PCG**.

6. **Generate**  
   - With the volume selected, **Details** → **Generate** (or Ctrl+Click).  
   - Save the level.

See [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md) §6.3.

---

## 3. Portal — Level To Open (DemoMap → planetoid)

**When:** The portal on DemoMap does not load the planetoid when you walk into it (e.g. nothing happens or wrong level).

**Why manual:** The C++ property `LevelToOpen` on the portal actor is not writable from Python on the placed instance. **Workaround:** Use the Blueprint **BP_PortalToPlanetoid** (created by `ensure_portal_blueprint.py`) so the default LevelToOpen is already **Planetoid_Pride**; then you do not need this step. If you placed a different actor (e.g. cube or base class without default), do the following.

### Steps

1. **Open DemoMap** and select the **portal actor** in the Outliner (at the position from `planetoid_map_config.json`, e.g. (800, 0, 100)).
2. In **Details**, find **Dungeon** (or the component/actor section that has **Level To Open**).
3. Set **Level To Open** to **Planetoid_Pride** (the level name, no path).
4. **Save** the level.

**Alternative:** Run `ensure_portal_blueprint.py` then `ensure_demo_portal.py` so the portal is **BP_PortalToPlanetoid**; its class default already has LevelToOpen = Planetoid_Pride. See [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 1.

---

## 4. Main menu widget (WBP_MainMenu)

**When:** The game starts but there is no main menu, or the menu has no buttons / wrong parent class.

**Why manual:** MCP and some Python paths cannot create the widget with parent **HomeWorldMainMenuWidget** or add buttons and bindings. The script `ensure_wbp_main_menu.py` creates the asset when the Editor allows; buttons and bindings are often still manual.

### Steps

1. **Create widget if missing**  
   - Content Browser → **Content → HomeWorld → UI**.  
   - Right‑click → **User Interface → Widget Blueprint**.  
   - Name: **WBP_MainMenu**.  
   - Open it → **Class Settings** → **Parent Class**: **HomeWorldMainMenuWidget**.

2. **Layout and buttons**  
   - In the Designer: add **Canvas Panel**, then a **Vertical Box** with four **Buttons**: **Play**, **Character**, **Options**, **Quit**.

3. **Bindings**  
   - For each button, **On Clicked** → assign the C++ method:  
     - Play → **OnPlayClicked**  
     - Character → **OnCharacterClicked**  
     - Options → **OnOptionsClicked**  
     - Quit → **OnQuitClicked**

4. **Config**  
   - In **Config/DefaultGame.ini**, under `[/Script/HomeWorld.HomeWorldGameInstance]`:  
     `MainMenuWidgetClassPath=/Game/HomeWorld/UI/WBP_MainMenu.WBP_MainMenu_C`  
   - In **Config/DefaultEngine.ini**, under `[/Script/EngineSettings.GameMapsSettings]`:  
     `GameDefaultMap=/Game/HomeWorld/Maps/MainMenu.MainMenu`  
   - Ensure **GameInstanceClass** is **HomeWorldGameInstance**.

See [CHARACTER_GENERATION_AND_CUSTOMIZATION.md](CHARACTER_GENERATION_AND_CUSTOMIZATION.md) §2.

---

## 5. State Tree — Night? and Defend branch (ST_FamilyGatherer)

**When:** You want family agents to switch to Defend behavior at night. C++ and console (`hw.TimeOfDay.Phase 2`) already set night; the State Tree graph must have a Night? branch and Defend task.

**Why manual:** There is no Python/MCP API to edit the State Tree graph (add branches, conditions, tasks, blackboard keys).

### Steps

1. **Open the State Tree**  
   Content Browser → **Content → HomeWorld → AI** (or the path where **ST_FamilyGatherer** lives) → double‑click **ST_FamilyGatherer**.

2. **Root**  
   - Ensure the root is a **Selector**.  
   - Add a **Night?** branch as the **first** child (highest priority).

3. **Night? condition**  
   - Set the branch **condition** to read Blackboard **IsNight** (Bool).

4. **Defend state**  
   - Inside that branch, add a **Defend** state with a task (e.g. **Move To** rally point or enemy).

5. **Blackboard**  
   - In the State Tree **Blackboard**, add **IsNight** (Bool).  
   - In game code (e.g. Mass processor or Blueprint), set IsNight from **UHomeWorldTimeOfDaySubsystem::GetIsNight()** (night when phase is 2; console: `hw.TimeOfDay.Phase 2`).

6. **Compile and save** the State Tree.

**Validate:** PIE → console `hw.TimeOfDay.Phase 2` → agents using ST_FamilyGatherer should switch to the Defend branch. See [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) § Gap 2 and [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md).

---

## 6. State Tree — BUILD branch (full agentic building)

**When:** You want family agents to find build orders, move to the Smart Object, and complete the build (Path 2). Path 1 (console **hw.PlaceWall**, **hw.CompleteBuildOrder**) works without this.

**Why manual:** Same as §5 — no API to edit the State Tree graph.

### Steps

1. **Open ST_FamilyGatherer** in the State Tree editor.
2. Add a **BUILD** branch (e.g. after Gather, before Defend): condition = “has incomplete build order nearby” (EQS or blackboard).
3. In that branch add: **Move To** (target from EQS: nearest actor with tag **BuildOrder** and `bBuildCompleted == false`), then **Claim Smart Object** (SO_WallBuilder), then task that triggers build and calls **CompleteBuildOrder()** when done.
4. **EQS:** Create an EQS query that finds actors with tag **BuildOrder** in range; use “nearest” or first result as target for Move To.
5. **Blackboard:** Optional keys **TargetBuildOrder**, **CurrentJob** (Build) for the BUILD branch.
6. **Compile and save.**

See [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md) Step 3 and [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md).

---

## 7. Planetoid level — create from scratch (if no template)

**When:** `ensure_planetoid_level.py` reports that the planetoid level does not exist and you have not set `template_level_path` in `planetoid_map_config.json`.

**Why manual:** The script cannot create a level from nothing; it can only create from a template or tell you to create it.

### Steps

1. **File → New Level → Empty Open World.**
2. **File → Save As** → save under **Content/HomeWorld/Maps/** as **Planetoid_Pride** (path `/Game/HomeWorld/Maps/Planetoid_Pride`).
3. Run **assemble_planetoid_from_config.py** or **setup_planetoid_pcg.py** again; they will use this level.

See [DAYS_16_TO_30.md](tasks/DAYS_16_TO_30.md) Day 16.

---

## 8. Planetoid — Pride terrain (canyons, valleys, mountains, spires)

**When:** You want the Pride planetoid to look like the vision (canyons, valleys, mountains, large spires). Scripts do not sculpt terrain.

**Why manual:** No script or MCP for Landscape heightmap sculpting, Erosion, or Noise; spires are placed as static meshes or by hand.

### Steps

1. **Open Planetoid_Pride** (or the planetoid level).
2. **Landscape**  
   - Select the Landscape. Use **Sculpt** mode to block out mountains, valleys, and canyon cuts.  
   - Use **Erosion** and **Noise** tools to break up flatness and add natural variation (see engine docs: Landscape Erosion Tool, Landscape Noise Tool).  
   - For **canyons**: lower elevation along curves or splines; erosion on walls; optional material mask (rock on walls, different on floor).  
   - For **spires**: add **Static Mesh** actors (rock pillars) as landmarks, or combine a heightmap peak with a mesh on top.
3. **Materials**  
   - Paint or use height/slope-based materials so slopes and valleys read correctly (e.g. rock on steep, grass/dirt in valleys).
4. **Save** the level.

See [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md) §3 and [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md).

---

## 9. Planetoid — Homestead plateau and spawn

**When:** You want the homestead to start on a plateau at the top of a mountain with the option to glide down.

**Why manual:** Designer choice for spawn location and any “plateau” volume or actor; glide is a separate ability (GAS or movement mode).

### Steps

1. **Open the planetoid level** and sculpt or place a **plateau** (flat area at a high point) if not already there.
2. **Place spawn / homestead**  
   - Place the player start (or a “homestead” actor/volume) on the plateau.  
   - Set **GameMode** default spawn or the level’s **Player Start** to this location.
3. **Glide**  
   - Implement later as a GAS ability or movement mode; design is in [VISION.md](workflow/VISION.md) and [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md).

---

## 10. Optional — Meal triggers (overlap component)

**When:** You want breakfast/lunch/dinner to trigger on **overlap** as well as on **interact** (E). Scripts create the Blueprints and place them; they may not add **UHomeWorldMealTriggerComponent**.

### Steps

1. Open **BP_MealTrigger_Breakfast**, **BP_MealTrigger_Lunch**, **BP_MealTrigger_Dinner** (in Content).
2. **Add Component** → **HomeWorldMealTriggerComponent** (or search **Meal Trigger**).
3. Set **Meal Type** on each (Breakfast, Lunch, Dinner).
4. Save each Blueprint.

Interact (E) on the tagged actor already works via GA_Interact; this adds overlap-based triggering. See [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) research log (List 57).

---

## 11. Optional — World Partition (load landscape for PCG)

**When:** The planetoid (or any level) uses World Partition and PCG “Generate” still produces no instances; the Landscape may not be loaded in the editor.

**Why manual:** Get Landscape Data (By Tag) only sees actors that are loaded. In WP, landscape components live on **LandscapeStreamingProxy** actors; they must be in a loaded region.

### Steps

1. In the **World Partition** window, **select all cells** (or the full grid) that contain the landscape.
2. **Load region from selection** (or equivalent) so the Landscape proxies load.
3. Run the script that tags the Landscape (`setup_planetoid_pcg.py` or `ensure_landscape_has_pcg_tag`) so **all loaded** proxies get tag **PCG_Landscape**.
4. Then in the PCG graph set **Get Landscape Data** → **By Tag** = **PCG_Landscape** (§1 or §2) and **Generate**.

See [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) (World Partition, Empty Open World).

---

## Quick reference — what is manual

| Area | What you do | Section |
|------|-------------|---------|
| **PCG Forest (DemoMap)** | Get Landscape Data By Tag + tag `PCG_Landscape`; Actor/Static Mesh Spawner template or mesh list; assign graph; Generate | §1 |
| **PCG Planetoid** | Same for Planetoid_POI_PCG; Template = BP_Shrine_POI (or chosen POI) | §2 |
| **Portal** | Level To Open = Planetoid_Pride (or use BP_PortalToPlanetoid so not needed) | §3 |
| **Main menu** | Create WBP_MainMenu, parent HomeWorldMainMenuWidget, four buttons + bindings; config DefaultGame/DefaultEngine | §4 |
| **State Tree Night?/Defend** | Add Night? branch, IsNight condition, Defend task, Blackboard IsNight | §5 |
| **State Tree BUILD** | Add BUILD branch, EQS BuildOrder, MoveTo + Claim SO + CompleteBuildOrder | §6 |
| **Planetoid level** | New Level → Empty Open World → Save As Planetoid_Pride (if no template) | §7 |
| **Pride terrain** | Sculpt / Erosion / Noise; spires as meshes | §8 |
| **Homestead plateau** | Place spawn/homestead on plateau; glide = future | §9 |
| **Meal overlap** | Add HomeWorldMealTriggerComponent to meal Blueprints | §10 |
| **World Partition** | Load landscape region so Get Landscape Data can find tagged actors | §11 |

---

## See also

- [PCG_SETUP.md](PCG_SETUP.md) — Full PCG checklist and troubleshooting.  
- [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) — Why each PCG setting is manual.  
- [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) — All gaps and workarounds (portal, State Tree, WBP_MainMenu).  
- [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md) — Planetoid checklist and manual follow-up.  
- [CHARACTER_GENERATION_AND_CUSTOMIZATION.md](CHARACTER_GENERATION_AND_CUSTOMIZATION.md) — Main menu and character screen.  
- [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md) — BUILD branch and build orders.  
- [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md) — Defend-at-night and State Tree.
