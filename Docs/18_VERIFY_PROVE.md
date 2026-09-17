# Docs/18 — Verify & Prove (VP2)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / ACTIVE** — Lead Luke Thompson, **`APPROVE VP2 STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Baseline main** | `cab7e9c` — Docs/17 HS **SIGNED OFF**; Docs/16 PL **CLOSED** |
| **Why now** | PL + HS closed at ~A, but **PL-B** and **VP-A re-verify** were **WAIVED**. HS-D shipped `evidence:grep` — use it before inventing features. |
| **Prior tracks** | [14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) **CLOSED** · [16_PLAYABLE_LOOP.md](16_PLAYABLE_LOOP.md) **CLOSED** · [17_HS_AUDIT_SIGN_OFF.md](17_HS_AUDIT_SIGN_OFF.md) **SIGNED OFF** |

---

## Goal

Prove the signed playable loop on **DESKTOP-21CT3H0** with **real** editor-log greps (not waivers). No new gameplay verbs. No combat. No free-flight.

**Success:** `evidence:grep` reports **PASS** (or Lead-accepted MISSING with written reason) for:

`FORM:` · `FALLBACK:` · `HEAL:` · `NURTURE:` · `DAWN:` · `TAME:` · `GATHER:` · `STORE:` · `INVENTORY:`

**Evidence PASS policy (Lead gates):** Soft-reject / diagnostic-only tables are **not** sufficient for **`APPROVE VP2-A`** / **`APPROVE VP2-B`** — require success-path greps or Lead **`ACCEPT SOFT-REJECT`**. Canonical: [17g_HS_G_OPS_DIET.md](17g_HS_G_OPS_DIET.md) (**APPROVED / COMPLETE**, Lead **`APPROVE HS-G`**, 2026-09-17 ET).

---

## Non-goals

| Out | Why |
|-----|-----|
| New product systems / NP-scale features | Prove first |
| Branch protection apply | Already **ACCEPT HS-C DEFER** |
| Doctor / DevEnvTemplate rewrite | HS ACCEPT residual |
| `.uasset`/`.umap` commits | Hard rule; KEEP-LOCAL Mannequins stay local |
| Reopening Docs/07 | CLOSED |
| Inventing tracks beyond VP2-C menu | Lead picks after prove |

---

## Board status

| Track | Status |
|-------|--------|
| Docs/16 PL | **CLOSED** |
| Docs/17 HS | **CLOSED / COMPLETE** |
| **Docs/18 / VP2 strategy** | **APPROVED** — Lead **`APPROVE VP2 STRATEGY`**, 2026-09-17 ET |
| **VP2-A** | **APPROVED / COMPLETE** — Lead **`APPROVE VP2-A`**, 2026-09-17 ET (retry **9/9 PASS**; soft-reject caveats historical — [VP2_A_EVIDENCE.md](handoffs/VP2_A_EVIDENCE.md)) |
| **VP2-B** | **APPROVED / COMPLETE** — Lead **`APPROVE VP2-B`**, 2026-09-17 ET (DESKTOP 9/9 success-path; [VP2_B_FIX.md](handoffs/VP2_B_FIX.md)) |
| **VP2 prove (A+B)** | **COMPLETE** — Lead **`APPROVE VP2-A`** + **`APPROVE VP2-B`**, 2026-09-17 ET |
| **VP2-C** | LOCKED (optional; Lead picks flavor or **`APPROVE VP2-C STOP`** / **`CLOSE VP2`**) |

---

## Plan (Lead gates each)

Naming: **VP2-A … VP2-C** (Verify & Prove 2). Do **not** reuse Docs/14 `VP-A…D` or Docs/16 `PL-*` gate strings.

### VP2-A — DESKTOP prove (required)

**Goal:** Conductor-parent DESKTOP run produces a scored evidence table.

| Item | Spec |
|------|------|
| **Host** | DESKTOP-21CT3H0 · Conductor **parent** only (`machineId`) — never Task executors |
| **Prereq** | `git pull`; Mannequins present (HS-E KEEP-LOCAL); MCP 55557; `preflight:ue` exit 0 |
| **PIE** | Map `L_VS_MVP_Markers` (or documented VS_MVP map); exercise FORM/FALLBACK/HEAL/NURTURE/DAWN/TAME/GATHER/STORE; `hw.Inventory.Dump` |
| **Score** | `node scripts/evidence-grep.js --log Saved/Logs/HomeWorld.log --json Saved/vp2_a_evidence.json` |
| **Deliverable** | [Docs/handoffs/VP2_A_EVIDENCE.md](handoffs/VP2_A_EVIDENCE.md) — real table + JSON excerpt; **no invented greps** |
| **Gate** | Lead **`APPROVE VP2-A`** |

**Done criteria:**

- [x] Preflight PASS on DESKTOP
- [x] Evidence table filed with honest PASS/MISSING counts — **RETRY 9/9 PASS, 0 MISSING** (2026-09-17 ET)
- [x] First-run 0/9 contrast + caveats documented (soft-reject vs success; VP2-B backlog)
- [x] Lead **`APPROVE VP2-A`**

### VP2-B — Success-path fixes (Lead early unlock)

**Goal:** DESKTOP **success-path** greps for GATHER / STORE / HEAL / NURTURE / TAME / INVENTORY / DAWN via normal console + PIE interact — not soft-reject-only or ObjectIterator hacks.

| Item | Spec |
|------|------|
| **Trigger** | Lead direction 2026-09-17 ET — unlock VP2-B **before** VP2-A approve |
| **In** | Play-world console fallback, CVar→SetPhase/Dawn snapshot, interact trace fallback, `place_vs_mvp_resource_piles.py`, evidence runbook |
| **Out** | New verbs, combat, free-flight, art campaigns, AnimGraph spikes, `.uasset`/`.umap` commits |
| **Re-prove** | Re-run VP2-A checklist with success-path rows; **`log LogTemp Log`** before greps |
| **Deliverable** | [Docs/handoffs/VP2_B_FIX.md](handoffs/VP2_B_FIX.md) + DESKTOP `Saved/vp2_b_evidence.json` |
| **Gate** | Lead **`APPROVE VP2-B`** |

**Status:** **APPROVED / COMPLETE** — Lead **`APPROVE VP2-B`**, 2026-09-17 ET. DESKTOP re-prove **9/9 PASS** success-path ([VP2_B_FIX.md](handoffs/VP2_B_FIX.md)).

**Done criteria:**

- [x] CLOUD success-path fixes merged
- [x] DESKTOP Safe-Build + PIE re-prove **9/9 PASS**
- [x] Lead **`APPROVE VP2-B`**

### VP2-C — Optional follow-on (Lead picks one)

**Goal:** One thin follow-on **after** prove — or stop.

| Option | Spec | Gate string |
|--------|------|-------------|
| **C0 Stop** | Track complete after A/(B) | Lead **`APPROVE VP2-C STOP`** or **`CLOSE VP2`** |
| **C1 Thin playability** | Prompts / gather-store feel / nurture readable (extend VP-C polish class) | Lead **`APPROVE VP2-C PLAY`** then implement |
| **C2 Presentation** | Replace P6 still and/or fix black HighResShot from `CAM_Hero` | Lead **`APPROVE VP2-C SHOT`** then implement |

**Deliverable:** [Docs/18c_VP2_FOLLOWON.md](18c_VP2_FOLLOWON.md) only if C1/C2 chosen.

---

## Hard rules

| Rule | Source |
|------|--------|
| Docs/07 CLOSED | Vertical slice |
| FALLBACK FLIGHT armed | No free-flight / flight HUD |
| No combat | Canon |
| No `.uasset`/`.umap` commits | KEEP-LOCAL Mannequins |
| Exactly 10 masters | Unchanged |
| DESKTOP = Conductor parent only | HS-B / HR3-A |
| Lead `APPROVE *` gates | No skip without Lead WAIVE/ACCEPT string |
| Batch digests | Phase-end with PR links |

---

## Immediate unlock

1. Lead **`APPROVE VP2 STRATEGY`** — **DONE** (2026-09-17 ET; PR #101)
2. Conductor **VP2-A DESKTOP prove** — **APPROVED** — Lead **`APPROVE VP2-A`**, 2026-09-17 ET ([VP2_A_EVIDENCE.md](handoffs/VP2_A_EVIDENCE.md))
3. Conductor **VP2-B DESKTOP re-prove** — **APPROVED** — Lead **`APPROVE VP2-B`**, 2026-09-17 ET ([VP2_B_FIX.md](handoffs/VP2_B_FIX.md))

---

## Gate

Lead **`APPROVE VP2 STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET).

**VP2-A APPROVED** — Lead **`APPROVE VP2-A`**, 2026-09-17 ET ([VP2_A_EVIDENCE.md](handoffs/VP2_A_EVIDENCE.md)). **VP2-B APPROVED** — Lead **`APPROVE VP2-B`**, 2026-09-17 ET. Required prove track (A+B) **COMPLETE**; VP2-C optional (LOCKED).

*APPROVED strategy — Docs/18 Verify & Prove. Lead **`APPROVE VP2 STRATEGY`**, 2026-09-17 ET. VP2-A/B gates closed.*
