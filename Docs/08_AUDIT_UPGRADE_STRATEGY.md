# Audit & Upgrade Strategy

| Field | Value |
|-------|-------|
| **Status** | PROPOSED (Lead-gated) |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |

## Why

Pre-swarm HomeWorld code (`Source/`, `Content/`, `Content/Python/`, `Tools/`, lowercase `docs/`, in-tree `DevEnvTemplate`) was built with an older harness and older AI. The signed MVP vertical slice (P0–P7) lives in `Docs/`, `Lib/`, `blender/`, `AssetCreation/Exports` MVP FBX, and `Maps/Preview_*`. We need a full audit and upgrade without maintaining dual canons.

## Repo map

| Item | Role |
|------|------|
| **Primary product** | `XylarDark/HomeWorld` (one repo) |
| **Companion harness** | `XylarDark/DevEnvTemplate` |
| **Cursor worktrees** | Under `.cursor/worktrees` — local copies, not separate remotes |
| **Canon split** | Capital `Docs/` = MVP swarm; lowercase `docs/` = UE/session/automation docs. Keep both; no conflicting truth. |

## WAVE plan (Lead gates each)

Each WAVE completes with a deliverable and requires **Lead approval** before the next WAVE starts.

### WAVE A — Inventory

Map `Source/`, `Content/`, `Content/Python/`, `Tools/`, `docs/`, `DevEnvTemplate/`, `AssetCreation/`, `Docs/`.

Tag every major area: **KEEP** | **UPGRADE** | **QUARANTINE** | **DELETE**.

- **Deliverable:** `Docs/08a_INVENTORY.md` + table
- **Gate:** Lead **APPROVE WAVE A**

### WAVE B — Harness align

Diff HomeWorld vs current DevEnvTemplate (AGENTS, Safe-Build, MCP, session log, swarm ops). Close gaps; no gameplay rewrite.

- **Deliverable:** `Docs/08b_HARNESS_GAP.md` + PRs
- **Gate:** Lead **APPROVE WAVE B**

### WAVE C — Boot health

Editor must open on UE 5.7.x without assert. Includes GoToBed/Meal constructor fix class of bugs; Safe-Build green.

- **Deliverable:** [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) — green editor open evidence + known crash list closed
- **Gate:** Lead **APPROVE WAVE C**

### WAVE D — MVP slice vs legacy Content

Decide what old Homestead/PCG/Mass/abilities stays vs yields to `Docs/04` import path (`/Game/HomeWorld/Meshes/...`, FALLBACK glide, portal both ways). No dual canons for transit/look.

- **Deliverable:** [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md)
- **Gate:** Lead **APPROVE WAVE D**

### WAVE E — Upgrade pass

Upgrade C++/BP/Python that touch the signed vertical slice first; defer off-slice polish systems.

- **Deliverable:** [08e_UPGRADE_PASS.md](08e_UPGRADE_PASS.md)
- **Gate:** Lead **APPROVE WAVE E**

### WAVE F — Archive / delete

Kill dead bat loops, stale agent runners, docs that fight `Docs/`.

- **Gate:** Lead **SIGN OFF AUDIT** (`Docs/08_AUDIT_SIGN_OFF.md`)

## Hard rules

- Do **not** reopen `Docs/07` vertical-slice sign-off as unfinished
- **FALLBACK FLIGHT** stays armed unless Lead reverses
- No new features during audit WAVEs unless Lead names them
- Exclusive file ownership; durable handoffs under `Docs/handoffs/`

## Immediate parallel (not a WAVE)

UE first-pass import per [Docs/05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md) (batch FBX) can proceed once the editor boots — it does **not** wait for the full audit.
