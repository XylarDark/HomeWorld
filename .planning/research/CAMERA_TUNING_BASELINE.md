# Camera tuning baseline (research deliverable)

**Source:** Phase 2 research (R-2-1), 2026-10-17.  
**Status:** Draft — pending playtest (Phase 1) and Lead tuning.  
**Canon impact:** none yet. Values land in `Docs/canon/FEEL.md`.

## The 6 FEEL.md tunables (all TODO, none chosen)

| Tunable | Current | Target window (canon) | Status |
|---------|---------|----------------------|--------|
| Glide gravity scale | unmeasured | — | TODO |
| Glide lateral influence | unmeasured | — | TODO |
| Camera arm length | unmeasured | — | TODO |
| Camera pitch bias | unmeasured | — | TODO |
| Night length | unmeasured | — | TODO |
| Gather node cooldown | unmeasured | — | TODO |

## Measurement plan

1. Run `Content/Python/probe_movement_budget.py` in-editor to extract walk speed (already done: 600 cm/s = 6.0 m/s).
2. Record current values of all 6 tunables from `BP_HomeWorldCharacter` CDO and camera component. Write to `Docs/qa/POLISH_BASELINE.json`.
3. Run `traversal_budget.py` to check reachability against canon windows.
4. After Phase 1 playtest, tune one constant at a time (Swink: "one constant per experiment"). Record before/after + commit per change.

## Motion-sickness mitigation checklist (P0)

- [ ] FOV slider (default ~70-80, adjustable 60-100)
- [ ] Motion-blur toggle (off by default recommended)
- [ ] Camera sensitivity slider (separate X/Y)
- [ ] Head-bob toggle (off by default)
- [ ] Target 60 FPS minimum; avoid input lag
- [ ] Avoid enclosed low-light spaces in the glide (cloud descent is open — good)
- [ ] Third-person (already) — generally safer than first-person

## Camera occlusion risks (HomeWorld-specific)

- Pine forests (5m/7m/9m pines) — camera may clip through foliage. Test during playtest.
- Cliff geometry — camera may collide with cliff faces during the cloud descent.
- Homestead (cottage 9×11m, 5m walls) — tight interior; camera may need a closer arm indoors.

## Notes

- Swink: "Tuning is only horizontal if you know where you started." Measurement before tuning is the precondition.
- Camera is a first-class feel component, not a settings screen. Treat tuning as feel work (G-FEEL gate).