# Next queue — after the first-loop code

Written 2026-10-08 from the interview that followed `T0_FIRST_LOOP_NOW.md`.

The code queue is done. This file is the work queue. A later lock line wins. Do not copy route numbers into chat. The route file owns the meters.

Run in order. Stop on a decide, a do, or a second fail on the same writer.

## Already decided

- The spread is the night flight. Two cloud wisps stay the cap. One heals the homestead wound, and those healed wisps are the flight. One mixes with a dung. The player spreads that mix over the field herb sites. No morning pile. No third cloud wisp. Recorded in `Docs/context/HOMEWORLD_ROUTE.md`.
- `M_FamilySilhouette` and `M_ValleyNight` remap onto the ten masters in `Docs/02_MATERIAL_SHEET.md`. No eleventh master.
- Camp images are generated from the existing camp prompts and the art bible. The interview lock replaces any stale size, guard count, or rune in those prompts.

## Implement

| # | Change | Done when |
|---|---|---|
| 1 | Place the wake-yard actors from `Docs/context/T0_SHAPE_PLAN.md`: `NODE_BED`, `NPC_PARTNER`, `NPC_CHILD`, `NODE_GARDEN`, `NODE_WOUND`, `NODE_SHRINE`. Open `Docs/level/L_VS_MVP_Markers_manifest.json` first and use it as the actor scan. No meshes. The rune is not placed. **Done 2026-10-08.** | The manifest names each of those actors. |
| 2 | The night flight spreads the mixed fertilizer over field herb sites. It uses the healed wound wisps as the flight and the one mixed wisp as the load. It does not collect a third wisp and it does not spawn a morning pile. **Done 2026-10-08.** | `HomeWorld.T0.FL10.NightFlightSpreadsFertilizer` passed. |
| 3 | Remap `M_FamilySilhouette` and `M_ValleyNight` to instances of masters in `Docs/02_MATERIAL_SHEET.md` §2. Record the cite. The master-binding gate stays a hard fail until those two names are gone. **Blocked:** the Blender 4.4 install has no `blender.exe`, so the blend was not renamed. The cite is recorded and `Content/Python/remap_family_valley_materials.py` is ready. | The blend no longer assigns either name, and the binding check no longer lists them. |
| 4 | Generate the camp reference images from `Docs/art/GROK_IMAGINE_PROMPTS.md` Part 2B and the art bible, using the interview lock where the prompt is stale. Then build the camp modules from those images. **Images and the three-guard graybox are in. Art meshes are not:** `CAMP.json` still marks those modules authored, not built. | Images: `Docs/art/camp/camp_clearing_top.jpg`, `Docs/art/camp/camp_approach.jpg`. The manifest names `NODE_GUARD`, `NODE_GUARD_1`, `NODE_GUARD_2`, and `NODE_SHRINE_CAMP`. |

## Parked

- Family-hint words past "toward the edge."
- Desktop Wake prove. Luke plays that.
- Re-deriving `Docs/WORLD_METRICS.md` onto the scale pass.
- Shrine look past a standing stone at twice player height.
