# VP-B Smoke & Character — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-B |
| **Status** | **EVIDENCE COMPLETE — PENDING LEAD `APPROVE VP-B`** |
| **Lead gate** | **`APPROVE VP-B`** before marking complete or unlocking VP-C |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-B |
| **Baseline** | Main @ `5d09cf8` (PR #66 mesh-only) — DESKTOP **DESKTOP-21CT3H0** |

## Summary

VP-A hard-fail root cause: missing `/Game/Man/Mesh/Full/SK_Man_Full_01`, broken `ABP_HomeWorldCharacter` skeleton compile, and preflight treating empty `anim_class` as blocker. **Interim strategy:** Engine `DefaultSkeletalMesh` + **mesh-only** spawn (no AnimBP on BP) until real mannequin returns. Preflight and bootstrap scripts align with this — spawn > AnimGraph.

**PA-02 NightMix smoke:** Fixed on DESKTOP — UE 5.7 Python exposes `unreal.MaterialLibrary` (not `KismetMaterialLibrary`). Repo fix in `smoke_nightmix_phase.py` prefers `MaterialLibrary`, falls back to `KismetMaterialLibrary`.

## Interim mesh-only strategy

| Item | Value |
|------|-------|
| **Config** | [character_blueprint_config.json](../../Content/Python/character_blueprint_config.json) |
| **Skeletal mesh** | `/Engine/EditorMeshes/SkeletalMesh/DefaultSkeletalMesh` |
| **Anim blueprint** | `""` (empty — mesh-only) |
| **Re-apply on DESKTOP** | MCP `execute_python_script("setup_character_blueprint.py")` + `vp_b_apply_character.py` |
| **Local `.uasset`** | BP mesh/anim changes stay on DESKTOP; **no `.uasset` commits** |

Scripts are **idempotent**: re-run after pull applies config-driven mesh and clears `anim_class` when `anim_blueprint` is empty.

## Preflight changes (HR3-B + VP-B)

| Check | Mesh-only behavior |
|-------|-------------------|
| `ASSET_MISSING_ON_DISK` | Skips `/Engine/...` paths; skips ABP disk check when `anim_blueprint` empty |
| `CONFIG_EMPTY_PATH` | Requires `skeletal_mesh` only; empty `anim_blueprint` OK |
| `EDITOR_BP_MESH_EMPTY` | Does **not** fail when mesh set + `anim_class` None |
| `EDITOR_ABP_SKELETON` | **Warning** only when config `anim_blueprint` empty and BP has no `anim_class` |

## DESKTOP evidence (2026-09-17)

| Check | Result |
|-------|--------|
| `git pull` @ `5d09cf8` | OK |
| `setup_character_blueprint.py` + `vp_b_apply_character.py` | `VP_B: anim_class None` / `VP_B: DONE` |
| `preflight_ue_editor.py` | `ok: true`, `mesh_only: true`, `blockers: []` |
| `npm run preflight:ue -- --skip-mcp --require-editor` | exit **0** (PASS); warning only `EDITOR_ABP_SKELETON` mesh-only interim |
| `smoke_nightmix_phase.py` (PA-02) | exit **0** — 4/4 phases (see log excerpts below) |

### NightMix smoke log excerpts (PA-02)

```text
smoke_nightmix_phase: OK phase=Day NightMix=0.00
smoke_nightmix_phase: OK phase=Dusk NightMix=0.35
smoke_nightmix_phase: OK phase=Night NightMix=0.85
smoke_nightmix_phase: OK phase=Dawn NightMix=0.15
smoke_nightmix_phase: Smoke complete: 4/4 phases written to MPC
```

**Fix:** `unreal.MaterialLibrary.set_scalar_parameter_value` on `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` (UE 5.7 Python API; `KismetMaterialLibrary` absent on DESKTOP build).

## NightMix smoke (PA-02)

| Item | Status |
|------|--------|
| Script | `Content/Python/smoke_nightmix_phase.py` |
| DESKTOP evidence | **Complete** — 4/4 phases, exit **0** |
| Repo fix | Prefer `MaterialLibrary`, fallback `KismetMaterialLibrary` |
| Done criteria | Exit **0** with four `OK phase=` lines — **met** |

## ABP deferred accept (PA-03)

| Item | Decision |
|------|----------|
| `ABP_HomeWorldCharacter` | **Deferred** — asset may remain broken on disk; not assigned to BP |
| PIE spawn | Mesh-only T-pose / static pose acceptable for VP-B smoke |
| Preflight | `EDITOR_ABP_SKELETON` **warning only** (mesh-only interim) — accepted |
| Full AnimGraph | Out of scope — [ANIMGRAPH_AUTOMATION_SPIKE.md](../../docs/TaskLists/TaskSpecs/ANIMGRAPH_AUTOMATION_SPIKE.md) deferred |

## Evidence checklist (DESKTOP)

- [x] `setup_character_blueprint.py` applied — log shows Engine mesh + cleared `anim_class`
- [x] `npm run preflight:ue -- --require-editor` exit **0**
- [x] `smoke_nightmix_phase.py` exit **0** (PA-02) — 4/4 phases
- [ ] PIE spawn visible (mesh-only) — optional verb re-grep after spawn fixed (HR3-D / post-APPROVE)

## Hard rules

- **Docs/07 CLOSED** — no reopen
- **No free-flight**
- **No `.uasset` / `.umap` commits**

---

*VP-B DESKTOP evidence filed — pending Lead **`APPROVE VP-B`**. VP-C remains **LOCKED** until gate.*
