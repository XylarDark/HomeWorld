# Docs/14 — Verify & Polish (VP) Strategy

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / ACTIVE** — Lead Luke Thompson, **`APPROVE VP STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Baseline** | Main post-NP + HR2 — product NP-A…E **CLOSED**, HR2-A…C **CLOSED** |
| **Author** | Conductor (HomeWorld) |
| **Prior tracks** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) (NP **CLOSED**), [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) (HR2 **CLOSED**) |
| **Audit input** | Post-NP audit residuals PA-01…PA-08 (see § Why VP) |

---

## Gate

Lead **`APPROVE VP STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET).

**Next gate (VP):** Lead **`APPROVE VP-C`** — VP-C impl **IN PROGRESS / PENDING APPROVE VP-C** ([handoffs/VP_C_POLISH.md](handoffs/VP_C_POLISH.md)); VP-A re-verify **STILL FAIL** gates COMPLETE.

**VP-A APPROVED** — Lead **`APPROVE VP-A`**, 2026-09-17 ET (hard-fail accepted). **VP-B APPROVED / CLOSED** — Lead **`APPROVE VP-B`**, 2026-09-17 ET ([handoffs/VP_B_SMOKE_CHARACTER.md](handoffs/VP_B_SMOKE_CHARACTER.md); PR #67 @ `e00c542`). **VP-C IN PROGRESS** (unlocked). **VP-D LOCKED**.

### Re-verify (HR3-D)

After **VP-B** (or any blocker-fix phase), **VP-A verb greps must re-run** on DESKTOP before **VP-C done criteria** are met. Do not treat the original VP-A hard-fail record as permanent — append a **§ Re-verify** section to [handoffs/VP_A_PIE.md](handoffs/VP_A_PIE.md) with updated pass/fail table. Checklist: [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md). Conductor must file re-verify (or Lead **WAIVE** per prefix) before marking VP-C **COMPLETE** — VP-C planning/impl may proceed in parallel.

---

## Why VP (not another NP or HR pass)

Product NP (NP-A…E) and Harness Refine 2 (HR2-A…C) are **CLOSED**. Senior post-NP audit at NP-E merge identified **verify-and-polish residuals** — code and runbooks exist, but **Windows PIE evidence** and **thin polish** remain. VP is a **surgical pass**: prove verbs in Editor, fix smoke/character blockers, optional playability dress, bootstrap + branch-protection hygiene.

| ID | Residual | Severity | VP phase |
|----|----------|----------|----------|
| **PA-01** | Full PIE verb pass (FORM / FALLBACK / HEAL / NURTURE / DAWN / TAME) — runbooks in Docs/12c–12e but **no filed Output Log evidence** on DESKTOP | **High** | **VP-A** |
| **PA-02** | NightMix Python smoke — `KismetMaterialLibrary` API may fail on some UE 5.7 Editor builds | **Med** | **VP-B** |
| **PA-03** | ABP skeleton warning risk — `ABP_HomeWorldCharacter` may warn on PIE if mesh/skeleton mismatch | **Med** | **VP-B** |
| **PA-04** | `M_Nurtured` visual vs `bNurtured` flag — nurture success logs but mesh/MI swap may not show emissive | **Med** | **VP-C** |
| **PA-05** | Content binary volatility — `.uasset`/`.umap` local-only; re-run scripts after clone | **Med** | **VP-D** (bootstrap dry-run) |
| **PA-06** | Interact prompts / gather node dress gaps — placement exists; UX polish thin | **Med** | **VP-C** |
| **PA-07** | Store-transfer (World ↔ Stored gatherables) — spec in Lib/03; not wired | **Low** | **VP-C** (optional if cheap) |
| **PA-08** | Navmesh deferred (NP-C) | **Low** | **Out of VP** — document only |
| — | Doctor noise on UE host | **Low** | **Closed** — HR2-A `doctor:ue` |

**Explicitly OUT of VP:** new SYS verbs, combat, free-flight, Lumen/Nanite gates, Docs/07 reopen, product NP-F, HR2-D.

---

## Board status

| Track | Status |
|-------|--------|
| **Product NP (Docs/11)** | **CLOSED** |
| **Harness HR2 (Docs/13)** | **CLOSED** |
| **Docs/14 / VP strategy** | **APPROVED** — Lead **`APPROVE VP STRATEGY`**, 2026-09-17 ET |
| **VP-A** | **APPROVED** — Lead **`APPROVE VP-A`**, 2026-09-17 ET (verb PIE hard-fail accepted; PA-03 → VP-B) |
| **VP-B** | **APPROVED / CLOSED** — Lead **`APPROVE VP-B`**, 2026-09-17 ET; PA-03 deferred accept (mesh-only interim) |
| **VP-C** | **IN PROGRESS / PENDING APPROVE VP-C** — PA-04/06 impl landed; done criteria require VP-A re-verify PASS or WAIVE (HR3-D) |
| **VP-D** | **LOCKED** |

---

## VP plan (Lead gates each phase)

Naming: **VP-A … VP-D** (Verify & Polish). Do **not** reuse NP-* or HR2-* phase ids.

### VP-A — PIE evidence (Windows DESKTOP)

**Goal:** Execute existing NP runbooks on **DESKTOP-21CT3H0**, capture **Output Log greps** for all MVP verb prefixes, file evidence — **no new features**.

| Item | Spec |
|------|------|
| **Runbooks** | [12c_NP_C_FORM_V1.md](12c_NP_C_FORM_V1.md) (FORM, FALLBACK, portal), [12d_NP_D_SYS_V3_V4.md](12d_NP_D_SYS_V3_V4.md) (GATHER, TAME), [12e_NP_E_SYS_V6_V8.md](12e_NP_E_SYS_V6_V8.md) (HEAL, NURTURE, DAWN) |
| **Map** | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| **Prerequisites** | `.\Tools\Safe-Build.ps1`; bootstrap chain (`bootstrap_project.py` or individual `place_vs_mvp_*.py`) |
| **Log prefixes (grep Output Log)** | `FORM:`, `FALLBACK:`, `HEAL:`, `NURTURE:`, `DAWN:`, `TAME:`, `GATHER:` (supporting) |
| **Optional automation** | `execute_python_script("pie_test_runner.py")` → `Saved/pie_test_results.json` |
| **Evidence deliverable** | [handoffs/VP_A_PIE.md](handoffs/VP_A_PIE.md) — timestamp, host, UE version, pass/fail per verb, log excerpts |
| **Gate** | Lead **`APPROVE VP-A`** before VP-B implementation PR |

**In scope:** PIE walk-through per runbook tables; copy/paste log excerpts; note any soft-fail vs hard-fail.

**Out of scope:** New C++ verbs; combat; free-flight; committing `.uasset`/`.umap`; changing runbook expected behavior without Lead gate.

**Done criteria:**

- [x] All six primary prefixes (`FORM`, `FALLBACK`, `HEAL`, `NURTURE`, `DAWN`, `TAME`) have **pass or documented fail** with log excerpt — **all FAIL** (filed 2026-09-17)
- [x] `handoffs/VP_A_PIE.md` filed with DESKTOP evidence
- [x] Any hard-fail blocks VP-B/C until root-caused — **ABP skeleton hard-fail** blocks verb PIE; fix in **VP-B** (PA-03)

---

### VP-B — Smoke & character risk

**Goal:** Fix NightMix Python smoke for UE 5.7; investigate/fix ABP skeleton warning **if it blocks PIE** or spam-floods Output Log.

| Item | Spec |
|------|------|
| **PA-02 NightMix smoke** | `Content/Python/smoke_nightmix_phase.py` — prefer `unreal.MaterialLibrary.set_scalar_parameter_value` on UE 5.7; fallback `KismetMaterialLibrary` if present (see [KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md), [12-python.mdc](../.cursor/rules/12-python.mdc)) — **DESKTOP 4/4 @ `5d09cf8`** |
| **PA-03 ABP skeleton** | `ABP_HomeWorldCharacter` — if PIE shows skeleton/mesh mismatch warning, fix retarget or default mesh assignment in C++/placement scripts; **defer** if warning is cosmetic only and PIE verbs pass |
| **Evidence** | `Docs/handoffs/VP_B_SMOKE_CHARACTER.md` — before/after smoke script exit code; ABP warning status |
| **Gate** | Lead **`APPROVE VP-B`** before VP-B implementation PR |

**In scope:** Python smoke API fix; ABP/mesh assignment fix when blocking; log-driven validation per [16-feature-debug-instrumentation.mdc](../.cursor/rules/16-feature-debug-instrumentation.mdc).

**Out of scope:** Full AnimGraph automation ([ANIMGRAPH_AUTOMATION_SPIKE.md](../docs/TaskLists/TaskSpecs/ANIMGRAPH_AUTOMATION_SPIKE.md) deferred); new character systems; Milady import.

**Done criteria:**

- [x] `smoke_nightmix_phase.py` exits **0** on DESKTOP with four `OK phase=` lines — **4/4 @ DESKTOP-21CT3H0**
- [x] ABP skeleton: **documented accept** (mesh-only interim; `EDITOR_ABP_SKELETON` warning only) — [handoffs/VP_B_SMOKE_CHARACTER.md](handoffs/VP_B_SMOKE_CHARACTER.md)
- [x] Safe-Build green if C++ touched — PR #67 @ `e00c542`

---

### VP-C — Playability polish (thin)

**Goal:** Small UX/visual gaps that improve the signed slice without new systems.

| Item | Spec |
|------|------|
| **Interact prompts** | Ensure gather/heal/nurture/tame targets show readable interact feedback (widget or debug overlay — minimal) |
| **Gather node dress** | `place_vs_mvp_*` / dress scripts — close placement gaps noted in VP-A evidence |
| **PA-04 M_Nurtured visual** | On `NURTURE: success`, apply **M_Nurtured** emissive read (MI swap or material parameter) matching `bNurtured` flag — [Lib/03_Gatherables/PLANTERS_PATH.md](../Lib/03_Gatherables/PLANTERS_PATH.md) |
| **PA-07 Store-transfer (optional)** | World ↔ Stored gatherable transfer per [GATHERABLES_WORLD_STORED.md](../Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md) — **only if cheap**; else log defer in handoff |
| **Evidence** | `Docs/handoffs/VP_C_POLISH.md` |
| **Gate** | Lead **`APPROVE VP-C`** before VP-C implementation PR |

**In scope:** Thin polish; C++/Python allowed; no new masters (stay at **10**).

**Out of scope:** Combat; free-flight / flight HUD; navmesh bake (PA-08 defer); store-transfer if > small PR.

**Done criteria:**

- [ ] VP-A re-verify greps **PASS** (or Lead **WAIVED** per prefix) after VP-B — **STILL FAIL** ([VP_A_PIE.md](handoffs/VP_A_PIE.md) § Re-verify)
- [x] Nurture success visibly distinct (M_Nurtured dynamic MI path in C++ — pending DESKTOP PIE visual confirm)
- [x] Interact/gather gaps from VP-A closed or logged with reason — markers present; interact prompts added; PA-07 deferred

---

### VP-D — Bootstrap & branch protection

**Goal:** Prove fresh-clone → script chain on Windows; document GitHub branch protection checks Lead must enable (settings outside repo).

| Item | Spec |
|------|------|
| **PA-05 Bootstrap dry-run** | Cold or clean clone path: submodule init (HR2-B) → `npm run doctor:ue` → Editor open → `bootstrap_project.py` (or documented chain) → idempotent re-run — log excerpts in handoff |
| **Branch protection** | **HR3-C** — [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection + [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md); Lead applies GitHub settings ([handoffs/HR3_C_BRANCH_PROTECTION.md](handoffs/HR3_C_BRANCH_PROTECTION.md)) |
| **Evidence** | `Docs/handoffs/VP_D_BOOTSTRAP_CI.md` |
| **Gate** | Lead **`APPROVE VP-D`** before VP-D implementation PR; Lead configures GitHub settings separately |

**In scope:** Runbook evidence; CI_SETUP checklist for Lead; optional validate.yml/doc cross-links.

**Out of scope:** Changing GitHub org settings from repo (Lead action); second submodule; cloud UE.

**Done criteria:**

- [ ] Fresh-clone dry-run log shows bootstrap chain success on DESKTOP or documented gap → [AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md)
- [ ] CI_SETUP lists required status checks and Lead steps for `main` protection
- [ ] Lead confirms branch protection configured (note in handoff — no bot access required)

---

## Hard rules (every VP phase)

| Rule | Source |
|------|--------|
| **Docs/07 CLOSED** | Do not reopen vertical-slice sign-off |
| **FALLBACK FLIGHT armed** | Scripted glide + portal only — [09_FALLBACK_GLIDE.md](09_FALLBACK_GLIDE.md) |
| **No free-flight / flight HUD** | Lead locked |
| **No combat** | Placeholder only per [AGENTS.md](../AGENTS.md) |
| **No Lumen/Nanite gates** | Docs/04 deferred |
| **No `.uasset` / `.umap` commits** | Local Windows Editor only |
| **Exactly 10 masters** | [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) |
| **Lead APPROVE each VP-* before implementation PR** | This doc |
| **Windows Safe-Build** | `.\Tools\Safe-Build.ps1` after any C++ change — [BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md) |

---

## Explicit OUT (VP track)

| Item | Reason |
|------|--------|
| Product NP-F or new SYS verbs | NP track CLOSED |
| HR2-D or harness redo | HR2 track CLOSED |
| Combat / night waves / foe conversion deep work | AGENTS.md placeholder boundary |
| Free-flight / Docs/07 reopen | Lead CLOSED |
| Navmesh bake (PA-08) | NP-C defer — document only |
| Nanite/Lumen beauty pass | Off-slice |
| Mass Entity / StateTree / ZoneGraph enablement | Week 2+ scope |
| Committing content binaries | Policy — scripts + C++ only in git |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE VP STRATEGY`** | VP-A planning / DESKTOP PIE evidence |
| 1 | **`APPROVE VP-A`** | VP-A evidence PR or handoff sign-off |
| 2 | **`APPROVE VP-B`** | VP-B smoke + ABP PR(s) |
| 3 | **`APPROVE VP-C`** | VP-C polish PR(s) |
| 4 | **`APPROVE VP-D`** | VP-D bootstrap + CI doc PR(s) |

Phases run **sequentially** (recommended: A → B → C → D) unless Lead directs parallel work after strategy approval — each phase still requires its own APPROVE before implementation.

```
Docs/14 / VP STRATEGY: APPROVED — Lead Luke Thompson, APPROVE VP STRATEGY, 2026-09-17 ET
VP-A: APPROVED — re-verify STILL FAIL (HR3-D) before VP-C COMPLETE
VP-B: APPROVED / CLOSED — Lead APPROVE VP-B, 2026-09-17 ET
VP-C: IN PROGRESS / PENDING APPROVE VP-C — VP-D: LOCKED
Product NP: CLOSED — HR2: CLOSED — HR3: CLOSED / COMPLETE
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) | Product NP **CLOSED** — VP is post-NP verify/polish only |
| [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) | HR2 **CLOSED** — VP-D extends branch protection doc from HR2-C |
| [12c_NP_C_FORM_V1.md](12c_NP_C_FORM_V1.md) | VP-A runbook — FORM, FALLBACK, portal |
| [12d_NP_D_SYS_V3_V4.md](12d_NP_D_SYS_V3_V4.md) | VP-A runbook — GATHER, TAME |
| [12e_NP_E_SYS_V6_V8.md](12e_NP_E_SYS_V6_V8.md) | VP-A runbook — HEAL, NURTURE, DAWN |
| [09_FALLBACK_GLIDE.md](09_FALLBACK_GLIDE.md) | FALLBACK hard rules — unchanged in VP |
| [07_VERTICAL_SLICE_SIGN OFF.md](07_VERTICAL_SLICE_SIGN%20OFF.md) | **CLOSED** — VP does not reopen |
| [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) | VP-D branch protection checklist (Lead settings) |
| [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) | Cloud agents → DESKTOP for VP-A/B/C evidence |

---

*Conductor prepared this file; Lead **`APPROVE VP STRATEGY`** locked 2026-09-17 ET. VP-A **APPROVED** — Lead **`APPROVE VP-A`**, 2026-09-17 ET ([handoffs/VP_A_PIE.md](handoffs/VP_A_PIE.md)) — hard-fail accepted. **VP-B APPROVED / CLOSED** — Lead **`APPROVE VP-B`**, 2026-09-17 ET ([handoffs/VP_B_SMOKE_CHARACTER.md](handoffs/VP_B_SMOKE_CHARACTER.md)). **VP-C IN PROGRESS** — Conductor must file VP-A re-verify (or Lead **WAIVE**) per HR3-D before VP-C **COMPLETE**.*
