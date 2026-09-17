# DEFECT_P6_QA_002 — Lookout still does not prove landing / portal / first harvest / home naming

- **ID:** DEFECT_P6_QA_002
- **Phase:** P6
- **Owner:** LIT / WLD / ENV-P (sightline + still); CHA family already placed
- **Blocker:** **YES** — fails QA script step 1 (Lookout: name landing, portal, first harvest, home) as evidenced by still
- **Severity:** Blocker (script gate); related to Shot 1 framing
- **Status:** CLOSED / RESOLVED (QA re-judge 2026-09-16 ET)
- **Filed by:** QA
- **Date:** 2026-09-16

## Summary

QA lookout script requires the player/viewer to **name** landing, portal, first harvest, and home from the lookout. Named meshes exist in the blend, but `shot1_lookout.png` does not demonstrate that sightline.

## Repro

1. Confirm objects exist in `blender/floating_island_homestead_LIB.blend`: `SM_LandingCircle`, `SM_Shrine_Return`, `SM_Gather_FirstHarvest`, homestead/`SM_Cabin` (MCP verify 2026-09-16).
2. Inspect `Maps/Preview_Homestead_Night/shot1_lookout.png` and `Lib/00_Core/CAM_Hero.md` sightline checklist (landing, roofs, forest path, return shrine, first harvest).
3. Attempt to name landing / portal / first harvest / home from the still alone.

## Expected

From lookout / `CAM_Hero` still: landing circle, return portal shrine, first-harvest marker, and home/cabin are identifiable (per CAM_Hero sightline + canon lookout test).

## Actual

Shot 1 PNG does not provide a readable lookout naming proof for those four. Existence in Outliner ≠ script pass without still/frustum evidence.

## Evidence paths

- `Maps/Preview_Homestead_Night/shot1_lookout.png`
- `Lib/00_Core/CAM_Hero.md` (sightline checklist)
- `Maps/Preview_Lookout_To_Planet/README.md` (claims sightline; still under Homestead_Night does not show it)
- Blend objects: `SM_LandingCircle`, `SM_Shrine_Return`, `SM_Gather_FirstHarvest`, `SM_Cabin`
- `swarm/agents/qa.md` step 1

## Notes

May clear together with DEFECT_001 if a corrected Shot 1 still shows valley POIs + homestead home read.


---

## Fix status note (authors — 2026-09-16 ET) — CLOSED for authoring / READY for QA re-judge

- Still overwritten: `Maps/Preview_Homestead_Night/shot1_lookout.png`
- Handoff: `Docs/handoffs/P6_FIX_shot1.md`
- Also: `Docs/qa/P6_FIX_SHOT1_NOTE.md`
- **Do not treat as PASS** — QA re-judges DEFECT_P6_QA_001 / 002.

---

## QA re-judge resolution (2026-09-16 ET)

- **Verdict:** CLOSED / RESOLVED — P6 GATE **PASS** on re-judge
- **Report:** `Docs/qa/P6_QA_REPORT_REJUDGE.md`
- **Handoff:** `Docs/handoffs/P6_QA_rejudge.md`
- Evidence: same Shot 1 still + live `CAM_Hero` frustum (Blender MCP read-only)
- Home = `SM_Cabin` (warm window left); Landing = circular platform / `SM_LandingCircle*` in frustum; Return shrine = `SM_Shrine_Return_*` clear corners; First harvest = `SM_Gather_FirstHarvest` bushes in frustum
- Script step 1 PASS under still + known blend names with frustum claim

