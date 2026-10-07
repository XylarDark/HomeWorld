# SESSION_HANDOFF_ZONE_GENERATION — 2026-10-07

Session slice: design interviews closure → camp blockout → bull encounter code →
zone-generation research and the "straight to generation" decision.

## Where things stand

- **Pushed through** `92fcc5a` (Q1 recorded). After that, local and uncommitted:
  `FHomeWorldZoneGenerator` and `FHomeWorldZoneCrossing`, plus
  `HomeWorld.T0.ZoneGenerator`. The field now decides its edges, places the
  edge assets, and places the camp only when the player reaches a pine_forest
  asset boundary. Loading note is in docs/39_ZONE_GENERATION_RESEARCH.md.
  Spec numbers for jitter and pine clumps are machine-readable on FIELD.json
  and FOREST.json. Q2 and Q3 are still open.
- Earlier commits: `517c988`, `b6a98c7`, `5ce9468`, `6c5c7fb`, `598ae73`
  (`Lib/02_Zones/combat/FOREST.json` — not `forest/FOREST.json`).
- **Tests:** `HomeWorld.T0.ZoneGenerator` — 12 passed / 0 failed, editor exit 0.
  The earlier full `HomeWorld.T0` run was 24 passed / 0
  failed (report lists 25 — known UE counter quirk). `HomeWorld.Transit` was
  3/3 earlier today.
- **Blend:** `blender/floating_island_homestead_LIB.blend` open in **Mixar**
  (MCP add-on already ported; Mixar `version_string` says 4.2.2 but the engine
  is 5.2.0 — misleading string only). Five `SM_Camp_*` modules built from boxes
  to spec envelopes with masters, in new `06_Camp` collection, placed at the
  (now-superseded) CAMP.json origin — see DEFECT below.

## Decisions locked this session (Lead 2026-10-07)

1. **Style forks (asked one at a time):** stealth = spirit-form default, ring
   detection with soft fill + hard border, **WoW Shadowlands palette** (no
   cone, no HUD eye) — recorded in `CAMP.json.visibility`. Tame fail =
   **charge-and-boot**. Healed wound wisps = **companion followers** (Ni No Kuni
   style) — recorded in `HOMEWORLD_ROUTE.md`. Day discovery = **boot home**.
2. **Zone architecture (the big one):** homestead island stays custom
   hand-made; **field + forest become Path-of-Exile-style generated maps** —
   vague preset shape + seeded variables; **plains and forest are the first two
   use cases**; neighbors generate **based on the direction the player travels**;
   custom content (camp etc.) inserted intelligently via slots so it feels less
   generative. When asked which field edge hosts the first static forest, the
   Lead chose **"straight to generation"** — no throwaway static placement.
3. **Field and forest are two separate zones; camp never in the field**
   (explicit Lead instruction).
4. Image→blockout photo-placeholder work is **deferred** ("leave all of the
   image to blockout work for latter").

## Known defect (must fix as part of generation work)

CAMP.json `world_origin` `(20,-80,-95)` is still inside FIELD bounds.
The blend is not: `02_Forest` / `06_Camp` kit meshes are on the +10000 m X
shelf (Lead interview #17). Interview #19: `LIT_Planet_Fill` is back at
(-13.948, -60, -85). The three Planet_Day lights are in `09_Planet_Day`.
Sun and LandingDay transforms are unchanged. Recorded in
`FIELD.json.zone_contract`, `FOREST.json`, and docs/39 §5.

## Next steps (in order)

1. **FOREST.json** — done. `Lib/02_Zones/combat/FOREST.json` (commit `598ae73`).
2. **Seeded zone generator** — done locally, not committed.
   `Source/HomeWorld/HomeWorldZoneGenerator.h/.cpp` and
   `HomeWorldZoneGeneratorTests.cpp`. Same seed matches; jitter stays inside
   the spec; herb spacing and pine cap hold; both `pine_forest` edges share
   one drift; entry band width ignores the seed; FIELD.json has zero camp
   slots and FOREST.json keeps `SLOT_CAMP`.
3. **Edge-crossing instantiation** — done locally, not committed.
   `FHomeWorldZoneCrossing`: first `pine_forest` edge instantiates FOREST from
   `SeedForEdge`; the same edge reactivates that instance; the other pine edge
   stays dormant; cliff and river open no T0 neighbor.
4. **Slot insertion** — done locally. Shrine, camp, and wound pin at their
   authored offsets, and only after the player reaches a forest edge's placed
   assets. Fire, lashings, and the guard stake stay unplaced. The 108 m
   clearing is subtracted from the pine budget.
5. **In-world streaming** — homestead streams the field; the field streams the
   two walkable forests without the camp. Cliff streams on the upgraded glider.
   River streams on the boat. Camp still pins only at the forest asset boundary.
   Night spirit traversal of those edges is open. See docs/39.
6. Blend: `02_Forest`/`06_Camp` kit meshes parked +10000 m on X (interview #17). Merged as `a595235`.
7. Then: camp art image→blockout pass (deferred), prove scripts M8/M10–M14
   against generated geometry (GATE 3), six `NO_VERDICT` prove runs.

## Open questions carried

- Research doc §7: **Q1** straight to generation. **Q2** and **Q3** answered
  in interview #17: use ±15% extent and ±25 m edge drift; shrine-return and the
  spirit wound pin into forest slots, like the camp. Night: spirit form crosses
  forest edges only; cliff and river stay closed. Not yet in code.
- Moon disc distance/size = taste call, still unswept.
- Homestead slope air-time re-derivation; field clump counts for 420 m field.
- Six `NO_VERDICT` prove scripts (M2/M3/M4/M6/M7/skybox) still blocked by the
  KNOWN_ERRORS PIE-gap (editor quits before PIE ticks).

## Quirks to remember

- Test run: trust the report, not exit code 255; counter says 24/25 listed.
- PowerShell: `;` not `&&`; no `head` — `Select-Object`.
- This model/harness **cannot read image input** — render PNGs and hand the
  path to the Lead instead (camp render at
  `C:\Users\User\AppData\Local\Temp\camp_blockout.png`).
- Git paths are case-sensitive for `add`: use `Docs/context/HOMEWORLD_ROUTE.md`
  exactly.
- Beast-encounter constants are **agent-proposed, Lead-flagged**: aggro 9 m,
  too-close 3.5 m, fill 0.25/s, decay 0.5/s, still ≤1.5 m/s.
