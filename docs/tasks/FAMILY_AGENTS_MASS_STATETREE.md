# Task: Family agents (Mass + State Tree) — Week 2

**Goal:** 5–10 autonomous family agents in the PCG forest: wander → gather → return → defend at night. No paid tools; agentic = needs/time/world-driven. Scales to 100s with UE 5.7 recommended Mass Entity + Mass AI.

**Status:** Not started.

**Prerequisites:** Plugins enabled (see [SETUP.md](../SETUP.md) Week 2 plugins); PCG forest and main map (existing); [UHomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h) for IsNight.

---

## Step 1: Plugins (already in .uproject)

1. **Open Editor** with the HomeWorld project.
2. **Edit → Plugins** (or **Settings → Plugins**).
3. In the search box, type **Mass** and ensure these are **Enabled** (checkmark):
   - **MassEntity**
   - **MassGameplay**
   - **MassAI**
4. Search **StateTree** → enable **StateTree**.
5. Search **ZoneGraph** → enable **ZoneGraph**.
6. Search **SmartObjects** → enable **SmartObjects**.
7. If you enabled any plugin for the first time, **restart the Editor** when prompted.
8. **Validation:** In the Plugins window, confirm Mass, StateTree, ZoneGraph, and SmartObjects show as enabled.

**Ensure content folders exist:** With Editor open, run `execute_python_script("ensure_week2_folders.py")` via MCP (or **Tools → Execute Python Script** → `Content/Python/ensure_week2_folders.py`). This creates `/Game/HomeWorld/Mass/`, `AI/`, `ZoneGraph/`, `SmartObjects/`, `Building/` if missing.

---

## Step 2: First family agent (Mass Entity Config) — In-depth

### 2.1 Create the Mass Entity Config asset

1. **Content Browser:** Navigate to **Content → HomeWorld → Mass** (create the folder via the script above if needed).
2. **Right-click** in the Mass folder → **Miscellaneous → Mass Entity Config** (or **Miscellaneous → Mass → Mass Entity Config** depending on UE version).
3. Name it **MEC_FamilyGatherer** and press Enter. Double-click to open.

### 2.2 Add Mass traits

In the **Details** panel for the config:

1. Find **Traits** (or **Mass Traits**) and click **Add** (or **+**).
2. Add the following traits one by one (search by name if needed):

| Trait | Purpose |
|-------|--------|
| MassAgent | Core agent identity |
| MassMovement | Walk/run movement |
| MassZoneGraphLaneNavigation (or MassNavigation) | Pathfinding on lanes |
| MassRepresentationPoint | Visual representation (mesh) |
| MassStateTree | Decision brain (assign State Tree in next step) |
| MassCrowdFX | Avoidance (optional) |

If a trait name differs in your UE 5.7 build (e.g. **MassNavigation** instead of **MassZoneGraphLaneNavigation**), use the one listed in the **Add** dropdown and document it in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) if relevant.

### 2.3 Assign visual mesh

1. In the config Details, find the **MassRepresentationPoint** (or representation) section.
2. **Static Mesh:** Assign a mesh (e.g. project character mesh, or a simple cube/capsule for testing). Use a mesh from your project (e.g. from `/Game/Man/` or `/Game/HomeWorld/Characters/`).
3. **Scale:** Set to **1.0** (or as needed).

**Save** the asset (Ctrl+S). The agent template is ready.

---

## Step 3: State Tree brain — In-depth

### 3.1 Create the State Tree asset

1. **Content Browser:** Navigate to **Content → HomeWorld → AI**.
2. **Right-click** → **AI → State Tree** (or **Artificial Intelligence → State Tree**).
3. Name it **ST_FamilyGatherer**, save under `/Game/HomeWorld/AI/`. Double-click to open.

### 3.2 Build the decision flow

1. In the State Tree editor, add a **Selector** (or **State Tree Selector**) as the root. The selector evaluates children **top to bottom** and runs the first whose conditions pass.
2. Add the following **states** (or **branches**) as children of the Selector, in this order (top = highest priority):

   - **Night?** → State that runs **Defend** behavior (e.g. MoveTo enemy). Condition: **IsNight** (from blackboard or EQS).
   - **Hungry?** → State that runs **Gather** (e.g. MoveTo Smart Object farm, play gather anim). Condition: **Hunger > threshold** (e.g. 50).
   - **Idle** → State that runs **Wander** (e.g. MoveTo random point in home bounds).
   - **Sleep** → State that runs **Sleep** at a Smart Object (e.g. bed). Condition can be time or blackboard.

3. **Conditions:** For each branch, add a **Condition** that reads from the **Blackboard** or an **EQS** query (e.g. "IsNight", "Hunger", "Nearest Bed").
4. **Tasks:** Inside each state, add **Tasks** such as:
   - **MoveTo** (target: resource, home, or enemy).
   - **PlayAnimMontage** (e.g. gather idle).
   - **Use Smart Object** (claim slot, interact, release).

### 3.3 Blackboard

1. In the State Tree asset, open or create the **Blackboard**.
2. Add variables:
   - **Hunger** (Float, 0–100).
   - **IsNight** (Bool).
   - **HomePos** (Vector).

These will be set by a Mass processor or by game code (e.g. TimeOfDay subsystem).

### 3.4 Link State Tree to Mass config

1. Open **MEC_FamilyGatherer** again.
2. In Details, find **MassStateTree** (or the trait that holds the State Tree reference).
3. Set **State Tree** (or **StateTree asset**) to **ST_FamilyGatherer**.

**Compile** the State Tree (Compile button in toolbar). Fix any errors (missing pins, invalid references).

---

## Step 4: Spawn in PCG forest — In-depth

### 4.1 Place Mass Spawner

1. Open your level (**Main** or test level).
2. **Modes** panel (or **Window → Modes**) → search **Mass Spawner**.
3. Drag **Mass Spawner** into the level (or place from the Modes list).
4. Select the Mass Spawner actor. In **Details:**
   - **Config** (or **Mass Entity Config**): Set to **MEC_FamilyGatherer**.
   - **Spawn count** (or **Count**): Set to **10** (or 5–10 for testing).
   - **Bounds / Spawn area:** Define a box or shape around the home/forest area so agents spawn in the right region.

### 4.2 ZoneGraph (navigation lanes)

1. **Modes** → **ZoneGraph** (or place **ZoneGraph**-related actor if your project uses it).
2. Paint or generate **lanes** (splines or lanes) around the home and forest so agents have paths. Follow Epic’s ZoneGraph docs for your UE version.
3. Ensure the Mass config uses **MassZoneGraphLaneNavigation** (or **MassNavigation**) so agents follow these lanes.

### 4.3 Smart Objects (interactables)

1. **Farm / resource:** Place an actor (e.g. static mesh or blueprint) to represent a farm or resource node. **Right-click** the actor (or add component) → **Add Smart Object** (or add **Smart Object** component). Assign a Smart Object definition (e.g. **Harvestable**). Agents will claim slots and play gather behavior.
2. **Bed / sleep:** Similarly, place a bed proxy and add a Smart Object (e.g. **Bed** or **Sleep**). Point the State Tree Sleep state to this.

### 4.4 PIE test

1. **Play** (Alt+P).
2. Confirm: agents **spawn**, **move** along lanes, **approach** the farm and **play gather** (or idle) anim, and **return** toward home or wander.
3. **Success:** Agents move autonomously without player input.

---

## Step 5: Agentic needs + night defense — In-depth

1. **Blackboard:** Ensure Hunger, IsNight, HomePos are in the State Tree blackboard and are writable (e.g. from a Mass processor).
2. **Needs update:** Either:
   - **(a)** Create a **Mass Processor** Blueprint (Content → Mass → Mass Processor): on Tick, increase **Hunger** over time and broadcast so the State Tree re-evaluates; or
   - **(b)** Use GAS attributes on a representative actor and sync to Mass blackboard (see [STACK_PLAN](../STACK_PLAN.md) Layer 3).
3. **Night defense:** Use [UHomeWorldTimeOfDaySubsystem::GetCurrentPhase()](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h). When phase is **Night**, set **IsNight** in blackboard (or enable an enemy spawner). In the State Tree, the **Night?** branch should then run **Defend** (e.g. MoveTo enemy). Optionally use DaySequence plugin event **NightStart** to trigger updates.

---

## Checklist

- [ ] Plugins: MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects enabled; Editor restarted if needed.
- [ ] `ensure_week2_folders.py` run (Editor open) so Mass/AI/ZoneGraph/SmartObjects/Building paths exist.
- [ ] MEC_FamilyGatherer created in `/Game/HomeWorld/Mass/` with traits and mesh.
- [ ] ST_FamilyGatherer created in `/Game/HomeWorld/AI/` with Selector, Night/Hungry/Idle/Sleep branches, blackboard, and tasks.
- [ ] MEC linked to ST_FamilyGatherer; State Tree compiles.
- [ ] Mass Spawner placed, config = MEC_FamilyGatherer, spawn count 10, bounds set.
- [ ] ZoneGraph lanes and Smart Objects (farm, bed) placed; PIE shows agents spawning and behaving.
- [ ] Needs (Hunger) and night (IsNight) wired so State Tree switches behaviors; PIE test passed.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| Agents not visible | MassRepresentationPoint → Static Mesh assigned; spawn count and bounds correct. |
| Agents stuck / no movement | ZoneGraph lanes cover the area; MassNavigation (or lane navigation) trait added. |
| State Tree errors | Compile State Tree; fix missing blackboard vars or invalid task links. |
| No gather/sleep behavior | Smart Object components and definitions (Harvestable, Bed) present; State Tree tasks reference correct SO. |
| Plugin not found | Use exact plugin names from **Edit → Plugins**; see [SETUP.md](../SETUP.md) Week 2 plugins. |

---

## Integration with HomeWorld

- **IsNight:** From `UHomeWorldTimeOfDaySubsystem::GetCurrentPhase()` (implement with DaySequence in level or C++ when ready).
- **Needs (Week 2):** Extend [UHomeWorldAttributeSet](../../Source/HomeWorld/HomeWorldAttributeSet.h) or add a second attribute set per STACK_PLAN; optional Mass processor to mirror Hunger for agents.

---

## Success criteria

- [ ] 5–10 agents spawn and walk.
- [ ] State Tree switches behaviors (e.g. Hungry → Gather, Night → Defend).
- [ ] ZoneGraph pathing is smooth.
- [ ] PIE test passed; commit e.g. "Week2: Mass Family Agents + StateTree".

---

## References

- Epic: [Your First 60 Minutes with Mass](https://dev.epicgames.com/community/learning/tutorials/JXMl/unreal-engine-your-first-60-minutes-with-mass)
- State Trees + Mass (Epic docs / video)
- ZoneGraph: Epic community tutorials
- [SETUP.md](../SETUP.md) (Week 2 plugins), [STACK_PLAN.md](../STACK_PLAN.md) Layer 5, [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md)
- For automation options that do not use MCP or Python, see [ALTERNATIVE_AUTOMATION_OPTIONS.md](../ALTERNATIVE_AUTOMATION_OPTIONS.md).

---

## Next: Agentic building

After gather/defend/wander and Smart Objects for gather/sleep are working, add the **BUILD** branch and resource inventory: [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md). Uses C++ bases [AHomeWorldBuildOrder](../../Source/HomeWorld/HomeWorldBuildOrder.h) and [AHomeWorldResourcePile](../../Source/HomeWorld/HomeWorldResourcePile.h); player places build-order holograms via [UBuildPlacementSupport](../../Source/HomeWorld/BuildPlacementSupport.h).
