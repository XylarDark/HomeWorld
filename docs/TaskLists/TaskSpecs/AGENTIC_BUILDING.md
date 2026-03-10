# Task: Agentic building (Mass + Smart Objects) — Week 2

**Goal:** Family agents autonomously build home structures (walls, farms, beds) from player-placed build orders. Player places a hologram (build order) using the existing placement API; agents detect it, gather resources, claim Smart Object, and complete the build.

**Status:** Not started.

**Prerequisite:** [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Steps 1–4 done (plugins, MEC_FamilyGatherer, ST_FamilyGatherer, spawner, ZoneGraph, Smart Objects for gather/sleep).

**Player placement:** Use existing [UBuildPlacementSupport::GetPlacementTransform](../../Source/HomeWorld/BuildPlacementSupport.cpp) (and GetPlacementHit) from a Blueprint or input handler to place build-order actors at the trace result (hologram preview).

---

## Build-order claim and completion path (T1 / List 60)

A **path** exists for "family agent claims and completes one build order" in two forms; both are documented here so the flow is playable or observable in PIE.

| Path | Description | Verification |
|------|-------------|--------------|
| **Path 1 (simulated, PIE-observable)** | Place a build order (key **P** or **hw.PlaceWall**), then simulate agent completion: **hw.SimulateBuildOrderActivation** or **hw.CompleteBuildOrder**. No family agents required; SO activation and completion are triggerable and observable in Output Log. | [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) — hw.PlaceWall, hw.CompleteBuildOrder, hw.SimulateBuildOrderActivation; [DAY10_AGENTIC_BUILDING.md](DAY10_AGENTIC_BUILDING.md) § T3 verification. |
| **Path 2 (full agent)** | State Tree **BUILD branch** per [Step 3](#step-3-state-tree-build-branch--in-depth-guide) below: EQS BuildOrder nearby → MoveTo SO → Claim SO_WallBuilder → play build → CompleteBuildOrder(). Requires manual State Tree graph setup (no Python API; see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2). Alternatively a Blueprint-only build-order flow per [DAY10_AGENTIC_BUILDING.md](DAY10_AGENTIC_BUILDING.md). | PIE with family agents (Mass spawner + ST_FamilyGatherer BUILD branch); or follow Step 3 in Editor. |

**Pre-demo / run sequence:** For step-by-step run sequence and all commands (including agentic building), use the single entry point: [VERTICAL_SLICE_CHECKLIST §3](../../../VisionBoard/VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing) (run sequence) and [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (command reference). Open CONSOLE_COMMANDS for both §3 and the hw.* commands.

---

## Build-order targeting (family agents — T2 / List 60)

Mechanism for **family agents to find and select** incomplete build orders so the BUILD branch (or Blueprint equivalent) can pick one. Use one or more of the following; the BUILD branch in [Step 3](#step-3-state-tree-build-branch--in-depth-guide) uses EQS + tag.

| Mechanism | Description | Use in BUILD |
|-----------|-------------|--------------|
| **Tag BuildOrder** | All [AHomeWorldBuildOrder](../../Source/HomeWorld/HomeWorldBuildOrder.h) actors get tag **BuildOrder** in C++ constructor. Blueprint children (e.g. BP_BuildOrder_Wall) inherit it; you can add **Wall** (or other) in Details for EQS filtering by type. | EQS query filters by **Tag = BuildOrder**. |
| **Incomplete only** | Build orders are **incomplete** when **`bBuildCompleted == false`**. After [CompleteBuildOrder()](../../Source/HomeWorld/HomeWorldBuildOrder.cpp) the order is complete and should be excluded from targeting. | In EQS or State Tree: use a query that returns actors; in a Mass processor or Blueprint, filter with `!bBuildCompleted`. EQS does not filter by C++ property; use a custom test or post-filter in State Tree (e.g. condition that checks result is incomplete). |
| **EQS (recommended)** | Create an EQS query: find actors overlapping a sphere/capsule (e.g. 500–1000 u), filtered by **Tag = BuildOrder**. Returns candidate locations/actors; the BUILD branch condition requires at least one result (or nearest distance valid). | [Step 3](#step-3-state-tree-build-branch--in-depth-guide): BUILD condition references this EQS; tasks use **nearest** result as target. |
| **Selection rule** | **Nearest:** pick the build order closest to the agent (EQS “nearest” or sort results by distance). **By BuildDefinitionID:** filter by [GetBuildDefinitionID()](../../Source/HomeWorld/HomeWorldBuildOrder.h) (e.g. `Wall`) if the agent should only target certain types. | State Tree: use EQS “nearest” generator or first result; optional blackboard key **TargetBuildOrder** (object or vector) set from EQS result for MoveTo. |
| **Blackboard (optional)** | In [ST_FamilyGatherer](FAMILY_AGENTS_MASS_STATETREE.md) or BUILD branch: **TargetBuildOrder** (Object or Vector), **CurrentJob** (Gather/Build/Defend). Set when entering BUILD so MoveTo and SO claim use the chosen order. | Step 3 blackboard: set **CurrentJob = Build** and optionally **TargetBuildOrder** from EQS. |
| **Subsystem / service (optional)** | A future **subsystem or service** could list incomplete build orders in the level (e.g. `GetIncompleteBuildOrders(World, Origin, Radius)`). Not required for List 60; EQS + tag is sufficient. | If added: BUILD condition or processor could call it and set blackboard; same selection rule (nearest or by BuildDefinitionID). |

**Console parity:** The commands **hw.CompleteBuildOrder** and **hw.SimulateBuildOrderActivation** ([CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md)) use the same idea: find all `AHomeWorldBuildOrder`, filter `!bBuildCompleted`, pick **nearest to player**, then complete. Agents use the same “nearest incomplete” rule from the agent’s position via EQS.

---

## Step 1: Prep building assets — In-depth guide

### 1.1 Modular building pieces

1. Use Megascans, Medieval pack, or project meshes for **walls, floors, roofs**.
2. **Convert to Construction Mesh:** In Content Browser, **right-click** the static mesh asset → **Asset Actions → Convert to Construction Mesh** (or equivalent in your UE version). This marks the mesh for use in construction/snap workflows.
3. Note the asset paths (e.g. under `/Game/HomeWorld/Building/` or your content folder) for use in the hologram and final wall mesh.

### 1.2 Hologram Blueprint (BP_BuildOrder_Wall)

1. **Content Browser:** Navigate to **Content → HomeWorld → Building** (create folder via `ensure_week2_folders.py` if needed).
2. **Right-click** → **Blueprint Class**. In the picker, search for **HomeWorldBuildOrder** (the C++ class [AHomeWorldBuildOrder](../../Source/HomeWorld/HomeWorldBuildOrder.h)). Select it and create a child Blueprint.
3. Name it **BP_BuildOrder_Wall**.
4. **Open** the Blueprint. In **Components:**
   - The root may be an **OverlapVolume** (from C++). Add a **Static Mesh** component (or use the root for overlap and add a child mesh).
   - **Static Mesh:** Assign a wall mesh (or a simple plane/cube for testing). For a “hologram” look, assign a **translucent blue material** (create one in Materials if needed: Opacity < 1, blue tint).
   - **Collision:** Ensure the mesh or root uses **Overlap Only** (e.g. collision preset **OverlapAllDynamic** or custom Overlap).
5. **Details (Blueprint):** Under **Build Order** (from C++), set **Build Definition ID** to `Wall` (optional; used by EQS/State Tree to filter).
6. **Tags:** The C++ class already adds tag **BuildOrder**. In the Blueprint **Details**, **Actor** section, you can add tag **Wall** if desired for EQS.
7. **Save.** **Place test:** Drag **BP_BuildOrder_Wall** into the level 2–3 times; confirm they appear and that in **Details** the actor has tag **BuildOrder**.

---

## Step 2: Smart Objects for building — In-depth guide

### 2.1 Create SO_WallBuilder (Smart Object definition)

1. **Content Browser:** **Right-click** in `/Game/HomeWorld/Building/` or `/Game/HomeWorld/SmartObjects/` → **Smart Object** (or **Artificial Intelligence → Smart Object** / **Smart Object Definition** depending on UE version).
2. Name it **SO_WallBuilder**. Open it.
3. **Interaction definition:**
   - Add an interaction (e.g. name **BuildWall**).
   - **Slots:** Set to **2** (two agents can work together at this SO).
4. **Events:**
   - **OnActivated:** When an agent claims and “activates” the SO, trigger: play build anim (e.g. montage) and **spawn the final wall mesh** at the hologram location (replace or hide the hologram).
   - **OnDeactivated:** When the interaction ends, **destroy the hologram** (or hide it) so the built wall remains.

Implementation of OnActivated/OnDeactivated: use Blueprint logic on the SO definition or on the BP_BuildOrder_Wall that holds the SO component; from C++ call **AHomeWorldBuildOrder::CompleteBuildOrder()** when the build finishes (sets `bBuildCompleted`, logs). Blueprint can bind to `bBuildCompleted` to hide hologram and show final mesh. Console **hw.CompleteBuildOrder** (PIE) completes the nearest incomplete build order for testing. Goal: agent claims SO → build anim plays → CompleteBuildOrder() → final mesh appears, hologram removed.

### 2.2 Link SO_WallBuilder to the hologram

1. Open **BP_BuildOrder_Wall**.
2. **Add Component** → **Smart Object** (or **Smart Object Component**). If the SO component requires a **Smart Object definition** reference, set it to **SO_WallBuilder**.
3. Ensure the SO component’s **bounds/slots** cover the hologram area so agents can claim slots. Save.

### 2.3 Resource pile (BP_WoodPile)

1. **Content Browser:** **Right-click** in Building (or SmartObjects) → **Blueprint Class**. Search for **HomeWorldResourcePile** ([AHomeWorldResourcePile](../../Source/HomeWorld/HomeWorldResourcePile.h)). Create a child Blueprint.
2. Name it **BP_WoodPile**.
3. In **Details**, set **Resource Type** to `Wood`, **Amount Per Harvest** to **10** (or as desired).
4. **Add Component** → **Smart Object**. Assign a Smart Object definition that represents **HarvestWood** (grants 10 wood per harvest). Create the definition if needed (e.g. under SmartObjects: **HarvestWood**, one slot, OnActivated → grant wood to the agent / Mass blackboard).
5. **Save.** Place **BP_WoodPile** instances near PCG trees or in the test area.

---

## Step 3: State Tree BUILD branch — In-depth guide

**T3 / List 60 (CURRENT_TASK_LIST):** This step is the **BUILD branch** implementation. There is no automation API for State Tree graph editing (see [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2); follow the steps below manually in the Editor. **Verification:** Run sequence → [VERTICAL_SLICE_CHECKLIST §3](../../../VisionBoard/VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing); commands → [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (**hw.PlaceWall**, **hw.CompleteBuildOrder**, **hw.SimulateBuildOrderActivation**). Path 1 (simulated) needs no BUILD branch; Path 2 (full agent) requires completing this step then PIE with family agents.

**Targeting:** How agents find and select build orders is defined in [Build-order targeting (family agents)](#build-order-targeting-family-agents--t2--list-60) above (EQS + tag **BuildOrder**, nearest incomplete, optional blackboard). The BUILD branch uses that mechanism to pick an incomplete [AHomeWorldBuildOrder](../../Source/HomeWorld/HomeWorldBuildOrder.h) (e.g. nearest or by BuildDefinitionID).

1. Open **ST_FamilyGatherer** (Content → HomeWorld → AI).
2. Add a **new top-priority branch** (highest in the Selector): **BuildOrder nearby?** → **BUILD**.
   - **Condition:** Use an **EQS** (Environment Query System) query: e.g. “find overlapping actors with tag **BuildOrder** within 500 units” (or “Nearest BuildOrder < 500u”). In the State Tree condition, reference this EQS and require at least one result (or distance < 500).
   - **EQS setup:** Create an EQS asset (Content → AI → Environment Query). Add a test that finds actors overlapping a sphere/capsule, filtered by **Tag = BuildOrder**. Use that query in the State Tree condition.
3. **BUILD tasks** (inside the BUILD state):
   - **MoveTo** the Smart Object slot (of the nearest build order).
   - **Claim** the Smart Object (SO_WallBuilder).
   - **Play** “Haul” montage (or your build montage).
   - **Wait** ~3 seconds (or trigger “Built!” event).
   - **Release** and return (or transition to Idle/Home).
4. **Blackboard (optional):** Add **CurrentJob** (Enum: Gather / Build / Defend) and set it when entering BUILD so other logic can read it.

**EQS for detection:** In the condition, use an EQS query that returns overlapping actors with tag **BuildOrder**; the State Tree checks that the query succeeded (e.g. result count > 0 or distance valid).

---

## Step 4: Mass processor for resources — In-depth guide

1. **MEC_FamilyGatherer:** Open the config. Add traits **MassEntityPersistent** (if available) and **MassNavigationZones** (if needed) so agents can persist and use zones.
2. **MP_WoodInventory (Mass Processor Blueprint):**
   - **Content Browser** → **Right-click** in Mass (or AI) → **Blueprint Class** → search **Mass Processor** (or **Mass → Mass Processor**). Create a Blueprint named **MP_WoodInventory**.
   - In the Blueprint: Add a variable **WoodCount** (Integer), default 0.
   - **On Harvest** (or when the agent completes a HarvestWood Smart Object interaction): **WoodCount += 10** (or use **AmountPerHarvest** from the resource pile).
   - **Requirement for BUILD:** When **WoodCount >= 5** (or your threshold), enable the BUILD branch — e.g. set a blackboard key **CanBuild** (Bool) to true, and in the State Tree the BUILD condition also requires **CanBuild**.
3. **Link:** Open **MEC_FamilyGatherer** → **Processors** (or **Mass Processors**) → **Add** → select **MP_WoodInventory** so it runs and updates WoodCount / blackboard.

---

## Step 5: Spawn and test — In-depth guide

1. **Mass Spawner:** Ensure config is **MEC_FamilyGatherer**, spawn count **8** (or 5–10).
2. **Level:** Place **BP_WoodPile** (e.g. 1–2) near trees or test area. Place **BP_BuildOrder_Wall** (e.g. 2) where you want walls built.
3. **PIE:** Press Play. Expected flow:
   - Agents spawn and gather wood from BP_WoodPile (HarvestWood SO).
   - WoodCount increases (MP_WoodInventory); when >= 5, BUILD branch can run.
   - Agents with BuildOrder nearby and enough wood: **MoveTo** build order SO → **Claim** SO_WallBuilder → play Haul/build anim → **Built!** (final wall spawns, hologram removed).
4. **Verify:** Walls appear after agents complete the build SO; agents return or go idle. Fix any issues (EQS radius, tags, SO slots, or blackboard) and re-test.

---

## Checklist

- [ ] Prerequisite: Task 5 (Family agents) Steps 1–4 done.
- [ ] Building assets: modular meshes converted to Construction Mesh; BP_BuildOrder_Wall created from AHomeWorldBuildOrder, mesh + overlap + tag BuildOrder.
- [ ] SO_WallBuilder: interaction BuildWall, 2 slots; OnActivated = spawn wall + anim, OnDeactivated = destroy hologram; SO component added to BP_BuildOrder_Wall.
- [ ] BP_WoodPile: from AHomeWorldResourcePile, HarvestWood SO, AmountPerHarvest 10; placed in level.
- [ ] ST_FamilyGatherer: BUILD branch added (top priority), EQS condition (BuildOrder < 500u), tasks MoveTo → Claim SO → Haul → Built.
- [ ] MP_WoodInventory: WoodCount, on Harvest +10, WoodCount >= 5 enables BUILD; linked to MEC.
- [ ] PIE: agents gather wood, then build walls when build orders are nearby; commit e.g. `feat(week2): agentic building — Smart Objects + State Tree BUILD`.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| Agents ignore build orders | EQS radius (e.g. 500–1000u); actor tag **BuildOrder** on BP_BuildOrder_Wall; BUILD branch is top priority. |
| No build anim | Assign Haul/build montage in BUILD tasks; retarget if using Paragon. |
| Smart Object stuck | Add timeout (e.g. 10s) in SO or State Tree; ensure slots and bounds allow claim. |
| Wood not counting | MP_WoodInventory linked to MEC; Harvest SO triggers the processor or sets blackboard; BUILD condition requires WoodCount >= 5 (or CanBuild). |

---

## Success criteria

- [ ] Agents build walls autonomously after player places holograms (or pre-placed build orders).
- [ ] Commit e.g. `feat(week2): agentic building — Smart Objects + State Tree BUILD`.

---

## References

- Epic Smart Objects + Mass tutorials.
- [BuildPlacementSupport](../../Source/HomeWorld/BuildPlacementSupport.h) (GetPlacementTransform, GetPlacementHit).
- [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) (agent base).
- [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) (`/Game/HomeWorld/Building/`).
- For automation options that do not use MCP or Python, see [ALTERNATIVE_AUTOMATION_OPTIONS.md](../ALTERNATIVE_AUTOMATION_OPTIONS.md).
