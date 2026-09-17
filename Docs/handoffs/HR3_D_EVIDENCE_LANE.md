# HR3-D DESKTOP Evidence Lane + Auto Re-verify — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR3-D |
| **Status** | **EVIDENCE FILED** — await Lead **`APPROVE HR3-D`** |
| **Lead gate** | **`APPROVE HR3-D`** — closes HR3 track (HR3-C **DEFERRED** by Lead skip) |
| **Spec** | [15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) § HR3-D |
| **Date** | 2026-09-17 ET |

## Summary

Swarm ops now require **explicit host ownership** (**CLOUD** vs **DESKTOP**) on [PHASE_BOARD.md](../../swarm/PHASE_BOARD.md), a **handoff PR contract** (host, grep prefixes, evidence path, pass/fail table) in [SWARM_OPS.md](../../swarm/SWARM_OPS.md) and [CLOUD_AGENT_PACKET.md](../../swarm/CLOUD_AGENT_PACKET.md), and an **auto re-verify rule**: after any blocker-fix phase (e.g. **VP-B**), prior hard-fail greps (**VP-A**) must **re-run and pass** before **VP-C** unlocks.

This handoff is **docs-only** — no fake branch-protection **APPLIED** stamp; no `.uasset`/`.umap`.

---

## Deliverables (this PR)

| Deliverable | Path | Status |
|-------------|------|--------|
| PHASE_BOARD owner lane column | [swarm/PHASE_BOARD.md](../../swarm/PHASE_BOARD.md) | **DONE** |
| Handoff contract + re-verify rule | [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) §4 | **DONE** |
| Cloud packet contract | [swarm/CLOUD_AGENT_PACKET.md](../../swarm/CLOUD_AGENT_PACKET.md) | **DONE** |
| VP re-verify cross-link | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § Re-verify | **DONE** |
| HR3-D spec checkboxes | [15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) § HR3-D | **DONE** |

---

## Host ownership convention

| Tag | Host | Who runs evidence |
|-----|------|-------------------|
| **CLOUD** | Linux Cursor cloud VM | Docs, C++ source, validate CI; **no** MCP/PIE/Shell on DESKTOP |
| **DESKTOP** | Self-hosted **DESKTOP-21CT3H0** | Conductor **parent** only — Safe-Build, Editor, MCP, PIE, Output Log greps ([HR3_A_WINDOWS_EXEC.md](HR3_A_WINDOWS_EXEC.md)) |
| **Lead** | GitHub Settings / human gate | Branch protection apply, **`APPROVE *`** stamps |

Task executors are **not** DESKTOP owners — do not assign Shell/PIE to spawned workers.

---

## Handoff PR contract (required fields)

Every DESKTOP or cross-host phase handoff **and** its PR body must include:

| Field | Example (VP-A) |
|-------|----------------|
| **Host** | `DESKTOP-21CT3H0` |
| **Grep prefixes** | `FORM:`, `FALLBACK:`, `HEAL:`, `NURTURE:`, `DAWN:`, `TAME:`, `GATHER:` |
| **Evidence path** | `Docs/handoffs/VP_A_PIE.md`; log source `Saved/Logs/HomeWorld.log` |
| **Pass/fail table** | One row per prefix — **PASS**, **FAIL**, or **WAIVED** (Lead only) with log excerpt |
| **Preflight** | `npm run preflight:ue` exit code before DESKTOP PIE ([HR3_B_UE_PREFLIGHT.md](HR3_B_UE_PREFLIGHT.md)) |
| **PR URL + merge SHA** | After merge — cloud agents file in handoff |

Conductor **refuses** the next gate if any field is missing or if a prior hard-fail phase was not re-verified when required.

---

## Re-verify rule (blocker-fix → re-prove)

When phase **B** fixes a blocker that caused hard-fail in phase **A**:

1. **B completes** — evidence filed; Lead **`APPROVE VP-B`** (or equivalent).
2. **Re-verify A** — DESKTOP owner re-runs **A's grep checklist** on current `main`; update **A's handoff** with a dated **Re-verify** section (do not delete original fail record).
3. **Unlock C** — **VP-C** (or downstream polish) stays **LOCKED** until step 2 shows **PASS** on all required prefixes **or** Lead explicit **WAIVED** per prefix.

Canonical chain for product VP track:

```
VP-A (filed hard-fail) → VP-B (blocker fix) → VP-A re-verify (greps) → VP-C unlock
```

Same pattern applies to any future blocker-fix phase that invalidates prior DESKTOP evidence.

---

## Example: VP-A re-verify checklist (after VP-B)

Run on **DESKTOP-21CT3H0** after VP-B merge. Conductor parent only.

### Prerequisites

- [ ] `git pull` on `main` at merge SHA ≥ VP-B evidence SHA
- [ ] `.\Tools\Safe-Build.ps1` green
- [ ] `npm run preflight:ue` exit **0** (no `--skip-mcp` for full PIE path)
- [ ] Editor open; MCP port **55557** reachable
- [ ] Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`
- [ ] Bootstrap chain current (`bootstrap_project.py` or documented subset)

### Runbooks (same as VP-A)

| Runbook | Verbs |
|---------|-------|
| [12c_NP_C_FORM_V1.md](../12c_NP_C_FORM_V1.md) | FORM, FALLBACK, portal |
| [12d_NP_D_SYS_V3_V4.md](../12d_NP_D_SYS_V3_V4.md) | GATHER, TAME |
| [12e_NP_E_SYS_V6_V8.md](../12e_NP_E_SYS_V6_V8.md) | HEAL, NURTURE, DAWN |

### Grep table (`Saved/Logs/HomeWorld.log`)

| Prefix | VP-A (2026-09-17) | Re-verify (fill after VP-B) | Pass? |
|--------|-------------------|----------------------------|-------|
| `FORM:` | **FAIL** (0 gameplay) | _pending VP-B + re-run_ | |
| `FALLBACK:` | **FAIL** | _pending_ | |
| `HEAL:` | **FAIL** | _pending_ | |
| `NURTURE:` | **FAIL** | _pending_ | |
| `DAWN:` | **FAIL** | _pending_ | |
| `TAME:` | **FAIL** | _pending_ | |
| `GATHER:` | **FAIL** | _pending_ | |

### Re-verify filing

- Append **§ Re-verify** to [VP_A_PIE.md](VP_A_PIE.md) with timestamp, repo SHA, and updated table.
- [PHASE_BOARD.md](../../swarm/PHASE_BOARD.md): set VP-A re-verify row; unlock **VP-C** only when all required rows **PASS** or Lead **WAIVED**.
- Optional: `execute_python_script("pie_test_runner.py")` → `Saved/pie_test_results.json` (character spawn must pass for verb greps).

---

## PHASE_BOARD owner map (HR3 + VP active phases)

| Phase | Host owner | Evidence runner |
|-------|------------|-----------------|
| HR3-A | DESKTOP | Conductor parent |
| HR3-B | CLOUD + DESKTOP | Cloud script PR; DESKTOP dry-run |
| HR3-C | Lead | GitHub Settings ( **DEFERRED** — Lead skip) |
| HR3-D | CLOUD | This docs PR |
| VP-A | DESKTOP | Conductor parent (filed; re-verify pending VP-B) |
| VP-B | DESKTOP | Conductor parent (**PARKED**) |
| VP-C | CLOUD + DESKTOP | Locked until VP-A re-verify |
| VP-D | CLOUD + DESKTOP | Locked |

---

## Gate

Lead **`APPROVE HR3-D`** closes the HR3 track for swarm A+ (with HR3-C explicitly deferred). Resume **VP-B** after HR3-D approval; then run VP-A re-verify before **VP-C**.
