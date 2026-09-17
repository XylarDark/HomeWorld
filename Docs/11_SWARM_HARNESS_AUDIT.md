# Docs/11 — Swarm & Harness Performance Audit

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — awaiting Lead **`APPROVE Docs/11`** / **`APPROVE HR STRATEGY`** |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Scope** | How **swarm ops** and **engineering harness** performed from P0–P7 through WAVE A–F and post-audit wrap (Docs/05–10) |
| **Refine plan** | [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) (HR-A…HR-D) |
| **Product next-phase** | **PARKED** — see [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) (DEFERRED until HR refine signed off) |

**Grading:** 1 = broken / blocking · 3 = workable with friction · 5 = reliable at scale. Letter grades summarize the 1–5 score for Lead scan.

---

## Executive summary

| Track | Grade | 1–5 | Headline |
|-------|-------|-----|----------|
| **Swarm (MVP lookdev)** | **B** | 3.6 | P0–P7 + Lead gates delivered signed slice; PHASE_BOARD and dual-OS cleanup lag post-Docs/10 |
| **Harness (UE + automation)** | **C+** | 3.1 | Safe-Build + no-binary policy strong; cloud/CI split, submodule doctor, rules token load, and Windows-only UE loop create recurring friction |
| **Combined readiness for product NP** | **C** | 2.8 | Do **not** start gameplay/lookdev NP until HR-A…D improve measure → tighten → prove loop |

Lead redirected: **refine swarm + harness before product next-phase.** This audit is evidence-based from repo artifacts, not session vibes.

---

## Period audited

| Phase | Evidence |
|-------|----------|
| **P0–P7** | `swarm/PHASE_BOARD.md` (all CLOSED); 29× `Docs/handoffs/P*_*`; `Docs/07_VERTICAL_SLICE_SIGN OFF.md` SIGNED |
| **WAVE A–F** | `Docs/08a`–`08e`, `Docs/08_AUDIT_SIGN_OFF.md` (492-path delete, PR #16); `Docs/08b_HARNESS_GAP.md` |
| **Post-audit** | `Docs/05`–`06`, `Docs/09`, `Docs/10_POST_AUDIT_WRAP.md` (PR #21); transit PR #19/#20; dress runbook + mesh-index fix (`3fed13d`) |

---

## Swarm scorecard

| Dimension | Grade | 1–5 | Evidence (repo) | Friction observed |
|-----------|-------|-----|-----------------|-------------------|
| **Role clarity** | B+ | 4 | `swarm/SWARM_OPS.md` §1 two-tier model; §6 collision map; role cards under `swarm/agents/` | `AGENTS.md` still lists deleted agent-loop entrypoints until WAVE F stub; newcomers see two agent OS narratives |
| **Lead gates** | A | 5 | P0–P7 gate files in `Docs/`; `APPROVE P6` / `SIGN OFF P7`; WAVE A–F each gated; `SIGN OFF AUDIT` on #16 | None blocking — gates worked as designed |
| **Handoffs** | B+ | 4 | `Docs/handoffs/` complete P0–P7 set; `HANDOFF_TEMPLATE.md`; blockers → KNOWN_ERRORS / AUTOMATION_GAPS policy | Post-audit UE work often used runbooks (`05`, `06`, `09`) without parallel `Docs/handoffs/NP_*` discipline |
| **PHASE_BOARD freshness** | C | 3 | Board shows P0–P7 CLOSED, FALLBACK armed | **Stale after Docs/10:** no row for post-audit or HR track; "Current phase: —" does not reflect next work |
| **Conductor vs fan-out** | A- | 4 | P3/P4/P5 fan-out (ENV-H/PROP/LIT, etc.) per SWARM_OPS §7; Conductor-only PHASE_BOARD writes | Cloud-agent PRs (#19 transit, #20 portal fix) bypassed Conductor packet → extra merge/rebase cost |
| **Packet discipline** | B | 3 | SWARM_OPS §7: worker = role card + packet inputs only | Thin-context rule violated when cloud agents loaded full `docs/` + SESSION patterns |
| **Dual OS (swarm vs agent company)** | C+ | 3 | WAVE F removed `Start-AllAgents*`, `gui_automation/`, loop scripts; quarantine on `docs/Automation/AGENT_COMPANY.md` | **856 KB** `docs/SESSION_LOG.md` still dominated by pre-swarm 30-day loop narrative; DAILY_STATE referenced WAVE E after F signed off |
| **Durable memory / docs** | B- | 3 | KNOWN_ERRORS, AUTOMATION_GAPS, capital `Docs/` canon split documented | SESSION_LOG append-only bloat; no rolling summary; agents re-read thousands of lines |

**Swarm average (weighted): 3.6 / 5 → B**

---

## Harness scorecard

| Dimension | Grade | 1–5 | Evidence (repo) | Friction observed |
|-----------|-------|-----|-----------------|-------------------|
| **Safe-Build protocol** | B+ | 4 | `Tools/Safe-Build.ps1`; `docs/Setup/BUILD_POLICY.md`; `08b` canonical table | Cloud agents **cannot** run Safe-Build (no UE on Linux VM); C++ PRs marked "verify on DESKTOP-21CT3H0" — validation gap |
| **DevEnvTemplate submodule** | D+ | 2 | Gitlink `213673f`; `08b` documents init; `npm run doctor` → **MODULE_NOT_FOUND** when submodule empty (verified 2026-09-17) | Fresh clone: empty `DevEnvTemplate/`; pin **behind** template `main` (`2efd756`); doctor/sync blocked until `git submodule update --init` + `doctor:build` |
| **MCP (UE + Blender)** | B- | 3 | `docs/Setup/MCP_SETUP.md`; port 55557; MCP-first in rules | Cloud agent SESSION: "MCP: Failed to connect to Unreal Engine"; Blender MCP absent at P2 TA write time; inherited UPROPERTY invisible to MCP (`KNOWN_ERRORS.md`) |
| **Cursor rules token cost** | C | 3 | **34** always-applied `.cursor/rules/*.mdc`; ~11k lines total; `08b` notes ~3k+ tokens/turn vs template | **Accepted decline** to migrate — but cost hits every cloud-agent turn; overlaps with `AGENTS.md` + skills |
| **CI: validate vs build-win64** | B- | 3 | `validate.yml` on Ubuntu every PR; `ci.yml` on `[self-hosted, windows, ue57]` | **PR #10:** validate **FAILED** until quarantine stubs for moved `docs/workflow/30_DAY_SCHEDULE.md` (`a539123`); build-win64 not gating most doc PRs; runner availability unknown |
| **Cloud agents** | B | 3 | Docs/08–10, transit (#19), materials (#21) shipped via cloud PRs | No Editor/MCP on cloud VM; Windows handoff required for dress/material `.uasset` build; merge conflicts on busy branches |
| **Windows self-hosted link** | C+ | 3 | `docs/Setup/CI_SETUP.md`; handoffs name **DESKTOP-21CT3H0** | No single "Windows Computers" runbook tying Cursor cloud agent → self-hosted runner → local Editor; Lead manually bridges hosts |
| **Python Editor scripts** | B+ | 4 | Idempotent patterns; `place_vs_mvp_*`, `create_master_materials.py`; JSON contract test | **Dress:** 74/78 actors first run — mesh basename `.SM_*` suffix bug (`Docs/handoffs/VS_MVP_DRESS.md`); **Portal #20:** wrong UPROPERTY names in Python until reflection fix |
| **Content binary policy** | A | 5 | Consistent: no `.uasset`/`.umap` in repo across #10, #16, #21 | Windows hosts hold untracked Content; recovery sometimes needed via **git stash** before pull — risk of losing local dress/material work |
| **Merge-conflict hotspots** | C | 3 | Frequent touches: `Docs/README.md`, `docs/SESSION_LOG.md`, `Content/Python/place_vs_mvp_*.py` | Parallel PRs **#18/#19** (transit stack) needed rebase; SESSION_LOG conflicts on every doc PR |

**Harness average (weighted): 3.1 / 5 → C+**

---

## Incident log (evidence-linked)

| ID | Incident | Source | Impact |
|----|----------|--------|--------|
| **SH-01** | CI validate failed: missing `docs/workflow/30_DAY_SCHEDULE.md` after DOCS_LAYOUT move | `08b` §Parallel PR #10; commit `a539123` stubs | Blocked merge until stub paths added — **process smell** (validate checks stale paths) |
| **SH-02** | VS_MVP dress 4/78 meshes missing (basename parsing) | `Docs/handoffs/VS_MVP_DRESS.md`; fix `3fed13d` | First Windows dress run incomplete; required script fix + re-run |
| **SH-03** | Portal marker Python used wrong property names | PR #20 `6902320` | Portal triggers spawned but `DestinationLabel` not set until UPROPERTY names aligned |
| **SH-04** | Cloud agent cannot MCP to Editor | SESSION 2026-09-17 import staging | Scripts land unverified until Windows pass |
| **SH-05** | `npm run doctor` fails on default cloud checkout | Live run 2026-09-17; `08b` init table | Harness health unknown until submodule init |
| **SH-06** | Untracked local Content vs repo scripts | Lead report; WAVE F deleted legacy maps | `git pull` on Windows may require stash/recover of local `.uasset` dress output |

---

## What worked (keep)

- **Lead-gated phases** from P0 through audit WAVE F — clear stop lines.
- **Capital `Docs/` vs lowercase `docs/`** split — product canon survived harness churn.
- **No Content binaries in git** — dress/material graphs stay on Windows; scripts + handoffs are portable.
- **FALLBACK FLIGHT + Docs/07 CLOSED** — scope cuts enforced without reopening slice.
- **Handoff path discipline** during P0–P7 — artifact paths in `Docs/handoffs/` enabled QA re-judge.

---

## Top friction (fix in HR-A…D)

1. **Measure harness health** — doctor, submodule pin, CI path list, rules token budget (HR-A).
2. **Single Windows bridge doc** — cloud agent → DESKTOP/self-hosted runner → Editor/MCP (HR-B).
3. **Refresh PHASE_BOARD + kill dual-OS refs** in entrypoints (HR-C).
4. **Prove one dry-run loop** with re-grade before product NP (HR-D).

---

## Hard rules (unchanged)

| Rule | Status |
|------|--------|
| Docs/07 CLOSED | Do not reopen |
| FALLBACK FLIGHT armed | No free-flight / flight HUD |
| No V3–V8 gameplay in HR track | Product verbs parked |
| No `.uasset`/`.umap` commits | Keep |
| Exactly 10 masters | Keep |

---

## Gate

```
Docs/11 audit status: DRAFT — awaiting Lead APPROVE Docs/11 / APPROVE HR STRATEGY
Do NOT start HR-A until Lead approves.
Product next-phase (NP-A…E) remains DEFERRED until HR-D re-grade passes or Lead parks refine.
```

*Prepared from repo evidence; re-grade after HR-D dry-run.*
