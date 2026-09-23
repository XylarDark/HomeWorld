# PS-A — Placement Stills inventory (homestead Markers)

| Field | Value |
|-------|-------|
| **Status** | **GATE READY** — pending Lead **`APPROVE PS-A`** after DESKTOP live verify |
| **Track** | PS-A (inventory) · PS-0 **CLOSED** |
| **Scope** | **Homestead kit only** — `L_VS_MVP_Markers` ([33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md)) |
| **Host** | CLOUD (this doc) · **DESKTOP** fills live counts / confirms cam labels |
| **Impl** | [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) metrics + camera catalogs |

---

## Lead gate

```text
APPROVE PS-A
```

---

## Script chain (reference)

```text
place_vs_mvp_markers.py   → CRUMB_*, VS_MARKER, ANCHOR_*, CAM_* (JSON)
place_vs_mvp_dress.py     → DRESS_* (folder VS_MVP/Dress)
place_vs_mvp_pa_d.py      → PA_D_* (folder VS_MVP/PA_D) + refresh DRESS_*
```

Level: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`

---

## 1. Actor inventory

### 1.1 Markers / anchors (`place_vs_mvp_markers.py` + JSON)

Source: `AssetCreation/Exports/MVP_CRUMB_SPLINE.json` — not placement-metric targets except anchor Z reference.

| Label pattern | Source | Notes |
|---------------|--------|--------|
| `CRUMB_*` | JSON `CRUMB[]` | Glide spline targets; not kit meshes |
| `VS_MARKER` names | JSON `VS_MARKER[]` | **TBD** — enumerate from JSON on DESKTOP |
| `ANCHOR_<key>` | JSON `anchors` keys | Dress anchor positions (e.g. `ANCHOR_SM_Cabin`) |
| `CAM_*` | JSON `CAM[]` | See §2 — cameras, not dress actors |

### 1.2 `DRESS_*` (`place_vs_mvp_dress.py`)

Folder: `VS_MVP/Dress` · Prefix: `DRESS_` + **StaticMesh asset basename**.

| Anchor / rule | Mesh prefix (spawn all matches in index) | Expected labels (pattern) | Count note |
|---------------|------------------------------------------|---------------------------|------------|
| `SM_IslandTop` | `SM_IslandTop` (exact) | `DRESS_SM_IslandTop` | 1 if mesh exists |
| `SM_Cabin` | `SM_Cabin` | `DRESS_SM_Cabin_*` | **TBD** — all `SM_Cabin*` meshes at anchor |
| `SM_Lookout_Pad` | `SM_Lookout_Pad` (exact) | `DRESS_SM_Lookout_Pad` | 1 |
| `SM_Glider_Perch` | `SM_Glider_Perch` (exact) | `DRESS_SM_Glider_Perch` | 1 |
| `SM_Shrine_Homestead` | `SM_Shrine_Homestead_` | `DRESS_SM_Shrine_Homestead_*` | **TBD** |
| `SM_LandingCircle` | `SM_LandingCircle_` | `DRESS_SM_LandingCircle_*` | **TBD** |
| `SM_Shrine_Return` | `SM_Shrine_Return_` | `DRESS_SM_Shrine_Return_*` | **TBD** |
| `CRUMB_Islet_01/02/03` | `SM_Islet_01_` … `SM_Islet_03_` | `DRESS_SM_Islet_*` | **TBD** per islet |
| Extra @ landing | `SM_Planet_GroundPlate` | `DRESS_SM_Planet_GroundPlate` | 0–1 optional |
| Extra @ landing | `SM_Gather_FirstHarvest_Bush_` | `DRESS_SM_Gather_*` | **TBD** |
| Extra @ return shrine | `SM_Roof_Hamlet_01/02/03` | `DRESS_SM_Roof_Hamlet_*` | 0–3 optional |
| Extra @ cabin | `SM_Pine_Homestead_S/M/L` | `DRESS_SM_Pine_Homestead_*` | 0–3 optional |

**DESKTOP verify:** After `place_vs_mvp_dress.py`, grep level actors `label.startswith("DRESS_")` → fill **live count** column in `Saved/ps_a_desktop_verify.json` (optional stub; not committed).

### 1.3 `PA_D_*` (`place_vs_mvp_pa_d.py`)

Folder: `VS_MVP/PA_D` · Prefix: `PA_D_` + mesh basename (fence uses suffixed labels).

| Family | Script spec | Expected labels | Script expected count |
|--------|-------------|-----------------|------------------------|
| Cliffs | `CLIFF_SPECS` | `PA_D_SM_Cliff_LookoutFace`, `PA_D_SM_Cliff_CabinFace`, `PA_D_SM_Cliff_Rear` | **3** |
| Planters | `PLANTER_SPECS` | `PA_D_SM_Planter_A/B/C` | **3** (optional meshes) |
| Fence | `FENCE_SEGMENTS_BL` × `SM_Garden_Fence_Seg` | `PA_D_SM_Garden_Fence_Seg`, `PA_D_SM_Garden_Fence_Seg_2` … `_5` | **5** (optional mesh) |
| Path stones | `sample_path_points(5)` × `PATH_STONE_NAMES` | `PA_D_SM_PathStone_A/B/C` (cycled) | **5** (optional meshes) |

**Reported PA-D total (when all optional resolve):** 3 + 3 + 5 + 5 = **16** kit actors (+ DRESS refresh does not remove PA_D).

**DESKTOP verify:** Run `place_vs_mvp_pa_d.py` → confirm log `Done` counts vs table; **TBD** if optional meshes missing on host.

### 1.4 Out of PS-A homestead scope (do not assert)

Planetside / other tracks: scripts like `place_vs_mvp_*` for RS/GC/CD/etc. — **OUT** per PS-0 lock.

### 1.5 PA-E Arrange fixtures (reference only)

Night lit stills may use `VS_MVP/TMP_*` from PA-E Arrange — inventory for **placement metrics** focuses on `DRESS_*` + `PA_D_*`; TMP_* listed for camera/light context only (**TBD** live list on DESKTOP).

---

## 2. Camera map (10 PS IDs → level / harness)

JSON cameras from markers (`MVP_CRUMB_SPLINE.json` `CAM[]`):

| Level label | In JSON |
|-------------|---------|
| `CAM_CabinClose` | yes |
| `CAM_GlideDepart` | yes |
| `CAM_Hero` | yes |
| `CAM_LandingDay` | yes |
| `CAM_PortalNight` | yes |

`pa_e_shotlist_common.py` **`SHOTS`** aliases (resolve order):

| Shot | `camera_labels` tuple |
|------|-------------------------|
| shot1 | `CAM_Hero`, `Shot1`, `Lookout`, `Hero` |
| shot2 | `CAM_CabinClose`, `Shot2`, `Cabin`, `Garden`, `CAM_CabinGarden` |

MRQ spawn (DESKTOP, not in JSON): `PA_E_MRQ_shot1`, `PA_E_MRQ_shot2` — copies Arrange pose from shot diagnostics; **do not** treat as PS placement actors.

### PS strategy cam ID → reuse vs new

| PS cam ID | Intent | Existing label(s) | PS-B action |
|-----------|--------|-------------------|-------------|
| `PS_N_HighIso` | North high iso | — | **New `PS_*` actor** (no JSON cam) |
| `PS_E_HighIso` | East high iso | — | **New `PS_*` actor** |
| `PS_S_HighIso` | South high iso | — | **New `PS_*` actor** |
| `PS_W_HighIso` | West high iso | — | **New `PS_*` actor** |
| `PS_Cabin_ThreeQuarter` | 3/4 cabin + garden | **`CAM_CabinClose`** (+ shot2 aliases) | **Relocate / aim** existing; MRQ sibling `PA_E_MRQ_shot2` |
| `PS_Lookout_Hero` | Lookout hero | **`CAM_Hero`** (+ shot1 aliases) | **Relocate / aim** existing; MRQ sibling `PA_E_MRQ_shot1` |
| `PS_Garden_Close` | Garden close | **`CAM_CabinClose`** family (same as shot2) | **Relocate** or derive variant from CabinClose |
| `PS_Cliff_Underside` | Cliff underside | — | **New `PS_*` actor** |
| `PS_Path_Corridor` | Path continuity | — ( `CAM_LandingDay` is landing/day, not path corridor) | **New `PS_*` actor** |
| `PS_Shrine_Read` | Shrine + pad | — ( `CAM_PortalNight` = portal night, not shrine read) | **New `PS_*` actor** (P0+ optional) |

**Unused for PS iso set (keep for transit/portal):** `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight` — do not delete; PS-B may reference for sightlines only.

**Rule:** No new Unreal assets in PS-A — inventory only. PS-B creates/aims actors on DESKTOP.

---

## 3. Threshold table (prototype freeze)

From [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) metrics catalog — **starting values**; tune on DESKTOP baseline after PS-B Arrange.

| Metric ID | Prototype threshold (UU) | Notes |
|-----------|--------------------------|--------|
| `ground_z_delta_uu` | **8** | \|lowest contact Z − landscape/island proxy Z\| |
| `float_gap_uu` (kit props) | **4** | Air gap under support |
| `float_gap_uu` (cliff underside) | **12** | Underside / plateau edge |
| `dress_aabb_inside` margin | **50** | Actor bounds must stay inside homestead dress AABB + margin |
| `pair_overlap_uu` | **2** | Unrelated kit AABB penetration flag |
| `anchor_height_delta_uu` | **TBD per actor** | From PS-A inventory + anchor table after DESKTOP sample |
| `facing_dot_look_at` | **TBD** | When sidecar specifies look-at |

**Tune on DESKTOP baseline** after first `Saved/ps_placement_metrics.json` dry run (PS-C).

---

## 4. Bounds JSON spec (`Saved/ps_dress_bounds.json`)

Filled in PS-B/C by Arrange/metrics — **schema only** for PS-A.

```json
{
  "version": 1,
  "level_path": "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers",
  "coordinate_space": "ue_world_uu",
  "dress_aabb": {
    "center": [0.0, 0.0, 0.0],
    "extent": [0.0, 0.0, 0.0]
  },
  "dress_aabb_minmax": {
    "min": [0.0, 0.0, 0.0],
    "max": [0.0, 0.0, 0.0]
  },
  "margin_uu": 50,
  "anchors": {
    "SM_Cabin": { "location_uu": [0.0, 0.0, 0.0], "note": "from ANCHOR_SM_Cabin or JSON" }
  },
  "source": "arrange_ps_homestead | manual_desktop | placeholder",
  "generated_at_iso": null
}
```

Either **`center` + `extent`** or **`minmax`** required when non-placeholder; metrics code prefers `center`/`extent` (matches `get_actor_bounds`).

---

## 5. Metrics output (PS-C pointer)

`Saved/ps_placement_metrics.json` — schema fixed in PS-B/C; PS-A locks metric IDs + thresholds in §3.

---

## DONE-WHEN (PS-A)

- [x] Actor inventory tables for `DRESS_*`, `PA_D_*`, marker/cam references (this doc)
- [x] Camera map: 10 PS IDs vs `CAM_*` / `PA_E_MRQ_*` / new `PS_*` flags
- [x] Prototype threshold table frozen with tune note
- [x] `Saved/ps_dress_bounds.json` schema documented
- [ ] **DESKTOP:** Live actor counts for `DRESS_*` / `PA_D_*`; confirm five JSON `CAM_*` exist; note any `CAM_CabinGarden` / `Shot1`/`Shot2` alias actors in level
- [ ] Lead **`APPROVE PS-A`**

---

## DESKTOP verify checklist (next)

1. Open Markers → run markers → dress → pa_d chain (see [PS_STRATEGY.md](PS_STRATEGY.md)).
2. Export actor label counts: `DRESS_*`, `PA_D_*` (expect PA-D **16** if all optional meshes present).
3. Confirm cameras: `CAM_CabinClose`, `CAM_Hero`, `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight`.
4. After PA-E Arrange/MRQ: note whether `PA_E_MRQ_shot1` / `PA_E_MRQ_shot2` exist (ephemeral vs saved — **TBD**).
5. Append counts to session log or `Saved/ps_a_desktop_verify.json` (local only).

Cloud: [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).
