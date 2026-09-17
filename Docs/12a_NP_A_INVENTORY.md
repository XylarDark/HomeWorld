# Docs/12a — NP-A Inventory / Gap Map

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE NP-A`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Scope** | UE realization vs [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) + [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) + [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) |
| **Evidence base** | Repo scripts/C++ at `ae7f649`; Windows DESKTOP-21CT3H0 confirmed via `cmd dir` (Lead update ~2026-09-17 ET) |

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

Confirmed on Windows host **DESKTOP-21CT3H0** at repo **HEAD `ae7f649`** via **`cmd dir`** (~2026-09-17 ET). Cloud/Linux clone carries **scripts + JSON only** — VS_MVP binaries are local-only in git.

### Meshes (PRESENT)

| UE path | Windows count | Repo (git) | Disposition |
|---------|---------------|------------|-------------|
| `/Game/HomeWorld/Meshes/Homestead/` | **≈49** `.uasset` | **0** (folder absent) | **PRESENT** |
| `/Game/HomeWorld/Meshes/Forest/` | **≈20** | **0** | **PRESENT** |
| `/Game/HomeWorld/Meshes/Gatherables/` | **≈41** | **0** | **PRESENT** |
| `/Game/HomeWorld/Meshes/Transit/` | **≈11** | **0** | **PRESENT** |

### Materials (PRESENT — assign gap → NP-B)

| Asset | Windows | Repo (git) | Disposition |
|-------|---------|------------|-------------|
| `MPC_HomeWorld_Time.uasset` | **PRESENT** | **0** | **PRESENT** (local-only) |
| `Materials/Masters/M_BeastStylized` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_CliffRock` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_FoliageCard` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_GatherHerb` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_Nurtured` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_PathStone` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_SpiritUnlit` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_StylizedGrass` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_WoodCabin` | **PRESENT** | **0** | **PRESENT** |
| `Materials/Masters/M_WoodWild` | **PRESENT** | **0** | **PRESENT** |
| MI assignment on `DRESS_*` meshes | **MISSING** | N/A | **MISSING** → **NP-B** |

All ten Docs/02 masters confirmed on host. `place_vs_mvp_dress.py` spawns kit actors but **does not assign** master instances — NP-B scope.

### Maps (PRESENT)

| Asset / folder | Windows | Repo (git) | Disposition |
|----------------|---------|------------|-------------|
| `Maps/VS_MVP/L_VS_MVP_Markers.umap` | **PRESENT** | **0** `.umap` in git | **PRESENT** (local-only) |
| `Maps/MainMenu.umap` | **PRESENT** | **PRESENT** (tracked) | **PRESENT** |
| `Maps/VS_MVP/Cameras/` | **PRESENT** | **0** | **PRESENT** (local-only) |
| `Maps/VS_MVP/Markers/` | **PRESENT** | **0** | **PRESENT** (local-only) |
| `Maps/VS_MVP/Transit/` | **PRESENT** | **0** | **PRESENT** (local-only) |

### Characters (PRESENT — skeleton risk)

| Asset | Windows | Repo (git) | Disposition / risk |
|-------|---------|------------|-------------------|
| `Characters/BP_HomeWorldCharacter.uasset` | **PRESENT** | **PRESENT** (tracked) | **PRESENT** |
| `Characters/ABP_HomeWorldCharacter.uasset` | **PRESENT** | **PRESENT** (tracked) | **PRESENT** — **risk:** may still warn missing skeleton on compile/open |

### C++ / Python (PRESENT — repo + host)

| Layer | Landed on host | Disposition |
|-------|----------------|-------------|
| C++ | FallbackGlide, ShrinePortal (+Trigger), Character, TimeOfDaySubsystem | **PRESENT** |
| Python | `place_vs_mvp_markers`, `place_vs_mvp_dress`, `place_fallback_glide_markers`, `create_master_materials*`, `wire_nightmix*` | **PRESENT** (scripts in repo; run on Windows Editor) |

### Content binary volatility (NP-B call-out)

Per project policy, **no `.uasset`/`.umap` commits**. Windows Editor at `ae7f649` currently holds full VS_MVP state (meshes, ten masters, MPC, markers map). After **`git pull` on a fresh clone**, local-only assets may be **absent** until automation re-runs:

1. `batch_import_asset_creation.py` → Meshes categories  
2. `place_vs_mvp_markers.py` → markers + MPC  
3. `place_vs_mvp_dress.py` → DRESS_* kit  
4. `create_master_materials.py` → ten masters (confirmed present on current host)  
5. `place_fallback_glide_markers.py` → GP_GlideStart + portal triggers  

**NP-B** primary gap is **MI assignment onto DRESS_* meshes**, not master recreation on the current host. New clones still need the full script chain above.

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
| M_StylizedGrass | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_CliffRock | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_WoodCabin | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_WoodWild | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_FoliageCard | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_PathStone | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_GatherHerb | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_BeastStylized | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_SpiritUnlit | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| M_Nurtured | **KEEP** | **PRESENT** | **PRESENT** | **MISSING** → NP-B |
| MPC_HomeWorld_Time | **KEEP** | **PRESENT** (script) | **PRESENT** | N/A (runtime driver) |

**Summary:** Script + JSON + all ten master `.uasset` + MPC = **PRESENT** on Windows at `ae7f649`. **MI assignment on DRESS_* meshes = MISSING** → **NP-B**.

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
| **Materials ×10** | Script+JSON ([02_MATERIAL_SHEET](02_MATERIAL_SHEET.md)) | Ten masters + MPC **PRESENT** on host; MI on DRESS_* **MISSING** | Assign masters to dress meshes | **NP-B** |

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
| UE master material graphs | **PRESENT** | All 10 `.uasset` confirmed on Windows; `create_master_materials.py` | — |
| NightMix MPC wiring | **PRESENT** | `MPC_HomeWorld_Time.uasset` on host; C++ `ApplyNightMixForPhase` | NP-B smoke |
| MI instances on kit meshes | **MISSING** | Dress script skips `M_*`; no assign pass | **NP-B** |
| Lumen / Nanite | **DEFER** | Docs/04 | — |

### Content / integration

| Item | Disposition | Evidence | Owner phase |
|------|-------------|----------|-------------|
| VS_MVP mesh import | **PRESENT** (Windows) | ≈121 meshes across 4 categories | — |
| VS_MVP dress actors | **PRESENT** (Windows) | `place_vs_mvp_dress.py` | NP-B materials |
| L_VS_MVP_Markers + VS_MVP subfolders | **PRESENT** (Windows) | Markers map; Cameras/Markers/Transit folders | Volatility on fresh clone |
| BP + ABP HomeWorldCharacter | **PRESENT** | Tracked in git; ABP skeleton warning **risk** | NP-C if anim blocks PIE |
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
| **NP-B** | Assign 10 masters (MI) on DRESS_* meshes; NightMix smoke | Masters + MPC already **PRESENT** on host |
| **NP-C** | V1 walk bounds; V2/V5 PIE verify; form swap + GP_PlayerStart |
| **NP-D** | V3 gather + V4 tame — full SYS inventory-lite |
| **NP-E** | V6 heal + V7 nurture + V8 dawn persist |

---

## Verification checklist (NP-A only — no implementation)

- [x] Verb table vs Docs/03_GAMEPLAY + Docs/03_SYSTEMS
- [x] Materials ×10 vs Docs/02 + script inventory
- [x] Windows live mesh counts recorded
- [x] Windows materials (10 masters + MPC) confirmed **PRESENT** via `cmd dir`
- [x] Windows maps (L_VS_MVP_Markers + VS_MVP folders) confirmed **PRESENT**
- [x] MI assignment on DRESS_* recorded **MISSING** → NP-B
- [x] ABP skeleton warning noted as risk
- [x] Content binary volatility documented for NP-B
- [x] C++ / Python landed list matches repo at `ae7f649`
- [ ] PIE verify V2/V5 — **PENDING** Windows host (not NP-A scope)

---

*Delivered under Lead **`APPROVE NP STRATEGY`** (Luke Thompson, 2026-09-17 ET). Awaiting Lead **`APPROVE NP-A`** to unlock NP-B.*
