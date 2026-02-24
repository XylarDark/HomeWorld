# Task: Fix character orientation while moving

**Goal:** Character faces movement direction when moving.

**Status:** Verify — C++ done (`bOrientRotationToMovement`, `RotationRate`). Manual PIE test needed.

**Latest:** PIE re-run — character spawned (HomeWorldCharacter). Manual WASD test still required for orientation.

---

## Remaining steps

### 1. Test in PIE

1. Play (Alt+P).
2. Move with WASD in different directions.
3. Confirm character turns to face movement direction.

### 2. Fix mesh facing (if needed)

If capsule turns correctly but mesh faces wrong way:
- Open `BP_HomeWorldCharacter`.
- Set **MeshForwardYawOffset**: 90 or -90 if 90° off, 180 if backward, 0 if correct.

---

**Reference:** [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp) — orientation in C++.
