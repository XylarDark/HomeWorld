# Lead proposal — Prototype flat-material → HomeWorld master mapping

| Field | Value |
|-------|-------|
| **Status** | **PROPOSAL ONLY** — do **not** assign until Lead approves |
| **Date** | 2026-10-05 ET |
| **Context** | Post-`60dc2bd` import cleanup. Revert of 104 churned `.uasset`s landed as `ee32ea1`. New prototype meshes/materials kept. |
| **Canon** | [docs/02_MATERIAL_SHEET.md](../02_MATERIAL_SHEET.md) — exactly **10** masters under `/Game/HomeWorld/Materials/Masters/` |
| **Rule** | Flat prefix-violating mats (`Cabin_*`, `Portal_*`, `Flowers_*`) must become `MI_*` instances of locked masters. No 11th master. |

---

## 1. Inventory — new flat / prefix-violating materials (kept from 60dc2bd)

### Cabin_* (Homestead mesh folder — should be MI_*, not orphan mats)

| New asset | Suggested master | Suggested MI name | Confidence | Notes |
|-----------|------------------|-------------------|------------|-------|
| `Cabin_BrownTimber` | `M_WoodCabin` | `MI_Cabin_BrownTimber` | **high** | Primary cabin wood — sheet §2.3 |
| `Cabin_LightWood` | `M_WoodCabin` | `MI_Cabin_LightWood` | **high** | Lighter plank / porch deck |
| `Cabin_DoorBrown` | `M_WoodCabin` | `MI_Cabin_DoorBrown` | **high** | Door — wood cabin cite |
| `Cabin_BandBrown` | `M_WoodCabin` | `MI_Cabin_BandBrown` | **med** | Accent band; same master, darker BaseColor |
| `Cabin_DarkSlate` | `M_WoodCabin` | `MI_Cabin_DarkSlate` | **med** | Likely roof A/B; cabin kit cites roof on WoodCabin. Alt: `M_CliffRock` if Lead wants stone roof |
| `Cabin_WarmAmber` | `M_WoodCabin` | `MI_Cabin_WindowWarm` | **high** | Window/lantern glass — sheet allows warm emissive on glass instances; also see existing `M_WoodCabin_Window` under Homestead |
| `Cabin_StoneGray` | `M_CliffRock` | `MI_Cabin_StoneGray` | **high** | Foundation / stone base |
| `Cabin_StoneCapGray` | `M_CliffRock` | `MI_Cabin_StoneCapGray` | **high** | Chimney / foundation cap |
| `Cabin_BlackIron` | `M_CliffRock` | `MI_Cabin_BlackIron` | **low** | Chimney iron / hardware. No metal master in the ten. Rough dark CliffRock tint is pragmatic; Lead may prefer WoodCabin dark or defer |
| `Cabin_TanCeramic` | `M_CliffRock` | `MI_Cabin_TanCeramic` | **med** | Chimney pot / ceramic trim — rock family |
| `Cabin_OliveHerb` | `M_GatherHerb` | `MI_Cabin_OliveHerb` | **high** | Hanging herbs on cabin |

### Portal_* (Gatherables mesh folder)

| New asset | Suggested master | Suggested MI name | Confidence | Notes |
|-----------|------------------|-------------------|------------|-------|
| `Portal_Crystal_Cyan` | `M_SpiritUnlit` | `MI_Portal_Crystal_Cyan` | **high** | Shrine portal glow — sheet §2.9 / §3 |
| `Portal_Crystal_LightCyan` | `M_SpiritUnlit` | `MI_Portal_Crystal_LightCyan` | **high** | Lighter crystal face |
| `Portal_Stone_Gray` | `M_CliffRock` | `MI_Portal_Stone_Gray` | **high** | Portal stone body |
| `Portal_Stone_Midgray` | `M_CliffRock` | `MI_Portal_Stone_Midgray` | **high** | Mid stone variant |
| `Portal_Stone_Lightgray` | `M_CliffRock` | `MI_Portal_Stone_Lightgray` | **med** | Could be `M_PathStone` if Lead wants path palette; default CliffRock |

### Flowers_* (Gatherables mesh folder)

| New asset | Suggested master | Suggested MI name | Confidence | Notes |
|-----------|------------------|-------------------|------------|-------|
| `Flowers_DarkGreen` | `M_GatherHerb` | `MI_Flowers_DarkGreen` | **high** | Foliage / leaf — herb master §2.7 |
| `Flowers_Olive` | `M_GatherHerb` | `MI_Flowers_Olive` | **high** | Leaf tint |
| `Flowers_Lilac` | `M_GatherHerb` | `MI_Flowers_Lilac` | **high** | Bloom tint (instance BaseColor) |
| `Flowers_Purple` | `M_GatherHerb` | `MI_Flowers_Purple` | **high** | Bloom tint |

### Duplicate masters dropped next to meshes (do not use as source of truth)

| New asset path | Action | Confidence | Notes |
|----------------|--------|------------|-------|
| `Meshes/Homestead/M_GatherHerb` | **Cite** `/Game/HomeWorld/Materials/Masters/M_GatherHerb` instead | **high** | Accidental re-import / sidecar; masters live under Materials/Masters |
| `Meshes/Homestead/M_Nurtured` | **Cite** `/Game/HomeWorld/Materials/Masters/M_Nurtured` instead | **high** | Same — do not treat mesh-folder copy as new master |

---

## 2. Mesh → master cite (new prototype statics)

| Mesh | Slot / part (guess from name) | Suggested master | Confidence | Notes |
|------|-------------------------------|------------------|------------|-------|
| `SM_Cabin_Prototype` | multi-slot wood | `M_WoodCabin` | **high** | Modular cabin kit |
| `SM_Cabin_Prototype` | stone / foundation | `M_CliffRock` | **med** | If slots exist for stone |
| `SM_Cabin_Prototype` | window glass | `M_WoodCabin` (emissive MI) or `M_WoodCabin_Window` | **med** | Confirm slots in Editor |
| `SM_Cabin_Prototype` | hanging herb | `M_GatherHerb` | **low** | Only if slot present |
| `SM_Cabin_CornerPosts` | wood | `M_WoodCabin` | **high** | |
| `SM_Cliff_CabinFace` | rock | `M_CliffRock` | **high** | Sheet §3 |
| `SM_Cliff_LookoutFace` | rock | `M_CliffRock` | **high** | |
| `SM_Cliff_Rear` | rock | `M_CliffRock` | **high** | |
| `SM_PathStone_A/B/C` | stone | `M_PathStone` | **high** | Sheet §2.6 / §3 |
| `SM_Planter_A/B/C` | box wood/stone | `M_WoodCabin` | **med** | Alt `M_CliffRock` if planter reads as stone |
| `SM_Planter_A/B/C` | crop / soil fill | `M_Nurtured` or `M_GatherHerb` | **med** | Nurture target → `M_Nurtured`; decorative herbs → `M_GatherHerb` |
| `SM_Garden_Fence_Seg` | wood | `M_WoodCabin` | **med** | Homestead dress wood; alt `M_WoodWild` if rustic |
| `SM_Portal_Prototype` | crystal / glow | `M_SpiritUnlit` | **high** | |
| `SM_Portal_Prototype` | stone frame | `M_CliffRock` | **high** | |
| `SM_Flowers_Prototype` | all slots | `M_GatherHerb` | **high** | MI tints for lilac/purple/olive |

**Existing modular cabin parts** (`SM_Cabin_Wall_*`, roof, porch, chimney, window, door, etc.) were **reverted** to pre-60dc2bd binaries in `ee32ea1`. Their prior master binds (if any) should still be the pre-import state. Do **not** re-bind until Lead approves this table. New placement (task C) uses the **new** prototypes (`SM_Cabin_Prototype`, `SM_Portal_Prototype`, `SM_Flowers_Prototype`, cliffs/planters/path/fence) at old transforms.

---

## 3. Unknowns / Lead decisions needed

1. **`Cabin_BlackIron`** — no metal master in the locked ten. Approve dark `M_CliffRock` MI, or leave unbound?
2. **`Cabin_DarkSlate`** — roof as `M_WoodCabin` (kit default) vs stone `M_CliffRock`?
3. **Planter body** — wood vs stone master?
4. **Fence** — `M_WoodCabin` vs `M_WoodWild`?
5. **`Portal_Stone_Lightgray`** — CliffRock vs PathStone?
6. **Mesh-folder `M_GatherHerb` / `M_Nurtured` copies** — delete/ignore after bind, or keep as redirects? Recommend ignore + cite Masters path only.
7. **Slot discovery** — exact FBX slot names on `SM_*_Prototype` not verified in this pass (needs Editor/OpenCode inspect). Mapping above is by asset name + art-bible cite matrix.

---

## 4. Explicit non-actions (this proposal)

- **Do not** assign materials to meshes until Lead approves (or amends) this table.
- **Do not** create an 11th master.
- **Do not** delete old level actors as part of material work.

---

## 5. Suggested approve string

Lead: `APPROVE MATERIAL MAP` (or amend rows, then approve).
