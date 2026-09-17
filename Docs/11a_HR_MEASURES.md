# Docs/11a — HR-A Measure & Inventory

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE** — awaiting Lead **`APPROVE HR-A`** |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Parent gate** | Lead **`APPROVE Docs/11`** — **GRANTED** (Luke Thompson, 2026-09-17 ET; equivalent: "go with your suggestion") |
| **Audit input** | [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) |
| **Refine plan** | [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) (HR-A deliverable) |
| **Hard rules** | Docs/07 CLOSED; FALLBACK armed; no V3–V8 gameplay; docs/config measure only |

**Gate:** Lead **`APPROVE HR-A`** unlocks HR-B harness tighten. Do **not** start HR-B until granted.

---

## 1. Host matrix (cloud vs Windows)

| Check | Cloud VM (Cursor agent) | Windows DESKTOP-21CT3H0 |
|-------|-------------------------|-------------------------|
| **Repo HEAD at measure** | `333e4b0` (post PR #23) | **`675388a`** (Docs/11 PR #22 tip) |
| **Measure timestamp** | 2026-09-17 UTC | **2026-09-17 ~23:13 ET** |
| **`git submodule update --init DevEnvTemplate`** | **PASS** — checked out `213673f` after init | **PASS** — pin `213673ff181743a703ab390af0d43097f889a0f9`; `DevEnvTemplate/package.json` = True; `dist/scripts/doctor/cli.js` = True after init |
| **Node version** | **v22.14.0** / npm 10.9.7 (EBADENGINE vs template `>=24` — accepted decline) | **v22.17.1** / npm **10.9.2** (EBADENGINE — accepted decline) |
| **`npm run doctor:build`** | **PASS** — exit 0 after submodule init | **Not re-run** — `cli.js` present after init (dist prebuilt in submodule checkout) |
| **`npm run doctor` exit code** | **0** — score **77/100** | **Non-zero** — Critical ×5: TypeScript Not Configured, ESLint Not Configured, No JS Unit Tests Detected, Secrets Handling Not Detected, **Always-Applied Rule Budget Exceeded**; Warnings ×5; Working ×1 (CI pipeline configured). Report: `.devenv/health-report.json` (gitignored) |
| **Safe-Build / Editor / MCP** | **N/A** — no UE on Linux cloud VM | **Not measured this pass** — HR-D dry-run scope |

### Cloud vs Windows note

On a **default cloud checkout**, `DevEnvTemplate/` is **empty** until `git submodule update --init DevEnvTemplate`. Without init, `npm run doctor` fails with `MODULE_NOT_FOUND` (`DevEnvTemplate/dist/scripts/doctor/cli.js`) — incident **SH-05** class. After init + `npm run doctor:build`, doctor runs on cloud with exit 0.

On **Windows DESKTOP-21CT3H0**, submodule init alone yields a checkout with prebuilt `dist/`; doctor runs but exits **non-zero** on the same **accepted-decline** criticals (TS/ESLint/JS tests/secrets/rule budget) plus rule-budget flag. **UE validation (Safe-Build, Editor, MCP) still requires Windows** — deferred to HR-D.

---

## 2. DevEnvTemplate submodule

**Command (cloud, 2026-09-17):**

```
$ git submodule status DevEnvTemplate
 213673ff181743a703ab390af0d43097f889a0f9 DevEnvTemplate (heads/main)
```

**Windows (DESKTOP-21CT3H0, 2026-09-17 ~23:13 ET, HEAD `675388a`):**

```
$ git submodule status DevEnvTemplate
 213673ff181743a703ab390af0d43097f889a0f9 DevEnvTemplate
```

| Item | Value |
|------|-------|
| **Remote** | `https://github.com/XylarDark/DevEnvTemplate.git` |
| **Pinned SHA (HomeWorld gitlink)** | `213673ff181743a703ab390af0d43097f889a0f9` |
| **Pin message** | `feat(agents): put the human on steer, taste, and test` |
| **Template `main` HEAD (reference)** | `2efd756` — behind per [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) |
| **Fresh clone symptom** | Empty `DevEnvTemplate/` → doctor MODULE_NOT_FOUND until init (+ build on cloud) |
| **Init recipe** | `git submodule update --init DevEnvTemplate` → `npm run doctor:build` (if no dist) → `npm run doctor` |

---

## 3. Always-applied Cursor rules token budget

| Metric | Cloud VM | Windows DESKTOP-21CT3H0 |
|--------|----------|-------------------------|
| **Always-applied `.cursor/rules/*.mdc` files** | **34** | **34** |
| **Total lines** | **2,221** | **2,255** |
| **Total bytes (chars)** | **121,768** (~119 KB) | **122,342** (~119 KB) |

**File list (34):** `00-core-principles` through `22-unreal-editor-ui`, plus `automation-standards`, `pcg-best-practices`, `ue57-*`, `unreal-*`.

**Doctor flag (both hosts):** `Always-Applied Rule Budget Exceeded` — **accepted decline** per AGENTS.md DevEnvTemplate adoption table; HR-B may glob-scope incrementally.

**Overlap:** Rules duplicate content in root `AGENTS.md` and `.agents/skills/` — HR-B target is slimming without mass delete.

---

## 4. CI validate.yml — required-doc audit (SH-01 class)

**Source:** `.github/workflows/validate.yml` — "Check required docs exist and are non-empty" + "Check task docs exist".

### 4.1 Required docs (workflow list)

| Path | On disk (both hosts) | Notes |
|------|----------------------|-------|
| `docs/SETUP.md` | OK | |
| `docs/CONVENTIONS.md` | OK | |
| `docs/KNOWN_ERRORS.md` | OK | |
| `docs/SESSION_LOG.md` | OK | **854 KB** — bloat risk |
| `docs/workflow/README.md` | OK | **Residue:** references deleted `Start-AllAgents-InNewWindow.ps1` |
| `docs/workflow/30_DAY_SCHEDULE.md` | OK | Stub exists (PR #10) — **SH-01 mitigated by stubs**, not DOCS_LAYOUT alignment |
| `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` | OK | |
| `AGENTS.md` | OK | Entrypoint grep clean on Windows (see §6) |

**Missing from validate list:** **0** (all paths exist and non-empty).

### 4.2 Task docs (workflow list)

| Path | On disk | Notes |
|------|---------|-------|
| `docs/tasks/CHARACTER_ANIMATION.md` | OK | **Quarantine pointer stub** → `docs/TaskLists/TaskSpecs/` |
| `docs/tasks/CHARACTER_ORIENTATION.md` | OK | Stub |
| `docs/tasks/CHARACTER_GROUND.md` | OK | Stub |
| `docs/tasks/PCG_FOREST_ON_MAP.md` | OK | Stub |

**SH-01 class drift:** CI enforces **stub paths** under `docs/tasks/` that are **not** in [docs/DOCS_LAYOUT.md](../docs/DOCS_LAYOUT.md) canonical tree (`docs/TaskLists/TaskSpecs/` is canonical). Files exist so CI passes on Windows and cloud — **stubs mask drift**; HR-B should repoint validate.yml to TaskSpecs or drop stub requirement.

---

## 5. Swarm board freshness (post-Docs/10 gap)

**Source:** `swarm/PHASE_BOARD.md` (cloud + Windows, 2026-09-17)

| Field | Current value | Gap |
|-------|---------------|-----|
| **Current phase** | **Blank** (`—` / MVP vertical slice CLOSED) | No **POST-AUDIT** or **HR-A…D** row |
| **P0–P7 rows** | All **CLOSED** | Correct |
| **Docs/05–10 track** | Not listed | Missing post-audit CLOSED section |
| **HR track** | Not listed | Should show HR-A COMPLETE → gate HR-A |
| **Product NP** | Not listed | Should show DEFERRED per [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Open tasks / defects** | **Empty** (`—`) | Expected until HR-C refresh |

**Verdict:** PHASE_BOARD **stale after Docs/10** on both hosts — confirms audit score **C (3/5)** for board freshness. HR-C deliverable.

---

## 6. Dual-OS / agent-company residue scan

### 6.1 Entrypoint grep (Windows DESKTOP-21CT3H0)

Pattern: `Start-AllAgents|AGENT_COMPANY|gui_automation|run_automation_cycle`

| File | Matches |
|------|---------|
| **`AGENTS.md`** | **None** — WAVE F cleanup landed on Windows tree |
| **`README.md`** | **None** |
| **`docs/TaskLists/DAILY_STATE.md`** | **None** |

### 6.2 Residual (both hosts — HR-B/C scope)

| Location | Finding |
|----------|---------|
| **`docs/workflow/README.md`** | References deleted `Start-AllAgents-InNewWindow.ps1` |
| **`docs/TaskLists/README.md`** | Same |
| **`.cursor/rules/07-ai-agent-behavior.mdc`** | Multiple live Start-AllAgents instructions |
| **`.cursor/rules/19-automation-gaps.mdc`** | Run-GapSolverAgent / AGENT_COMPANY references |
| **`docs/SESSION_LOG.md`** | ~854 KB historical agent-loop narrative |
| **`Tools/Start-AllAgents*`** | **0 files** — deleted WAVE F |

**Summary:** Primary entrypoints (`AGENTS.md`, `README.md`, `DAILY_STATE.md`) are **clean on Windows**. Workflow docs and always-applied rules still carry pre-WAVE-F residue — HR-B/C trim.

---

## 7. SESSION_LOG / memory bloat

| Metric | Value |
|--------|-------|
| **`docs/SESSION_LOG.md` size** | **854 KB** (~873,827 bytes) |
| **CI requires non-empty** | Yes — validate.yml |
| **HR-C policy** | Rolling `docs/SESSION_SUMMARY.md` (last 30 days); stop mandatory full SESSION read for swarm |

---

## 8. HR-A checklist vs refine spec

| HR-A item ([11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md)) | Status |
|------|--------|
| Doctor pass/fail matrix | **Done** — cloud + Windows §1 |
| Submodule gitlink vs template main | **Done** — §2 |
| Rules token budget (count lines/chars) | **Done** — §3 |
| CI flake map (validate paths vs DOCS_LAYOUT) | **Done** — §4 (SH-01 class noted) |
| PHASE_BOARD snapshot + post-Docs/10 gaps | **Done** — §5 |
| Dual-OS pointer inventory | **Done** — §6 |
| Deliverable `Docs/11a_HR_MEASURES.md` | **Done** — this file |

---

## 9. Gate

```
Docs/11 status: APPROVED — Lead Luke Thompson, 2026-09-17 ET
HR-A status: COMPLETE — awaiting Lead APPROVE HR-A
Do NOT start HR-B until Lead approves.
Measured: cloud VM 2026-09-17 UTC; Windows DESKTOP-21CT3H0 2026-09-17 ~23:13 ET (HEAD 675388a).
```

*HR-A measurement pass complete on both hosts.*
