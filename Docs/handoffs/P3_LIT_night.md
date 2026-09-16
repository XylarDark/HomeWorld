# Handoff

- **ID:** P3_LIT_night
- **Phase:** P3 (WAVE 2 Homestead)
- **Role:** LIT
- **Owner agent:** LIT (lighting)
- **Status:** DONE (specs; Blender MCP unavailable)
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md`
- `Lib/07_Night_SpiritLayer/LIT_Moon.md`
- `Lib/07_Night_SpiritLayer/LIT_CabinWindows.md`
- `Lib/07_Night_SpiritLayer/VOLUME_Haze.md`
- `Lib/07_Night_SpiritLayer/CAM_Hero_LIT_NOTES.md`
- `Maps/Preview_Homestead_Night/README.md`
- `Docs/handoffs/P3_LIT_night.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| PRESET_Homestead_Night | LIT preset spec | NightMix on all 10 | Lib/07_Night_SpiritLayer |
| LIT_Moon | LIT disc + key | emissive disc / cool-neutral key | Lib/07_Night_SpiritLayer |
| LIT_Moon_Key | LIT directional/area | — | Lib/07_Night_SpiritLayer |
| LIT_CabinWindows | LIT emissive windows | MI_WoodCabin_WindowGlow (M_WoodCabin) | Lib/07_Night_SpiritLayer |
| LIT_CabinWarm | LIT warm spill (refine graybox) | — | Lib/07 + graybox |
| LIT_MoonCool | LIT cool fill (refine graybox) | — | Lib/07 + graybox |
| VOLUME_Haze | volume under cliff | — | Lib/07_Night_SpiritLayer |
| CAM_Hero_LIT_NOTES | CAM addendum (no WLD overwrite) | — | Lib/07_Night_SpiritLayer |

## Phase exit boxes I claim

- [x] Night preset specs: huge moon disc + LIT_Moon + window emissives + volume haze
- [x] Preview_Homestead_Night assembly checklist targets key-art read (Shot 1 + Shot 2)
- [x] Windows bloom specified (2700–3200K + bloom)
- [x] Moon huge and warm specified (`#FFD56A`–`#FFE28A`, ~18° angular)
- [x] CAM_Hero framing gaps addressed via addendum only (no overwrite of WLD `CAM_Hero.md`)
- [ ] Live Eevee/UE key-art stills — blocked on Blender MCP + ENV-H/PROP dress

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path (did not overwrite `Lib/00_Core/CAM_Hero.md`; no PHASE_BOARD; no new maps beyond preview notes; no new materials)

## Inputs I used

- `Docs/02_ART_BIBLE.md`
- `Docs/02_MATERIAL_SHEET.md` + `Lib/06_Materials_Master/NIGHTMIX_DEMO.md` + `M_WoodCabin.json` / `M_SpiritUnlit.json`
- `Docs/00_SHOTLIST.md` Shots 1–2
- `Lib/00_Core/CAM_Hero.md` + `Lib/00_Core/GRAYBOX_LAYOUT.md`
- `refs/keyart_homestead_night.jpg`
- `Docs/00_CANON.md`
- `swarm/packets/WAVE_2_HOMESTEAD.md` / LIT role card

## Blockers

- Blender MCP not available — no live lights/volumes in `.blend`; markdown/JSON specs only.
- Live Preview_Homestead_Night stills require ENV-H cabin/cliff/pines + PROP planters/path (+ optional lantern) dressed on graybox.

## Risks for the next owner

- ENV-H: every cabin window pane must accept `MI_WoodCabin_WindowGlow` (or equivalent M_WoodCabin emissive instance) — never ship dark glass.
- PROP: planter/path kits must sit in warm spill range of `LIT_CabinWarm` for Shot 2.
- GP later: one GameState time float → NightMix + enable this preset + spirit layer visibility; do not author `_Night` texture sets.
- QA: gate against key art + shotlist — reject tiny white moon / dark windows / missing haze height / muddy grade.
- WAVE 3 LIT: Planet_Day is separate preset; do not overload Homestead_Night.

## Evidence

- Spec pack under `Lib/07_Night_SpiritLayer/` with embedded JSON contracts for preset, moon, windows, haze.
- `Maps/Preview_Homestead_Night/README.md` Shot 1 key-art match table + Shot 2 close tests.
- NightMix drive default **0.85** documented; moon angular ~18°; windows 2700–3200K bloom.
- WLD `CAM_Hero` left intact; LIT notes in `CAM_Hero_LIT_NOTES.md` only.
