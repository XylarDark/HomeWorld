# Lib/05_Spirits — CHA kit (WAVE 4 / P5)

**ID:** P5_CHA_life  
**Date:** 2026-09-16  
**Role:** CHA (spirit wisps)  
**Status:** DONE (Blender Lab MCP — placeholders in `blender/floating_island_homestead_LIB.blend`)  
**Blender collection:** `05_Spirits` (also linked into `07_Night_SpiritLayer` for NightMix visibility)  
**Inputs (read-only):** `Docs/00_CANON.md`, `Docs/01_GDD_MVP.md` §7, `Docs/02_MATERIAL_SHEET.md` (§2.9 M_SpiritUnlit), `Lib/06_Materials_Master/M_SpiritUnlit.json`

---

## Purpose

Three heal targets for night Verb V6. Hurt vs healed is an **M_SpiritUnlit** state (emission/color), not a new mesh family or 11th master.

---

## Assets in blend

| Name | State instance | Placement |
|---|---|---|
| `SK_Spirit_01_Hurt` | `M_SpiritUnlit_Hurt` | Near `SM_SpiritWound_01` |
| `SK_Spirit_02_Hurt` | `M_SpiritUnlit_Hurt` | Near wound |
| `SK_Spirit_03_Hurt` | `M_SpiritUnlit_Hurt` | Near wound |
| `SK_Spirit_01_Healed` | `M_SpiritUnlit_Healed` | Near `SM_Shrine_Homestead` (hopeful home glow) |
| `SK_Spirit_02_Healed` | `M_SpiritUnlit_Healed` | Near homestead shrine |
| `SK_Spirit_03_Healed` | `M_SpiritUnlit_Healed` | Near homestead shrine |
| `SOCKET_Heal_SK_Spirit_*` | EMPTY | Per-wisp heal interact |

**Lookdev split:** 3 hurt at planet wound + 3 healed at homestead shrine so both states read in one file. Runtime may use **one mesh ×3** with hurt→healed material-state swap (GDD §7); these six are state exemplars, not six unique spirit species.

### State instance params (cite master `M_SpiritUnlit`)

| Instance | BaseColor | Emissive | Strength |
|---|---|---|---|
| `M_SpiritUnlit_Hurt` | cooler thinner `(0.35, 0.45, 0.70)` | `(0.25, 0.40, 0.75)` | ~0.9 |
| `M_SpiritUnlit_Healed` | sheet default `(0.55, 0.72, 0.95)` | warmer bloom `(0.55, 0.78, 1.0)` | ~3.2 |

Custom props: `spirit_state=hurt|healed`, `master_cite=M_SpiritUnlit`.

---

## Verb hooks

| Verb | Objects | Notes |
|---|---|---|
| V6 Heal ×3 | `SK_Spirit_0{1,2,3}_Hurt` + heal sockets | Night/spirit; consume RES_HERB (or RES_SEED); flip to healed emissive |
| V5 Portal cue | Healed wisps near shrine | Soft spirit arrival read for Shot 5 — not sci-fi |

---

## Rules

- Exactly **three** heal targets. No fourth spirit.
- Hurt/healed = same master family; instances only.
- Night-visible via `07_Night_SpiritLayer` + NightMix; day may hide layer.
- No combat VFX, no capture minigame, no hologram kits.

## Handoff

`Docs/handoffs/P5_CHA_life.md`
