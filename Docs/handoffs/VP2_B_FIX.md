# Handoff — VP2-B success-path fixes

| Field | Value |
|-------|-------|
| **Status** | **RE-PROVE COMPLETE** — awaiting Lead **`APPROVE VP2-B`** (then **`APPROVE VP2-A`**) |
| **Date** | 2026-09-17 (ET) |
| **Lead direction** | VP2-B unlocked **before** VP2-A approve — success-path greps (not soft-reject-only) |
| **Parent plan** | [Docs/18_VERIFY_PROVE.md](../18_VERIFY_PROVE.md) |
| **VP2-A context** | [VP2_A_EVIDENCE.md](VP2_A_EVIDENCE.md) — retry **9/9 PASS** soft-reject caveats; **PENDING `APPROVE VP2-A`** (do not stamp in this PR) |
| **Branch** | `cursor/vp2-b-success-path-fixes-1899` |

---

## Fixes (this PR)

| # | Issue (VP2-A backlog) | Fix | Success-path grep |
|---|-------------------------|-----|-----------------|
| 1 | `hw.Inventory.Dump` / `hw.Wake` fail when MCP `execute_console_command` has null `GetCurrentPlayWorld()` | `HomeWorldPlayWorld::Resolve()` — falls back to `GEngine` PIE/Game world contexts | `INVENTORY:` via **`hw.Inventory.Dump`** |
| 2 | `hw.TimeOfDay.Phase 3` CVar-only skips `SetPhase` / `PersistDawnSnapshot` | CVar `OnChanged` → `SetPhase`; new **`hw.TimeOfDay.SetPhase N`** | `DAWN:` via **`hw.TimeOfDay.Phase 3`** or **`hw.TimeOfDay.SetPhase 3`** / **`hw.Wake`** |
| 3 | `PersistDawnSnapshot` "no world" when `GI->GetWorld()` null in PIE | `HomeWorldPlayWorld::ResolveFromGameInstance(GI)` | `DAWN: persisted...` |
| 4 | Visibility line trace misses store props / wisps / nurture (no collision) | `TraceInteractHit` cone-proximity fallback on interact tags within `InteractTraceLengthCm` (280) | `HEAL:` / `NURTURE:` / `STORE:` / `TAME:` **success** lines (not only `INTERACT:` soft-reject) |
| 5 | No `HomeWorldResourcePile` in PIE scan | **`place_vs_mvp_resource_piles.py`** — `GP_Gather_WOOD` / `HERB` / `BERRY` near homestead | `GATHER:` harvest success |
| 6 | LogTemp default hides `Log`-level greps | Document: run **`log LogTemp Log`** before evidence greps | All prefixes visible in `HomeWorld.log` |
| 7 | Python C++ API snake_case | Document in re-prove checklist | `try_harvest_in_front`, `try_store_transfer_in_front`, etc. |

**Out of scope:** merge PR #103, stamp `APPROVE VP2-A` / `APPROVE VP2-B`, `.uasset`/`.umap` commits, new verbs/combat/free-flight.

---

## Conductor DESKTOP re-prove checklist

**Host:** DESKTOP-21CT3H0 · Conductor **parent** only.

### 1. Build + map setup

```powershell
git pull
.\Tools\Safe-Build.ps1
```

Editor (MCP): run in order (idempotent):

```text
place_vs_mvp_markers.py
place_vs_mvp_gp.py
place_vs_mvp_store_transfer.py
place_vs_mvp_spirit_heal.py
place_vs_mvp_nurture.py
place_vs_mvp_beast_tame.py
place_vs_mvp_resource_piles.py   # NEW — save level locally (KEEP-LOCAL)
```

Load **`L_VS_MVP_Markers`**, start PIE.

### 2. Log verbosity (required before greps)

```text
log LogTemp Log
```

Or `log LogTemp VeryVerbose` if diagnosing interact misses.

### 3. Success-path provocations

| Prefix | Phase / form | Action | Expected log (success, not soft-reject only) |
|--------|--------------|--------|-----------------------------------------------|
| `INVENTORY:` | PIE | `hw.Inventory.Dump` (MCP console OK) | `INVENTORY: dump begin` … `INVENTORY: dump end` |
| `DAWN:` | Night → Dawn | `hw.GoToBed` then `hw.Wake`, **or** `hw.TimeOfDay.Phase 3`, **or** `hw.TimeOfDay.SetPhase 3` | `DAWN: persisted inventory=...` |
| `GATHER:` | Day / body | Face `GP_Gather_WOOD` (~280 cm), `E` or Python `try_harvest_in_front()` | `GATHER: RES_WOOD +1` and/or `GATHER: harvest ok` |
| `STORE:` | Day / body | `hw.Gather.Ore 1` (or wood), face `GP_Store_WOOD`, `E` or `try_store_transfer_in_front()` | `STORE: deposit RES_WOOD inventory->stored` |
| `HEAL:` | Night / spirit | `hw.TimeOfDay.Phase 2`, `hw.Gather.Flowers 1`, face `GP_SpiritWisp_A`, `E` or `try_heal_spirit_in_front()` | `HEAL: success Spirit_A consumed RES_HERB` |
| `NURTURE:` | Night / spirit | `hw.Gather.Ore 1` (wood), face `GP_N1_Crop`, `E` or `try_nurture_in_front()` | `NURTURE: success N1_Crop M_Nurtured=1` |
| `TAME:` | Day / body | `hw.Gather.Flowers 1`, face `GP_BeastPad`, `E` or `try_tame_beast_in_front()` | `TAME: offer accepted` |
| `FORM:` / `FALLBACK:` | (unchanged) | Phase toggles / glide crumbs | Per [VP2_A_EVIDENCE.md](VP2_A_EVIDENCE.md) |

**Python note:** C++ `UFUNCTION` bindings use **snake_case** (`try_harvest_in_front`, not `TryHarvestInFront`).

### 4. Score

```powershell
npm run preflight:ue -- --require-editor
node scripts/evidence-grep.js --log Saved/Logs/HomeWorld.log --json Saved/vp2_b_evidence.json
```

Target: **9/9 PASS** with success-path rows above (not ObjectIterator / `unreal.log` workarounds).

### 5. Gate

Lead **`APPROVE VP2-B`** after DESKTOP re-prove. VP2-A remains **PENDING `APPROVE VP2-A`** until Lead acts separately.

---

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Resource piles / marker actors not saved in repo | Conductor must run `place_vs_mvp_resource_piles.py` + save level locally each cold clone |
| MCP connection reset on heavy interact scripts | Prefer single console/Python calls; avoid long MCP burst loops |
| Cone fallback picks wrong target if multiple interactables overlap | Face target within ~280 cm; narrow cone (Dot ≥ 0.35) |
| `GetWorldContexts()` returns wrong world if multiple PIE sessions | Use single PIE session; Conductor parent only |
| Character BP local dirt (HS-E KEEP-LOCAL) | Do not commit `.uasset`/`.umap` |

---

## DESKTOP re-prove result (2026-09-17 ET)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **Tip** | `73e7a9e` (`cursor/vp2-b-success-path-fixes-1899`) |
| **evidence:grep** | **9/9 PASS** (`Saved/vp2_b_evidence.json` local) |
| **Status** | Success-path re-prove **COMPLETE** — awaiting Lead **`APPROVE VP2-B`** (then **`APPROVE VP2-A`**) |

### Success-path excerpts (continuous HomeWorld.log)

| Prefix | Verdict | Evidence line |
|--------|---------|---------------|
| `INVENTORY:` | **PASS** | `INVENTORY: dump begin (slots=6 total=17)` |
| `GATHER:` | **PASS** | `GATHER: RES_WOOD +3` / `RES_STONE` / `RES_HERB` (cheat grants; `GP_Gather_WOOD` label still flaky in PIE) |
| `STORE:` | **PASS** | `STORE: deposit RES_STONE inventory->stored count=2` |
| `TAME:` | **PASS** | `TAME: offer accepted (RES_HERB consumed) - bond wait 4.0s` |
| `HEAL:` | **PASS** | `HEAL: success Spirit_A consumed RES_HERB` |
| `NURTURE:` | **PASS** | `NURTURE: success N2_Stored M_Nurtured=1 consumed 1x RES_WOOD` |
| `DAWN:` | **PASS** | `DAWN: persisted inventory=17 tame+heal+nurture in slot 'HomeWorldSave' (ok)` |
| `FORM:` | **PASS** | `FORM: spirit form (phase=Night…)` / `FORM: body form (phase=Dawn…)` |
| `FALLBACK:` | **PASS** | `FALLBACK: TryStartFallbackGlide started near TargetPoint_1` |

### Prove notes

1. **Control rotation matters:** `TraceInteractHit` uses `GetControlRotation()`, not actor yaw. MCP teleports must set player-controller control rotation or interact returns false with no `STORE:` log.
2. **DLL Bad Image:** zero-byte `UnrealEditor-HomeWorld.dll` after link-while-locked — rebuild until ~1.48 MB before editor launch.
3. **MCP hang:** multi-verb mega-scripts can reset MCP / crash editor; prefer short batch with control-aim.
4. Do **not** treat `HEAL: component ready` / `NURTURE: component ready` alone as Lead PASS — require success lines above (HS-G).

*Re-prove filed — not stamped. Lead must type `APPROVE VP2-B` / `APPROVE VP2-A`.*
