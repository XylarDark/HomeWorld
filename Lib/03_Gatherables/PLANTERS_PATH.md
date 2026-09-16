# PLANTERS_PATH.md — planters + path 3-pack

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP  
**Graybox zone:** `SM_Garden_Beds` (−3.5, 0.5, 0.0), `SM_Path_Homestead` (0, 0, 0) — dress, do not relocate volumes without WLD.

---

## 1. Raised planters (Shot 2 + nurture N1)

Handmade wooden boxes with dirt fill + crop proxies. Cozy, not ornate. Warm wood read against cool night fill; colorful plant read for Shot 2.

| Mesh | Size (X×Y×Z m) | Origin | Materials | Notes |
|---|---|---|---|---|
| `SM_Planter_A` | 1.2 × 0.6 × 0.45 | Ground contact under box | Frame: **M_WoodCabin**; dirt: **M_StylizedGrass** (dry instance OK); crop day: **M_GatherHerb**; crop nurtured: **M_Nurtured** | Primary nurture target N1 (GDD §8) |
| `SM_Planter_B` | 1.0 × 0.55 × 0.40 | Ground contact | Same as A | Second bed for garden read |
| `SM_Planter_C` | 0.8 × 0.5 × 0.35 | Ground contact | Same as A | Optional third; keep within garden volume |

**Sockets / slots**

| Socket | On | Purpose |
|---|---|---|
| `SOCKET_Crop` | Planter top center | Day crop proxy / night nurtured swap |
| `SOCKET_NurtureInteract` | Front face ~0.9 m height | SYS V7 interact volume attach |
| `SOCKET_Dirt` | Inner bed | Dirt plane / fill mesh child |

**Nurture contract (N1 — Crop)**

- Day/body: planters visible; nurture blocked (GDD V7).
- Night/spirit + 1× `RES_SEED` (or planted seed waiting): Use → apply **M_Nurtured** emissive on / growth read on crop instance.
- Do **not** invent a third nurture master. Off state = `M_GatherHerb` or `M_Nurtured` with Emissive near-black.

**Placement intent:** Cluster inside `SM_Garden_Beds` graybox; readable from `CAM_CabinClose` (Shot 2). Cabin amber should catch planter faces at night.

---

## 2. Path stone 3-pack

Modular tiles for homestead path and planet path reuse. Cite **M_PathStone** only (material sheet §2.6 / cite matrix).

| Mesh | Footprint (X×Y m) | Thickness Z | Variation | Role |
|---|---|---|---|---|
| `SM_PathStone_A` | 1.0 × 1.0 | 0.08–0.12 | Pack A (default Variation) | Straight / plaza base |
| `SM_PathStone_B` | 1.0 × 0.7 | 0.08–0.12 | Pack B | Offset / stagger |
| `SM_PathStone_C` | 0.7 × 0.7 | 0.08–0.12 | Pack C | Corner / fill / curve hint |

**Rules**

- Origins at ground contact (top of stone ≈ path walk height).
- Handmade irregular edges; not CAD pavers; not photoreal scans.
- Homestead: dress `SM_Path_Homestead` (~10 × 1.2 m volume).
- Planet: ENV-P / WLD may reuse same 3-pack on `SM_Path_Planet_SegA/B/C` — same masters.
- `SM_LandingCircle` stone ring also cites **M_PathStone** (see `SM_LandingCircle.md`).

**Optional child**

| Mesh | Material | Role |
|---|---|---|
| `SM_PathDirt_Clump` | **M_StylizedGrass** | Soft edge clumps between stones (sheet allows path floor clumps) |

---

## 3. Crop / dirt proxies (planter children)

| Mesh | Material | State |
|---|---|---|
| `SM_CropProxy_Day` | **M_GatherHerb** | Default day / pre-nurture |
| `SM_CropProxy_Nurtured` | **M_Nurtured** | Night nurtured success (or same mesh, MI swap) |
| `SM_DirtFill` | **M_StylizedGrass** (dry tint instance) | Bed fill |

Prefer **one crop mesh + material instance swap** over two hero sculpts.

---

## 4. Rejects

- Extra biome flora / alien plants in planters
- Photoreal wood or scanned stone
- Sci-fi hydroponics
- Unique planter shaders
- Moving garden/path graybox origins without WLD
