# Handoff

- **ID:** P6_QA_judge
- **Phase:** P6 / WAVE 5
- **Role:** QA
- **Owner agent:** QA (independent judge)
- **Status:** DONE (gate failed — defects filed)
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Docs/qa/P6_QA_REPORT.md`
- `Docs/qa/DEFECT_P6_QA_001_shot1_keyart_mismatch.md`
- `Docs/qa/DEFECT_P6_QA_002_lookout_still_naming.md`
- `Docs/handoffs/P6_QA_judge.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| — | — | — | — |

## Phase exit boxes I claim

- [x] Ran QA script from `swarm/agents/qa.md` against docs + stills + handoffs + Blender verify
- [x] Wrote `Docs/qa/P6_QA_REPORT.md` with pass/fail + evidence paths
- [x] Filed defects only (did not edit kits / blend / PHASE_BOARD / Docs/07)
- [x] Issued **GATE FAIL** for P6 (cannot close phase)

## P6 criteria summary

| Criterion | Result |
|---|---|
| Leave island, reach planet, return by portal (FALLBACK + portal OK) | **PASS** |
| Night homestead still matches key art (stills present; keyart comparison noted) | **FAIL** (stills present; Shot 1 fails shotlist hard rejects vs `refs/keyart_homestead_night.jpg` — see DEFECT_001; subjectivity noted in report) |
| Library still instance-based (10 masters) | **PASS** |

**Overall: GATE FAIL** — defect count **2**.

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit kits, blend, PHASE_BOARD, or Docs/07 sign-off

## Inputs I used

- `swarm/PHASE_BOARD.md`, `swarm/packets/WAVE_5_SLICE.md`, `swarm/agents/qa.md`
- `Docs/00_SHOTLIST.md`, `Docs/02_MATERIAL_SHEET.md`, `Docs/03_GAMEPLAY_MVP.md`, `Docs/03_SYSTEMS_MVP.md`
- `Docs/04_EXPORT_TABLE.md`, `Docs/04_UE_HANDOFF_NOTES.md`
- `Docs/handoffs/P6_INT_slice.md`, `P5_CND_fallback_flight.md`, `P5_GP_verbs.md`, `P5_PROP_verbs.md`, `P5_CHA_life.md`, `P3_BLENDER_kit.md`
- `Maps/VS_MVP/*`, `Maps/Preview_*` stills, `refs/keyart_homestead_night.jpg`
- `Lib/06_Materials_Master/M_*.json` (10), `Lib/08_Transit/GLIDE_SPLINE.md`, `Lib/00_Core/CAM_Hero.md`
- Live blend via `user-blender` MCP (read-only inventory)

## Blockers

- DEFECT_P6_QA_001 (key-art Shot 1)
- DEFECT_P6_QA_002 (lookout naming not proven in Shot 1 still)

## Risks for the next owner

- Conductor: set board to GATE FAILED / keep P6 open; do not open P7 until defects cleared or Lead waives with written note
- LIT/ENV: re-render Shot 1 night still proving key-art + lookout naming; refresh Preview README checklist (still says live stills pending)
- GP later: place missing `GP_*` empties (docs-only today) — not counted as P6 blocker while `VS_MARKER_*` cover FALLBACK path

## Evidence

- `Docs/qa/P6_QA_REPORT.md`
- Defects under `Docs/qa/DEFECT_P6_QA_00*.md`
- Stills: `Maps/Preview_Homestead_Night/shot{1,2,5}_*.png`, `Maps/Preview_Lookout_To_Planet/shot{3,4}_*.png`
- Masters: `Lib/06_Materials_Master/M_*.json` (count = 10)
- Blend verify: collection `VS_MVP`, crumbs, shrines, RES_*, spirits×3, nurture×2, 10 master slot reuse
