# GATHERABLES_WORLD_STORED.md — six resources World + Stored

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP  
**Canon:** `Docs/00_CANON.md` §4  
**GDD:** `Docs/01_GDD_MVP.md` §5 (gather/store), §8 (nurture N2), §10 (inventory)

Each resource has **World** (planet day gather node) and **Stored** (homestead store prop) meshes. Naming: `SM_RES_<TYPE>_World` / `SM_RES_<TYPE>_Stored`.

---

## Naming lock

| RES_ID | Resource | World mesh | Stored mesh |
|---|---|---|---|
| RES_WOOD | Wood | `SM_RES_WOOD_World` | `SM_RES_WOOD_Stored` |
| RES_FIBER | Fiber | `SM_RES_FIBER_World` | `SM_RES_FIBER_Stored` |
| RES_STONE | Stone | `SM_RES_STONE_World` | `SM_RES_STONE_Stored` |
| RES_BERRY | Forage fruit | `SM_RES_BERRY_World` | `SM_RES_BERRY_Stored` |
| RES_HERB | Herb | `SM_RES_HERB_World` | `SM_RES_HERB_Stored` |
| RES_SEED | Spirit seed | `SM_RES_SEED_World` | `SM_RES_SEED_Stored` |

No seventh resource. Inventory holds RES_IDs only (6 slots).

---

## World meshes (day gather)

| Mesh | Read | Size guide (m) | Master | Interact |
|---|---|---|---|---|
| `SM_RES_WOOD_World` | Branch / choppable pine node | ~1.2 × 0.4 × 1.0 | **M_WoodWild** (+ foliage card child OK → **M_FoliageCard**) | Day Use → +1 Wood; deplete/cooldown until dawn |
| `SM_RES_FIBER_World` | Fern / vine / flax cluster | ~0.8 × 0.8 × 0.7 | **M_GatherHerb** (+ **M_FoliageCard** cards OK) | Day Use → +1 Fiber |
| `SM_RES_STONE_World` | Loose rock pile | ~0.6 × 0.6 × 0.35 | **M_CliffRock** | Day Use → +1 Stone |
| `SM_RES_BERRY_World` | Berry bush | ~0.9 × 0.9 × 0.9 | **M_GatherHerb** (fruit tint instance) | Day Use → +1 Berry; also tame offer food |
| `SM_RES_HERB_World` | Herb cluster | ~0.7 × 0.7 × 0.45 | **M_GatherHerb** | Day Use → +1 Herb; heal / tame sink |
| `SM_RES_SEED_World` | Faint day plant (rare) | ~0.4 × 0.4 × 0.35 | **M_GatherHerb** day; night crop path → **M_Nurtured** | Day Use → +1 Seed; nurture crop input |

**World rules**

- Origin at ground contact. Readable silhouette at stroll distance.
- Place along planet path / first-harvest zone (`SM_Gather_FirstHarvest` marker) — WLD/ENV-P place instances; PROP authors meshes.
- Night/spirit: gather disabled (GDD V3). Soft cool-down or depleted visual; no second night mesh set.
- Optional weak interact hint emissive on **M_GatherHerb** only if AD approves (sheet §2.7).

---

## Stored meshes (homestead)

| Mesh | Read | Size guide (m) | Master | Store / nurture |
|---|---|---|---|---|
| `SM_RES_WOOD_Stored` | Firewood / plank pile | ~1.0 × 0.6 × 0.5 | **M_WoodWild** (raw) | Default **N2** nurture target (GDD §8); night Use → **M_Nurtured** on |
| `SM_RES_FIBER_Stored` | Cord on rack / basket | ~0.5 × 0.4 × 0.6 | **M_GatherHerb** tint + rack wood **M_WoodCabin** | Visual store; alternate N2 if wood not used |
| `SM_RES_STONE_Stored` | Path-stone / tool-head pile | ~0.6 × 0.5 × 0.35 | **M_PathStone** | Visual store only |
| `SM_RES_BERRY_Stored` | Bowl / drying rack fruit | ~0.35 × 0.35 × 0.25 | **M_GatherHerb** | Visual store; rack may share `SM_DryingRack` |
| `SM_RES_HERB_Stored` | Poultice bundle / shelf | ~0.3 × 0.25 × 0.35 | **M_GatherHerb** | Visual store |
| `SM_RES_SEED_Stored` | Seed pouch / planter waiting | ~0.25 × 0.25 × 0.2 | **M_Nurtured** when tended; else **M_GatherHerb** | Feeds N1 crop; not a third nurture type |

**Store rules:** Homestead-only. Transfer 1 inventory unit → Stored count++. Count may drive simple mesh visibility / stack cards — no crafting tree.

**N2 note:** Default nurtured stored prop = `SM_RES_WOOD_Stored` (or fiber cord on `SM_DryingRack` — pick one in dress; default wood pile per GDD). Apply **M_Nurtured** on success.

---

## Sockets (all World + Stored)

| Socket | Purpose |
|---|---|
| `SOCKET_Interact` | SYS gather/store overlap (~1.0–1.5 m radius attach) |
| `SOCKET_FX_Pickup` | Optional gather spark (handmade, not sci-fi) |
| `SOCKET_Count` (Stored) | Optional stack card / count proxy attach |

---

## First-harvest lookout test

World instance of at least one gatherable (prefer berry or herb) must remain pointable from lookout near graybox `SM_Gather_FirstHarvest` (5.0, −88.0, −95.0). PROP does not move that marker.

---

## Rejects

- Extra RES types or merged IDs
- Photoreal produce scans
- Crafting bench outputs as new resource meshes
- Combat loot bags
- Unique shaders per berry color — use **M_GatherHerb** instances only
