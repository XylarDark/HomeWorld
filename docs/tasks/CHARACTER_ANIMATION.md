# Task: Fix character animation

**Goal:** Character plays idle when still, walk/run when moving.

**Status:** In progress — C++ and AnimBP asset done. AnimGraph state machine needs manual setup.

**Latest:** PIE re-run — character spawns; mesh/AnimInstance not reported by Python in PIE (possible reflection quirk). Manual AnimGraph + PIE test still required.

---

## Remaining steps

### 1. Rebuild C++ (if needed)

If you pulled new C++ or haven't built since adding `HomeWorldAnimInstance`:
- Close Editor, run `Build-HomeWorld.bat`, reopen.
- Via MCP: `execute_python_script("setup_animation_blueprint.py")` to set C++ parent on AnimBP.

### 2. Populate AnimGraph (manual)

1. Open `ABP_HomeWorldCharacter` (Content → `/Game/HomeWorld/Characters/`).
2. AnimGraph tab → Add State Machine → name `Locomotion`.
3. Add states: **Idle** (`ThirdPersonIdle`), **Walk/Run** (`ThirdPersonRun`).
4. Transitions: Idle→Walk when `Speed > 10`, Walk→Idle when `Speed < 10` (use `Speed` from C++ parent).
5. Set Idle as default, connect to Output Pose, compile and save.

### 3. Test in PIE

Play (Alt+P), move with WASD. Idle when still, walk/run when moving.

---

**Reference:** `UHomeWorldAnimInstance` exposes `Speed`, `bIsInAir`, `bIsMoving`. Animations in `/Game/Man/Demo/Animations/`.

**Bare-bones stack (Week 1):** Animation/orientation is part of core tech completion: run `setup_animation_blueprint.py` (via MCP or Editor), then manual AnimGraph + PIE per steps above.
