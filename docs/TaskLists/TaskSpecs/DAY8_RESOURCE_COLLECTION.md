# Day 8 [1.3]: Resource collection loop (player harvest)

**Goal:** When the player presses Interact (E) in front of a resource pile (e.g. BP_HarvestableTree), grant Wood (or other resource) to the existing inventory subsystem. GA_Interact remains the trigger; C++ provides trace + harvest; Blueprint invokes it. See [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md) Day 8.

**Status:** C++ implemented. **Option A** (reparent GA_Interact to C++ ability) is the project default—no Blueprint graph. Option B (wire the Blueprint graph) only if you need to keep the Blueprint parent as Home World Gameplay Ability.

---

## 1. Prerequisites

- [ ] Day 7 done: BP_HarvestableTree (or equivalent) placed on DemoMap with **Resource Type** = Wood and **Amount Per Harvest** set. See [DAY7_RESOURCE_NODES.md](DAY7_RESOURCE_NODES.md).
- [ ] C++ built (close Editor or disable Live Coding, run `Build-HomeWorld.bat`).

---

## 2. Implementation (what’s done)

### 2.1 C++ — Character harvest helper

- **`AHomeWorldCharacter::TryHarvestInFront()`** (BlueprintCallable, category "Interaction", display name "Try Harvest In Front"):
  - Runs a **line trace** forward from the character (~280 cm) using control rotation.
  - If the hit actor is `AHomeWorldResourcePile`, reads `ResourceType` and `AmountPerHarvest`.
  - Gets `UHomeWorldInventorySubsystem` from the game instance and calls **`AddResource(ResourceType, AmountPerHarvest)`**.
  - Returns **true** if harvest succeeded, **false** otherwise (no hit or not a resource pile).
  - **Log:** On success, logs `"HomeWorld: Harvest succeeded - <ResourceType> +<Amount>"` to Output Log.
- **Stub behavior:** Does **not** deplete or destroy the pile (infinite harvest per node); depletion can be added later.

### 2.2 GA_Interact — Harvest in C++ (Option A, recommended)

A C++ ability class **HomeWorldInteractAbility** does the harvest in `ActivateAbility` (get avatar → cast to character → `TryHarvestInFront()` → `EndAbility`). No Blueprint graph wiring needed.

**Steps:**

1. **Build C++** (Editor closed or Live Coding off): run **`Build-HomeWorld.bat`**.
2. **Open the Editor**, then run **`Content/Python/reparent_ga_interact_to_cpp.py`** (Tools → Execute Python Script or MCP `execute_python_script("reparent_ga_interact_to_cpp.py")`). The script reparents **GA_Interact** to **Home World Interact Ability**.
3. If the script reports that reparenting isn’t available, do it once by hand: open **GA_Interact** → **Class Settings** (toolbar) → **Parent Class** → choose **Home World Interact Ability** → **Compile** and **Save**.

After that, E (Interact) will run the C++ harvest logic when a resource pile is in front of the character.

### 2.3 GA_Interact — Blueprint wiring (Option B)

If you prefer to keep GA_Interact parented to **Home World Gameplay Ability** and implement harvest in the Blueprint graph, follow the detailed tutorial below.

---

#### Step-by-step checklist (quick reference)

1. Open **GA_Interact** → **Open Full Blueprint Editor** if needed → **Event Graph**.
2. From **Event ActivateAbility**’s **D** (execution) pin, drag a wire.
3. From **Event ActivateAbility**’s **Actor Info** pin, drag → add **Break GameplayAbilityActorInfo** (or “Break … Actor Info”) → use **Avatar Actor** out.
4. From **Avatar Actor**, drag → add **Cast to Home World Character** → plug Avatar Actor into **Object**.
5. From **Cast Succeeded** (execution), drag → add **Try Harvest In Front** → plug **As Home World Character** into the node’s **Target** (if it has one).
6. From **Try Harvest In Front**’s **Return Value**, drag → add **Branch**. Connect **Try Harvest In Front**’s execution out → **Branch**’s execution in.
7. From **Branch**’s **True** pin → add **End Ability** → wire **Handle**, **Actor Info**, **Activation Info** from **Event ActivateAbility** → set **bWas Cancelled** = false.
8. From **Branch**’s **False** pin → add **End Ability** again → same wires from **Event ActivateAbility** → set **bWas Cancelled** = true.
9. Connect **Event ActivateAbility**’s **D** pin into the **Break** node’s execution input (so the chain runs when the ability activates). Then **Compile** and **Save**.

---

#### Detailed tutorial: Wiring GA_Interact for harvest

*Uses the exact names shown in the GA_Interact Event Graph (parent: **Home World Gameplay Ability**).*

**1. Open the Blueprint graph**

- In **Content Browser**, go to **Content → HomeWorld → Abilities** and double‑click **GA_Interact**.
- If you only see the **Details** panel (Tags, Input, Costs, etc.) and a note about “data only blueprint,” click the blue link **“Open Full Blueprint Editor”** at the top of that note.
- In the full editor, open the **Event Graph** (e.g. under **GRAPHS** in the **My Blueprint** panel on the left). You should see **Event ActivateAbility** and **Event OnEndAbility**. We only use **Event ActivateAbility**; ignore **Event OnEndAbility** for this task.

**2. Start from Event ActivateAbility**

- Locate the red **Event ActivateAbility** node in the graph (the one that runs when the ability is activated).
- It has an execution output pin (often labeled **D**). Drag from that **D** pin to start the chain. You will attach the rest of the logic to this execution line.
- The same node should have data output pins such as **Handle**, **Actor Info**, **Activation Info**. We will use these later when we call **End Ability**.

**3. Get the Avatar Actor (the character)**

- From the **Actor Info** output pin of **Event ActivateAbility**, drag a wire and release.
- In the search box type **Break** and look for a node that breaks the actor info struct (e.g. **Break GameplayAbilityActorInfo** or **Break Gameplay Ability Actor Info**). Add it.
- That Break node exposes an **Avatar Actor** (or **Owner Actor**) output. That is the pawn/character that has the ability—use **Avatar Actor**.

**4. Cast to Home World Character**

- Drag from the **Avatar Actor** pin and release. Search for **Cast to** and add **Cast to Home World Character** (or **Cast to HomeWorldCharacter**).
- Plug **Avatar Actor** into the Cast node’s **Object** input.
- The Cast node has two execution outputs: **Cast Failed** and **Cast Succeeded**. We only continue on **Cast Succeeded** (so we only harvest when the avatar is our character).

**5. Call Try Harvest In Front**

- Drag from the **Cast Succeeded** execution pin to create a new node. Search **Try Harvest In Front** and add that function.
- The **Try Harvest In Front** node needs a **Target** (the character). Connect the **As Home World Character** (or **As HomeWorld Character**) output from the Cast node to the **Target** (or self) input of **Try Harvest In Front**. If the node has no separate Target pin, it may use the context from the Cast.
- **Try Harvest In Front** returns a **Boolean** (**Return Value**). Connect the **Cast Succeeded** execution pin into **Try Harvest In Front**, and use its **Return Value** for the next step.

**6. Branch on success or failure**

- Drag from the **Return Value** pin of **Try Harvest In Front** and add a **Branch** node.
- Connect the execution output of **Try Harvest In Front** to the execution input of **Branch**.
- **Branch** has two execution outputs: **True** (harvest succeeded) and **False** (no resource pile in front or cast failed).

**7. Call End Ability in both branches**

- You must call **End Ability** in both the **True** and **False** branches so the ability always ends.
- From the **True** pin of the Branch, drag and search **End Ability**. Add the **End Ability** node. It needs **Handle**, **Actor Info**, **Activation Info**, **bReplicate End Ability**, and **bWas Cancelled**. Wire **Handle**, **Actor Info**, and **Activation Info** from **Event ActivateAbility** into this **End Ability**. Set **bReplicate End Ability** to **false** and **bWas Cancelled** to **false** (successful harvest).
- From the **False** pin of the Branch, add a **second End Ability** node. Again wire **Handle**, **Actor Info**, and **Activation Info** from **Event ActivateAbility**. Set **bReplicate End Ability** to **false** and **bWas Cancelled** to **true** (no harvest / cancelled).

**8. Optional: Commit Ability first**

- If you want to use cost/commit (e.g. for later): from the **D** pin of **Event ActivateAbility**, add **Commit Ability**, then on **Commit Succeeded** do the chain (Break Actor Info → Cast → Try Harvest In Front → Branch → End Ability). On **Commit Failed**, call **End Ability** with **bWas Cancelled** = true. For harvest-only with no cost, you can skip this and go straight from **Event ActivateAbility** to the Break node.

**9. Compile and save**

- Click **Compile** in the Blueprint toolbar and fix any red pins or errors.
- **Save** the Blueprint (Ctrl+S or File → Save).

**Summary flow:**  
**Event ActivateAbility** (pin **D**) → Break Actor Info → **Avatar Actor** → **Cast to Home World Character** (**Cast Succeeded**) → **Try Harvest In Front** → **Branch** → **End Ability** on **True** (bWas Cancelled = false) and **End Ability** on **False** (bWas Cancelled = true).

No change to the GA_Interact parent class or input binding (E key, InteractAbilityClass) is required.

---

## 3. Validation and testing

### Test procedure (Option A — C++ ability)

1. **Build C++** — Close the Editor (or disable Live Coding). Run **`Build-HomeWorld.bat`** and wait until it finishes (check `Build-HomeWorld.log` for "Exit code: 0" or completion). Exit code 6 usually means the Editor had Live Coding active; close Editor and build again.
2. **Open the project** in the Editor.
3. **Reparent GA_Interact** — Run **`Content/Python/reparent_ga_interact_to_cpp.py`** (Tools → Execute Python Script or MCP). Confirm in Output Log: "Reparented GA_Interact to HomeWorldInteractAbility" or "already parented."
4. **PIE on DemoMap** — Play in Editor on DemoMap. Move the character close to a harvestable tree (BP_HarvestableTree or PCG-spawned harvestable).
5. **Press E (Interact)** while facing the tree. In **Output Log** (Window → Developer Tools → Output Log), filter or scroll for: **`HomeWorld: Harvest succeeded - Wood +10`** (or your Amount Per Harvest).
6. **Optional:** Press E multiple times; each press should log another harvest (infinite harvest stub). Move away and press E; no log line (no pile in trace).

### Success criteria

- **Log-driven:** At least one line `HomeWorld: Harvest succeeded - Wood +10` (or your Amount Per Harvest) when pressing E in front of a resource pile.
- **No regression:** Movement, look, and other abilities (Left Mouse, Shift) still work in PIE.

---

## 4. After Day 8

- [ ] **30_DAY_SCHEDULE:** Day 8 [1.3] item marked [x] when validation passes.
- [ ] **DAILY_STATE:** Yesterday = Day 8 resource collection; Today = Day 9 (1.4); Current day = 9.
- [ ] **SESSION_LOG:** Short entry for Day 8 (TryHarvestInFront, GA_Interact wired, PIE validated).

**Future enhancements (out of scope for this stub):**

- Depleting or destroying the pile after harvest (infinite harvest is acceptable for Day 8).
- GAS attribute “Wood” (schedule allows inventory or attribute; we use inventory subsystem).
- Harvest animation/montage in GA_Interact.
- UI showing wood count.
