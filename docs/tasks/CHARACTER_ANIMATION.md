# Task: Fix character animation

**Goal:** Character plays idle when still, walk/run when moving.

**Status:** ✓ Completed (this round of requirements).

**Latest:** AnimGraph Locomotion state machine (Idle/WalkRun driven by Speed from C++), compile/save, and PIE verification done. Character plays idle when still and walk/run when moving.

---

## What you can run (before manual steps)

1. **Rebuild C++ (if needed)**  
   If you pulled new C++ or haven't built since adding `HomeWorldAnimInstance`:
   - Close Editor, run `Build-HomeWorld.bat`, reopen.

2. **Create/update AnimBP (script)**  
   With Editor open and MCP connected:
   - Run: `execute_python_script("setup_animation_blueprint.py")`  
   Or: **Tools → Execute Python Script** → select `Content/Python/setup_animation_blueprint.py`.  
   This creates or reuses `ABP_HomeWorldCharacter` at `/Game/HomeWorld/Characters/` with C++ parent `UHomeWorldAnimInstance`. **(Done 2026-02-24 with Editor open.)**

---

## In-depth guide: Populate AnimGraph (manual)

The AnimGraph visual editor cannot be driven by Python/MCP; follow these steps in the Editor.

### 1. Open the Animation Blueprint

- **Content Browser:** Navigate to **Content → HomeWorld → Characters**.
- Double-click **ABP_HomeWorldCharacter** (or right-click → Open).
- The Animation Blueprint editor opens with **EventGraph**, **AnimGraph**, and **Designer** tabs.

### 2. Switch to AnimGraph

- Click the **AnimGraph** tab.
- You should see an empty graph or an existing state machine. We will add a **State Machine** named **Locomotion** that drives the final pose.

### 3. Add the Locomotion state machine

- In the **AnimGraph** palette (left or right panel), find **State Machine** (under "State Machines" or "Animation").
- Drag **State Machine** onto the graph.
- In the **Details** panel, set **Name** to `Locomotion`.
- Connect the **Locomotion** node’s output to **Output Pose** (if there is an existing "Output" node).

### 4. Open the state machine and add states

- Double-click the **Locomotion** state machine node to open it.
- You should see an **Entry** state and an empty graph.

**Add Idle state:**

- Right-click in the graph → **Add State** → name it `Idle`.
- Double-click **Idle** to enter it.
- In the state’s graph, add an **Animation** node: drag **Play Animation** or **Sequence Player** from the palette.
- Set the animation to your idle sequence, e.g. **ThirdPersonIdle** from `/Game/Man/Demo/Animations/` (or whatever your project uses; see [CONTENT_LAYOUT](../CONTENT_LAYOUT.md) for character paths).
- Connect the animation output to the state’s **Output** pose.
- Return to the state machine (back arrow or double-click the Locomotion node again).

**Add Walk/Run state:**

- Right-click → **Add State** → name it `WalkRun`.
- Double-click **WalkRun**, add a **Sequence Player** (or **Play Animation**) and assign **ThirdPersonRun** (or **ThirdPersonWalk**).
- Connect to **Output** pose, then return to the state machine.

### 5. Set Idle as default and add transitions

- **Default state:** Click **Entry** and in Details set the default state to **Idle**, or drag a transition from **Entry** to **Idle** so Idle is the first state.
- **Idle → WalkRun:** Right-click between Idle and WalkRun → **Add Transition** (or drag from Idle to WalkRun).
  - Double-click the transition. In the transition graph, add a **Condition**: use the **Speed** variable (from the C++ parent `UHomeWorldAnimInstance`).
  - Condition: **Speed > 10** (or a small threshold, e.g. 1.0 if Speed is normalized). So: when Speed is above threshold, transition to WalkRun.
- **WalkRun → Idle:** Add transition from WalkRun back to Idle.
  - Condition: **Speed <= 10** (or **Speed < 10**). When Speed is below threshold, transition to Idle.

**How to get Speed in the transition graph:**

- **If Speed appears in the Variables list:** In the **My Blueprint** panel (left), under **Variables** or the **Locomotion** category, you should see **Speed**. Drag it into the transition graph.
- **If Speed is not listed:** Right-click in the transition graph → in the search box type **Speed**. Choose **Get Speed** (or the **Speed** property pin). Connect it to a **Greater** (float) or **Less** node and compare to **10** (or your threshold). The getter is available because the AnimBP’s parent is `UHomeWorldAnimInstance`; if you don’t see it, see **Troubleshooting** below.

**Troubleshooting: Speed not in the variables list**

Speed comes from the C++ parent class `UHomeWorldAnimInstance`. If it doesn’t appear:

1. **Reparent the AnimBP** so its parent is the C++ class: run `setup_animation_blueprint.py` again (via MCP: `execute_python_script("setup_animation_blueprint.py")` or **Tools → Execute Python Script**). The script now reparents an existing ABP to `UHomeWorldAnimInstance` when needed. Then close and reopen **ABP_HomeWorldCharacter**.
2. **Or reparent manually:** Open **ABP_HomeWorldCharacter** → **Class Settings** (toolbar) → set **Parent Class** to **HomeWorldAnimInstance**. Compile and save.
3. **Use the graph search:** In the transition graph, right-click and search for **Speed**; use **Get Speed** (or the Speed pin) even if it doesn’t show in the Variables panel.
4. **Confirm C++ is built:** If you added or changed `HomeWorldAnimInstance`, close the Editor, run `Build-HomeWorld.bat`, then reopen the project.

### 6. Compile and save

- Click **Compile** in the toolbar.
- Fix any errors (e.g. missing animation assets; point to the correct path in `/Game/Man/` or your character folder).
- **Save** (Ctrl+S).

### 7. Ensure character uses this AnimBP

- Open **BP_HomeWorldCharacter** (Content → HomeWorld → Characters).
- In **Details**, under the mesh or **Animation** category, set **Anim Class** to **ABP_HomeWorldCharacter**.
- Save.

---

## In-depth guide: Test in PIE

1. **Play:** Press **Alt+P** (or click Play).
2. **Stand still:** Character should play **Idle**.
3. **Move (WASD):** Character should transition to **Walk/Run**.
4. **Stop:** Character should return to **Idle**.

If the character never moves to Walk/Run, check: (a) **Speed** is updated in C++ (`UHomeWorldAnimInstance::NativeUpdateAnimation`), (b) transition threshold (e.g. 10) matches your movement speed range, (c) Anim Class on the pawn is set to ABP_HomeWorldCharacter.

---

## Checklist

- [x] C++ built (if needed); `setup_animation_blueprint.py` run (MCP or Tools → Execute Python Script).
- [x] ABP_HomeWorldCharacter opened; AnimGraph tab.
- [x] State Machine **Locomotion** added and connected to Output Pose.
- [x] States **Idle** and **WalkRun** added with correct animations (e.g. ThirdPersonIdle, ThirdPersonRun).
- [x] Transitions: Idle → WalkRun when Speed > threshold; WalkRun → Idle when Speed <= threshold.
- [x] Compile and Save; BP_HomeWorldCharacter Anim Class = ABP_HomeWorldCharacter.
- [x] PIE: idle when still, walk/run when moving.

---

## Reference

- **C++:** `UHomeWorldAnimInstance` exposes **Speed**, **bIsInAir**, **bIsMoving**. See [HomeWorldAnimInstance.h](../../Source/HomeWorld/HomeWorldAnimInstance.h). The class is `Blueprintable` so the ABP can use it as parent; if the ABP was created with the default `AnimInstance` parent, re-run `setup_animation_blueprint.py` to reparent and make Speed visible.
- **Animations:** Typically in `/Game/Man/Demo/Animations/` (e.g. ThirdPersonIdle, ThirdPersonWalk, ThirdPersonRun). See [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) and `Content/Python/character_blueprint_config.json`.
