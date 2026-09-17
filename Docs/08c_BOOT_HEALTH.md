# Docs/08c — WAVE C Boot Health

| Field | Value |
|-------|-------|
| **Board status** | WAVE C — BOOT HEALTH COMPLETE (awaiting Lead gate) |
| **Date** | 2026-09-17 |
| **Author** | Audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Prior waves** | [08a_INVENTORY.md](08a_INVENTORY.md) (APPROVED) · [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) (PR #12 merged — WAVE B) |
| **Hard rules honored** | Docs/07 CLOSED not reopened; FALLBACK FLIGHT armed; no new gameplay features; no WAVE D work |

**Gate:** stop for Lead **`APPROVE WAVE C`**

---

## 1. Board status — WAVE C

| Item | Status |
|------|--------|
| **WAVE A** | COMPLETE — [08a_INVENTORY.md](08a_INVENTORY.md) (PR #11 merged) |
| **WAVE B** | COMPLETE — [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) (PR #12 merged) |
| **WAVE C** | **THIS DELIVERABLE** — editor boot + Safe-Build green path; known crash list **CLOSED** |
| **WAVE D** | NOT STARTED — blocked until Lead `APPROVE WAVE C` |

WAVE C scope: confirm UE **5.7.x** Editor opens without the known assert class; document Safe-Build as the agent build entry; close the boot-blocking crash table. No gameplay features, no Content canon decisions (that is WAVE D).

---

## 2. Environment

| Item | Value |
|------|-------|
| **Engine** | Unreal Engine **5.7.x** (validated on **5.7.4** — DESKTOP-21CT3H0) |
| **Project** | `HomeWorld.uproject` from repo root |
| **Agent build entry** | **`.\Tools\Safe-Build.ps1`** (closes Editor → invokes `Build-HomeWorld.bat` → retries once on Live Coding / exit code 6) |
| **Human build entry** | `Build-HomeWorld.bat` when Editor already closed |
| **Build policy** | [docs/Setup/BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md) |
| **Full protocol** | [docs/Editor/EDITOR_BUILD_PROTOCOL.md](../docs/Editor/EDITOR_BUILD_PROTOCOL.md) |

### Safe-Build → Build-HomeWorld.bat policy

```
Tools/Safe-Build.ps1          ← canonical for agents / automation
  └─ Build-HomeWorld.bat      ← low-level UE Build.bat wrapper (log: Build-HomeWorld.log)
```

Orchestrator `py Content/Python/run_automation_cycle.py` applies the same Editor-close protocol when build is enabled.

---

## 3. Known crash / assert table — CLOSED

All boot-blocking items below are **CLOSED** on main after the cited PRs merged.

| ID | Symptom | Root cause | Fix PR | Status |
|----|---------|------------|--------|--------|
| **BOOT-001** | Fatal assert on Editor load: `NewObject` with empty name during CDO construction (`SetCollisionProfileName` in `UBoxComponent` subclass ctor) | `UHomeWorldGoToBedTriggerComponent` / `UHomeWorldMealTriggerComponent` called `SetCollisionProfileName` (and related box setup) in **constructors**; UE 5.7.4 runs `NewObject(NAME_None)` on CDO path | [#5](https://github.com/XylarDark/HomeWorld/pull/5) — defer profile init; FObjectInitializer + `PostInitProperties` | **CLOSED** |
| **BOOT-002** | `HomeWorldEditor` compile failure: `IsBoundToObject` not a member of dynamic delegate | `FOnNightStarted` in `HomeWorldGameMode` used deprecated/nonexistent `IsBoundToObject` | [#7](https://github.com/XylarDark/HomeWorld/pull/7) — `RemoveDynamic` / `AddDynamic` | **CLOSED** |
| **BOOT-003** | Compile failure: `SetGenerateOverlapEvents` misuse in trigger ctors (same boot-health class as BOOT-001) | Overlap flag set in ctor before CDO-safe init path | [#7](https://github.com/XylarDark/HomeWorld/pull/7) — moved to safe init alongside profile deferral | **CLOSED** |
| **BOOT-004** | Editor still assert on load after partial ctor fix — box extent / profile / overlap in ctor | Residual ctor-side `SetBoxExtent`, `SetCollisionProfileName`, `SetGenerateOverlapEvents` on trigger components | [#8](https://github.com/XylarDark/HomeWorld/pull/8) — all box setup in `PostInitProperties` | **CLOSED** |
| **BOOT-005** | Compile error **C2084**: duplicate `PostInitProperties` definition in same `.cpp` | PR #8 left two `PostInitProperties` bodies per trigger component | [#9](https://github.com/XylarDark/HomeWorld/pull/9) — merge into single `PostInitProperties` | **CLOSED** |

**Current pattern (main):** trigger components use empty constructors; `PostInitProperties` sets box extent, collision profile, and overlap events; `BeginPlay` binds overlap delegate.

No open boot-blocking asserts remain in the known list.

---

## 4. Evidence

### Editor open + Safe-Build green (Windows)

| Check | Result | Notes |
|-------|--------|-------|
| **Safe-Build green** | PASS | C++ module compiles after PRs #5–#9 on DESKTOP-21CT3H0 |
| **Editor opens** | PASS | UE 5.7.x loads project without BOOT-001 assert class |
| **Docs/05 first pass** | PASS | FBX import, markers, MPC stub — see below |

### Docs/05 first-pass handoff (DESKTOP-21CT3H0)

After Safe-Build green and Editor open, the **Docs/05 UE import first pass** succeeded on Windows:

| Step | Result | Reference |
|------|--------|-----------|
| FBX batch import | DONE | `/Game/HomeWorld/Meshes/{Homestead,Forest,Gatherables,Transit}/` |
| Marker level | DONE | `L_VS_MVP_Markers` — 28 actors (CRUMB_*, VS_MARKER_*, ANCHOR_*, CAM_*) |
| NightMix MPC stub | DONE | `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` |
| FALLBACK transit | UNCHANGED | Scripted glide + portal both ways (armed) |

**Runbook:** [Docs/05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md)  
**Handoff note:** [Docs/handoffs/UE_IMPORT_FIRST_PASS_DONE.md](handoffs/UE_IMPORT_FIRST_PASS_DONE.md) (PR #10 merged)  
**Automation:** `Content/Python/place_vs_mvp_markers.py`, `Content/Python/batch_import_asset_creation.py`

### Content binaries — local on Windows

`.uasset` / `.umap` from the first pass (imported meshes, marker level, MPC) are **not committed** to git. They exist on the Windows machine only; the repo carries scripts, runbooks, and handoff docs for re-run and audit traceability.

---

## 5. Remaining non-blocking risks

These items do **not** block Editor boot or WAVE C gate. Track in QA / import polish; not boot blockers.

| Risk | Symptom | Severity | Notes |
|------|---------|----------|-------|
| **UCX naming warnings** | `batch_import_asset_creation.py` returned False once; UCX proxy naming warnings in log | Low | Meshes still imported; verify collision proxies in viewport ([Docs/05](05_UE_IMPORT_FIRST_PASS.md) §7) |
| **Interchange assembly split** | FBX assemblies exploded to part meshes | Low | Expected Interchange behavior; dress/weld in later pass |
| **Blender→UE axis** | Marker/mesh Y flip, ×100 cm scale | Low | Verify in viewport; documented in handoff |
| **Camera rotators** | Best-effort from Blender euler | Low | Non-blocking for boot / first pass |
| **Marker axis polish** | VS_MARKER / CRUMB placement may need viewport tweak | Low | QA naming/sightline polish (see [DEFECT_P6_QA_002](qa/DEFECT_P6_QA_002_lookout_still_naming.md) — CLOSED for P6; UE placement polish deferred) |

---

## 6. Gate — APPROVE WAVE C

| | |
|---|---|
| **Gate** | Lead types **`APPROVE WAVE C`** on the WAVE C PR |
| **Unlocks** | **WAVE D** — [Docs/08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) (MVP slice vs legacy Content; no dual canons for transit/look) |
| **Do not start** | WAVE D until gate granted |

```
STOP — Lead approval required
Type: APPROVE WAVE C
```

---

## 7. Hard rules (unchanged)

| Rule | Status |
|------|--------|
| **Docs/07 vertical slice sign-off** | **CLOSED** — do not reopen as unfinished ([Docs/07_VERTICAL_SLICE_SIGN OFF.md](07_VERTICAL_SLICE_SIGN%20OFF.md)) |
| **FALLBACK FLIGHT** | **ARMED** — scripted glide + portal both ways unless Lead reverses |
| **No new features during audit WAVEs** | Honored in WAVE C (docs + crash closure only) |
| **Exclusive file ownership / handoffs** | Durable notes under `Docs/handoffs/` |

---

## Board / Actions / Gate / Next (for Lead)

| | |
|---|---|
| **Board** | WAVE C deliverable ready — boot health doc; crash list CLOSED; Safe-Build + Editor open evidenced |
| **Actions** | Review PR; comment **`APPROVE WAVE C`** to unlock WAVE D |
| **Gate** | `APPROVE WAVE C` — do not start WAVE D until granted |
| **Next (after gate)** | WAVE D — `Docs/08d_CONTENT_CANON.md` (legacy Homestead/PCG vs Docs/04 import path) |
