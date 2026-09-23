# Docs/33 — Placement Stills (PS — homestead placement confidence)

| Field | Value |
|-------|-------|
| **Track ID** | **PS** — Placement Stills (testing-stills suite) |
| **Status** | **APPROVED** — **PS-0 CLOSED** — Lead **`APPROVE PS STRATEGY — homestead kit only`**, 2026-09-22/23 ET |
| **Date** | 2026-09-23 |
| **Author** | Cloud agent (Conductor packet) |
| **Scope locked (P0)** | **Homestead kit on `L_VS_MVP_Markers` only** — same footprint as closed [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) (PA); planetside dress **OUT** |
| **Prior tracks** | [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) **CLOSED** (PA-E lit stills **deferred/accepted**) · [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) dress runbook |
| **Prefix** | **PS** — do **not** reuse **PA** / **PA-E** gate strings or treat PS phases as PA phases |

---

## Gate

Lead **`APPROVE PS STRATEGY — homestead kit only`** — **GRANTED** 2026-09-22/23 ET (unlocks **PS-A**). Scope: **homestead kit only** on Markers — no planetside dress.

**Approval ladder (track):**

| Step | Lead action | Unlocks |
|------|-------------|---------|
| PS-0 | **`APPROVE PS STRATEGY`** | PS-A metrics + angle inventory |
| PS-A | **`APPROVE PS-A`** | PS-B camera/fixture Arrange |
| PS-B | **`APPROVE PS-B`** | PS-C automated metric asserts + still capture |
| PS-C | **`APPROVE PS-C`** | PS-D Lead eyeball vs benchmarks |
| PS-D | **`APPROVE PS-D`** | PS-E close |
| PS-E | **`APPROVE PS-E`** | PS track **CLOSED / COMPLETE** |

**Handoff:** [handoffs/PS_STRATEGY.md](handoffs/PS_STRATEGY.md) (PS-0 **CLOSED**) · PS-A **CLOSED** ([handoffs/PS_A_INVENTORY.md](handoffs/PS_A_INVENTORY.md)) · PS-B **CLOSED** ([handoffs/PS_B_ARRANGE.md](handoffs/PS_B_ARRANGE.md)) · **PS-C OPEN** ([handoffs/PS_C_METRICS.md](handoffs/PS_C_METRICS.md))

---

## Goal

Build a **systematic testing-stills suite** so homestead kit placement on VS_MVP can be judged with **prototype-worthy confidence**:

1. **Enough camera angles** to catch floaters, gaps, and composition failures (not a single hero frame).
2. **Environment metrics** automation can **assert** (ground contact, height vs landscape/anchors, bounds, overlaps, optional facing).
3. **Benchmark stills** the dressed level should **match in intent** (key-art / kit plate / Lead-stamped goldens) — **prototype bar**, not ship-final.

**Success:** Assets read **grounded** (no obvious floaters), sit sensibly relative to anchors and dress AABB, and multi-angle stills + metrics align with Lead-approved benchmarks before further kit expansion.

---

## Quality bar

| In (prototype PASS) | Out (not PS scope) |
|---------------------|---------------------|
| Grounded placement; float ≤ threshold; in dress bounds | Ship-final lighting, hero Substance, Nanite/Lumen gates |
| Multi-view stills + JSON metric report per run | Automated pixel-perfect golden diff (**SCOUT-gated** — plan only) |
| Shot1/2 **compatible** framing where listed (composition intent) | Full planetside camp / forest path dress |
| Reuse MRQ / Arrange patterns from PA-E harness | Character hero meshes, combat props |
| Lead **eyeball** for taste/framing on PS-D | Reopening [Docs/07_VERTICAL_SLICE_SIGN OFF.md](07_VERTICAL_SLICE_SIGN%20OFF.md) |

**Metric ≠ visual:** Automated asserts gate **placement physics**; Lead eyeball gates **framing, mood, benchmark match** (same split as PA-E `capture_outcome` / `finalize_shot_validation` in harness).

---

## Harness practices (reuse — do not reinvent)

| Practice | Source |
|----------|--------|
| **Arrange before Act** | [docs/Automation/HARNESS_ARRANGE_TASKLIST.md](../docs/Automation/HARNESS_ARRANGE_TASKLIST.md) · `arrange_pa_e_shotlist()` pattern in [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py) |
| **Three-state outcomes** | `pass` / `soft_fail` / `closed_fail` — [docs/Automation/CAPTURE_REDUNDANCY.md](../docs/Automation/CAPTURE_REDUNDANCY.md) |
| **Docs-first / proven-results / gated SCOUT** | [docs/Automation/automation-standards.mdc](../.cursor/rules/automation-standards.mdc) (via CAPTURE_REDUNDANCY ladder) |
| **Level + placement scripts** | `place_vs_mvp_markers.py` → `place_vs_mvp_dress.py` → `place_vs_mvp_pa_d.py` ([06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md), PA-D) |
| **Capture path** | Prefer existing MRQ + [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py); extend with **`PS_*`** cameras or **`PA_E_MRQ_*` siblings** after inventory — **investigate level labels before adding actors** |

**Hard rules (every PS phase):**

- [Docs/07_VERTICAL_SLICE_SIGN OFF.md](07_VERTICAL_SLICE_SIGN%20OFF.md) **CLOSED** — do not reopen.
- **No `.uasset` / `.umap` commits** — local DESKTOP only ([20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md)).
- **FALLBACK FLIGHT armed** — no free-flight capture framing ([09_FALLBACK_GLIDE.md](09_FALLBACK_GLIDE.md)).
- Golden-image / Epic Screenshot Comparison: **mention as later rung only**; implement only after Lead **`APPROVE TOOL SCOUT`**.

---

## Scope IN (P0)

**World:** `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` only.

**Actors under test (initial inventory — extend in PS-A):**

| Label prefix / family | Script source | Notes |
|----------------------|---------------|--------|
| `DRESS_*` | `place_vs_mvp_dress.py` | Core anchors (cabin, island, lookout, shrine, …) |
| `PA_D_*` | `place_vs_mvp_pa_d.py` | Cliffs, planters, fence, path stones (16× reported PA-D) |
| `VS_MVP/TMP_*` | PA-E Arrange fixtures | Night stack for **lit** stills when TOD = homestead night |

**Dress bounds contract:** Homestead dress AABB / anchor envelopes from [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) + [Lib/00_Core/GRAYBOX_LAYOUT.md](../Lib/00_Core/GRAYBOX_LAYOUT.md) (PS-A to freeze numeric bounds JSON in `Saved/`).

---

## Scope OUT

- Planetside dress, forest path hero kit, hamlet roofs (separate track).
- Full golden-image pipeline without **`APPROVE TOOL SCOUT`**.
- Character heroes beyond silhouettes; combat props; new biomes.
- Re-litigating PA track closure or renaming PA gates to PS.

---

## Environment metrics catalog (PS-A deliverable)

Automation writes **`Saved/ps_placement_metrics.json`** (schema fixed in PS-A). Suggested asserts (thresholds tuned on DESKTOP baseline after PS-B):

| Metric ID | Description | Suggested assert |
|-----------|-------------|------------------|
| `ground_z_delta_uu` | Lowest mesh contact vs landscape (or island top proxy) Z at XY sample | \|delta\| ≤ **TBD** (start **8 UU** prototype) |
| `float_gap_uu` | Air gap under support point vs ground | ≤ **TBD** (start **4 UU** for kit props; **12 UU** cliff underside check) |
| `anchor_height_delta_uu` | Actor origin Z vs expected anchor Z from dress table | Per-actor band from PS-A inventory |
| `contact_overlap` | Static overlap with landscape / `SM_IslandTop` collision | Required for grounded props; forbidden for “floating” except approved islets |
| `dress_aabb_inside` | Actor bounds ⊆ homestead dress AABB (+ margin) | Fail if extent exits dress volume (margin **TBD**, start 50 UU) |
| `pair_overlap_uu` | AABB overlap between unrelated kit actors | Flag penetrations > **TBD** (start 2 UU) |
| `facing_dot_look_at` | Optional: forward vs vector to look-at target (shrine, path, cliff edge) | \|dot\| ≥ **TBD** when spec’d in sidecar |

**Sampling:** Use UE Python `get_actor_bounds(False)` tuple API ([docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md)). Landscape Z via line trace down from bounds center (PS-C implementation).

**Outcome:** Each metric → `pass` / `soft_fail` / `closed_fail`; aggregate **`placement_outcome`** mirrors harness capture outcomes.

---

## Camera / angle catalog (PS-A deliverable)

Enough views to catch **floaters**, **cliff underside gaps**, and **composition drift**. Prefer **reusing** in-level `CAM_*` where aim bounds already exist in PA-E; add **`PS_*`** only for gaps.

| PS cam ID | Intent | Primary failure mode | Shotlist / doc tie-in |
|-----------|--------|----------------------|------------------------|
| `PS_N_HighIso` | North high isometric overview | Missing island mass / kit outside bounds | Dress AABB sanity |
| `PS_E_HighIso` | East high iso | Cliff floaters east face | Cliff specs in `place_vs_mvp_pa_d.py` |
| `PS_S_HighIso` | South high iso | Garden/path misalignment | Garden blocking |
| `PS_W_HighIso` | West high iso | Cabin/path disconnect | |
| `PS_Cabin_ThreeQuarter` | 3/4 cabin + garden | Window/path/planter read | **Shot 2-compatible** ([00_SHOTLIST.md](00_SHOTLIST.md)) · `CAM_CabinClose` family |
| `PS_Lookout_Hero` | Lookout key-art framing | Silhouette cliff / moon side read | **Shot 1-compatible** · `CAM_Hero` / [P6_FIX_shot1.md](handoffs/P6_FIX_shot1.md) |
| `PS_Garden_Close` | Raised beds + path | Planter float / fence gaps | **Shot 2-compatible** |
| `PS_Cliff_Underside` | Low angle under plateau edge | **Floater / pancake** underside | Reject list Shot 1 “layered torn-earth” |
| `PS_Path_Corridor` | Path stone continuity | Stones floating / gaps | PA-D path stones |
| `PS_Shrine_Read` | Shrine + landing circle | Vertical offset vs pad | Optional P0+ |

**Naming rule:** New sequencer/MRQ cameras: `PS_<View>_<Variant>` under `/Game/HomeWorld/Cinematics/PS/` **or** sibling sequences next to `CINEMATICS_PA_E_DIR` — **inventory existing `CAM_*` labels in PS-A before creating**.

**TOD / lighting:** Homestead night for Shot1/2-compatible frames (Phase 2 + preset stack per PA-E — not Phase 2 alone). Day iso views optional for metric-debug only (document in PS-B).

---

## Benchmark sources (PS-D compare set)

| Source | Path / doc | Use |
|--------|------------|-----|
| Shot 1 / 2 intent | [00_SHOTLIST.md](00_SHOTLIST.md) | Framing + must-see / reject lists |
| Key art | `refs/keyart_homestead_night.jpg` (repo ref cited in shotlist) | Composition benchmark Shot 1 |
| Kit plate | [refs/ai/homestead_kit_plate_labeled.jpg](refs/ai/homestead_kit_plate_labeled.jpg) · [AssetCreation/RefImages/homestead_kit_plate_labeled.jpg](../AssetCreation/RefImages/homestead_kit_plate_labeled.jpg) | Kit layout + labels |
| Camera language | [CAMERA_BIBLE.md](CAMERA_BIBLE.md) | Orbit vs iso — PS stills are **judgment cameras**, not gameplay rig |
| Lead-stamped stills | `Saved/ps_benchmarks/` (DESKTOP) + optional `Docs/refs/ps/` after Lead stamp | Goldens for eyeball — **not** auto-committed pixels in git |
| PA-E evidence | [handoffs/PA_E_SHOTS.md](handoffs/PA_E_SHOTS.md) | Prior MRQ path; PS **supersedes** informal PA-E placement proof |

---

## Phase board

| Phase | Focus | Deliverable | Host |
|-------|--------|-------------|------|
| **PS-0** | Strategy | This doc + [PS_STRATEGY.md](handoffs/PS_STRATEGY.md) | CLOUD |
| **PS-A** | Metrics + angle **inventory** | [PS_A_INVENTORY.md](handoffs/PS_A_INVENTORY.md) — **CLOSED** Lead **`APPROVE PS-A`**, 2026-09-22 ET | CLOUD+DESKTOP |
| **PS-B** | Camera/fixture **Arrange** | [PS_B_ARRANGE.md](handoffs/PS_B_ARRANGE.md) · `arrange_ps_homestead.py` → `Saved/ps_arrange_gate.json` — **CLOSED** Lead **`APPROVE PS-B`**, 2026-09-22 ET | DESKTOP |
| **PS-C** | Metric asserts + still capture | [PS_C_METRICS.md](handoffs/PS_C_METRICS.md) · `ps_placement_prove.py` → `ps_placement_metrics.json` + `Saved/ps_stills/` | DESKTOP |
| **PS-D** | Lead eyeball vs benchmarks | Checklist vs key-art / plate / stamped stills; defects filed | Lead + QA |
| **PS-E** | Close | PHASE_BOARD **CLOSED**; optional pointer handoff for planetside PS-P2 | Lead |

**PS-C script:** [ps_placement_prove.py](../Content/Python/ps_placement_prove.py) — reads `ps_arrange_gate.json`, metrics sample, viewport stills; **do not** fork PA-E gate strings.

---

## Relationship to PA track

| PA (closed) | PS (this track) |
|-------------|-----------------|
| Mesh upgrade + PA-D place report | **Prove** placement with multi-angle stills + metrics |
| PA-E MRQ Shot1/2 **deferred/accepted** | Formal **placement** bar; may reuse same cameras/light stack |
| Gate strings `APPROVE PA-*` | Gate strings **`APPROVE PS-*`** only |

---

## References

- [00_SHOTLIST.md](00_SHOTLIST.md) — Shot 1–2 framing
- [CAMERA_BIBLE.md](CAMERA_BIBLE.md) — identity vs systems cameras
- [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) — dress anchors + script
- [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) — PA scope footprint (homestead only)
- [docs/Automation/HARNESS_ARRANGE_TASKLIST.md](../docs/Automation/HARNESS_ARRANGE_TASKLIST.md)
- [docs/Automation/CAPTURE_REDUNDANCY.md](../docs/Automation/CAPTURE_REDUNDANCY.md)
- [Content/Python/pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py)
- [Content/Python/place_vs_mvp_markers.py](../Content/Python/place_vs_mvp_markers.py) · [place_vs_mvp_dress.py](../Content/Python/place_vs_mvp_dress.py) · [place_vs_mvp_pa_d.py](../Content/Python/place_vs_mvp_pa_d.py)

---

*PS-0 **CLOSED** · PS-A **CLOSED** · PS-B **CLOSED** (Lead **`APPROVE PS-B`**, 2026-09-22 ET). **PS-C** metrics + stills **OPEN** — [PS_C_METRICS.md](handoffs/PS_C_METRICS.md); gate **`APPROVE PS-C`** after DESKTOP prove.*
