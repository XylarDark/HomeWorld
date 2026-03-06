# Task: Agentic building (Mass + Smart Objects) — Week 2

**Goal:** Family agents autonomously build home structures (walls, farms, beds) from player-placed build orders. Player places a hologram (build order) using the existing placement API; agents detect it, gather resources, claim Smart Object, and complete the build.

**Status:** Not started.

**Prerequisite:** [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Steps 1–4 done (plugins, MEC_FamilyGatherer, ST_FamilyGatherer, spawner, ZoneGraph, Smart Objects for gather/sleep).

**Player placement:** Use existing [UBuildPlacementSupport::GetPlacementTransform](../../Source/HomeWorld/BuildPlacementSupport.cpp) (and GetPlacementHit) from a Blueprint or input handler to place build-order actors at the trace result (hologram preview).

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
