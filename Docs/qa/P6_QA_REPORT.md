# P6 QA REPORT — WAVE 5 Independent Judge

- **ID:** P6_QA_judge
- **Phase:** P6 / WAVE 5
- **Role:** QA (independent judge)
- **Date:** 2026-09-16 (America/New_York)
- **Scope:** Docs + stills + handoffs + Blender-proven / FALLBACK only. Did **not** edit kits, blend models, `swarm/PHASE_BOARD.md`, or `Docs/07*` sign-off.
- **Board read:** `swarm/PHASE_BOARD.md` — P6 IN PROGRESS; Flight fallback armed YES; P6_INT_slice open; no open defects listed at judge start.

---

## Verdict

| Item | Result |
|---|---|
| **P6 GATE** | **FAIL** |
| Defect count | **2** |
| Defect files | `Docs/qa/DEFECT_P6_QA_001_shot1_keyart_mismatch.md`, `Docs/qa/DEFECT_P6_QA_002_lookout_still_naming.md` |

QA cannot close the phase. Gate failed on night homestead key-art still criteria (+ lookout naming not proven in Shot 1 still). Transit FALLBACK + portal path and 10-master library **pass** on evidence below.

---

## P6 gate checkboxes (`swarm/packets/WAVE_5_SLICE.md`)

| Gate | Pass/Fail | Severity if fail | Evidence paths |
|---|---|---|---|
| Leave island, reach planet, return by portal (FALLBACK + portal OK) | **PASS** | — | `Docs/03_GAMEPLAY_MVP.md` FALLBACK appendix; `Docs/handoffs/P5_CND_fallback_flight.md`; `Lib/08_Transit/GLIDE_SPLINE.md`; blend crumbs `CRUMB_Depart_Lookout`…`CRUMB_Landing`; `SM_LandingCircle`; `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`; `Maps/VS_MVP/README.md`; `Maps/VS_MVP/CAMERA_REEL.md`; stills `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`, `shot4_landing_day.png`, `Maps/Preview_Homestead_Night/shot5_portal_night.png`; blend collection `VS_MVP` empties `VS_MARKER_LeaveIsland_FALLBACK`, `VS_MARKER_LandPlanet`, `VS_MARKER_PortalHome`, `VS_MARKER_PortalPlanet` |
| Night homestead still matches key art | **FAIL** | **Blocker** | Stills **present**: `Maps/Preview_Homestead_Night/shot1_lookout.png`, `shot2_cabin_garden.png`, `shot5_portal_night.png`. North star: `refs/keyart_homestead_night.jpg`. Shot 1 still is greybox blockout and fails `Docs/00_SHOTLIST.md` Shot 1 must-see / reject list (huge warm moon, readable adult+2 child silhouettes, cabin-left warm windows, peach clouds / snow peak, planet valley with path+rooftops). Comparison is partly subjective on polish, but hard shotlist rejects are objective. See DEFECT_001. |
| Library still instance-based (10 masters) | **PASS** | — | Exactly 10 JSON masters: `Lib/06_Materials_Master/M_*.json` (`M_BeastStylized`, `M_CliffRock`, `M_FoliageCard`, `M_GatherHerb`, `M_Nurtured`, `M_PathStone`, `M_SpiritUnlit`, `M_StylizedGrass`, `M_WoodCabin`, `M_WoodWild`). Contract: `Docs/02_MATERIAL_SHEET.md`. Blend slot reuse on same masters (e.g. `M_FoliageCard` ×83, `M_WoodCabin` ×42, `M_PathStone`/`M_CliffRock` ×40). Allowed instances only (`M_StylizedGrass_Dry`, `M_SpiritUnlit_Hurt`/`_Healed`, `M_WoodCabin_Window`) + lookdev `M_MoonDisc` / `M_VOLUME_Haze` per P3 handoff — no 11th master family. |

---

## QA script (`swarm/agents/qa.md`) — step results

Judge mode: **Blender-proven / FALLBACK / docs** (no UE play session).

### 1. Lookout: name landing, portal, first harvest, home

| Check | Pass/Fail | Evidence |
|---|---|---|
| Named objects exist in blend | PASS (existence) | `SM_LandingCircle`, `SM_Shrine_Return` (portal B), `SM_Gather_FirstHarvest`, homestead/`SM_Cabin` + `SM_Lookout_Pad` — verified via Blender MCP on `blender/floating_island_homestead_LIB.blend` |
| Readable from Shot 1 still / lookout frustum proof | **FAIL** | `Maps/Preview_Homestead_Night/shot1_lookout.png` does not show a readable landing circle, return shrine, first-harvest, or home cabin composition matching `Lib/00_Core/CAM_Hero.md` sightline checklist / shotlist. See DEFECT_002. |

**Script step 1: FAIL**

### 2. Day: glide, gather each resource once, meet beast, return

| Check | Pass/Fail | Evidence |
|---|---|---|
| Glide (FALLBACK scripted) | PASS | Crumbs in blend: `CRUMB_Depart_Lookout`, `CRUMB_Air_01`, `CRUMB_Islet_01`, `CRUMB_Air_02`, `CRUMB_Islet_02`, `CRUMB_Air_03`, `CRUMB_Islet_03`, `CRUMB_Approach`, `CRUMB_Landing` + `CRUMB_GlideSpline`; still `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`; FALLBACK armed on board + `Docs/03_GAMEPLAY_MVP.md` |
| Gather each resource once (×6) | PASS (Blender-proven) | World nodes: `SM_RES_WOOD_World`, `SM_RES_FIBER_World`, `SM_RES_STONE_World`, `SM_RES_BERRY_World`, `SM_RES_HERB_World`, `SM_RES_SEED_World` (+ Stored twins); `Docs/03_SYSTEMS_MVP.md`; `Docs/handoffs/P5_PROP_verbs.md` |
| Meet beast | PASS (Blender-proven) | `SK_Beast_Small` on `SM_BeastPad_01`; `Docs/handoffs/P5_CHA_life.md` |
| Return | PASS (portal path) | Day return via night portal contract: `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`; still `shot5_portal_night.png`; `Docs/03_GAMEPLAY_MVP.md` §6 |

**Script step 2: PASS** (doc + blend + FALLBACK; not UE runtime)

### 3. Night: spirit, portal, heal 3, nurture 2

| Check | Pass/Fail | Evidence |
|---|---|---|
| Spirit form / layer | PASS (Blender-proven) | Collection `05_Spirits` / `07_Night_SpiritLayer`; `SK_Spirit_01/02/03_Hurt` + `_Healed`; night stills under `Maps/Preview_Homestead_Night/` |
| Portal | PASS | Shrines both ways + `CAM_PortalNight` + `shot5_portal_night.png` + `VS_MARKER_PortalHome` / `VS_MARKER_PortalPlanet` |
| Heal ×3 | PASS (Blender-proven) | Three hurt spirits + `SOCKET_Heal_*`; `Docs/03_SYSTEMS_MVP.md` §6; `Docs/handoffs/P5_CHA_life.md` |
| Nurture ×2 | PASS (Blender-proven) | `SM_NurtureGlow_Crop`, `SM_NurtureGlow_Stored` with `M_Nurtured`; `Docs/handoffs/P5_PROP_verbs.md` |

**Script step 3: PASS** (Blender-proven)

### 4. Shots 1–5 vs key art

| Shot | File | Present | vs key art / shotlist |
|---|---|---|---|
| 1 | `Maps/Preview_Homestead_Night/shot1_lookout.png` (1600×900, non-empty) | PASS | **FAIL** vs `refs/keyart_homestead_night.jpg` + `Docs/00_SHOTLIST.md` Shot 1 (DEFECT_001) |
| 2 | `Maps/Preview_Homestead_Night/shot2_cabin_garden.png` | PASS | PARTIAL — warm window read present; greybox; not key-art hero framing (expected for Shot 2) |
| 3 | `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png` | PASS | N/A key-art hero; glide/crumbs beat documented |
| 4 | `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png` | PASS | Day landing clearing beat documented |
| 5 | `Maps/Preview_Homestead_Night/shot5_portal_night.png` | PASS | Portal/spirit night beat; not key-art composition match |

**Script step 4: FAIL** (Shot 1 key-art gate)

---

## INT claimed artifacts (spot-check)

| Artifact | Present | Notes |
|---|---|---|
| `Docs/04_EXPORT_TABLE.md` | PASS | Paths + UCX proxy **names** documented |
| `Docs/04_UE_HANDOFF_NOTES.md` | PASS | Notes only; no UE dress required for P6 |
| `Maps/VS_MVP/README.md` | PASS | Leave / land / portal assembly |
| `Maps/VS_MVP/CAMERA_REEL.md` | PASS | Shots 1–5 order + still paths |
| `Docs/handoffs/P6_INT_slice.md` | PASS | DONE claim |
| Blend `VS_MVP` markers | PASS | Six `VS_MARKER_*` empties verified in open blend |
| Cameras ×5 | PASS | `CAM_Hero`, `CAM_CabinClose`, `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight` |
| `UCX_*` meshes in blend | N/A / note | Not present as objects (`ucx=[]`); INT exit box is **docs** proxies — acceptable for P6 portability notes |
| `GP_*` empties in blend | Note | `GP_PlayerStart`, `GP_GlideStart`, `GP_PortalA`, `GP_PortalB` **absent** (docs-only per `P5_GP_verbs.md`). Covered for P6 transit by `VS_MARKER_*` + shrine/landing names — not counted as separate P6 blocker |

---

## Subjectivity note (key art)

Pixel-perfect match of greybox Eevee stills to `refs/keyart_homestead_night.jpg` is subjective on polish. QA still **fails** the gate where shotlist **hard rejects** apply: Shot 1 still does not deliver readable key-art composition (moon, family trio, cabin-left warm windows, planet valley path/rooftops). Assets for family (`SK_Family_*`) and `LIT_Moon` exist in the blend and are not `hide_render`, but the checked still file does not prove the match.

---

## What QA did not do

- Did not edit kits, blend, PHASE_BOARD, or Docs/07 sign-off
- Did not invent features or pass on vibes without paths
- Did not run UE playtest (out of evidence mode for this wave)
