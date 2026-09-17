# Docs/17d — HS-D Evidence & Re-verify Automation

| Field | Value |
|-------|-------|
| **Status** | **PENDING** Lead **`APPROVE HS-D`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (HomeWorld) — `gh` Contents API only |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | [17c_HS_CI_LAW.md](17c_HS_CI_LAW.md) — Lead **`ACCEPT HS-C DEFER`**, 2026-09-17 ET (PR #91) |
| **Debt** | Docs/17a ledger **#3** — Human PIE / verb greps → WAIVE culture |
| **Baseline** | HR3-B preflight ([HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md)) · HR3-D evidence lane ([HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md)) |
| **Hard rules honored** | Docs/07 CLOSED; FALLBACK glide only; no combat; no `.uasset`/`.umap` commits; exactly 10 masters; no invented product phases |

**Gate:** Lead **`APPROVE HS-D`** — **not claimed here**. Until stamped: HS-E stays locked.

---

## Goal

Shrink **WAIVE** / human **Alt+P** dependence for verbs we already claim:

`FORM` · `FALLBACK` · `HEAL` · `NURTURE` · `DAWN` · `TAME` · `GATHER` · `STORE` (+ `INVENTORY` dump companion)

**Approach:** Extend the existing **preflight:ue** gate + **MCP/scripted** evidence capture; enforce board **re-verify** for prior hard-fails before polish unlocks; document what is scriptable vs still Lead/human.

**Out of scope (this WAVE):** Branch protection (HS-C permanently deferred) · Mannequins policy (HS-E) · full unattended playtest farm · inventing new verbs/product phases.

---

## Why (debt #3)

| Event | What happened | Cost |
|-------|---------------|------|
| VP-A | PIE greps hard-fail (empty prefixes) | Filed fail; later **WAIVE VP-A re-verify** (#70) |
| PL-B | Human Alt+P not run (Lead away) | **WAIVE PL-B** (#79) — unlocks continued without greps |
| Pattern | Evidence = human count of Output Log lines | Burns Lead time or normalizes WAIVE |

HR3-B already fails loud **before** empty greps when MCP/ABP/mesh blockers exist. HR3-D already defines host ownership + re-verify chain. HS-D **extends** those lanes so Conductor can capture/score greps without inventing log lines, and so polish cannot unlock past unreverified hard-fails without an explicit Lead WAIVE.

---

## Canonical grep prefixes (HS-D)

| Prefix | Source (examples) | Scriptable today? |
|--------|-------------------|-------------------|
| `FORM:` | Time/phase / form path logs | **Partial** — needs PIE + verb action (human or future MCP drive) |
| `FALLBACK:` | `HomeWorldFallbackGlideComponent` | **Partial** — interact/glide in PIE |
| `HEAL:` | Heal ability / spirit path | **Partial** |
| `NURTURE:` | Nurture component | **Partial** |
| `DAWN:` | Time-of-day dawn transition | **Partial** — console `hw.TimeOfDay.Phase` may help |
| `TAME:` | Beast pad / tame spend | **Partial** |
| `GATHER:` | `HomeWorldInventorySubsystem::TryAddResource` | **Partial** |
| `STORE:` | `HomeWorldStoreTransferComponent` deposit/withdraw | **Partial** |
| `INVENTORY:` | Console `hw.Inventory.Dump` (PL-C) | **Yes (PIE)** — console command; dump is deterministic |

**Host-side (no UE):** After any real log exists under `Saved/Logs/`, `npm run evidence:grep` scores prefixes (PASS if ≥1 match, else MISSING). Does **not** invent greps.

**Preflight (no verb proof):** `npm run preflight:ue` still gates MCP/assets/editor blockers before PIE — [UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md).

---

## Spec — what HS-D delivers

### 1. Policy + board (this PR)

| Item | Path |
|------|------|
| HS-D filing (this doc) | [Docs/17d_HS_EVIDENCE.md](17d_HS_EVIDENCE.md) |
| Conductor DESKTOP checklist | [Docs/handoffs/HS_D_EVIDENCE.md](handoffs/HS_D_EVIDENCE.md) |
| Re-verify rule strengthened | [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) · [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) §4c |
| Preflight cross-link | [docs/Setup/UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) § Evidence capture (HS-D) |

### 2. Host scripts (no UE required to *author* or *unit-test*)

| Item | Path | Role |
|------|------|------|
| Evidence grep CLI | `scripts/evidence-grep.js` | Score log file for canonical prefixes; JSON + table |
| Unit tests | `scripts/evidence-grep.test.js` | Fixture logs; exit contracts |
| npm script | `package.json` → `evidence:grep` | `node scripts/evidence-grep.js` |
| Filtered-log keywords | `Content/Python/editor_log_filter_config.json` (+ defaults in `filter_editor_log.py`) | Keep verb/`INVENTORY:`/`STORE:` lines in filtered editor output |

### 3. DESKTOP proof (Conductor **parent** only — not this executor)

See [handoffs/HS_D_EVIDENCE.md](handoffs/HS_D_EVIDENCE.md). Executor **does not** claim Shell/MCP/PIE on DESKTOP-21CT3H0. Parent runs preflight + optional PIE + `evidence:grep` and pastes real excerpts.

---

## Board re-verify rule (HS-D strength)

Builds on HR3-D ([HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md)):

When phase **B** fixes a blocker that caused **hard-fail** greps in phase **A**:

1. File **B** evidence; Lead **`APPROVE`** when satisfied.
2. **Re-run A's prefix checklist** on current `main` (DESKTOP = Conductor parent); append **§ Re-verify** to A's handoff — **do not erase** the original fail/WAIVE record.
3. Prefer `npm run evidence:grep -- --log Saved/Logs/HomeWorld.log` (or dated copy) and paste the table into the handoff.
4. **Unlock downstream polish** only when A re-verify shows **PASS** on all required prefixes **or** Lead explicit **WAIVED** per prefix.

**HS-D addition:** Conductor **refuses** any polish / presentation unlock that depends on prior hard-fail verb evidence until step 2–4 is filed. WAIVE remains Lead-only and must name which prefixes — silent skip is forbidden.

Canonical historical chain (kept for auditors):

```
VP-A hard-fail → VP-B fix → VP-A re-verify (or Lead WAIVE) → VP-C unlock
```

Same pattern applies to future tracks (including any post–HS product track Lead names later).

---

## Scriptable vs still Lead/human

| Layer | Owner | Scriptable? | Notes |
|-------|-------|-------------|-------|
| Repo/config/MCP port blockers | CLOUD + DESKTOP | **Yes** | `preflight:ue` / `preflight:ue:test` (HR3-B) |
| Editor deep checks (ABP/mesh/map) | DESKTOP parent | **Yes** | `preflight_ue_editor.py` via MCP |
| Character spawn / on-ground smoke | DESKTOP parent | **Partial** | `pie_test_runner.py` / `run_pie_verify.py` |
| Verb line emission | Game C++ (already landed) | N/A | Markers already in code |
| Verb **actions** in PIE | Lead or DESKTOP operator | **No (HS-D)** | Still human Alt+P / console; full farm = Out |
| Prefix **scoring** after log exists | CLOUD or DESKTOP | **Yes** | `evidence:grep` (this WAVE) |
| Inventory dump | DESKTOP in PIE | **Yes** | `hw.Inventory.Dump` → `INVENTORY:` |
| Gate stamp / WAIVE | Lead | Human | Never invented by agents |

---

## Pointers — existing lanes (do not orphan)

| Lane | Doc | HS-D use |
|------|-----|----------|
| HR3-B preflight | [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md) · [UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) | Run before any DESKTOP PIE evidence |
| HR3-D evidence + re-verify | [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md) | Host tags + handoff contract + re-verify skeleton |
| VP-A / PL-B WAIVE records | [VP_A_PIE.md](handoffs/VP_A_PIE.md) · [PL_B_PIE.md](handoffs/PL_B_PIE.md) | Historical debt; do not delete |
| PL-C STORE + Dump | [PL_C_LOOP_UX.md](handoffs/PL_C_LOOP_UX.md) | `STORE:` + `hw.Inventory.Dump` |
| DESKTOP parent-only | [HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md) · HS-B ops | Executors never claim DESKTOP |

---

## Verification (this PR — cloud)

- [ ] `npm run preflight:ue -- --skip-mcp --assets-only` exit 0
- [ ] `npm run preflight:ue:test` exit 0
- [ ] `npm run evidence:grep:test` (or `node --test scripts/evidence-grep.test.js`) exit 0
- [ ] PHASE_BOARD current = **HS-D IN PROGRESS**; no false **`APPROVE HS-D`**
- [ ] Handoff lists DESKTOP steps for Conductor **parent** only

## Verification (DESKTOP — Conductor parent; not claimed here)

See checklist in [handoffs/HS_D_EVIDENCE.md](handoffs/HS_D_EVIDENCE.md).

---

## Next (after Lead `APPROVE HS-D`)

**HS-E** — Character / bootstrap canon (Mannequins local vs Engine-path). Deliverable: [17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) (not started).

---

## Gate

```
STOP — Lead approval required
Type: APPROVE HS-D
```

**Status:** evidence & re-verify automation **COMPLETE as filing** — **PENDING** Lead **`APPROVE HS-D`**.

Until stamped: do not unlock HS-E; do not invent greps; do not claim DESKTOP proof from cloud/executor; Docs/07 remains CLOSED; FALLBACK FLIGHT remains armed.

---

*PENDING — Docs/17d HS-D Evidence. Awaiting Lead **`APPROVE HS-D`**. Do not claim APPROVE in this PR.*