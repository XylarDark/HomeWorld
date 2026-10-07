# SESSION_HANDOFF_ZONE_GENERATION — 2026-10-07

Session slice: design interviews closure → camp blockout → bull encounter code →
zone-generation research and the "straight to generation" decision.

## Where things stand

- **All pushed.** Last commits: `517c988` (art-bible Appendix A + T0
  implementation pass + style forks), `b6a98c7` (camp module blockout in blend),
  `5ce9468` (beast charge-and-boot C++ + 4 tests), `6c5c7fb` (zone-generation
  research + field/forest zone contracts). Tree clean.
- **Tests:** `HomeWorld.T0` 24 passed / 0 failed (report lists 25 — known UE
  counter quirk, KNOWN_ERRORS). `HomeWorld.Transit` was 3/3 earlier today.
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

CAMP origin `(20,-80,-95)` and the blend's `02_Forest` blob + `06_Camp` sit
**inside FIELD bounds** (~20 m from field centre) — violates FIELD's own reject
`camp_visible_from_the_field_centre`. Recorded in `FIELD.json.zone_contract`
and `CAMP.json.zone_contract`. Under straight-to-generation these become
template/slot source pieces, not world placements.

## Next steps (in order)

1. **`Lib/02_Zones/forest/FOREST.json`** — new zone spec, FIELD structure:
   blob template + depth band, entry bands matching both field forest edges,
   seed = hash(FIELD seed, edge id), slots: camp (5 modules + 4 actors),
   spirit wound, return shrine; pine density budget; identical-silhouette rule
   (both edges → same template); rejects (no camp slots in FIELD — structural).
   Research doc §4/§6 = the contract: `docs/39_ZONE_GENERATION_RESEARCH.md`.
2. **Seeded zone generator (C++)** — skeleton jitter + scatter from spec rules,
   `FRandomStream`, tests: determinism (same seed → same output), budgets,
   **field-has-zero-camp-slots** as permanent automation.
3. **Edge-crossing instantiation** — crossing a field forest edge instantiates
   (or re-activates) the forest neighbor; unchosen edge stays dormant.
4. Blend: reposition `02_Forest`/`06_Camp` as kit/template source (not inside
   field placement), or leave until the generator owns placement — Lead call.
5. Then: camp art image→blockout pass (deferred), prove scripts M8/M10–M14
   against generated geometry (GATE 3), six `NO_VERDICT` prove runs.

## Open questions carried

- Research doc §7: **Q2** shape-variance amounts (proposal: ±15% extent, edge
  bands ±25 m) and **Q3** confirm shrine-return + spirit wound follow the forest
  zone. Q1 answered: straight to generation.
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
