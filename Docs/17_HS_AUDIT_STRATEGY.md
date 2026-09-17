# Docs/17 — Harness & Swarm Audit (post–Docs/08)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / ACTIVE** — Lead Luke Thompson, **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Baseline main** | `d59a0b2` — Docs/16 PL **CLOSED**; session handoff filed |
| **Prior full audit** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) — **SIGNED OFF** ([08_AUDIT_SIGN_OFF.md](08_AUDIT_SIGN_OFF.md), PR #16) |
| **Prior harness tracks** | Docs/11 HR, Docs/13 HR2, Docs/15 HR3 — all **CLOSED** (HR3-C **DEFERRED**) |
| **Prior product tracks** | Docs/11 NP, Docs/14 VP, Docs/16 PL — all **CLOSED** |

---

## Why (this is not another HR polish pass)

Docs/08 audited **pre-swarm legacy** vs MVP canon. Since **`SIGN OFF AUDIT`**, we shipped three product tracks and three harness-refine tracks on the new swarm. Friction is now **operational debt from real work**, not dual-canon archaeology.

This track **audits everything since Docs/08**, then runs WAVE-style fixes aimed at **harness + swarm ROI** — fail loud earlier, fewer Lead waivers, less Conductor tribal knowledge, CI as law or honest permanent deferral.

**Blunt grade at PL close (Conductor):** harness **~A** (HR3-C still soft), swarm **~A−** (DESKTOP still Conductor-parent-only; evidence still too human; cloud agents still flake to Contents API).

---

## Scope boundary

| In | Out |
|----|-----|
| Inventory of PRs / tracks / handoffs since Docs/08 | New gameplay verbs / combat / free-flight |
| Swarm ops, DESKTOP lane, cloud packet, board hygiene | Reopening Docs/07 |
| CI / branch protection close-or-defer | `.uasset` / `.umap` commits |
| Evidence / re-verify automation | Inventing product NP/VP/PL phases |
| Character/bootstrap provenance (Manny local debt) | AnimGraph / lookdev campaigns |
| Re-grade + sign-off | Full DevEnvTemplate rewrite |

---

## What landed since Docs/08 (audit input)

| Track | Docs | Outcome | Notable SHAs / PRs |
|-------|------|---------|-------------------|
| Post-audit wrap | Docs/10 | CLOSED | — |
| Harness refine 1 | Docs/11 HR-A…D + B2 | CLOSED | #25–#29 |
| Product NP | Docs/11 / 12a–e | CLOSED | #30–#45 |
| Harness refine 2 | Docs/13 HR2-A…C | CLOSED | #47–#51 |
| Verify & Polish | Docs/14 VP-A…D | CLOSED | #52–#73 (VP-A re-verify **WAIVED**) |
| Harness refine 3 | Docs/15 HR3-A…D | CLOSED | #56–#65 (HR3-C **DEFERRED**) |
| Playable Loop | Docs/16 PL-A…D | CLOSED | #74–#85 (PL-B **WAIVED**) |
| Continuity | handoff | Filed | `Docs/handoffs/SESSION_HANDOFF_2026-09-17.md` |

**Product wins (context, not HS work):** Manny + ABP_Unarmed spawn path; store-transfer + HUD Inv; FALLBACK glide retained; VS_MVP markers dressed.

---

## Measured friction / open debt (post-product)

| # | Debt | Evidence | Severity |
|---|------|----------|----------|
| 1 | **Branch protection not applied** | HR3-C checklist only; merges still policy-honor | High |
| 2 | **DESKTOP Shell = Conductor parent only** | HR3-A happy path; Task executors FAIL | High (swarm ceiling) |
| 3 | **Human PIE / verb greps → WAIVE culture** | PL-B WAIVED; VP-A re-verify WAIVED | High |
| 4 | **Cloud agents ResourceExhausted / unreliable** | Repeated fallback to `gh` Contents API | Med–High |
| 5 | **Character assets local-only** | `Content/Characters/Mannequins` on DESKTOP, not committed | Med |
| 6 | **Stamp / phase PR volume** | ~70 merges in one day; Lead prefers batched digests | Med |
| 7 | **Presentation / HighResShot fragility** | PL-D UE shot black; still on P6 PNG | Low–Med |
| 8 | **Session transcript lag** | Chat refresh needed; handoff papered over | Low (process) |
| 9 | **Doctor / rule-budget theater residual** | HR2-A wrapper exists; template profile still mismatched | Low |

---

## WAVE plan (Lead gates each)

Naming: **HS-A … HS-F** (Harness/Swarm audit). Do **not** reuse Docs/08 WAVE A–F gate strings or HR*/VP*/PL* phase ids.

Each WAVE: deliverable doc + PR(s) → Lead **`APPROVE HS-*`** before next WAVE unlocks.

### HS-A — Inventory & debt ledger

**Goal:** One authoritative map of post–Docs/08 work and open debt — KEEP / FIX / ACCEPT / DEFER tags.

| Item | Spec |
|------|------|
| **Inputs** | Merged PRs ~#17–#85; Docs/10–16; handoffs; `swarm/`; CI workflows; DOCTOR_POLICY; WINDOWS_BRIDGE |
| **Deliverable** | [17a_HS_INVENTORY.md](17a_HS_INVENTORY.md) — track timeline + debt table with owners |
| **Gate** | Lead **`APPROVE HS-A`** |

**Done:** Every open debt from the table above is tagged; no silent orphans.

### HS-B — Swarm ops tighten

**Goal:** Make Conductor/swarm contracts match how we actually work after PL.

| Item | Spec |
|------|------|
| **PHASE_BOARD** | Post-PL section; current = HS track; explicit DESKTOP = Conductor-parent rule |
| **CLOUD_AGENT_PACKET / HANDOFF_TEMPLATE** | ResourceExhausted fallback (`gh` Contents API); no-DESKTOP-for-executors; batch digest preference |
| **SESSION** | Point to durable handoffs; SESSION_SUMMARY policy already exists — enforce “resume from handoff” line |
| **Deliverable** | [17b_HS_SWARM_OPS.md](17b_HS_SWARM_OPS.md) + ops PR |
| **Gate** | Lead **`APPROVE HS-B`** |

**Out:** New agent runners; GUI automation revival.

### HS-C — CI as law (close HR3-C or accept forever)

**Goal:** Branch protection **APPLIED** on `main` **or** Lead stamps **ACCEPT DEFER** with written risk.

| Item | Spec |
|------|------|
| **Baseline** | [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md) checklist |
| **Path** | Lead applies GitHub settings → Conductor verifies → handoff **APPLIED**; **or** Lead **`ACCEPT HS-C DEFER`** |
| **Deliverable** | [17c_HS_CI_LAW.md](17c_HS_CI_LAW.md) + [handoffs/HS_C_BRANCH_PROTECTION.md](handoffs/HS_C_BRANCH_PROTECTION.md) |
| **Gate** | Lead **`APPROVE HS-C`** (applied) **or** **`ACCEPT HS-C DEFER`** |

### HS-D — Evidence & re-verify automation

**Goal:** Shrink WAIVE/human Alt+P dependence for the verbs we already claim.

| Item | Spec |
|------|------|
| **Problem** | VP-A / PL-B loops burned Lead time or were waived |
| **Approach** | Extend `preflight:ue` + MCP/scripted evidence capture for FORM/FALLBACK/HEAL/NURTURE/DAWN/TAME/STORE where scriptable; board **re-verify** rule for prior hard-fails before polish unlocks |
| **Deliverable** | [17d_HS_EVIDENCE.md](17d_HS_EVIDENCE.md) + script/policy PR; DESKTOP proof excerpts |
| **Gate** | Lead **`APPROVE HS-D`** |

**Out:** Full unattended playtest farm; inventing new verbs.

### HS-E — Character / bootstrap canon

**Goal:** One honest policy for Mannequins/Manny path + bootstrap/preflight lists.

| Item | Spec |
|------|------|
| **Problem** | Local `Content/Characters/Mannequins` (128 files) powers PL-A; not in git; cold machines break spawn |
| **Decide** | KEEP-local + documented setup **or** Engine-path-only **or** Lead-approved binary strategy (no silent `.uasset` dumps) |
| **Deliverable** | [17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) + config/preflight PR |
| **Gate** | Lead **`APPROVE HS-E`** |

### HS-F — Sign-off & re-grade

**Goal:** Close the audit; publish harness/swarm grades; unlock next product only by Lead name.

| Item | Spec |
|------|------|
| **Deliverable** | [17_HS_AUDIT_SIGN_OFF.md](17_HS_AUDIT_SIGN_OFF.md) |
| **Gate** | Lead **`SIGN OFF HS AUDIT`** |

---

## Hard rules (every HS phase)

| Rule | Source |
|------|--------|
| Docs/07 CLOSED | Do not reopen vertical-slice sign-off |
| FALLBACK FLIGHT armed | No free-flight / flight HUD |
| No combat | Canon |
| No `.uasset`/`.umap` commits | Local Windows only unless Lead names a binary policy in HS-E |
| Exactly 10 masters | Unchanged |
| Lead `APPROVE *` gates | No WAVE skip without Lead WAIVE/ACCEPT string |
| Exclusive file ownership | Durable handoffs under `Docs/handoffs/` |

---

## Immediate unlock (after strategy gate)

1. Lead **`APPROVE HS STRATEGY`** — **DONE** (2026-09-17 ET)
2. Conductor unlocks **HS-A** only (inventory) — no implementation WAVEs until **`APPROVE HS-A`**

---

## Questions for Lead (optional; strategy can approve without answers)

1. Prefer **apply branch protection now** (HS-C) vs **ACCEPT DEFER** forever?
2. Character assets: **document local Mannequins** vs force **Engine-only** path?
3. After HS sign-off: next product track name, or park product until HS-F?

---

## Gate

Lead **`APPROVE HS STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET).

**HS-A UNLOCKED / IN PROGRESS** — inventory & debt ledger.

*APPROVED — Docs/17 Harness & Swarm Audit. Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET.*
