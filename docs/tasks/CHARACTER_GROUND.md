# Task: Character touching the ground

**Goal:** Character stands on ground (no floating or sinking).

**Status:** Completed — PIE check passed (MOVE_WALKING, not falling, capsule 42r/88h). Task closed.

**Latest:** Character on ground verified (capsule 88/42, MOVE_WALKING). Spawn ground trace in BeginPlay places capsule on hit; no floating or sinking. Walk on varied terrain / ground surface is a separate concern, deferred to later.

---

## Optional: In-depth verification

If you want to double-check or document ground contact:

1. **PIE:** Press Alt+P, spawn in the level.
2. **Check movement mode:** In **Output Log** (or via `pie_test_runner.py`), the character’s movement state should be **MOVE_WALKING** (not MOVE_Falling) when on flat ground.
3. **Capsule:** Default capsule (e.g. radius 42, height 88) should sit on the landscape/floor without visible gap or sink.
4. **Varied terrain:** Walk up/down slopes and over bumps; character should stay on the surface. If you see floating or clipping, adjust capsule size or collision in **BP_HomeWorldCharacter** or C++.

---

## Reference

Capsule, collision, and ground trace in [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp).
