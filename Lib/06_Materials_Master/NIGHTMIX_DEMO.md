# NIGHTMIX_DEMO — sphere row (Blender MCP pending)

**ID:** P2_TA_masters / NightMix demo  
**Date:** 2026-09-16  
**Status:** SPEC READY — Blender MCP not available; build when MCP connects  
**Owner:** TA  
**Collection (target):** `Lib/06_Materials_Master` / scene `NightMix_Demo`

## Purpose

Prove that every master responds to a single `NightMix` 0→1 parameter + overlay (no second map set). LIT / GP will later drive the same float from GameState time.

## Layout

- **10 UV spheres**, diameter **1.0 m**, origins on ground contact.
- Row along **+X**, spaced **1.5 m** center-to-center (span ≈ 13.5 m).
- Ground plane optional; use `M_StylizedGrass` instance if present.
- Camera: three-quarter front, all spheres in frame; label empties or text objects above each sphere with master id.

| Index | Object name | Master instance | NightMix |
|------:|---|---|--------:|
| 0 | `DEMO_Sphere_M_StylizedGrass` | MI_StylizedGrass_Demo | 0.00 |
| 1 | `DEMO_Sphere_M_CliffRock` | MI_CliffRock_Demo | 0.11 |
| 2 | `DEMO_Sphere_M_WoodCabin` | MI_WoodCabin_Demo | 0.22 |
| 3 | `DEMO_Sphere_M_WoodWild` | MI_WoodWild_Demo | 0.33 |
| 4 | `DEMO_Sphere_M_FoliageCard` | MI_FoliageCard_Demo | 0.44 |
| 5 | `DEMO_Sphere_M_PathStone` | MI_PathStone_Demo | 0.56 |
| 6 | `DEMO_Sphere_M_GatherHerb` | MI_GatherHerb_Demo | 0.67 |
| 7 | `DEMO_Sphere_M_BeastStylized` | MI_BeastStylized_Demo | 0.78 |
| 8 | `DEMO_Sphere_M_SpiritUnlit` | MI_SpiritUnlit_Demo | 0.89 |
| 9 | `DEMO_Sphere_M_Nurtured` | MI_Nurtured_Demo | 1.00 |

NightMix steps ≈ `i / 9` for i = 0…9.

## Build steps (when Blender MCP connects)

1. Create node-group masters `NG_M_*` from the JSON defs in this folder (one group per master).
2. Instance each as `MI_*_Demo` materials; set **only** `NightMix` per table; leave BaseColor / Roughness / Variation at master defaults; enable Emissive where the master defaults non-black (`M_SpiritUnlit`, `M_Nurtured`).
3. Assign one instance per sphere; name objects exactly as above.
4. Add a single scene custom property or driver root `NightMix_Global` (optional): for live scrub, drive all ten from one float — but the **acceptance row** keeps the stepped 0→1 values so a still frame proves the ramp.
5. Frame + screenshot → drop under `Docs/qa/` as `NightMix_sphere_row.png` when available.
6. Do **not** duplicate albedo/roughness maps for night. Overlay only: tint + desaturate + value mul (+ emissive mul where defined).

## Acceptance

- [ ] Exactly 10 spheres, one per canon master (no 11th).
- [ ] Left = day-ish (0), right = night-ish (1).
- [ ] `M_SpiritUnlit` and `M_Nurtured` show emissive response at high NightMix.
- [ ] No second texture set visible in the node trees.
- [ ] Screenshot or MCP confirmation logged in handoff evidence.

## Notes

- Foliage card on a sphere is opaque demo only; real meshes use masked cards.
- This demo is lookdev proof, not a shipping map prop.
