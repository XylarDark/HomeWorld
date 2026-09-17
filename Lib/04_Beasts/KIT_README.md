# Lib/04_Beasts — CHA kit (WAVE 4 / P5)

**ID:** P5_CHA_life  
**Date:** 2026-09-16  
**Role:** CHA (creatures / family blockouts)  
**Status:** DONE (Blender Lab MCP — placeholders in `blender/floating_island_homestead_LIB.blend`)  
**Blender collection:** `04_Beasts`  
**Inputs (read-only):** `Docs/00_CANON.md`, `Docs/01_GDD_MVP.md` §§6–7, `Docs/02_MATERIAL_SHEET.md` (§2.8 M_BeastStylized), `Lib/06_Materials_Master/M_BeastStylized.json`

---

## Purpose

Readable life at the homestead lookout + one tameable planet beast. Silhouettes / blockouts only — not photoreal, no combat anims, no extra fauna.

---

## Assets in blend

| Name | Type | Master / state | Placement |
|---|---|---|---|
| `SK_Family_Adult` | Mesh blockout | **M_WoodCabin** (silhouette read) | Lookout pad (~6.45, −3.35, 0) |
| `SK_Family_Child_A` | Mesh blockout | **M_WoodCabin** | Lookout (~7.35, −3.75, 0) |
| `SK_Family_Child_B` | Mesh blockout | **M_WoodCabin** | Lookout (~7.85, −3.3, 0) |
| `SK_Beast_Small` | EMPTY root | — | At `SM_BeastPad_01` (12, −108, −95) |
| `SK_Beast_Small_Body` | Mesh | **M_BeastStylized** | Child of root |
| `SK_Beast_Small_TameMark` | Mesh slot | **M_BeastStylized** | Shoulder tame-mark read |
| `SOCKET_TameMark` | EMPTY | — | Tame-mark socket |
| `SOCKET_Saddle` | EMPTY | — | Optional saddle |
| `SOCKET_GliderAttach` | EMPTY | — | Optional glider assist attach |
| `SOCKET_BeastInteract` | EMPTY | — | V4 interact volume |
| `SOCKET_BeastPerch` | EMPTY | — | On `SM_Glider_Perch` (optional perch socket) |

Replaced earlier cube stand-ins `SM_Silhouette_Family_0/1/2` with capsule family blockouts (adult + two children).

---

## Verb hooks (SYS / GP)

| Verb | Object | Notes |
|---|---|---|
| V4 Encounter / Tame | `SK_Beast_Small` + `SOCKET_BeastInteract` / `SOCKET_TameMark` | States wild → cautious → tamed → helper (SYS). Offer RES_BERRY / RES_HERB. |
| V2 assist (optional) | `SOCKET_Saddle` / `SOCKET_GliderAttach` | Constrained glide assist only — no free flight. |

Custom prop on root: `tame_state=wild`, `master_cite=M_BeastStylized`.

---

## Rules

- **One** beast only (`SK_Beast_Small`). No extra species.
- Family = lookout silhouettes for Shot 1 read — not playable pawns in MVP.
- Cite **M_BeastStylized** only for the beast (sheet §2.8). Family uses cabin wood for soft night silhouette.
- No combat animations, no damage shaders, no photoreal fur.

---

## Rejects

Extra beasts; combat; free-flight model; second tame-mark master; rewriting planet/homestead massing.

## Handoff

`Docs/handoffs/P5_CHA_life.md`
