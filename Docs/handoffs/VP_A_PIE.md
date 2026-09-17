# VP-A PIE Evidence — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-A |
| **Status** | **EVIDENCE FILED — HARD FAIL on verb PIE** (await Lead **`APPROVE VP-A`**) |
| **Lead gate** | **`APPROVE VP-A`** — after evidence review |
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

_(Awaiting Lead **`APPROVE VP-A`** — evidence filed 2026-09-17 ET; verb PIE **hard-fail**; VP-B recommended next.)_
