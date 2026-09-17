# VP-A PIE Evidence — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-A |
| **Status** | **APPROVED** — Lead Luke Thompson, **`APPROVE VP-A`**, 2026-09-17 ET (hard-fail accepted; re-verify after VP-B) |
| **Lead gate** | **`APPROVE VP-A`** — **APPROVED**; unlocks **VP-B** |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-A |

## Summary

DESKTOP PIE evidence run on **DESKTOP-21CT3H0** (2026-09-17 ~08:26–08:28 ET) via UnrealMCP. **Editor-world scene inventory PASS.** **Verb PIE HARD FAIL** — no spawnable character; all seven gameplay log prefixes absent. Root cause: **`ABP_HomeWorldCharacter` skeleton compile failure** (maps to PA-03 / **VP-B**). Treat VP-A as **evidence complete with documented fails**; unlock **VP-B first** before re-running verb PIE for green greps.

## Prerequisites

- `.\Tools\Safe-Build.ps1`
- Bootstrap chain (`bootstrap_project.py` or individual `place_vs_mvp_*.py`)
- Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`

## Runbooks

| Runbook | Verbs |
|---------|-------|
| [12c_NP_C_FORM_V1.md](../12c_NP_C_FORM_V1.md) | FORM, FALLBACK, portal |
| [12d_NP_D_SYS_V3_V4.md](../12d_NP_D_SYS_V3_V4.md) | GATHER, TAME |
| [12e_NP_E_SYS_V6_V8.md](../12e_NP_E_SYS_V6_V8.md) | HEAL, NURTURE, DAWN |

## Log prefixes (grep Output Log)

`FORM:`, `FALLBACK:`, `HEAL:`, `NURTURE:`, `DAWN:`, `TAME:`, `GATHER:` (supporting)

---

## Evidence checklist

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **UE version** | 5.7.4-51494982+++UE5+Release-5.7 |
| **Timestamp** | 2026-09-17 ~08:26–08:28 ET |
| **Repo tip** | `cb592fa` (after pull) |
| **Map open** | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` (confirmed) |
| **MCP** | TCP `execute_python_script` / `execute_console_command` OK (ping + scripts) |
| **Safe-Build** | Assumed current per host workflow (not re-run this session) |
| **Bootstrap** | Prior chain; placement actors present in editor world |

---

## Scene inventory (PASS — editor world)

Present in level at evidence time:

| Actor / marker | Notes |
|----------------|-------|
| `GP_PlayerStart` | Player start marker |
| `PlayerStart_VS_MVP` | VS_MVP player start |
| `GP_GlideStart` | Glide entry |
| `GP_PortalA` / `GP_PortalB` | `HomeWorldShrinePortalTrigger` |
| `CRUMB_*` | Glide spline points |
| `GP_SpiritWisp_A/B/C` | Spirit wisp markers |
| `GP_BeastPad` | Beast tame pad |
| `GP_N1_Crop` | Crop gather node |
| `GP_N2_Stored` | Stored gather node |
| `DRESS_*` | Dressed cabin / shrine / islets |

**Verdict:** Editor-world placement and dress **PASS** — runbook targets exist.

---

## `pie_test_runner` results

| Run | Condition | Result |
|-----|-----------|--------|
| **First** | PIE not running | **2/40** — level asset + MPC only |
| **After `vp_a_boot.py`** | `load_map` + `editor_request_begin_play` | `is_in_play` eventually **True**, but `get_pie_worlds` count **0**, no PlayerController/pawn → **Character spawned FAIL** |

Optional automation path: `execute_python_script("pie_test_runner.py")` → `Saved/pie_test_results.json` (character spawn check failed).

---

## Verb log greps (`Saved/Logs/HomeWorld.log`)

Gameplay prefixes only (not placement-script prose):

| Prefix | Result | Notes |
|--------|--------|-------|
| `FORM:` | **FAIL** | 0 gameplay lines. `hw.TimeOfDay.Phase 2/0` console accepted (`hw.TimeOfDay.Phase = "2"`) but no `FORM:` without character `OnPhaseChanged` |
| `FALLBACK:` | **FAIL** | 0 |
| `HEAL:` | **FAIL** | 0 gameplay; setup script text mentions "HEAL: logs" only |
| `NURTURE:` | **FAIL** | 0 gameplay; setup text only |
| `DAWN:` | **FAIL** | 0 |
| `TAME:` | **FAIL** | 0 gameplay; setup text only |
| `GATHER:` | **FAIL** | 0 |

**Verdict:** All six primary prefixes + supporting `GATHER:` — **documented hard-fail** (no gameplay emission in PIE).

---

## Root cause (hard-fail — maps to PA-03 / VP-B)

```
LogBlueprint: Error: ABP_HomeWorldCharacter - The skeleton asset for this animation Blueprint is missing, so it cannot be compiled!
BlueprintLog: Warning: Blueprint failed to compile: ABP_HomeWorldCharacter
LoadErrors: dependent package /Game/Man/Demo/Mesh/UE4_Mannequin_Skeleton was not available
(+ ThirdPersonIdle / ThirdPersonWalk missing)
```

Without a compiling ABP / spawnable character, interact verbs cannot emit `FORM:` / `FALLBACK:` / `HEAL:` / `NURTURE:` / `DAWN:` / `TAME:` in PIE.

| Audit ID | VP phase | Status from VP-A |
|----------|----------|------------------|
| **PA-01** | VP-A | **Evidence filed** — all verbs **FAIL** (blocked) |
| **PA-03** | VP-B | **Blocking** — ABP skeleton missing; fix before verb re-run |

---

## Recommendation

1. Treat VP-A as **evidence complete with documented fails** — do **not** fake pass or reopen [Docs/07](../07_VERTICAL_SLICE_SIGN%20OFF.md).
2. Unlock **VP-B first** (ABP skeleton + NightMix smoke) before re-running verb PIE for green greps.
3. Do **not** invent free-flight or expand VP scope beyond [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md).

---

## Prior stamp

Lead **`APPROVE VP STRATEGY`** (Luke Thompson, 2026-09-17 ET) — VP strategy **APPROVED**; VP-A **UNLOCKED**. Strategy merge `cb592fa` (PR #53).

## Stamp

Lead **`APPROVE VP-A`** (Luke Thompson, 2026-09-17 ET) — VP-A **APPROVED** (evidence filed; verb PIE **hard-fail accepted** — PA-03 ABP skeleton). **VP-B UNLOCKED** — fix ABP skeleton + NightMix smoke; re-run verb PIE greps after VP-B before VP-C.

---

## Re-verify (2026-09-17 post–VP-B)

Post–VP-B re-run on **DESKTOP-21CT3H0** after mesh-only character interim (PR #67 @ `e00c542`) and repo stamp **`0e4bca1`** (includes PR #68). Original fail record above **unchanged**; this section adds updated evidence only.

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **UE version** | 5.7.4-51494982+++UE5+Release-5.7 |
| **Timestamp** | 2026-09-17 (post–VP-B re-verify attempt) |
| **Repo tip** | `0e4bca1` (VP-B mesh-only `e00c542` / PR #67, then stamp incl. PR #68) |
| **Character BP** | Engine `DefaultSkeletalMesh`; `anim_class` **None**; `BlueprintEditorLibrary.compile_blueprint` **OK** |
| **Preflight** | `preflight:ue --require-editor` exit **0** (warning only `EDITOR_ABP_SKELETON`) |
| **Map** | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |

### MCP PIE / automation

| Check | Result | Notes |
|-------|--------|-------|
| `LevelEditorSubsystem.is_in_play_in_editor()` | **True** | After `editor_request_begin_play` |
| `EditorLevelLibrary.get_pie_worlds(True\|False)` count | **0** | No PIE worlds visible to automation |
| Editor-world PlayerController | **None** | No controllable pawn in automation path |
| `pie_test_runner` | **3/40** | **Character spawned FAIL** — No controlled pawn / No PIE world |

### Verb log greps (re-verify)

Gameplay prefixes only (not placement-script prose):

| Prefix | Result | Notes |
|--------|--------|-------|
| `FORM:` | **FAIL** | 0 gameplay lines — automation cannot drive PIE pawn |
| `FALLBACK:` | **FAIL** | 0 gameplay lines |
| `HEAL:` | **FAIL** | 0 gameplay lines |
| `NURTURE:` | **FAIL** | 0 gameplay lines |
| `DAWN:` | **FAIL** | 0 gameplay lines |
| `TAME:` | **FAIL** | 0 gameplay lines |
| `GATHER:` | **FAIL** | 0 gameplay lines |

**Verdict:** Re-verify **STILL FAIL** — all seven prefixes absent in automation PIE path. Mesh-only VP-B did **not** restore MCP/automation PIE world visibility or PlayerController.

### Root-cause update (post–VP-B)

| Item | Status |
|------|--------|
| **PA-03 ABP** | **Deferred accept** — ABP no longer assigned to BP (`anim_class` None); `EDITOR_ABP_SKELETON` warning only; not blocking preflight |
| **Remaining blocker** | **MCP/automation PIE world visibility / no PlayerController** — not fixed by mesh-only interim |
| **Human path** | Lead **Alt+P** PIE on DESKTOP or Lead **WAIVE** per prefix still required for green greps |

### Recommendation (re-verify)

1. Treat automation re-verify as **STILL FAIL** — do **not** invent PASS greps; honest fail record stands.
2. **VP-C impl may proceed**; re-verify gate **WAIVED** by Lead (see stamp below).
3. Optional follow-up: human Alt+P PIE walk-through per runbooks, **or** automation gap session for MCP `get_pie_worlds` / PlayerController visibility.

### Stamp (re-verify)

Lead **`WAIVE VP-A re-verify`** (Luke Thompson, 2026-09-17 ET) — all required verb prefixes (`FORM`, `FALLBACK`, `HEAL`, `NURTURE`, `DAWN`, `TAME`, `GATHER`) **WAIVED** for VP-C unlock per [HR3_D_EVIDENCE_LANE.md](HR3_D_EVIDENCE_LANE.md). Automation path remains **STILL FAIL**; waiver does not rewrite grep results.
