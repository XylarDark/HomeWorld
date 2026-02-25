# Task: Fix character orientation while moving

**Goal:** Character faces movement direction when moving.

**Status:** Completed — C++ done; mesh offset -90 applied and verified in PIE.

**Latest:** Mesh forward yaw offset default set to -90 in C++ ([HomeWorldCharacter.h](../../Source/HomeWorld/HomeWorldCharacter.h)); character and mesh face movement direction (WASD and diagonals) verified.

---

## What is already done (C++)

- In [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp), the Character Movement Component is configured so the pawn rotates toward movement:
  - **Orient Rotation to Movement** is enabled (or equivalent).
  - **Rotation Rate** is set so the turn feels responsive.
- **Mesh forward yaw offset** default is -90° in C++ ([HomeWorldCharacter.h](../../Source/HomeWorld/HomeWorldCharacter.h)) so the skeletal mesh faces the movement direction (skeleton forward was 90° right of capsule forward).
- No further code changes required unless you want to tune rotation speed or disable orientation in certain states.

---

## In-depth guide: Test orientation in PIE

1. **Open the level**  
   Open **Main** (or your test level): **Content → HomeWorld → Maps → Main**.

2. **Play**  
   Press **Alt+P** (or click **Play**). Wait for the level to load and the character to spawn.

3. **Move in multiple directions**  
   - Press **W** (forward), **S** (back), **A** (left), **D** (right).  
   - Use combinations (e.g. W+A) and move in circles.  
   - Confirm the **capsule/pawn** rotates so the character **faces the direction of movement**.

4. **Interpret the result**  
   - **Capsule turns correctly and mesh faces the same way:** Orientation is correct; task verified.  
   - **Capsule turns but mesh faces wrong way (e.g. 90° or 180° off):** Use the mesh offset fix below.  
   - **Capsule does not turn with movement:** Check that the Blueprint uses the C++ character class and that Character Movement → **Orient Rotation to Movement** is true (can be set in C++ or Blueprint).

---

## In-depth guide: Fix mesh facing (if needed)

If the capsule rotates correctly but the **skeletal mesh** faces the wrong direction (e.g. sideways or backward), adjust the mesh forward offset on the character Blueprint.

1. **Open the character Blueprint**  
   **Content Browser → HomeWorld → Characters → BP_HomeWorldCharacter** → double-click to open.

2. **Select the mesh component**  
   In the **Components** panel, select the **mesh** component (often named **Mesh** or **CharacterMesh0** — the one that has the Skeletal Mesh asset).

3. **Set Mesh Forward Yaw Offset**  
   In the **Details** panel, find **Transform** or **Rendering** (or search for "Forward").  
   - **Mesh Forward Yaw Offset** (or similar):  
     - **0**: Mesh forward matches capsule forward (default).  
     - **90** or **-90**: Mesh is rotated 90° (use if the artist’s forward is along the side).  
     - **180**: Mesh faces backward relative to capsule.

4. **Save and retest**  
   **Save** (Ctrl+S), then run PIE again and move with WASD. Repeat until the mesh faces movement direction.

---

## Checklist

- [x] PIE: Move with WASD in several directions.
- [x] Confirmed capsule (and mesh) face movement direction (mesh offset -90 in C++).
- [x] Mesh facing corrected via default `MeshForwardYawOffset = -90` in C++; override in BP_HomeWorldCharacter if needed for other characters.

---

## Reference

- Orientation and movement in [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp).
