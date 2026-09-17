# P6 QA REPORT — RE-JUDGE after FIX Shot 1

- **ID:** P6_QA_rejudge
- **Phase:** P6 / WAVE 5
- **Role:** QA (independent judge)
- **Date:** 2026-09-16 ~17:07 ET (America/New_York)
- **Scope:** Re-judge DEFECT_P6_QA_001 / 002 against overwritten Shot 1 still + FIX handoff. Did **not** edit kits, blend models, `swarm/PHASE_BOARD.md`, or `Docs/07*` sign-off.
- **Inputs:** `Docs/handoffs/P6_FIX_shot1.md`, `Docs/qa/P6_FIX_SHOT1_NOTE.md`, prior `Docs/qa/P6_QA_REPORT.md`, `Docs/00_SHOTLIST.md` Shot 1, `Lib/00_Core/CAM_Hero.md`, live blend via Blender MCP (read-only).

---

## Verdict

| Item | Result |
|---|---|
| **P6 GATE** | **PASS** |
| Defect count remaining | **0** |
| DEFECT_P6_QA_001 | **CLOSED / RESOLVED** |
| DEFECT_P6_QA_002 | **CLOSED / RESOLVED** |

Prior transit FALLBACK + portal path and 10-master library **still PASS** (reconfirmed).

---

## What changed since prior FAIL

| Artifact | Evidence |
|---|---|
| New Shot 1 still | `Maps/Preview_Homestead_Night/shot1_lookout.png` — 1600×900, mtime **2026-09-16 17:04 ET** (21:04 UTC), size 1 636 395 bytes |
| FIX handoff | `Docs/handoffs/P6_FIX_shot1.md` |
| FIX note | `Docs/qa/P6_FIX_SHOT1_NOTE.md` |
| `CAM_Hero` live pose | loc `(−9.0, −4.0, 5.8)`, Euler ≈ `(41.61°, 0°, −108.43°)`, lens **14 mm**, scene camera — matches FIX claim (md table in `CAM_Hero.md` still has older pose; live blend is authoritative for this still) |

---

## 1. Shot 1 vs key art + shotlist (DEFECT_001)

**Method:** Read PNG with Read tool + region crops; score against `Docs/00_SHOTLIST.md` Shot 1 must-see / rejects and `refs/keyart_homestead_night.jpg`. Greybox polish ≠ fail if hard must-sees / hard rejects are cleared. Peach clouds / snow peak allowed **PARTIAL**.

| # | Must-see | Result | Evidence |
|---|---|---|---|
| 1 | Cabin LEFT + warm glowing windows | **PASS** | Still: tan cabin left/foreground with bright emissive window pane; warm spill on adjacent faces. Hard reject “dark cabin windows” cleared. |
| 2 | Garden beds + stone path on plateau | **PASS** | Stone slab path from cabin across plateau readable; garden beds in frustum (blend `SM_GardenBed_A/B/C` NDC mid-left). Greybox beds OK. |
| 3 | Adult + 2 children silhouettes at cliff, facing moon | **PASS** | Family-zone crop: three black humanoid silhouettes (taller adult + two shorter) on south rim / lookout edge. Blend: `SK_Family_*` in frustum, scale 1.5–1.8, ray hits self (visible). Hard reject “family not readable as three” cleared. |
| 4 | Huge warm moon upper-right | **PASS** | Massive pale-warm disc occupies large right portion of frame (`LIT_Moon` NDC ≈ 0.82, 0.69; dims ~75 m scaled). Hard reject “tiny white moon” cleared. |
| 5 | Starry navy + peach clouds + snow peak | **PARTIAL** | Navy night BG present; stars / peach clouds / snow peak **not** hero-dressed in still. Allowed PARTIAL per re-judge brief — does **not** fail gate alone. |
| 6 | Layered torn-earth cliff (not pancake) | **PARTIAL / PASS** | Lookout cliff stack / angular island edge readable vs prior flat-path still; still kit blockout. Hard reject pancake/cylinder cleared for greybox. |
| 7 | World below: pines / path / 2–3 rooftops | **PASS** | Valley crop: green planet plate, pointed pine stand-ins, brown block rooftops/hamlet, path/line geometry, circular landing platform. Blend roofs `SM_Roof_Hamlet_01/02/03` + `SM_Path_Planet_SegA` in frustum with clear rays to own meshes. Hard reject “planet missing path/rooftops/valley” cleared. |
| 8 | Warm cabin vs cool moonlight | **PASS** | Warm window emissive vs cool night fill / moon key readable. |
| 9 | Extra floating islets | **PASS** | Mid-air grey block stacks / islets between homestead and valley. |

**Hard rejects (shotlist):** photoreal/muddy/grim/sci-fi — no; extra tree species — no; tiny white moon — no; dark windows — no; pancake/cylinder — no (acceptable layered blockout); family unreadable — no; planet missing path/rooftops/pines — no.

**Subjectivity note:** Still is homestead **kit blockout**, not illustration polish. Pixel match to key art is not required. Hard composition + reject criteria are met.

**DEFECT_001: RESOLVED — PASS**

---

## 2. Lookout naming (DEFECT_002)

**Script:** Name landing, portal/return shrine, first harvest, home from lookout still (and/or still + known blend names with frustum claim).

| Name | Still read | Blend + frustum | Result |
|---|---|---|---|
| **Home** | Cabin with warm window, left plateau | `SM_Cabin` in frustum (NDC ≈ 0.07, 0.11) | **PASS** |
| **Landing** | Circular gear/toothed platform on valley plate visible in still | `SM_LandingCircle` + stone children in frustum; `LandingCircle_B_*` corners clear | **PASS** |
| **Portal / return shrine** | Small at valley distance; identifiable with name knowledge | `SM_Shrine_Return_*` meshes in frustum, multiple clear corners; ray to shrine base | **PASS** (still + frustum claim) |
| **First harvest** | Valley harvest/bush cluster region | `SM_Gather_FirstHarvest` + bushes / `SM_RES_BERRY_World_Mesh` in frustum, clear corners | **PASS** (still + frustum claim) |

Note: empty `SM_LandingCircle` origin ray hits `SM_Planet_ValleyLip_A`, but landing **mesh** (circle stones / B circle) and still circular platform read remain visible — naming proof holds.

**DEFECT_002: RESOLVED — PASS**

---

## 3. Reconfirm prior PASS gates

| Gate | Result | Evidence |
|---|---|---|
| Leave island → planet → return by portal (FALLBACK + portal) | **PASS** (held) | Crumbs `CRUMB_Depart_Lookout`…`CRUMB_Landing` + `CRUMB_GlideSpline`; `VS_MARKER_LeaveIsland_FALLBACK`, `VS_MARKER_LandPlanet`, `VS_MARKER_PortalHome`, `VS_MARKER_PortalPlanet`; `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`; stills `shot3_glide_depart.png`, `shot4_landing_day.png`, `shot5_portal_night.png` |
| Library instance-based (10 masters) | **PASS** (held) | Exactly 10 JSON: `Lib/06_Materials_Master/M_BeastStylized`, `M_CliffRock`, `M_FoliageCard`, `M_GatherHerb`, `M_Nurtured`, `M_PathStone`, `M_SpiritUnlit`, `M_StylizedGrass`, `M_WoodCabin`, `M_WoodWild` |

---

## P6 gate checkboxes (re-judge)

| Gate | Pass/Fail | Evidence |
|---|---|---|
| Leave island, reach planet, return by portal (FALLBACK + portal OK) | **PASS** | Unchanged from prior report + live blend reconfirm |
| Night homestead still matches key art | **PASS** | New `shot1_lookout.png` clears shotlist hard rejects; peach/snow PARTIAL only |
| Library still instance-based (10 masters) | **PASS** | 10× `M_*.json` |

---

## What QA did not do

- Did not edit kits, blend, PHASE_BOARD, or Docs/07 sign-off
- Did not soft-fail on greybox polish when hard must-sees were present
- Did not invent a 6th shot or new master family

---

## Residual risks (non-blocking)

- Stars / peach clouds / distant snow peak still undressed (PARTIAL)
- Family silhouettes are small blockout pawns — readable as trio but not illustration-quality
- `Lib/00_Core/CAM_Hero.md` pose table lags live `CAM_Hero` (14 mm / new loc) — docs drift for later WLD tidy, not a P6 still blocker
