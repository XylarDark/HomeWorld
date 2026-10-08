# T0 ordered execution queue — 2026-10-07 re-pass

Pre-lock record. The first-loop queue is `Docs/TaskLists/T0_FIRST_LOOP_NOW.md`.
Item 4 below (rune unlock as the route into spirit) is superseded: sleep at the
bed is the form change. Item 3 (companion hint) is no longer parked for lack of
a design; the lock is one hint toward the edge.

Built from `T0_EXECUTION_PHASES.md` + `T0_PROTOTYPE_TRACK.md` under the
SESSION_START track sizing. In order. Owner column: who must act.

## A. Agent-owned, unblocked now

1. **`T0_M9` hardening** — ✅ DONE (already merged): `HomeWorldFormGateTests.cpp` carries the four M9 behaviour tests, added in `790bbd5` ("the P0 form law is executable, and proven able to fail"). Queue doc row was stale; no further work.
2. **Phase 5.3 — Tending** — ✅ resolved 2026-10-07: V2b "tending" is the same
   plant/nurture/collect mechanic as #3/#12 in two volumes: homestead plots (few,
   for morning tea + tending wounded spirits) and field herb sites (uncapped,
   materials-gated, for later uses like feeding bulls). No separate bed state
   machine. Route updated.
3. **Phase 5.1 — Companion NPC hint** — Parked: no design packet or actor exists.
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
7. **FIELD geometry** (4.1) — 420×420 (×6 pass), four edges, 2 beast pads, 15 items.
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
