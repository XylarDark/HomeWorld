# T0 ordered execution queue — 2026-10-07 re-pass

Built from `T0_EXECUTION_PHASES.md` + `T0_PROTOTYPE_TRACK.md` under the
SESSION_START track sizing. In order. Owner column: who must act.

## A. Agent-owned, unblocked now

1. **`T0_M9` hardening** — ✅ DONE (already merged): `HomeWorldFormGateTests.cpp` carries the four M9 behaviour tests, added in `790bbd5` ("the P0 form law is executable, and proven able to fail"). Queue doc row was stale; no further work.
2. **Phase 5.3 — Tending** — dung by day, soil at night (V2b). Done-when:
   garden bed state changes on a spirit-form night.
   ⚠️ Parked pending Lead design: V2b is a vision statement, not a design
   packet. No garden-bed state machine, dung/soil actors, or slot marks exist
   in Source. Inventing one is a Lead call, not an agent task.
3. **Phase 5.1 — Companion NPC hint** — one-line contextual hint (Q19).
   Done-when: state-appropriate line, no dialogue tree.
   ⚠️ Same shape: no design packet or actor exists. Lower priority than the
   mechanical beats above.
4. **`T0_M7` rune unlock gap** — ✅ DONE 2026-10-07: dedicated
   `HomeWorld.T0.M7.RuneUnlockGrantsNoSpiritAlone` added to
   `HomeWorldDayGateTests.cpp` — day+body unlock sets the latch, unlock alone
   never grants spirit (Anti row), and rune+bed is the only route to spirit.
   `HomeWorld.T0` run: 0 failures (20 passed, 21 listed — UE counter quirk,
   see KNOWN_ERRORS).
   M2/M3/M4/M6 coverage note: their negatives live in the day-gate table, their
   tag positives in `HomeWorldBeatNodeGateTests.cpp`; positive completion halves
   needing `UHomeWorldInventorySubsystem` are fixture-blocked (created world has
   no GameInstance) and remain for the UE-side prove scripts.

## B. UE-dependent, agent-runnable once Editor is up

5. **Run the 6 `NO_VERDICT` prove scripts** (M2, M3, M4, M6, M7, skybox).
   Done-when: each `NO_VERDICT` becomes a recorded result.

## C. Blender-needed (phase 4)

6. **`SM_Camp_*` five modules to `CAMP.json`** (4.2) — unblocks the
   M8/M10/M11/M12/M13/M14 proves; one location, four beats.
7. **FIELD geometry** (4.1) — 70×70, four edges, 2 beast pads, 15 items.
8. **Treeline opacity check** (4.3) — zero forest interior from landing and
   (+20,−15), or revisit DEC-0028.
9. **Spec-coverage audit** (1.3) — every mesh volume the blend has that no
   spec names.

## D. Needs the Lead, in order

10. Stamp or void `APPROVE-T0-MECHANIC-INV`.
11. Accept the 6 prove outcomes from B into `T0_BEAT_EVIDENCE`.
12. Resolve island-top truth (spec 21×14×0.5 vs layout 21×14×4.0 vs blend
    19.3×10.7×0.45) — then clear the 7 graybox findings.
13. Water master (1.5), shrine dims (Q21), `SM_SpiritWound_01`
    crater-vs-marker.
14. Camp clearing image → M8/M10/M11/M12/M13/M14 prove scripts → GATE 3.

## E. Finish line

15. **Phase 5.2 — the full chain**: field → forest → day discovery → eject →
    spirit → stealth → soothe → free. Blocked on 4.x. Done-when: a reviewer
    plays start to rescue with no guidance.
