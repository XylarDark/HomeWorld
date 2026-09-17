# Docs/18 — Verify & Prove (VP2)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — awaiting Lead **`APPROVE VP2 STRATEGY`** |
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
| **Docs/18 / VP2 strategy** | **DRAFT** — await **`APPROVE VP2 STRATEGY`** |
| **VP2-A** | LOCKED |
| **VP2-B** | LOCKED |
| **VP2-C** | LOCKED (optional; Lead picks flavor after VP2-A/B) |

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

- [ ] Preflight PASS on DESKTOP
- [ ] Evidence table filed with honest PASS/MISSING counts
- [ ] MISSING rows listed with likely cause (not papered over)

### VP2-B — Close MISSING blockers (only if needed)

**Goal:** Fix **script/config/spawn** blockers that caused VP2-A MISSING — not new features.

| Item | Spec |
|------|------|
| **Trigger** | VP2-A has any **MISSING** Lead wants closed |
| **In** | Preflight/config, apply scripts, interact/log prefixes, store-transfer registration, KEEP-LOCAL path fixes |
| **Out** | New verbs, combat, free-flight, art campaigns, AnimGraph spikes |
| **Re-prove** | Re-run VP2-A checklist; board **re-verify before polish** (HS-D rule) |
| **Deliverable** | [Docs/handoffs/VP2_B_FIX.md](handoffs/VP2_B_FIX.md) + evidence re-run |
| **Gate** | Lead **`APPROVE VP2-B`** |

If VP2-A is **all PASS** (or Lead **`WAIVE VP2-B`** with written MISSING accept), skip to VP2-C menu / close.

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

1. Lead **`APPROVE VP2 STRATEGY`**
2. Conductor unlocks **VP2-A** only

---

## Gate

Lead type **`APPROVE VP2 STRATEGY`** to unlock VP2-A.

*DRAFT — Docs/18 Verify & Prove. Not active until Lead APPROVE VP2 STRATEGY.*
