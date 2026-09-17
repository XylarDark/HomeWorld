# Docs/11 — Swarm & Harness Refine Strategy

| Field | Value |
|-------|-------|
| **Status** | **ACTIVE** — HR-B2 **COMPLETE awaiting APPROVE HR-B2**; HR-D dry-run **COMPLETE** but **`APPROVE HR-D` deferred** by Lead |
| **Approval notes** | Lead Luke Thompson, 2026-09-17 ET — Docs/11 / HR strategy; **APPROVE HR-A**; **APPROVE HR-B**; **APPROVE HR-C**; HR-D dry-run delivered; **HR-B2 before APPROVE HR-D** (2026-09-17 ET) |
| **Date** | 2026-09-17 |
| **HR-A stamp** | Lead Luke Thompson, **APPROVE HR-A**, 2026-09-17 ET |
| **HR-B stamp** | Lead Luke Thompson, **APPROVE HR-B**, 2026-09-17 ET — [11b_HR_B_HANDOFF.md](11b_HR_B_HANDOFF.md) |
| **HR-C stamp** | Lead Luke Thompson, **APPROVE HR-C**, 2026-09-17 ET — [11c_HR_C_HANDOFF.md](11c_HR_C_HANDOFF.md) |
| **HR-D dry-run** | **COMPLETE** — [11d_HR_D_HANDOFF.md](11d_HR_D_HANDOFF.md), [handoffs/HR_D_DRY_RUN.md](handoffs/HR_D_DRY_RUN.md) |
| **HR-D defer** | Lead deferred **`APPROVE HR-D`** → **HR-B2 first**, 2026-09-17 ET — [11d_HR_D_DEFER.md](11d_HR_D_DEFER.md) |
| **HR-B2 stamp** | **COMPLETE awaiting APPROVE HR-B2**, 2026-09-17 — [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) |
| **Author** | Conductor (HomeWorld) |
| **Audit input** | [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) |
| **Product next-phase** | **PARKED** — [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) (NP-A…E DEFERRED) |

---

## Why

Swarm delivered P0–P7 and audit/post-audit docs, but **harness friction** (submodule doctor, CI/doc drift, cloud-vs-Windows UE gap, SESSION bloat, dual agent OS residue, merge hotspots) consumed Lead and agent time on **#10 CI stubs**, **dress mesh discovery**, **portal UPROPERTY #20**, and **rebase conflicts** on transit PRs.

Lead directive: **refine swarm + harness technologies before any product gameplay next-phase.**

---

## Board status

| Track | Status |
|-------|--------|
| **Docs/11 audit + refine** | **APPROVED** — Lead Luke Thompson, 2026-09-17 ET |
| **HR-A** | **APPROVED** — [11a_HR_MEASURES.md](11a_HR_MEASURES.md) |
| **HR-B** | **APPROVED** — [11b_HR_B_HANDOFF.md](11b_HR_B_HANDOFF.md) |
| **HR-C** | **APPROVED** — [11c_HR_C_HANDOFF.md](11c_HR_C_HANDOFF.md) |
| **HR-D** | **COMPLETE — awaiting APPROVE HR-D** (Lead deferred approval → HR-B2 first) — [11d_HR_D_HANDOFF.md](11d_HR_D_HANDOFF.md), [11d_HR_D_DEFER.md](11d_HR_D_DEFER.md) |
| **HR-B2** | **COMPLETE awaiting APPROVE HR-B2** — [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) |
| **Product NP-A…E** | **PARKED** — blocked until **`APPROVE HR-D`** after HR-B2 **or** Lead explicitly unblocks NP |

---

## HR plan (Lead gates each)

Naming: **HR-A … HR-D** (Harness Refine). Do **not** reuse WAVE or NP ids here.

### HR-A — Measure & inventory

Baseline the harness and swarm ops state with **numbers**, not narratives.

| Item | Spec |
|------|------|
| **Doctor** | Run `git submodule update --init DevEnvTemplate`; `npm run doctor:build`; `npm run doctor` on Lead Windows + cloud snapshot; record pass/fail matrix |
| **Submodule** | Document current gitlink vs template `main`; list deltas (multi-agent-swarm guide, sync fixes) |
| **Rules token budget** | Count always-applied `.cursor/rules/*.mdc` lines/chars; sample turn cost vs `.agents/skills/` only |
| **CI flake map** | Audit `validate.yml` required-doc list vs `docs/DOCS_LAYOUT.md`; note stale paths (SH-01 class); document `ci.yml` runner last-seen status |
| **Swarm board** | Snapshot `PHASE_BOARD.md`; list missing post-Docs/10 rows; inventory open dual-OS pointers in `AGENTS.md`, `README.md`, `DAILY_STATE.md` |
| **Deliverable** | `Docs/11a_HR_MEASURES.md` (created after gate) — tables + command output excerpts |
| **Gate** | Lead **`APPROVE HR-A`** |

### HR-B — Harness tighten

Close the highest-impact harness gaps from the audit.

| Item | Spec |
|------|------|
| **DevEnvTemplate** | Bump gitlink **or** document accepted pin + init runbook in `docs/Setup/CURSOR_DEV.md`; ensure `npm run doctor` works after clone |
| **Safe-Build / MCP single path** | One entry in `AGENTS.md` Commands: Safe-Build → Editor → MCP; remove stray `Build-HomeWorld.bat`-only instructions |
| **CI policy** | Fix validate required-doc paths to match DOCS_LAYOUT; document when `ci.yml` is required vs `[skip ci]`; optional: CI status badge in README |
| **Rules slimming (non-destructive)** | Move UE-only rules to glob-scoped where safe; document token budget target — **no** mass delete without Lead |
| **Windows bridge** | New short runbook: **Cursor cloud agent → self-hosted runner (`docs/Setup/CI_SETUP.md`) → DESKTOP Editor/MCP** — when each host runs which script |
| **Deliverable** | PR(s) to harness docs + validate.yml path fixes; optional submodule bump |
| **Gate** | Lead **`APPROVE HR-B`** |

### HR-C — Swarm ops refine

Refresh coordination layer for post-audit work (including cloud-agent + Conductor).

| Item | Spec |
|------|------|
| **PHASE_BOARD** | Add **POST-AUDIT** section: Docs/05–10 CLOSED; current track = HR-A…D; product NP parked |
| **Handoff / packet templates** | Extend `HANDOFF_TEMPLATE.md` for **cloud-agent PR** flows: branch naming, evidence paths, "no MCP on cloud" checklist |
| **Kill stale dual-OS refs** | Trim `AGENTS.md` / `docs/TaskLists/DAILY_STATE.md` references to deleted agent-loop tools; point to `swarm/SWARM_OPS.md` + Conductor only |
| **SESSION_LOG hygiene** | Add rolling **`docs/SESSION_SUMMARY.md`** (last 30 days) policy; stop requiring full SESSION read at session start for swarm work |
| **Deliverable** | Updated `swarm/PHASE_BOARD.md`, template, entrypoint pointers |
| **Gate** | Lead **`APPROVE HR-C`** |

### HR-D — Prove (dry-run loop)

Demonstrate the refined harness end-to-end before unlocking product NP.

| Item | Spec |
|------|------|
| **Dry-run** | Conductor assigns one **docs-only** task to cloud agent → PR → (optional) Windows Safe-Build if C++ touched → handoff with evidence paths |
| **Re-grade** | Update [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) dimension scores with before/after |
| **Unlock rule** | If combined grade ≥ **B- (3.4)** on harness+swarm **or** Lead accepts residual risks, product next-phase doc may be rewritten/unblocked |
| **Deliverable** | `Docs/handoffs/HR_D_DRY_RUN.md` + amended audit grades |
| **Gate** | Lead **`APPROVE HR-D`** → unlock product NP planning **or** schedule HR-B2 if dry-run fails |

### HR-B2 — Residual harness risks (Lead before APPROVE HR-D)

Close deferred items from HR-B and audit residual list. Lead chose **HR-B2 before `APPROVE HR-D`** — see [11d_HR_D_DEFER.md](11d_HR_D_DEFER.md).

| Item | Spec |
|------|------|
| **DevEnvTemplate pin bump** | Bump gitlink from `213673f` toward template `master` (`2efd756`+); `npm run doctor:build`; revert if host scripts break |
| **Rules diet** | Non-destructive globs for `16`, `19`, and other safe always-on leftovers; report before/after counts |
| **Doctor criticals** | Document accepted declines in `docs/Setup/DOCTOR_POLICY.md` — no fake Node app |
| **Deliverable** | [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) |
| **Gate** | Lead **`APPROVE HR-B2`** → may unlock **`APPROVE HR-D`** |

---

## Hard rules (every HR phase)

| Rule | Source |
|------|--------|
| Docs/07 CLOSED | Do not reopen vertical-slice sign-off |
| FALLBACK FLIGHT armed | No free-flight / flight HUD |
| No V3–V8 gameplay implementation | Product verbs parked |
| No `.uasset`/`.umap` commits | Local Windows only |
| Exactly 10 masters | Docs/02 |
| Lead APPROVE each HR-* before implementation PR | This doc |
| Docs-only default for HR-A/C | HR-B may touch validate.yml + docs; no gameplay C++ unless HR-B explicitly includes build fix |

---

## Explicit DEFER (HR track)

| Item | Reason |
|------|--------|
| Product NP-A…E (lookdev apply, form swap, SYS verbs) | Lead redirect — after HR refine |
| Full forest PCG / new biomes | Off-slice |
| Nanite/Lumen beauty gates | Docs/04 deferred |
| Crafting / 7th resource / combat | Out of MVP canon |
| Reopening Docs/07 for free-flight | Lead CLOSED |
| Retire all 34 always-applied rules in one PR | Risky; HR-B incremental only |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE Docs/11`** or **`APPROVE HR STRATEGY`** | HR-A measurement work |
| 1 | **`APPROVE HR-A`** | HR-B harness PRs |
| 2 | **`APPROVE HR-B`** | HR-C swarm ops refresh |
| 3 | **`APPROVE HR-C`** | HR-D dry-run |
| 4 | **`APPROVE HR-D`** | Product next-phase rewrite (replace DEFERRED NP board) **or** Lead override |
| 4b | **`APPROVE HR-B2`** (Lead inserted before step 4) | Residual harness closure → then **`APPROVE HR-D`** |

```
Docs/11 / HR STRATEGY: APPROVED — Lead Luke Thompson, 2026-09-17 ET
HR-A: APPROVED — Lead Luke Thompson, 2026-09-17 ET
HR-B: APPROVED — Lead Luke Thompson, 2026-09-17 ET (see 11b_HR_B_HANDOFF.md)
HR-C: APPROVED — Lead Luke Thompson, APPROVE HR-C, 2026-09-17 ET (see 11c_HR_C_HANDOFF.md)
HR-D: dry-run COMPLETE — awaiting Lead APPROVE HR-D (see 11d_HR_D_HANDOFF.md); approval deferred → HR-B2 first (see 11d_HR_D_DEFER.md)
HR-B2: COMPLETE — awaiting Lead APPROVE HR-B2 (see 11e_HR_B2_HANDOFF.md)
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) | Complete — HR is **post-audit** harness/swarm pass |
| [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) | WAVE B baseline — HR-B may close remaining rows |
| [10_POST_AUDIT_WRAP.md](10_POST_AUDIT_WRAP.md) | Closed product wrap — HR does not redo masters/NightMix |
| [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) | Process authority — HR-C updates board/templates only |

---

*Conductor prepared this file; HR-B2 complete — awaiting Lead APPROVE HR-B2.*
