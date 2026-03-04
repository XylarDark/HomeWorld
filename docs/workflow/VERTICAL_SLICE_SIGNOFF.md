# Vertical slice sign-off

**Purpose:** Written sign-off that the vertical slice is showable (CURRENT_TASK_LIST T4/T6). Satisfies demo-recording-or-sign-off success criteria when a 1–3 min demo recording is not produced. See [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 (pre-demo) and §4 (recording steps).

**Date:** 2026-03-05 (T4 fourth list sign-off)

**T6 (sixth list) sign-off:** 2026-03-05 — Slice remains showable; T1–T5 (sixth list) completed (vertical slice re-check, PIE validation, agentic building verify, SaveGame persistence, Act 2 Defend). No demo clip recorded; this written sign-off satisfies T6. Linked from [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4 and [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).

**T7 (eighth list) sign-off:** 2026-03-05 — Vertical slice sign-off or 1–3 min demo (CURRENT_TASK_LIST T7). Slice is showable per sign-off summary below; no demo clip recorded. This written sign-off satisfies T7. Linked from [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4 and [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md).

---

## Sign-off summary

The HomeWorld vertical slice is **showable** with the following elements:

1. **Establish corner:** Homestead compound (DemoMap or Homestead) — placed buildings, resource nodes, PCG trees; viewport spot-check confirms no critical LOD/lighting issues. Locked in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
2. **Play moment:** Claim homestead — player places first home asset with key **P** (Place) after exploring/harvesting; placement API and GA_Place verified via pre-demo checklist and `pie_test_runner.py`. Locked in PROTOTYPE_SCOPE.
3. **Optional scope:** Planetoid (portal from DemoMap → Planetoid_Pride) and dungeon (AHomeWorldDungeonEntrance overlap → level load) are implemented; scripts and triggers in place per [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 16 and Day 24.

Pre-demo checklist (§3) items are satisfied: level open + PCG generated, character with GAS (LMB, Shift, E, P), moment and corner verified per T1/T5 CURRENT_TASK_LIST verification. Stability (PIE 2–5 min) is documented in the checklist.

**Recording (optional):** To capture a 1–3 min demo, follow [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4: open DemoMap, PIE, establish corner shot, play moment (harvest then place with P), optionally cut to planetoid/dungeon.

---

**See also:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) T6.
