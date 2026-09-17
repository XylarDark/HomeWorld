# DEFECT_P6_QA_001 — Shot 1 still fails key-art match

- **ID:** DEFECT_P6_QA_001
- **Phase:** P6
- **Owner:** LIT / ENV-H / CHA (lookdev still re-render); INT may refresh reel citation after fix
- **Blocker:** **YES** — fails P6 gate “Night homestead still matches key art”
- **Severity:** Blocker
- **Status:** CLOSED / RESOLVED (QA re-judge 2026-09-16 ET)
- **Filed by:** QA
- **Date:** 2026-09-16

## Summary

`Maps/Preview_Homestead_Night/shot1_lookout.png` is present but does not satisfy `Docs/00_SHOTLIST.md` Shot 1 must-see / reject criteria against north star `refs/keyart_homestead_night.jpg`.

## Repro

1. Open `refs/keyart_homestead_night.jpg` (key-art composition: cabin left + warm windows, garden/path, adult+2 children silhouettes at right lookout, huge warm moon upper-right, starry navy + peach clouds, layered cliff, planet valley with path + rooftops, islets).
2. Open `Maps/Preview_Homestead_Night/shot1_lookout.png` (claimed `CAM_Hero` still; 1600×900).
3. Score against `Docs/00_SHOTLIST.md` Shot 1 and `Maps/Preview_Homestead_Night/README.md` §3 key-art match table.

## Expected

Shot 1 still reads as key-art match: cabin left with warm glowing windows; garden + stone path; readable adult + two children at lookout edge facing moon; huge warm moon (not tiny white); layered torn-earth cliff; planet below with pine valley / path / 2–3 rooftops; warm-vs-cool contrast.

## Actual

Still is greybox/blockout framing that fails hard shotlist reads (moon/family/cabin-left hero composition/planet valley path+rooftops not established in the PNG). Blend contains `LIT_Moon`, `SK_Family_Adult` / `SK_Family_Child_A` / `SK_Family_Child_B` (not hide_render) — assets exist, **still evidence does not**.

## Evidence paths

- `refs/keyart_homestead_night.jpg`
- `Maps/Preview_Homestead_Night/shot1_lookout.png`
- `Docs/00_SHOTLIST.md` (Shot 1)
- `Maps/Preview_Homestead_Night/README.md` §3
- `Lib/00_Core/CAM_Hero.md`
- `Maps/VS_MVP/CAMERA_REEL.md` (cites Shot 1 still)
- `blender/floating_island_homestead_LIB.blend` (family + moon present)

## Notes

Polish vs illustration is subjective; hard rejects are not. Re-render Shot 1 from corrected `CAM_Hero` night stack before P6 gate retry.


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
- Evidence: overwritten `Maps/Preview_Homestead_Night/shot1_lookout.png` (1600×900, mtime 2026-09-16 17:04 ET)
- Hard rejects cleared: huge warm moon, warm cabin window, readable family×3 silhouettes, planet valley path/rooftops/pines
- PARTIAL only (non-failing): peach clouds / snow peak / stars not hero-dressed
- FIX claim docs: `Docs/handoffs/P6_FIX_shot1.md`, `Docs/qa/P6_FIX_SHOT1_NOTE.md`

