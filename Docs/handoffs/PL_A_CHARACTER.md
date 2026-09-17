# PL-A Character Realization — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-A |
| **Status** | **DRAFT IN PROGRESS** — unlocked by Lead **`APPROVE PL STRATEGY`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE PL-A`** before PL-B |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-A |

## Summary

Replace VP-B mesh-only interim (`DefaultSkeletalMesh` + empty anim_blueprint) with a project skeletal mesh + compiling AnimBP (or Lead-documented minimal walk). Root cause from VP-A/B: missing `/Game/Man/Mesh/Full/SK_Man_Full_01` and broken `ABP_HomeWorldCharacter` skeleton deps.

## Scope

| Item | Action |
|------|--------|
| Man mesh / skeleton | Import or Lead-accepted substitute onto DESKTOP; wire config paths |
| `character_blueprint_config.json` | Point at real mesh; set anim_blueprint when ABP compiles |
| ABP | Compile-clean or retire mesh-only with evidence |
| Preflight | Align `preflight:ue` with real paths (mesh-only skip no longer primary) |

## DESKTOP evidence

_Not filed — Conductor owns import/Safe-Build/apply. No invented evidence._

## Hard rules

- Docs/07 CLOSED — no reopen
- No free-flight
- No `.uasset` / `.umap` commits

---

*PL-A stub — DRAFT IN PROGRESS.*
