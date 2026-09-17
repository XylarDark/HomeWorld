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
| **`git submodule update --init DevEnvTemplate`** | **PASS** — checked out `213673f` after init (2026-09-17) | **PENDING Windows DESKTOP-21CT3H0** |
| **Node version** | **v22.14.0** (EBADENGINE vs template `>=24` — accepted decline per AGENTS.md) | **PENDING Windows DESKTOP-21CT3H0** |
| **`npm run doctor:build`** | **PASS** — exit 0 after submodule init | **PENDING Windows DESKTOP-21CT3H0** |
| **`npm run doctor` exit code** | **0** — score **77/100**; critical: TS/ESLint/JS tests/secrets/rule budget (accepted declines for UE host) | **PENDING Windows DESKTOP-21CT3H0** |
| **Safe-Build / Editor / MCP** | **N/A** — no UE on Linux cloud VM | **PENDING Windows DESKTOP-21CT3H0** |

### Cloud vs Windows note

On a **default cloud checkout**, `DevEnvTemplate/` is **empty** until `git submodule update --init DevEnvTemplate`. Without init, `npm run doctor` fails with `MODULE_NOT_FOUND` (`DevEnvTemplate/dist/scripts/doctor/cli.js`) — incident **SH-05** class. After init + `npm run doctor:build`, doctor runs on cloud; **UE validation still requires Windows**.

Conductor should fill **PENDING Windows** rows after a Lead Windows run and append evidence paths.

---

## 2. DevEnvTemplate submodule

**Command (cloud, 2026-09-17):**

```
$ git submodule status DevEnvTemplate
 213673ff181743a703ab390af0d43097f889a0f9 DevEnvTemplate (heads/main)
```

| Item | Value |
|------|-------|
| **Remote** | `https://github.com/XylarDark/DevEnvTemplate.git` |
| **Pinned SHA (HomeWorld gitlink)** | `213673ff181743a703ab390af0d43097f889a0f9` |
| **Pin message** | `feat(agents): put the human on steer, taste, and test` |
| **Template `main` HEAD (reference)** | `2efd756` — behind per [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) |
| **Fresh clone symptom** | Empty `DevEnvTemplate/` → doctor MODULE_NOT_FOUND until init + build |
| **Init recipe** | `git submodule update --init DevEnvTemplate` → `npm run doctor:build` → `npm run doctor` |

---

## 3. Always-applied Cursor rules token budget

**Count (cloud, 2026-09-17):**

| Metric | Value |
|--------|-------|
| **Always-applied `.cursor/rules/*.mdc` files** | **34** |
| **Total lines** | **2,221** |
| **Total bytes (chars)** | **121,768** (~119 KB) |

**File list (34):** `00-core-principles` through `22-unreal-editor-ui`, plus `automation-standards`, `pcg-best-practices`, `ue57-*`, `unreal-*`.

**Doctor flag:** `Always-Applied Rule Budget Exceeded` (critical on cloud run — **accepted decline** per AGENTS.md DevEnvTemplate adoption table; HR-B may glob-scope incrementally).

**Overlap:** Rules duplicate content in root `AGENTS.md` and `.agents/skills/` — HR-B target is slimming without mass delete.

---

## 4. CI validate.yml — required-doc audit (SH-01 class)

**Source:** `.github/workflows/validate.yml` — "Check required docs exist and are non-empty" + "Check task docs exist".

### 4.1 Required docs (workflow list)

| Path | On disk (cloud) | Notes |
|------|-----------------|-------|
| `docs/SETUP.md` | OK | |
| `docs/CONVENTIONS.md` | OK | |
| `docs/KNOWN_ERRORS.md` | OK | |
| `docs/SESSION_LOG.md` | OK | **854 KB** — bloat risk |
| `docs/workflow/README.md` | OK | **Residue:** references deleted `Start-AllAgents-InNewWindow.ps1` |
| `docs/workflow/30_DAY_SCHEDULE.md` | OK | Stub/quarantine path (SH-01 fixed post-PR #10) |
| `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` | OK | |
| `AGENTS.md` | OK | Partial dual-OS cleanup (see §6) |

**Missing from validate list:** **0** (all paths exist and non-empty on cloud snapshot).

### 4.2 Task docs (workflow list)

| Path | On disk | Notes |
|------|---------|-------|
| `docs/tasks/CHARACTER_ANIMATION.md` | OK | **Quarantine pointer stub** → `docs/TaskLists/TaskSpecs/` |
| `docs/tasks/CHARACTER_ORIENTATION.md` | OK | Stub |
| `docs/tasks/CHARACTER_GROUND.md` | OK | Stub |
| `docs/tasks/PCG_FOREST_ON_MAP.md` | OK | Stub |

**SH-01 class drift:** CI enforces **stub paths** under `docs/tasks/` that are **not** in [docs/DOCS_LAYOUT.md](../docs/DOCS_LAYOUT.md) canonical tree (`docs/TaskLists/TaskSpecs/` is canonical). Files exist so CI passes, but the list is **stale vs layout** — HR-B should repoint validate.yml to TaskSpecs or drop stub requirement.

---

## 5. Swarm board freshness (post-Docs/10 gap)

**Source:** `swarm/PHASE_BOARD.md` (read 2026-09-17)

| Field | Current value | Gap |
|-------|---------------|-----|
| **Current phase** | `—` (MVP vertical slice CLOSED) | No **POST-AUDIT** or **HR-A…D** row |
| **P0–P7 rows** | All **CLOSED** | Correct |
| **Docs/05–10 track** | Not listed | Missing post-audit CLOSED section |
| **HR track** | Not listed | Should show HR-A IN PROGRESS → gate HR-A |
| **Product NP** | Not listed | Should show DEFERRED per [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Open tasks / defects** | Empty (`—`) | Expected until HR-C refresh |

**Verdict:** PHASE_BOARD **stale after Docs/10** — confirms audit score **C (3/5)** for board freshness. HR-C deliverable.

---

## 6. Dual-OS / agent-company residue scan

Grep targets: `AGENTS.md`, `docs/TaskLists/DAILY_STATE.md`, `README.md`, entry workflow docs.

| Location | Pattern | Finding |
|----------|---------|---------|
| **`AGENTS.md`** | agent company / AGENT_COMPANY | Quarantine pointers only (lines 11, 85) — **OK** |
| **`AGENTS.md`** | Start-AllAgents | **Not in Commands** (removed WAVE F) — **OK** |
| **`AGENTS.md`** | automatic development cycle | **Still present** (line 94) — references removed loop scripts; **HR-C trim** |
| **`AGENTS.md`** | Fixer/Guardian/Watcher | Editor log bullet (line 88) — references removed agent company — **HR-C trim** |
| **`README.md`** | AGENT_COMPANY | Quarantine pointer only — **OK** |
| **`docs/TaskLists/DAILY_STATE.md`** | WAVE E / SIGN OFF | **Stale:** still says "await SIGN OFF AUDIT" / WAVE F prep; audit **signed off** — **HR-C refresh** |
| **`docs/workflow/README.md`** | Start-AllAgents-InNewWindow | **Active driver** references **deleted** script (WAVE F) — **HR-B/C fix** |
| **`docs/TaskLists/README.md`** | Start-AllAgents-InNewWindow | Same — **deleted tool residue** |
| **`docs/README.md`** | Agent company | Index row under Automation/ — historical label — **low priority** |
| **`.cursor/rules/07-ai-agent-behavior.mdc`** | Start-AllAgents* | **Multiple live instructions** for deleted bats — **HR-B rules trim** |
| **`.cursor/rules/19-automation-gaps.mdc`** | AGENT_COMPANY / Run-GapSolverAgent | References removed Gap-Solver path — **HR-C** |
| **`docs/SESSION_LOG.md`** | Start-AllAgents / agent company | **~854 KB** historical narrative — not entrypoint; **HR-C rolling summary policy** |
| **`Tools/Start-AllAgents*`** | filesystem | **0 files** — deleted WAVE F; docs still cite them |

**Summary:** WAVE F removed executables; **entrypoints and always-applied rules still teach the old agent-company loop**. Swarm path (`START_HERE` + Conductor) is documented but not exclusive in rules/session ops.

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
| Doctor pass/fail matrix | **Partial** — cloud filled; Windows PENDING |
| Submodule gitlink vs template main | **Done** — §2 |
| Rules token budget (count lines/chars) | **Done** — §3 |
| CI flake map (validate paths vs DOCS_LAYOUT) | **Done** — §4 (SH-01 class noted) |
| PHASE_BOARD snapshot + post-Docs/10 gaps | **Done** — §5 |
| Dual-OS pointer inventory | **Done** — §6 |
| Deliverable `Docs/11a_HR_MEASURES.md` | **Done** — this file |

---

## 9. Gate

```
HR-A status: COMPLETE — awaiting Lead APPROVE HR-A
Do NOT start HR-B until Lead approves.
Windows DESKTOP-21CT3H0: fill PENDING rows in §1 after local doctor run.
```

*Measured on cloud VM 2026-09-17; Windows columns for Conductor backfill.*
