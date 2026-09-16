# PINES_HOMESTEAD — Stylized Pine Spec

**Kit:** `Lib/01_Homestead`  
**Date:** 2026-09-16 · **ID:** P3_ENVH_kit · **Owner:** ENV-H

---

## 1. Role

**Stylized pines only** for the hero island. Height **6–12 m**. Same pine language as key art and planet (planet instances reuse this language under ENV-P — not authored here as forest kit).

No extra tree species. No deciduous, no alien flora.

---

## 2. Variants (height lock)

| Mesh | Height (m) | Canopy radius guide | Graybox socket |
|---|---|---|---|
| **SM_Pine_Homestead_S** | **6.0** | ~1.2 m | optional fill |
| **SM_Pine_Homestead_M** | **8.0–9.0** | ~1.6 m | `SOCKET_Pine_B` / A |
| **SM_Pine_Homestead_L** | **10.0–12.0** | ~2.0 m | `SOCKET_Pine_C` / A |

Graybox stand-ins: `SM_PineCluster_Homestead_A` (9 m), `B` (8 m), `C` (10 m) at (−8,−2,0), (3,3,0), (5.5,1.5,0).

Origin: ground contact at trunk base. Apply scale. Trunk vertical +Z.

---

## 3. Shape language

- Conical silhouette; slightly fluffy
- **Tiered foliage cards** wrapping the trunk, smaller toward the tip
- Clear readable tiers (3–6 card rings) — stylized, not photoreal needles
- Trunk slightly tapered; handmade bark read via material Variation

---

## 4. Materials

| Part | Master | Notes |
|---|---|---|
| Trunk / branches | **M_WoodWild** | Bark ↔ cut-face lighten within allowed tweaks |
| Foliage cards | **M_FoliageCard** | Masked opacity; foliage palette only; no emissive |

Instance only. Delete unique bark/leaf shaders.

---

## 5. Card / mesh construction

| Element | Spec |
|---|---|
| Cards | Crossed or radial card quads / simple lobes per tier |
| Trunk | Low-poly cylinder / tapered trunk (~8–12 sides) |
| LOD | LOD0 hero near cabin; LOD1 for mid; billboard/card LOD2 optional later (TA LOD policy) |
| Collision | Capsule or simple trunk cylinder |

---

## 6. Placement notes (homestead only)

- Cluster toward cabin left and lookout approach (key art)
- Keep lookout pad + path clear for family silhouettes (Shot 1)
- Do not invent a second species to “fill gaps” — duplicate/scale within 6–12 m and rotate instances

---

## 7. Naming / export

- `SM_Pine_Homestead_S` / `_M` / `_L`
- Collection: `Lib/01_Homestead`
- Cite: `M_WoodWild` + `M_FoliageCard`

---

## 8. Rejects

Heights outside 6–12 m; oak/birch/palm/alien trees; photoreal scans; unique foliage master; planet forest blockouts in this folder.
