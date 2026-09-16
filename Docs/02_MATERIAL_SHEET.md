# Docs/02_MATERIAL_SHEET.md

**Status:** LOCKED (P2 TA definitions)  
**Date:** 2026-09-16  
**ID:** P2_TA_masters  
**Owner:** TA  
**Input:** `Docs/00_CANON.md` §6 only (ten masters)  
**Definitions:** `Lib/06_Materials_Master/*.json`  
**NightMix demo spec:** `Lib/06_Materials_Master/NIGHTMIX_DEMO.md`

Blender MCP was not available at write time. These are **master definitions** (parameters, defaults, cite rules). Node-group `.blend` builds follow the same contracts when MCP connects.

---

## 1. Shared contract (all 10)

| Parameter | Type | Range | Role |
|---|---|---|---|
| **BaseColor** | Color (RGBA) | 0–1 | Albedo / unlit color |
| **Roughness** | Float | 0–1 | Surface response (parity even on Unlit) |
| **Variation** | Float | 0–1 | Handmade breakup amount |
| **NightMix** | Float | **0–1** | Day→night **parameter + overlay** |
| **Emissive** | Color (RGBA) | 0–1 | Optional glow |

**Hard rule:** Night is **not** a second map set. Overlay = tint + desaturate + value multiply (and emissive multiply where noted). Runtime driver: GameState time float → `NightMix`.

**Naming:** Masters `M_*`. Instances `MI_*` / `M_*_Inst_*`. Blender node groups `NG_M_*`.

**Instances allowed in brief:** grass dry/lush; wood painted/raw; spirit hurt/healed; nurtured on/off — all as instances of the ten masters below. No 11th master.

---

## 2. Defaults + allowed instance tweaks

### 2.1 M_StylizedGrass

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.35, 0.55, 0.22)` | Dry amber ↔ lush green within palette |
| Roughness | `0.85` | 0.6–1.0 |
| Variation | `0.35` | Amount only |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Keep off |

**May cite:** island top ground, garden edge grass, PCG grass homestead/forest, path floor clumps.

### 2.2 M_CliffRock

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.42, 0.36, 0.30)` | Warm/cool within cliff palette |
| Roughness | `0.78` | 0.55–0.95 |
| Variation | `0.45` | Strata contrast |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Keep off |

**May cite:** `SM_Cliff`, loose rock / RES_STONE world, ledge trim, lookout shelves.

### 2.3 M_WoodCabin

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.55, 0.38, 0.24)` | Painted ↔ raw |
| Roughness | `0.72` | Paint lower / raw higher (0.45–0.90) |
| Variation | `0.30` | Grain / plank seams |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Warm only on window/lantern glass instances |

**May cite:** cabin modular kit (wall, roof, chimney, door, window, porch), painted workbench, drying-rack posts, glider-perch cabin wood.

**Reject:** dark cabin windows.

### 2.4 M_WoodWild

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.28, 0.20, 0.14)` | Bark ↔ cut-face lighten |
| Roughness | `0.88` | 0.65–1.0 |
| Variation | `0.40` | Bark / lichen flecks |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Keep off |

**May cite:** pine trunks/branches, RES_WOOD world, firewood/plank stored (raw), lookout wild posts.

### 2.5 M_FoliageCard

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.22, 0.42, 0.20)` | Foliage palette only |
| Roughness | `0.80` | 0.55–0.95 |
| Variation | `0.35` | Per-card noise |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Keep off (spirit glow → other masters) |
| Opacity | masked | Clip threshold tweak OK |

**May cite:** pine needle/canopy cards, fern/vine/flax cards, distant pine instances.

### 2.6 M_PathStone

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.48, 0.44, 0.38)` | Path palette |
| Roughness | `0.82` | 0.60–0.95 |
| Variation | `0.40` | Pack A/B/C |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Keep off |

**May cite:** path stone 3-pack, `SM_LandingCircle` stone ring, homestead/forest path stones, stored path-stone proxies.

### 2.7 M_GatherHerb

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.40, 0.58, 0.28)` | Herb / berry / fiber leaf-fruit tints |
| Roughness | `0.75` | Leaf matte ↔ berry glossier |
| Variation | `0.30` | Cluster breakup |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Weak interact hint only if AD approves |

**May cite:** herb cluster, berry bush, fern/vine/flax gather proxies, stored plant parts (tint).

**Night crop / spirit seed tended:** use **M_Nurtured**, not a new herb set.

### 2.8 M_BeastStylized

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.62, 0.48, 0.36)` | State tints (wild→bonded) |
| Roughness | `0.70` | 0.40–0.90 |
| Variation | `0.35` | Coat + tame-mark read |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | black | Optional low eye / tame-mark |

**May cite:** single MVP beast (`SK_Beast_MVP`), pad paint if needed, tame-mark slot.

**Reject:** extra beasts, combat shaders.

### 2.9 M_SpiritUnlit

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.55, 0.72, 0.95)` | Hurt ↔ healed |
| Roughness | `1.0` | Parity only (Unlit ignores) |
| Variation | `0.25` | Soft fringe |
| NightMix | `1.0` | Dim by day; peak at night |
| Emissive | `(0.45, 0.70, 1.0)` | **Primary** — hurt low/cool, healed warm bloom |

**May cite:** 3 spirits, spirit-wound accents, shrine portal socket glow, `Lib/07_Night_SpiritLayer`.

**Rule:** hurt vs healed = instance state, not new mesh family.

### 2.10 M_Nurtured

| Param | Default | Allowed instance tweaks |
|---|---|---|
| BaseColor | `(0.45, 0.62, 0.30)` | Crop ↔ stored material tint |
| Roughness | `0.70` | 0.40–0.95 |
| Variation | `0.30` | Growth breakup |
| NightMix | `0.0` | Runtime / LIT |
| Emissive | `(0.15, 0.35, 0.18)` | **On** when nurtured; near-black when off |

**May cite:** planter crop (nurture target 1), stored-material nurture target, RES_SEED day plant → night crop instance.

**Reject:** third nurture master, crafting-tree shaders.

---

## 3. Mesh → master cite matrix (MVP)

| Mesh / kit family | Master |
|---|---|
| Island top / ground grass | M_StylizedGrass |
| Cliff / ledge rock | M_CliffRock |
| Cabin modular wood | M_WoodCabin |
| Pine trunk / RES_WOOD | M_WoodWild |
| Pine cards / canopy | M_FoliageCard |
| Path 3-pack / landing ring | M_PathStone |
| Herb / berry / fiber gather | M_GatherHerb |
| Single beast | M_BeastStylized |
| Spirits / shrine portal glow / spirit layer | M_SpiritUnlit |
| Nurture crop + tended store / spirit seed night | M_Nurtured |

Every later mesh **must** cite one of these ten on this sheet. Unique shaders are deleted and replaced with a master instance.

---

## 4. Export notes (UE later)

| Topic | Rule |
|---|---|
| Units | **Meters**. Adult 1.8 m; cabin 5–6 m; island 18–24 m; pines 6–12 m. Apply scale. |
| Axis | Blender → UE FBX: **-Y Forward, Z Up** (UE FBX import preset). Origins at ground contact. |
| Materials | One UE master material per `M_*`. Instances only for variants. Parameter names match this sheet (`BaseColor`, `Roughness`, `Variation`, `NightMix`, `Emissive`). |
| Night | Single scalar `NightMix` from GameState / time-of-day; material function overlay — **no** `_Night` texture sets. |
| Foliage | `M_FoliageCard` → masked MI; foliage tool / PCG after P2. |
| Unlit | `M_SpiritUnlit` → Unlit or emissive-only path; still expose the five params for API parity. |
| LODs | TA owns LOD policy; masters stay shared across LODs (no per-LOD unique shader). |
| Nanite / Lumen | After P2 + P3 cabin kit; do not invent materials for UE lighting. |
| Prefixes | `M_` material, `SM_` static, `SK_` skeletal, `FX_`, `PCG_`, `BP_`, `CAM_`, `LIT_`. |

---

## 5. Count lock

Exactly **10** masters. No 11th. Photoreal scans, grimdark, sci-fi kits, and one-off shaders are hard rejects per canon.
