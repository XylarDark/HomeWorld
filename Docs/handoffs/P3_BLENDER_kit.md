# Handoff

- **ID:** P3_BLENDER_kit
- **Phase:** P3 / WAVE 2
- **Role:** ENV-H + LIT + PROP dress (live Blender Lab MCP)
- **Owner agent:** Executor (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend`
- `Maps/Preview_Homestead_Night/shot1_lookout.png`
- `Maps/Preview_Homestead_Night/shot2_cabin_garden.png`
- `Docs/handoffs/P3_BLENDER_kit.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_IslandTop | SM_ | M_StylizedGrass | 01_Homestead |
| SM_Cliff_Slab_A/B/C, SM_Cliff_Chunk_Torn | SM_ modules | M_CliffRock | 01_Homestead |
| SM_Cliff_LookoutFace (+ L0–L4, Lip, TornA/B) | SM_ layered assembly | M_CliffRock | 01_Homestead |
| SM_Cliff_CabinFace (+ L0–L4, Torn) | SM_ layered assembly | M_CliffRock | 01_Homestead |
| SM_Cliff_Rear (+ L0–L4) | SM_ layered assembly | M_CliffRock | 01_Homestead |
| SM_Cliff_IsletHint | SM_ | M_CliffRock | 01_Homestead |
| SM_Cabin (+ walls/roof/chimney/porch/door/windows) | SM_ modular set | M_WoodCabin / M_CliffRock / warm window instance | 01_Homestead |
| SM_Cabin_Window_Pane_Front / Side | SM_ emissive panes | M_WoodCabin_Window (~2700–3200K) | 01_Homestead |
| SM_Pine_Homestead_L / M / S | SM_ | M_WoodWild + M_FoliageCard | 01_Homestead |
| SM_GardenBed_A/B/C (+ soil) | SM_ blocking | M_WoodCabin + M_StylizedGrass_Dry | 01_Homestead |
| SM_Planter_A/B/C | SM_ placeholders | M_WoodCabin | 01_Homestead |
| SM_PathStone_A/B/C_* tiles | SM_ | M_PathStone | 01_Homestead |
| SM_Lookout_Pad | SM_ | M_PathStone | 01_Homestead |
| SM_Glider_Perch | SM_ | M_WoodCabin | 01_Homestead |
| SM_Shrine_Homestead (+ base/posts/lintel/glow + sockets) | SM_ | M_CliffRock / M_WoodCabin / M_SpiritUnlit | 03_Gatherables |
| SM_LandingCircle (+ center + stone ring + sockets) | SM_ | M_PathStone + M_StylizedGrass | 03_Gatherables |
| Planet sightline placeholders (roofs/path/valley/peak/islets) | SM_ planes | masters as cited | 03_Gatherables / 01_Homestead |
| SOCKET_* (island + cabin + shrine + landing) | EMPTY | — | 01_Homestead / 03_Gatherables |
| CAM_Hero, CAM_CabinClose | CAM_ | — | 00_Core |
| LIT_Moon, LIT_Moon_Key, LIT_MoonCool, LIT_CabinWarm, LIT_CabinWindows* | LIT_ | M_MoonDisc / lights | 07_Night_SpiritLayer |
| VOLUME_Haze | VOLUME_ | M_VOLUME_Haze | 07_Night_SpiritLayer |
| M_StylizedGrass, M_CliffRock, M_WoodCabin, M_WoodWild, M_FoliageCard, M_PathStone, M_GatherHerb, M_BeastStylized, M_SpiritUnlit, M_Nurtured | M_ Principled stand-ins | BaseColor/Roughness + NightMix=0.85 | Scene |

## Phase exit boxes I claim

- [x] **Layered cliff** — SM_Cliff_* slabs/chunks/face assemblies (not pancake/cylinder)
- [x] **Warm windows** — SM_Cabin_Window_Pane_* with warm emissive (~FFB060 / 2700–3200K feel) + LIT_CabinWarm / LIT_CabinWindows
- [x] **Huge moon** — LIT_Moon disc (~32 m class) warm yellow + LIT_Moon_Key cool fill
- [x] **Landing + shrine published** — SM_LandingCircle at planet clearing; SM_Shrine_Homestead with SOCKET_Portal / Interact / Arrive
- [x] Blend saved; Shot 1–2 preview PNGs written
- [x] Ten TA masters instanced as Principled BSDF stand-ins (no 11th master family)

## What I did not invent

- [x] No extra biome / tree species
- [x] No free-flight model / combat
- [x] No new master shader beyond the ten sheet masters (+ window/moon/haze lookdev variants of same contracts)
- [x] Did not edit PHASE_BOARD
- [x] Did not start WAVE 3

## Inputs I used

- `Lib/01_Homestead/*.md` (IslandTop, Cliff, CABIN_MODULES, PINES, GARDEN_BLOCKING, KIT_README)
- `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`
- `Lib/03_Gatherables/SM_LandingCircle.md`, `SM_Shrine_Homestead.md`, `PLANTERS_PATH.md`
- `Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md`, `LIT_Moon.md`, `LIT_CabinWindows.md`
- `Docs/00_SHOTLIST.md` shots 1–2
- `Docs/02_MATERIAL_SHEET.md`
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- Blender 5.2 Eevee Next has no classic `use_bloom` flag; bloom not fully matched to preset (emissive + lights still punch). VOLUME_Haze left `hide_render` for lookdev speed.
- `CAM_Hero` location matches `CAM_Hero.md`; rotation uses Blender −Z look-at toward lookout+valley (documented Euler is non-Blender cam convention). Custom props store canon euler.
- Interactive MCP `execute_blender_code` timed out on full-res render; stills produced via `blender -b` CLI against the saved `.blend`.

## Risks for the next owner

- Dress/polish pine card LODs and cliff undercut sculpt; current pines/cliff are layered blockout-accurate but not hero sculpted.
- Re-enable VOLUME_Haze + compositor bloom when beauty-rendering for key-art match.
- PROP may replace planter crop proxies; ENV-P dresses planet slice beyond placeholders.
- Keep SM_IslandTop and SM_Cliff_* separate — do not merge into pancake.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `blender/floating_island_homestead_LIB.blend`
  - `Docs/handoffs/P3_BLENDER_kit.md`
  - `Maps/Preview_Homestead_Night/shot1_lookout.png`
  - `Maps/Preview_Homestead_Night/shot2_cabin_garden.png`
- Screenshot / frame / render / checklist output:
  - Shot 1: `Maps/Preview_Homestead_Night/shot1_lookout.png` (CAM_Hero)
  - Shot 2: `Maps/Preview_Homestead_Night/shot2_cabin_garden.png` (CAM_CabinClose) — cabin warm window + garden/path readable
- Test or verify notes (command run + outcome):
  - Lab MCP `get_objects_summary` / `execute_blender_code` build on Blender 5.2.2
  - `blender -b ... --python-expr` rendered both stills (Eevee, 1600×900)
  - Object counts at save: **166** objects (124 mesh); collections `00_Core`, `01_Homestead`, `03_Gatherables`, `07_Night_SpiritLayer`
