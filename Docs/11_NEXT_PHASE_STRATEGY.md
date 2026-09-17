# Docs/11 — Next-Phase Strategy

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — awaiting Lead **`APPROVE Docs/11`** (or **`APPROVE NEXT PHASE STRATEGY`**) |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Parent closed tracks** | [07_VERTICAL_SLICE_SIGN OFF.md](07%20_VERTICAL_SLICE_SIGN%20OFF.md) (P7 CLOSED), [08_AUDIT_SIGN_OFF.md](08_AUDIT_SIGN_OFF.md) (WAVE A–F SIGNED OFF), [10_POST_AUDIT_WRAP.md](10_POST_AUDIT_WRAP.md) (post-audit wrap CLOSED) |
| **Scope authority** | [01_GDD_MVP.md](01_GDD_MVP.md), [02_ART_BIBLE.md](02_ART_BIBLE.md), [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md), [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md), [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md), [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md), [04_UE_HANDOFF_NOTES.md](04_UE_HANDOFF_NOTES.md) |

---

## Why

The signed MVP vertical slice (P0–P7), audit WAVE A–F, and post-audit wrap (Docs/05/06/09 + ten NightMix masters) are **closed**. UE now has imported FBX, VS_MVP markers, FALLBACK glide + portal contracts, and master-material automation — but **lookdev assignment**, **form/day-night polish**, and **SYS verbs V3–V8** remain unimplemented in playable UE.

This document proposes **Lead-gated Next Phase (NP-*) waves** to close the gap between **what exists in UE** and **what Docs/03 verbs + Docs/02 materials require**, without reopening Docs/07 or inventing scope beyond existing canon.

**Do not start NP-A implementation until Lead types approval on this doc.**

---

## Board status

| Track | Status |
|-------|--------|
| **Docs/07** vertical slice | **SIGNED CLOSED** — do not reopen |
| **Docs/08** audit WAVE A–F | **SIGNED OFF** |
| **Docs/10** post-audit wrap | **CLOSED** (master graphs + NightMix wiring) |
| **Docs/11** next phase | **DRAFT** — this document |
| **NP-A … NP-E** | **NOT STARTED** — blocked until Lead **`APPROVE Docs/11`** then per-phase **`APPROVE NP-*`** |

---

## Repo map (current UE vs canon)

| Layer | Current state | Canon target |
|-------|---------------|--------------|
| **Meshes** | FBX imported under `/Game/HomeWorld/Meshes/…`; dress script at markers ([06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md)) | [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md) paths + cite matrix |
| **Materials** | Ten `M_*` master graphs via `create_master_materials.py`; NightMix from `MPC_HomeWorld_Time` | [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) §3 cite matrix; `MI_*` instances only |
| **Transit** | FALLBACK CRUMB glide + dual shrine portal (Docs/09, PR #19/#20) | [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) V2/V5 — no free-flight |
| **Form / TOD** | `TimeOfDaySubsystem` NightMix phases partial | Body↔spirit at dusk/dawn; spirit layer visibility ([03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) §4, §7) |
| **SYS verbs** | Not implemented in UE | [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) — 6-slot inventory, gather ×6, tame SM, heal ×3, nurture ×2 |
| **Walk / spawn** | Markers exist; GameMode pawn / bounds soft | V1 walk + `GP_PlayerStart`; soft pushback off island |

NP-A inventory will tag each row **KEEP** | **UPGRADE** | **DEFER** with evidence paths.

---

## NP plan (Lead gates each)

Each **NP-*** phase completes with a deliverable and requires **Lead approval** before implementation PRs merge and before the next NP starts.

Naming: **NP-A … NP-E** (Next Phase). Do **not** reuse WAVE A–F ids.

### NP-A — Inventory / gap map

Map UE content, C++/BP/Python, and dressed VS_MVP state against Docs/03 eight verbs and Docs/02 material cite matrix.

| Item | Spec |
|------|------|
| **Inputs** | `/Game/HomeWorld/…` asset audit (meshes, materials, maps), `Source/HomeWorld/`, `Content/Python/` VS_MVP scripts, PIE harness results |
| **Outputs** | Per-verb and per-mesh-family table: exists / partial / missing; material assigned vs default; disposition **KEEP** \| **UPGRADE** \| **DEFER** |
| **Deliverable** | [11a_INVENTORY.md](11a_INVENTORY.md) — created **after** Lead `APPROVE Docs/11`; stub not required in DRAFT |
| **Gate** | Lead **`APPROVE NP-A`** before any UPGRADE implementation |

### NP-B — Lookdev apply

Assign the ten masters (or `MI_*` instances) onto dressed VS_MVP meshes per [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) §3 cite matrix. Smoke NightMix phase transitions (Day → Dusk → Night → Dawn) on dressed geometry.

| Item | Spec |
|------|------|
| **Scope** | Material assignment on `place_vs_mvp_dress.py` spawned meshes; window emissive `MI_*` where cited; no new masters |
| **Out** | PCG foliage tool pass, hero lighting beauty, Nanite/Lumen |
| **Deliverable** | Assignment table in 11a or NP-B handoff; optional `Docs/handoffs/NP_B_LOOKDEV.md`; screenshot evidence on Windows host |
| **Gate** | Lead **`APPROVE NP-B`** |

### NP-C — Form + V1 polish

Body↔spirit form swap at dusk/dawn with NightMix + spirit-layer visibility. Ensure `GP_PlayerStart` / GameMode default pawn and soft walk bounds if missing.

| Item | Spec |
|------|------|
| **Scope** | [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) §3–§4, §7 — form flag, NightMix 0↔1, spirit layer; V1 walk volumes / soft pushback |
| **Out** | Free-flight, flight HUD, combat, inventory (SYS) |
| **Deliverable** | Form swap + walk evidence (PIE log / short capture); updates to gameplay handoff if needed |
| **Gate** | Lead **`APPROVE NP-C`** |

### NP-D — SYS verbs V3–V4

Six-slot inventory + gather ×6 + beast tame state machine — **day/body only** per [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md).

| Item | Spec |
|------|------|
| **Verbs** | V3 Gather (six `RES_*`), V4 Encounter/tame (`wild` → `cautious` → `tamed` → optional `helper`) |
| **Rules** | Exactly 6 slots, stack max 9, no 7th resource; day/body gates; no combat |
| **Deliverable** | C++ GameState or subsystem + minimal interact wiring; PIE/log evidence for one full gather + tame offer path |
| **Gate** | Lead **`APPROVE NP-D`** |

### NP-E — SYS verbs V6–V8

Heal ×3, nurture ×2, dawn/return persist hooks — **night/spirit**; portal night-gate optional if already partially wired.

| Item | Spec |
|------|------|
| **Verbs** | V6 heal (3 spirits), V7 nurture (2 targets → `M_Nurtured`), V8 return/dawn + optional persist of inventory/tame/nurture |
| **Rules** | Night/spirit only for heal/nurture; spend `RES_HERB` / `RES_SEED` / `RES_BERRY` per SYS tables; portal night-gate aligns with [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) V5 |
| **Deliverable** | Night loop demo path evidence; persist hooks documented (save optional MVP) |
| **Gate** | Lead **`APPROVE NP-E`** |

---

## Hard rules (every NP phase)

These apply to **all** NP-* work. Violations block merge.

| Rule | Source |
|------|--------|
| **Docs/07 CLOSED** — do not reopen vertical-slice sign-off or PHASE_BOARD P0–P7 | [07_VERTICAL_SLICE_SIGN OFF.md](07%20_VERTICAL_SLICE_SIGN%20OFF.md) |
| **FALLBACK FLIGHT armed** — scripted CRUMB glide only; **no free-flight**, no flight HUD | [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) FALLBACK appendix |
| **No combat** — no HP, weapons, aggro, conversion combat depth | [01_GDD_MVP.md](01_GDD_MVP.md), [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) |
| **No Lumen/Nanite as gates** — deferred per Docs/04 | [04_UE_HANDOFF_NOTES.md](04_UE_HANDOFF_NOTES.md) |
| **No committing `.uasset` / `.umap`** — Editor-built binaries stay local on Windows host | [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md), [10_POST_AUDIT_WRAP.md](10_POST_AUDIT_WRAP.md) |
| **Exactly 10 masters** — no 11th master or unique shader families | [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) §5 |
| **Lead APPROVE each NP-*** before that phase's implementation PR | This doc |
| **Scope ceiling** — do not invent features beyond Docs/02–04, Docs/03_GAMEPLAY, Docs/03_SYSTEMS | Lead directive |

---

## Explicit DEFER (not in NP-A…E unless Lead renames)

| Item | Reason |
|------|--------|
| Full forest PCG / new biomes | Off-slice; legacy PCG removed in WAVE F |
| Nanite / Lumen beauty passes | Docs/04 — later, not MVP gates |
| Crafting / 7th resource / combat systems | [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) explicit out-of-scope |
| Reopening Docs/07 for free-flight or interactive glide | Lead CLOSED + FALLBACK armed |
| Mass/family agents, State Tree, DemoMap/Homestead maps | WAVE F quarantine; not MVP slice |
| New locations, props, or master shader families | [02_ART_BIBLE.md](02_ART_BIBLE.md) out-of-scope |

NP-A inventory may tag additional **DEFER** rows with evidence; implementation PRs must not expand scope without a new Lead-gated doc.

---

## Approval gate

```
Docs/11 status: DRAFT — awaiting Lead APPROVE Docs/11
Do NOT start NP-A implementation until Lead types approval in chat or PR.
After Docs/11 approval: gate each NP-* separately before implementation.
```

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 1 | **`APPROVE Docs/11`** or **`APPROVE NEXT PHASE STRATEGY`** | NP-A inventory work; create `Docs/11a_INVENTORY.md` |
| 2 | **`APPROVE NP-A`** | NP-B lookdev PRs |
| 3 | **`APPROVE NP-B`** | NP-C form + walk PRs |
| 4 | **`APPROVE NP-C`** | NP-D gather + tame PRs |
| 5 | **`APPROVE NP-D`** | NP-E heal + nurture + dawn PRs |
| 6 | **`APPROVE NP-E`** | Next strategy doc or MVP ship review (Lead choice) |

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) | **Complete** — audit closed; NP-* is post-audit product execution |
| [10_POST_AUDIT_WRAP.md](10_POST_AUDIT_WRAP.md) | **Closed** — masters + NightMix; NP-B assigns them to meshes |
| [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) | Runbook NP-B builds on; dress without lookdev is NP-A finding |
| [09_FALLBACK_GLIDE.md](09_FALLBACK_GLIDE.md) | Transit **KEEP** — NP phases do not replace glide/portal contracts |

---

*Conductor prepared this file; Lead approval required before NP-A execution.*
