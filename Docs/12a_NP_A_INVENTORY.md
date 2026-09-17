# Docs/12a — NP-A Inventory / Gap Map

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE NP-A`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Scope** | UE realization vs [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) + [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) + [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) |
| **Evidence base** | Repo scripts/C++ at `ae7f649`; Windows DESKTOP-21CT3H0 live counts (Conductor ~2026-09-17 03:01 ET) |

**Gate:** stop for Lead **`APPROVE NP-A`** before NP-B lookdev apply.

---

## Disposition legend

| Tag | Meaning |
|-----|---------|
| **KEEP** | Canon or landed substrate — do not delete or duplicate |
| **PRESENT** | Exists in repo scripts/C++ or on Windows Editor host (may be local-only `.uasset`) |
| **MISSING** | Spec requires it; not implemented or not verified in UE |
| **DEFER** | Explicitly out of NP scope — do not build in NP-A…E without Lead reopen |

---

## Windows DESKTOP-21CT3H0 live notes

Conductor measured on Windows host **DESKTOP-21CT3H0** at repo **HEAD `ae7f649`**, ~**2026-09-17 03:01 ET**. Cloud/Linux clone carries **scripts + JSON only** — no VS_MVP binaries in git.

| Asset area | Windows count | Repo (git) | Gap / note |
|------------|---------------|------------|------------|
| `/Game/HomeWorld/Meshes/Homestead/` | **≈49** `.uasset` | **0** (folder absent) | **PRESENT** on host; local-only |
| `/Game/HomeWorld/Meshes/Forest/` | **≈20** | **0** | **PRESENT** on host |
| `/Game/HomeWorld/Meshes/Gatherables/` | **≈41** | **0** | **PRESENT** on host |
| `/Game/HomeWorld/Meshes/Transit/` | **≈11** | **0** | **PRESENT** on host |
| `/Game/HomeWorld/Materials/Masters/` | **file count may be 0** after pulls | **0** | **PENDING** — masters are local-only; `create_master_materials.py` can recreate |
| `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` | **PRESENT** (Editor) | **0** `.umap` in git | **PRESENT** on host; volatile across clones |
| `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` | **PRESENT** (Editor) | **0** in git | Created by `place_vs_mvp_markers.py`; same volatility |
| Dress mesh material assignment | **Not done** | N/A | Scripts spawn meshes; **no MI assignment** — **NP-B** |

### Content binary volatility (NP-B blocker call-out)

Per project policy, **no `.uasset`/`.umap` commits**. Windows Editor holds the authoritative VS_MVP state. After `git pull`, masters, MPC, and `L_VS_MVP_Markers` may be **missing or stale** until automation re-runs:

1. `batch_import_asset_creation.py` → Meshes categories  
2. `place_vs_mvp_markers.py` → markers + MPC  
3. `place_vs_mvp_dress.py` → DRESS_* kit  
4. `create_master_materials.py` → ten masters  
5. `place_fallback_glide_markers.py` → GP_GlideStart + portal triggers  

**NP-B** must treat **recreate + assign** as first-class work, not assume binaries survive pulls.

---

## C++ substrate (repo — KEEP / PRESENT)

| Component | Path | Disposition | NP phase |
|-----------|------|-------------|----------|
| Character + Enhanced Input | `Source/HomeWorld/HomeWorldCharacter.*` | **PRESENT** — walk, harvest trace, glide/portal hooks | NP-C (walk polish) |
| FallbackGlide | `HomeWorldFallbackGlideComponent.*` | **PRESENT** — CRUMB_* scripted glide, day gate | Verify PIE (NP-A evidence) |
| ShrinePortal + Trigger | `HomeWorldShrinePortalComponent.*`, `HomeWorldShrinePortalTrigger.*` | **PRESENT** — Homestead↔Return, night gate | Verify PIE |
| TimeOfDaySubsystem | `HomeWorldTimeOfDaySubsystem.*` | **PRESENT** — phase CVar + NightMix → MPC | NP-C/E |
| InventorySubsystem | `HomeWorldInventorySubsystem.*` | **PRESENT** stub — `Wood`/`Ore`/`Flowers`, not RES_* six-slot | NP-D |
| HealAbility | `HomeWorldHealAbility.*` | **PRESENT** minimal stub — log only | NP-E |
| Harvest / yield | `HomeWorldResourcePile.*`, `HomeWorldYieldNode.*`, `TryHarvestInFront` | **PRESENT** partial — legacy types, not SYS tables | NP-D |
| Tame / nurture | — | **MISSING** — no C++ | NP-D / NP-E |

---

## Python automation (repo — KEEP)

| Script | Purpose | Disposition |
|--------|---------|-------------|
| `place_vs_mvp_markers.py` | 28 TargetPoints + `MPC_HomeWorld_Time` | **KEEP** / **PRESENT** (script) |
| `place_vs_mvp_dress.py` | DRESS_* kit at JSON anchors | **KEEP** / **PRESENT** (script; assignment not done) |
| `place_fallback_glide_markers.py` | `GP_GlideStart`, `GP_PortalA/B` | **KEEP** / **PRESENT** (script) |
| `create_master_materials.py` (+ stub) | Ten Docs/02 masters under `/Materials/Masters/` | **KEEP** / **PRESENT** (script) |
| `wire_nightmix_mpc_note.py` | NightMix phase table + MPC ensure log | **KEEP** / **PRESENT** (script) |
| `batch_import_asset_creation.py` | FBX → Meshes categories | **KEEP** / **PRESENT** |
| `create_ga_heal.py`, harvest BPs | Legacy GA/BP creators | **KEEP** — pre-SYS; superseded by NP-D/E |

**JSON canon:** `Lib/06_Materials_Master/M_*.json` (10 files) — **KEEP**.  
**Export staging:** `AssetCreation/Exports/` (18 FBX/GLB in repo) — **KEEP**; Windows has full import set.

---

## Materials ×10 vs Docs/02

| Master | Docs/02 | Script def | Windows `.uasset` | Assigned on dress meshes |
|--------|---------|------------|-------------------|--------------------------|
| M_StylizedGrass | **KEEP** | **PRESENT** | **PENDING** (may be 0) | **MISSING** |
| M_CliffRock | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_WoodCabin | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_WoodWild | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_FoliageCard | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_PathStone | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_GatherHerb | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_BeastStylized | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_SpiritUnlit | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |
| M_Nurtured | **KEEP** | **PRESENT** | **PENDING** | **MISSING** |

**Summary:** Script + JSON = **PRESENT**. Runtime masters and mesh MI assignment = **MISSING** until NP-B on Windows.

---

## Eight verbs — required table

| Verb | Docs status | UE status | Gap | NP phase |
|------|-------------|-----------|-----|----------|
| **V1 Walk** | Spec done ([03_GAMEPLAY_MVP](03_GAMEPLAY_MVP.md) §3) | Partial — `AHomeWorldCharacter`, nav not VS_MVP-bound | Soft bounds, `GP_PlayerStart` dress | **NP-C** |
| **V2 Glide** | **FALLBACK** ([09_FALLBACK_GLIDE](09_FALLBACK_GLIDE.md)) | C++ landed — `HomeWorldFallbackGlideComponent` | Verify PIE / GP markers on host | **NP-C** (verify) |
| **V3 Gather** | SYS tables ([03_SYSTEMS_MVP](03_SYSTEMS_MVP.md) §2–3) | Not in UE — legacy harvest only | RES_* six-slot + world nodes | **NP-D** |
| **V4 Tame** | SYS ([03_SYSTEMS_MVP](03_SYSTEMS_MVP.md) §5) | Not in UE | Beast SM + food spend SM | **NP-D** |
| **V5 Portal** | **FALLBACK** ([03_GAMEPLAY_MVP](03_GAMEPLAY_MVP.md) §6) | C++ landed — shrine portal + trigger | Verify PIE / night gate | **NP-C** (verify) |
| **V6 Heal** | SYS ([03_SYSTEMS_MVP](03_SYSTEMS_MVP.md) §6) | Not in UE — stub GA only | ×3 spirits, herb/seed spend | **NP-E** |
| **V7 Nurture** | SYS ([03_SYSTEMS_MVP](03_SYSTEMS_MVP.md) §7) | Not in UE | N1/N2 + `M_Nurtured` flag | **NP-E** |
| **V8 Dawn/form** | Spec ([03_GAMEPLAY_MVP](03_GAMEPLAY_MVP.md) §4, §7) | Partial — TimeOfDay + NightMix stub | Body↔spirit swap, persist | **NP-C/E** |
| **Materials ×10** | Script+JSON ([02_MATERIAL_SHEET](02_MATERIAL_SHEET.md)) | Masters may need recreate + assign | Content volatility + no MI on dress | **NP-B** |

---

## Gap map by domain

### Gameplay (Docs/03_GAMEPLAY_MVP)

| Item | Disposition | Evidence | Owner phase |
|------|-------------|----------|-------------|
| Walk volumes / island bounds | **MISSING** in UE | GP spec; no VS_MVP navmesh contract landed | NP-C |
| Form swap body↔spirit | **MISSING** | NightMix driver partial; no form component | NP-C |
| CRUMB_* glide route | **KEEP** spec | C++ + markers script; **PRESENT** on host | Verify → NP-C |
| Shrine portal A↔B | **KEEP** spec | C++ + `place_fallback_glide_markers.py` | Verify → NP-C |
| Demo cameras / GP markers | **PRESENT** (script) | 28 markers JSON; CAM_* in `place_vs_mvp_markers.py` | NP-C polish |
| Free-flight | **DEFER** | Hard reject in canon | — |

### Systems (Docs/03_SYSTEMS_MVP)

| Item | Disposition | Evidence | Owner phase |
|------|-------------|----------|-------------|
| 6-slot inventory RES_* | **MISSING** | Stub uses Wood/Ore/Flowers | NP-D |
| Gather +1 / cooldown / day gate | **MISSING** | Legacy harvest trace only | NP-D |
| Store transfer homestead | **MISSING** | Spec only | NP-D |
| Beast wild→tamed→helper | **MISSING** | `Lib/04_Beasts/` spec; no C++/BP | NP-D |
| Heal ×3 hurt→healed | **MISSING** | `HomeWorldHealAbility` stub | NP-E |
| Nurture N1/N2 M_Nurtured | **MISSING** | Master def only | NP-E |
| Dawn persist inventory/tame | **MISSING** | SaveGame exists; no SYS persist | NP-E |
| Combat / 7th resource | **DEFER** | Forbidden in SYS §2 | — |

### Lookdev / materials (Docs/02)

| Item | Disposition | Evidence | Owner phase |
|------|-------------|----------|-------------|
| Ten master definitions | **KEEP** | Docs/02 + `Lib/06_Materials_Master/` | — |
| UE master material graphs | **PRESENT** script / **PENDING** binary | `create_master_materials.py`; Windows count may be 0 | NP-B |
| NightMix MPC wiring | **PRESENT** script / **PENDING** binary | C++ `ApplyNightMixForPhase`; MPC local-only | NP-B |
| MI instances on kit meshes | **MISSING** | Dress script skips `M_*`; no assign pass | NP-B |
| Lumen / Nanite | **DEFER** | Docs/04 | — |

### Content / integration

| Item | Disposition | Evidence | Owner phase |
|------|-------------|----------|-------------|
| VS_MVP mesh import | **PRESENT** (Windows) | ≈121 meshes across 4 categories | — |
| VS_MVP dress actors | **PRESENT** (Windows) | `place_vs_mvp_dress.py` | NP-B materials |
| L_VS_MVP_Markers | **PRESENT** (Windows) | Not in git | Volatility → NP-B |
| Legacy DemoMap/Homestead UE assets | **KEEP** quarantine | `Content/__ExternalActors__` — not VS_MVP slice | WAVE F |
| Crafting tree | **DEFER** | Not in MVP SYS | — |
| Docs/07 reopen | **DEFER** | CLOSED per audit | — |

---

## Explicit DEFER (do not implement in NP-A…E without Lead)

| Item | Reason |
|------|--------|
| **Free-flight** | Canon hard reject; FALLBACK CRUMB glide only |
| **Combat** | Placeholder only per AGENTS.md; sin-strip not in NP scope |
| **Lumen / Nanite gates** | Docs/04 deferred |
| **Crafting** | Not in 03_SYSTEMS_MVP |
| **Docs/07 reopen** | Vertical slice sign-off CLOSED |
| **WAVE F mass delete** | Separate Lead gate |
| **NFT / Milady / wallet C++** | Quarantine per 08a_INVENTORY |

---

## NP phase routing (from gaps)

| Phase | Closes |
|-------|--------|
| **NP-A** (this doc) | Evidence map — **COMPLETE** |
| **NP-B** | Recreate masters if needed; assign 10 masters on DRESS_*; NightMix smoke |
| **NP-C** | V1 walk bounds; V2/V5 PIE verify; form swap + GP_PlayerStart |
| **NP-D** | V3 gather + V4 tame — full SYS inventory-lite |
| **NP-E** | V6 heal + V7 nurture + V8 dawn persist |

---

## Verification checklist (NP-A only — no implementation)

- [x] Verb table vs Docs/03_GAMEPLAY + Docs/03_SYSTEMS
- [x] Materials ×10 vs Docs/02 + script inventory
- [x] Windows live mesh counts recorded
- [x] Content binary volatility documented for NP-B
- [x] C++ / Python landed list matches repo at `ae7f649`
- [ ] PIE verify V2/V5 — **PENDING** Windows host (not NP-A scope)

---

*Delivered under Lead **`APPROVE NP STRATEGY`** (Luke Thompson, 2026-09-17 ET). Awaiting Lead **`APPROVE NP-A`** to unlock NP-B.*
