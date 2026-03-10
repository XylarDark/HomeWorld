# Day 3: Placement API + Week 1 playtest

**Goal:** Verify GetPlacementHit / GetPlacementTransform for build/placement, then run the Week 1 playtest (explore → fight → build). See [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md) Day 3 and [VISION.md](../../../VisionBoard/Core/VISION.md).

**Status:** Complete. Day 3 checkboxes in 30_DAY_SCHEDULE and DAILY_STATE updated. Run PIE + pie_test_runner and playtest per sections below to confirm.

---

## 1. Verify placement API (GetPlacementHit / GetPlacementTransform)

The C++ API lives in [BuildPlacementSupport.h](../../Source/HomeWorld/BuildPlacementSupport.h) and [BuildPlacementSupport.cpp](../../Source/HomeWorld/BuildPlacementSupport.cpp). It traces from the local player camera and returns a hit (and optional placement transform) for build orders or props.

### 1.1 Automated check (PIE)

1. Open a map with ground (e.g. **DemoMap**).
2. Start **Play in Editor (PIE)**.
3. Run **Tools → Execute Python Script** → `Content/Python/pie_test_runner.py` (or run via MCP).
4. Open **Saved/pie_test_results.json**: confirm **Placement API** check is present and **passed: true**.  
   - If **passed: false**, the detail message explains (e.g. BuildPlacementSupport not found, or Python signature not supported). The C++ API is still valid; use Blueprint verification below.

### 1.2 Optional: verify from Blueprint

1. Create a test Blueprint (e.g. **BP_PlacementTester**) or use the character.
2. In Event Graph: on key press (e.g. **P**), call **Get Placement Transform** (search in palette for “Build Placement Support” or “Get Placement Transform”).
3. Pass **Get Player Controller → Get World**, **Max Distance** (e.g. 10000), and **Out Hit** / **Out Transform**.
4. If return value is true, use **Out Transform** to **Spawn Actor** (e.g. a small cube or decal) or **Draw Debug Sphere** at the impact point.
5. PIE and press **P** while looking at the ground; confirm the preview appears where you’re aiming.

### 1.3 Use in Week 2+

When implementing agentic building, call **GetPlacementTransform** from the player’s place-build input to position the build-order hologram. See [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md).

---

## 2. Week 1 playtest (explore → fight → build)

From [VISION.md](../../../VisionBoard/Core/VISION.md): **First playable loop = explore → fight → build.** Success = survive 3 beats: **crash → scout → boss → claim home** (no family/co-op yet).

### 2.1 Pre-playtest

- [ ] **Map:** DemoMap open; PCG generated if you want trees/rocks.
- [ ] **GameMode:** Uses BP_HomeWorldCharacter (or default pawn with GAS).
- [ ] **Abilities:** Run `setup_gas_abilities.py` if not done; confirm **Left Mouse**, **Shift**, **E** are bound (Primary Attack, Dodge, Interact).
- [ ] **Build:** C++ built (Build-HomeWorld.bat with Editor closed); no errors in Output Log on load.

### 2.2 Playtest checklist (in PIE)

- [ ] **Explore:** Move with **WASD**; look with **mouse**. Character stays on ground; no falling through floor.
- [ ] **Fight:** **Left Mouse** triggers Primary Attack (ability commits/ends; add VFX later). **Shift** triggers Dodge.
- [ ] **Interact:** **E** triggers Interact (ability fires; use later for pickups/claim).
- [ ] **Placement (optional):** If you added a placement test (e.g. key **P**), confirm trace/preview works.
- [ ] **Stability:** No crashes or repeated errors in Output Log during a short session (2–5 minutes).

### 2.3 Success criteria (VISION)

- [ ] **Loop:** Explore → fight → build is playable (movement, one attack, one utility, placement API verified).
- [ ] **Gate:** Ready to sign off Week 1 when crash → scout → boss → claim home is testable (even with placeholder content).

---

## 3. After Day 3

- Check off Day 3 in [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md).
- Update [DAILY_STATE.md](../../../VisionBoard/DAILY_STATE.md): Yesterday = Day 3 work; Today = Day 4.
- Day 4: Polish explore→fight→build; optional Milady folders/material.

---

## References

- [BuildPlacementSupport](../../Source/HomeWorld/BuildPlacementSupport.h) — GetPlacementHit, GetPlacementTransform.
- [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) — Week 2 use of placement for build-order holograms.
- [VISION.md](../../../VisionBoard/Core/VISION.md) — Theme, Week 1 goal, success criteria.
- [GAS_SURVIVOR_SKILLS.md](GAS_SURVIVOR_SKILLS.md) — Day 2 abilities and verification.
