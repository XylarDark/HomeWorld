# VP-B Smoke & Character — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-B |
| **Status** | **IN PROGRESS** — repo fixes merged pending DESKTOP re-apply |
| **Lead gate** | **`APPROVE VP-B`** before marking complete |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-B |

## Summary

VP-A hard-fail root cause: missing `/Game/Man/Mesh/Full/SK_Man_Full_01`, broken `ABP_HomeWorldCharacter` skeleton compile, and preflight treating empty `anim_class` as blocker. **Interim strategy:** Engine `DefaultSkeletalMesh` + **mesh-only** spawn (no AnimBP on BP) until real mannequin returns. Preflight and bootstrap scripts align with this — spawn > AnimGraph.

## Interim mesh-only strategy

| Item | Value |
|------|-------|
| **Config** | [character_blueprint_config.json](../../Content/Python/character_blueprint_config.json) |
| **Skeletal mesh** | `/Engine/EditorMeshes/SkeletalMesh/DefaultSkeletalMesh` |
| **Anim blueprint** | `""` (empty — mesh-only) |
| **Re-apply on DESKTOP** | MCP `execute_python_script("setup_character_blueprint.py")` or full `bootstrap_project.py` |
| **Local `.uasset`** | BP mesh/anim changes stay on DESKTOP; **no `.uasset` commits** |

Scripts are **idempotent**: re-run after pull applies config-driven mesh and clears `anim_class` when `anim_blueprint` is empty.

## Preflight changes (HR3-B + VP-B)

| Check | Mesh-only behavior |
|-------|-------------------|
| `ASSET_MISSING_ON_DISK` | Skips `/Engine/...` paths; skips ABP disk check when `anim_blueprint` empty |
| `CONFIG_EMPTY_PATH` | Requires `skeletal_mesh` only; empty `anim_blueprint` OK |
| `EDITOR_BP_MESH_EMPTY` | Does **not** fail when mesh set + `anim_class` None |
| `EDITOR_ABP_SKELETON` | **Warning** only when config `anim_blueprint` empty and BP has no `anim_class` |

**DESKTOP gate after re-apply:**

```text
execute_python_script("preflight_ue_editor.py")
npm run preflight:ue -- --require-editor
```

Expected: exit **0** (map + BP mesh OK; broken unused ABP may remain on disk as soft warn).

## NightMix smoke (PA-02)

| Item | Status |
|------|--------|
| Script | `Content/Python/smoke_nightmix_phase.py` |
| DESKTOP evidence | **Pending** — run after mesh-only preflight green |
| Done criteria | Exit **0** with four `OK phase=` lines |

## ABP deferred accept (PA-03)

| Item | Decision |
|------|----------|
| `ABP_HomeWorldCharacter` | **Deferred** — asset may remain broken on disk; not assigned to BP |
| PIE spawn | Mesh-only T-pose / static pose acceptable for VP-B smoke |
| Full AnimGraph | Out of scope — [ANIMGRAPH_AUTOMATION_SPIKE.md](../../docs/TaskLists/TaskSpecs/ANIMGRAPH_AUTOMATION_SPIKE.md) deferred |

## Evidence checklist (DESKTOP — pending)

- [ ] `setup_character_blueprint.py` applied — log shows Engine mesh + cleared `anim_class`
- [ ] `npm run preflight:ue -- --require-editor` exit **0**
- [ ] `smoke_nightmix_phase.py` exit **0** (PA-02)
- [ ] PIE spawn visible (mesh-only) — optional verb re-grep after spawn fixed

## Hard rules

- **Docs/07 CLOSED** — no reopen
- **No free-flight**
- **No `.uasset` / `.umap` commits**

---

*VP-B repo lane — cloud agent docs + Python/config; DESKTOP owns Editor re-apply and evidence.*
