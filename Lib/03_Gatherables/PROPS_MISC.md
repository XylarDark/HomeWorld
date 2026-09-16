# PROPS_MISC.md — lantern, drying rack, workbench

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP  
**Materials:** **M_WoodCabin** / **M_WoodWild** (+ warm emissive glass instance of **M_WoodCabin** for lantern per material sheet §2.3)

---

## 1. Lantern — `SM_Lantern_Homestead`

| Field | Spec |
|---|---|
| Size | ~0.25 × 0.25 × 0.45 m |
| Origin | Hang pivot or ground-stake contact (document chosen pivot in mesh) |
| Body | **M_WoodCabin** (or metal-tint via BaseColor instance — still M_WoodCabin, no 11th master) |
| Glass / flame card | **M_WoodCabin** instance with warm **Emissive** (~cabin amber; sheet allows warm on window/lantern glass) |
| Placement | Porch / path edge / near shrine approach — supports Shot 2 warm accents; LIT owns moon/window hero |

**Sockets:** `SOCKET_Hang`, `SOCKET_Emissive`

**Reject:** Dark / dead lantern at night; sci-fi LED bar; photoreal oil-lamp scan.

---

## 2. Drying rack — `SM_DryingRack`

| Field | Spec |
|---|---|
| Size | ~1.4 × 0.5 × 1.6 m |
| Origin | Ground contact under posts |
| Posts / rails | **M_WoodCabin** (sheet: drying-rack posts) |
| Hangables | Berry / herb / fiber cord proxies — **M_GatherHerb** or stored mesh children |
| Role | Homestead store surface; may host `SM_RES_FIBER_Stored` / `SM_RES_BERRY_Stored` / `SM_RES_HERB_Stored` |

**Sockets:** `SOCKET_Hang_A/B/C`, `SOCKET_Interact`, `SOCKET_Nurture` (if N2 uses fiber cord instead of wood pile)

Handmade A-frame or post-and-rail; not industrial scaffold.

---

## 3. Workbench — `SM_Workbench`

| Field | Spec |
|---|---|
| Size | ~1.2 × 0.6 × 0.9 m (top ~0.75–0.85 m height) |
| Origin | Ground contact |
| Top / legs | **M_WoodCabin** (sheet: painted workbench) |
| Optional tool block | **M_WoodWild** or **M_PathStone** (tool head visual only — **no crafting tree**) |
| Role | Homestead cozy prop + optional store proximity; MVP has **no recipe web** |

**Sockets:** `SOCKET_Interact` (flavor / future), `SOCKET_Surface` (small stored props)

**Reject:** Full crafting UI bench, anvil combat station, sci-fi fabricator.

---

## Placement intent

Cluster near cabin / garden / path without blocking `SM_Path_Homestead` walk. Readable in Shot 2 mid/close. Night: lantern emissive supports warm-vs-cool; windows remain LIT/ENV-H cabin responsibility — PROP lantern must not replace window bloom.

---

## Glider perch note

`SM_Glider_Perch` is **ENV-H** (lookout + perch kit), not authored here. Transit departure crumb references that volume; see `Lib/08_Transit/GLIDE_SPLINE.md`. PROP only publishes landing mesh ref under Lib/08.
