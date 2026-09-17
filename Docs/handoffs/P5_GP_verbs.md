# Handoff

- **ID:** P5_GP_verbs
- **Phase:** P5 / WAVE 4
- **Role:** GP
- **Owner agent:** Executor (docs + named markers only; no Blender save; no UE C++)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Docs/03_GAMEPLAY_MVP.md`
- `Docs/handoffs/P5_GP_verbs.md`
- (Prerequisite read: `Docs/03_SYSTEMS_MVP.md` — SYS first)

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| GP_PlayerStart | EMPTY marker (documented) | — | Docs/03_GAMEPLAY_MVP.md §8 |
| GP_GlideStart | EMPTY marker (documented) | — | Docs/03_GAMEPLAY_MVP.md §8 |
| GP_PortalA | EMPTY marker (documented) | — | Docs/03_GAMEPLAY_MVP.md §8 |
| GP_PortalB | EMPTY marker (documented) | — | Docs/03_GAMEPLAY_MVP.md §8 |
| Time float → NightMix + spirit visibility | GP cycle driver | (all 10 masters NightMix) | Docs tables |

Markers are **named in docs only** this wave; CHA/PROP place empties in the `.blend`.

## Phase exit boxes I claim

- [x] Body walk (V1) specified on homestead volumes
- [x] Dusk/shrine form swap body ↔ spirit
- [x] Scripted glide along `CRUMB_*` / GLIDE_SPLINE — **not** free flight (FALLBACK = same crumbs)
- [x] Portal `SM_Shrine_Homestead` ↔ `SM_Shrine_Return` both ways (night/spirit)
- [x] Time float drives NightMix + spirit visibility (dawn/dusk)
- [x] Eight verbs executable or camera-demoable via marker + CAM path
- [x] No combat / no full flight controller / no inventory authorship

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path / PHASE_BOARD
- [x] Did not open or save the `.blend` (CHA/PROP owns Blender this wave)

## Inputs I used

- `Docs/00_CANON.md` §§2–3, §8
- `Docs/01_GDD_MVP.md` §§3–4, §9, Appendix A
- `Docs/03_SYSTEMS_MVP.md` (SYS-first gate)
- `Lib/08_Transit/GLIDE_SPLINE.md`
- `swarm/agents/gameplay.md`
- `swarm/packets/WAVE_4_VERBS.md`
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- Empties `GP_*` not yet placed in blend — documented for CHA/PROP. Cameras `CAM_GlideDepart` / `CAM_LandingDay` / `CAM_PortalNight` already from P4 WLD.

## Risks for the next owner

- Follow EMPTY crumb order, not `CRUMB_GlideSpline` bevel deformation.
- Portal is shrine link only — never reuse day glide spline for night transit.
- SYS spend gates need GP form/time flag; do not re-author inventory in GP files.
- Do not start WAVE 5; Conductor closes P5.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `Docs/03_GAMEPLAY_MVP.md`
  - `Docs/03_SYSTEMS_MVP.md` (SYS prerequisite)
  - `Docs/handoffs/P5_GP_verbs.md`
  - `Lib/08_Transit/GLIDE_SPLINE.md` (crumb contract; not rewritten)
- Screenshot / frame / render / checklist output:
  - Camera-demo path uses existing P4 previews: `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`, `shot4_landing_day.png`
- Test or verify notes (command run + outcome):
  - Confirmed SYS file exists before GP write; glide documented as CRUMB_*/FALLBACK only; portal names match kit `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`
