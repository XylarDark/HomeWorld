# Docs/17a — HS-A Inventory & Debt Ledger (post–Docs/08)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead Luke Thompson, **`APPROVE HS-A`**, 2026-09-17 ET |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (HomeWorld) — gh Contents API only |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Baseline** | Docs/08 **SIGNED OFF** ([08_AUDIT_SIGN_OFF.md](08_AUDIT_SIGN_OFF.md), PR **#16** / **#17**); strategy baseline main `d59a0b2` (PL CLOSED); inventory filed against main tip at authoring |
| **Scope** | Authoritative map of work since Docs/08 SIGN OFF (PRs ~**#17–#85** + strategy **#86**) — tracks, keepers, open debt with owners + HS WAVE |
| **Hard rules honored** | Docs/07 CLOSED; FALLBACK glide only; no combat; no `.uasset`/`.umap` commits; exactly 10 masters; no invented product phases |

**Gate:** Lead **`APPROVE HS-A`** — **APPROVED** (Luke Thompson, 2026-09-17 ET). **HS-B UNLOCKED**.

---

## Disposition legend (HS-A)

| Tag | Meaning |
|-----|---------|
| **KEEP** | Landed, still required as-is; do not reopen or duplicate |
| **FIX** | Open debt — this HS track owns a concrete remediation WAVE |
| **ACCEPT** | Real constraint or residual; document honestly; do not pretend CI/automation already covers it |
| **DEFER** | Explicitly out of HS scope, or parked until Lead names a later product/policy |

Owners: **Lead** (gates + GitHub settings) · **Conductor** (swarm ops, PRs, digests) · **DESKTOP** (Conductor-parent Shell on DESKTOP-21CT3H0 only) · **GitHub settings** (branch protection UI/API — Lead admin)

HS WAVEs: **HS-B** swarm ops · **HS-C** CI as law · **HS-D** evidence automation · **HS-E** character/bootstrap canon · **HS-F** sign-off & re-grade

---

## 1. Track timeline since Docs/08 SIGN OFF

| Track | Docs | Outcome | PR range (merged) | Notable SHAs / notes | Area tag |
|-------|------|---------|-------------------|----------------------|----------|
| Docs/08 close | 08 sign-off | **CLOSED** | #16–#17 | SIGN OFF AUDIT recorded | **KEEP** |
| Post-audit wrap | Docs/10 | **CLOSED** | #18–#21 (dress, FALLBACK, materials) | VS_MVP dress; CRUMB glide + portal; master graphs + NightMix | **KEEP** |
| Harness refine 1 | Docs/11 HR-A…D + B2 | **CLOSED** | #22–#29 | CI paths, swarm ops, dry-run, DevEnvTemplate bump | **KEEP** |
| Product NP | Docs/11 / 12a–e | **CLOSED** | #30–#46 | Inventory → lookdev → form/V1 → gather/tame → heal/nurture/dawn | **KEEP** |
| Harness refine 2 | Docs/13 HR2-A…C | **CLOSED** | #47–#51 | `doctor:ue`, cold-clone, `build-win64` path gate | **KEEP** |
| Verify & Polish | Docs/14 VP-A…D | **CLOSED** | #52–#55, #66–#73 | VP-A verb hard-fail; VP-A re-verify **WAIVED**; mesh-only interim; nurture polish; bootstrap | **KEEP** (debt → HS-D/E) |
| Harness refine 3 | Docs/15 HR3-A…D | **CLOSED** | #56–#65 | DESKTOP parent lane; preflight loud; HR3-C **DEFERRED**; evidence lane | **KEEP** (debt → HS-B/C/D) |
| Playable Loop | Docs/16 PL-A…D | **CLOSED** | #74–#85 | Manny+ABP_Unarmed; PL-B **WAIVED**; store-transfer+HUD; Shot 1 = P6 PNG | **KEEP** (debt → HS-D/E + ACCEPT #7) |
| Continuity | handoff | **Filed** | — | [SESSION_HANDOFF_2026-09-17.md](handoffs/SESSION_HANDOFF_2026-09-17.md) | **KEEP** (process → HS-B) |
| HS strategy | Docs/17 | **APPROVED / ACTIVE** | #86 | Lead **`APPROVE HS STRATEGY`**; HS-A unlocked | **KEEP** |

**Product wins (context — not HS implementation work):** Manny + `ABP_Unarmed` spawn path; store-transfer + HUD Inv; FALLBACK glide retained; VS_MVP markers dressed; 10 masters + NightMix.

**Not product phases:** HS does **not** invent NP/VP/PL successors. Next product track name is Lead-only after HS-F (or Lead override).

---

## 2. Major area map (post–08 keepers vs debt)

| Area | Disposition | Why | Owner | HS WAVE |
|------|-------------|-----|-------|---------|
| Capital `Docs/08`–`16` + handoffs | **KEEP** | Closed track evidence; do not reopen as unfinished product | Conductor / Lead | — |
| `Docs/17*` HS track | **KEEP** | Active harness/swarm audit | Conductor / Lead | HS-A…F |
| `swarm/PHASE_BOARD`, `SWARM_OPS`, packets | **FIX** | Post-PL section + DESKTOP parent rule + ResourceExhausted fallback still tribal | Conductor | **HS-B** |
| FALLBACK glide + portal (Docs/09 / #19) | **KEEP** | Armed; no free-flight | Conductor / DESKTOP | — |
| Exactly 10 masters + NightMix (#21 / NP-B) | **KEEP** | Canon materials path | DESKTOP / Conductor | — |
| NP verb substrate (FORM/GATHER/TAME/HEAL/NURTURE/DAWN/STORE) | **KEEP** | Landed C++/scripts; evidence automation is the debt | Conductor / DESKTOP | debt → **HS-D** |
| HR2 doctor:ue + cold-clone + build-win64 | **KEEP** | Harness A− substrate | Conductor | residual → **HS-F** (#9) |
| HR3-A DESKTOP = Conductor parent only | **ACCEPT** | Proven ceiling; document as law, do not assign DESKTOP to Task executors | Conductor / DESKTOP | **HS-B** |
| HR3-C branch protection checklist | **FIX** | Checklist exists (#62); GitHub apply still not done | Lead / GitHub settings | **HS-C** |
| VP-A / PL-B human verb greps | **FIX** | WAIVE culture burned Lead time | Conductor / DESKTOP / Lead | **HS-D** |
| Character Mannequins local-only (PL-A) | **FIX** | Cold machine spawn breaks without local copy | Lead / Conductor / DESKTOP | **HS-E** |
| PL-D presentation / HighResShot | **ACCEPT** | Shot still `Maps/Preview_Homestead_Night/shot1_lookout.png`; UE HighResShot black unused | Lead / Conductor | **HS-F** |
| Cloud agent Contents API fallback | **FIX** | ResourceExhausted → `gh` Contents API is real path; encode in packet | Conductor | **HS-B** |
| Stamp/phase PR volume (~70/day) | **FIX** | Prefer batched digests + PR links | Conductor | **HS-B** |
| Session transcript lag | **FIX** | Resume from durable handoff; SESSION_SUMMARY enforce | Conductor | **HS-B** |
| Doctor / rule-budget residual | **ACCEPT** | HR2-A wrapper exists; template profile mismatch low severity | Conductor | **HS-F** |
| Docs/07 vertical slice | **KEEP** | **CLOSED** — never reopen in HS | Lead | — |
| Combat / free-flight / `.uasset` commits | **DEFER** | Hard out of scope forever unless Lead names binary policy in HS-E | Lead | **DEFER** |

---

## 3. Authoritative debt ledger (strategy #1–9)

Every row from [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) § Measured friction — tagged, owned, WAVE-assigned. **No silent orphans.**

| # | Debt | Severity | Tag | Owning WAVE | Owner(s) | Evidence | Fix / accept note |
|---|------|----------|-----|-------------|----------|----------|-------------------|
| 1 | **Branch protection not applied** on `main` | High | **FIX** (Lead may **`ACCEPT HS-C DEFER`**) | **HS-C** | **Lead** + **GitHub settings**; Conductor verifies | [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md); handoff `HR3_C_BRANCH_PROTECTION.md`; PR #62–#63; merges still policy-honor | Apply required checks `validate` / `python-lint` / `build-win64` **or** Lead stamps permanent ACCEPT DEFER with written risk |
| 2 | **DESKTOP Shell = Conductor parent only** | High (swarm ceiling) | **ACCEPT** | **HS-B** | **Conductor** (ops contract); **DESKTOP** lane = parent only | [handoffs/HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md); Task executors FAIL | Encode explicit rule in PHASE_BOARD / CLOUD_AGENT_PACKET / WINDOWS_BRIDGE — do not pretend executors can DESKTOP |
| 3 | **Human PIE / verb greps → WAIVE culture** | High | **FIX** | **HS-D** | **Conductor** + **DESKTOP** + **Lead** (gate) | PL-B **WAIVED** (#79); VP-A re-verify **WAIVED** (#70); VP_A_PIE STILL FAIL record | Extend `preflight:ue` + MCP/scripted capture for FORM/FALLBACK/HEAL/NURTURE/DAWN/TAME/STORE; board re-verify before polish unlocks |
| 4 | **Cloud agents ResourceExhausted / unreliable** | Med–High | **FIX** | **HS-B** | **Conductor** | Repeated fallback to `gh` Contents API (this HS-A filing uses same path) | Packet + HANDOFF_TEMPLATE: Contents API fallback is sanctioned; no-DESKTOP-for-executors |
| 5 | **Character assets local-only** | Med | **FIX** | **HS-E** | **Lead** (decide) + **Conductor** + **DESKTOP** (setup) | PL-A (#75–#77): `Content/Characters/Mannequins` on DESKTOP, not committed | KEEP-local + documented setup **or** Engine-path-only **or** Lead-approved binary strategy — no silent `.uasset` dumps |
| 6 | **Stamp / phase PR volume** | Med | **FIX** | **HS-B** | **Conductor** | ~70 merges in one day across HR/VP/PL | Batch digests preference in swarm ops; fewer stamp-only PRs when safe |
| 7 | **Presentation / HighResShot fragility** | Low–Med | **ACCEPT** | **HS-F** | **Lead** / **Conductor** | PL-D (#84–#85): UE HighResShot black; still on P6 `shot1_lookout.png` | Accept P6 PNG as presentation until Lead names a lookdev pass — **not** a new product phase in HS |
| 8 | **Session transcript lag** | Low (process) | **FIX** | **HS-B** | **Conductor** | Chat refresh; [SESSION_HANDOFF_2026-09-17.md](handoffs/SESSION_HANDOFF_2026-09-17.md) papered continuity | Enforce “resume from handoff” + SESSION_SUMMARY policy |
| 9 | **Doctor / rule-budget theater residual** | Low | **ACCEPT** | **HS-F** | **Conductor** | HR2-A wrapper (#48); template profile still mismatched | Re-grade at sign-off; no DevEnvTemplate rewrite in HS (strategy Out) |

### Ledger integrity

| Check | Result |
|-------|--------|
| Strategy debts #1–9 present | **YES** — all nine rows above |
| Each has KEEP/FIX/ACCEPT/DEFER | **YES** — FIX: 1,3,4,5,6,8 · ACCEPT: 2,7,9 · (debt #1 allows Lead ACCEPT DEFER at HS-C gate) |
| Each has owning WAVE | **YES** — HS-B: 2,4,6,8 · HS-C: 1 · HS-D: 3 · HS-E: 5 · HS-F: 7,9 |
| No invented product phases | **YES** |

---

## 4. PR index (audit input — merged ~#17–#86)

Compact index for auditors. Full titles on GitHub.

### 4.1 Post-audit wrap + Docs/10 era

| PR | Title (short) |
|----|---------------|
| #17 | Docs/08: Lead SIGN OFF AUDIT recorded |
| #18 | Docs/06: VS_MVP dress script |
| #19 | FALLBACK: scripted CRUMB glide + dual shrine portal |
| #20 | fix(python): portal marker UPROPERTY names |
| #21 | feat(materials): post-audit master graphs + NightMix |

### 4.2 Docs/11 HR + NP

| PR | Title (short) |
|----|---------------|
| #22–#29 | HR strategy → HR-A…D + B2 close / unlock NP |
| #30–#31 | NP-A inventory (+ Windows confirm) |
| #32–#33 | NP-B lookdev assign + Windows 78/78 evidence |
| #34–#37 | NP-C form/V1 + Safe-Build fixes + placement evidence |
| #38–#39 | NP-D gather/tame + beast pad |
| #40–#46 | NP-E heal/nurture/dawn + placement fixes → **APPROVE NP-E** close |

### 4.3 Docs/13 HR2

| PR | Title (short) |
|----|---------------|
| #47 | HR2 strategy |
| #48 | HR2-A `doctor:ue` |
| #49 | HR2-B cold-clone |
| #50 | HR2-C `build-win64` path gate |
| #51 | APPROVE HR2-C — track CLOSED |

### 4.4 Docs/14 VP (+ interleaved Docs/15 HR3)

| PR | Title (short) |
|----|---------------|
| #52–#55 | VP strategy → APPROVE VP-A |
| #56–#65 | HR3 strategy → A/B/C-deferred/D close |
| #66–#68 | VP-B mesh-only + NightMix smoke → APPROVE VP-B |
| #69–#70 | VP-C polish + **WAIVE VP-A re-verify** |
| #71–#73 | APPROVE VP-C → VP-D bootstrap → **APPROVE VP-D** close |

### 4.5 Docs/16 PL + Docs/17 HS

| PR | Title (short) |
|----|---------------|
| #74 | APPROVE PL STRATEGY |
| #75–#77 | PL-A Manny + ABP_Unarmed + APPROVE PL-A |
| #78 | PL-B prep checklist (closed unmerged companion to waive path) |
| #79 | **WAIVE PL-B** |
| #80–#83 | PL-C store-transfer + Dump register + evidence → APPROVE PL-C |
| #84–#85 | PL-D Shot 1 evidence → **APPROVE PL-D** — Docs/16 CLOSED |
| #86 | Docs/17 HS strategy (Lead **`APPROVE HS STRATEGY`** stamped on branch / main) |

---

## 5. Key durable handoffs (do not orphan)

| Handoff | Track | Role in HS |
|---------|-------|------------|
| `HR3_A_WINDOWS_EXEC.md` | HR3-A | Debt #2 evidence — DESKTOP parent-only |
| `HR3_C_BRANCH_PROTECTION.md` | HR3-C | Debt #1 — PENDING APPLY / DEFERRED |
| `HR3_D_EVIDENCE_LANE.md` | HR3-D | Re-verify rule input for HS-D |
| `VP_A_PIE.md` | VP-A | Verb hard-fail + re-verify WAIVE record |
| `VP_B_SMOKE_CHARACTER.md` | VP-B | Mesh-only / ABP deferred accept → HS-E |
| `VP_D_BOOTSTRAP_CI.md` | VP-D | Bootstrap evidence; protection still deferred |
| `PL_A_CHARACTER.md` | PL-A | Manny local debt → HS-E |
| `PL_B_PIE.md` | PL-B | WAIVED — debt #3 |
| `PL_C_LOOP_UX.md` | PL-C | Store-transfer landed |
| `PL_D_PRESENTATION.md` | PL-D | HighResShot ACCEPT → HS-F |
| `SESSION_HANDOFF_2026-09-17.md` | Continuity | Debt #8 process input |

---

## 6. Recommended next — after Lead `APPROVE HS-A`

Per [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md):

1. Conductor unlocks **HS-B** only (swarm ops tighten) — no HS-C…F until gated.
2. Lead optional answers (strategy § Questions): apply branch protection now vs ACCEPT DEFER; Mannequins local vs Engine-only; next product after HS-F.
3. Do **not** invent product phases; do **not** reopen Docs/07; FALLBACK stays armed.

---

## Gate

```
STOP — Lead approval required
Type: APPROVE HS-A
```

**Status:** inventory & debt ledger **COMPLETE as filing** — **PENDING** Lead **`APPROVE HS-A`**.

On approval, Conductor opens HS-B (`Docs/17b_HS_SWARM_OPS.md` + ops PR). Until then: no HS implementation WAVEs, no merge claims of APPROVE HS-A, Docs/07 remains CLOSED, FALLBACK FLIGHT remains armed.

*HS-A deliverable — Docs/17a. Does **not** claim Lead APPROVE HS-A.*

## Lead APPROVE HS-A

Lead **`APPROVE HS-A`** (Luke Thompson, 2026-09-17 ET) — inventory & debt ledger **APPROVED / CLOSED**. **HS-B** (swarm ops tighten) **UNLOCKED**.

---

*HS-A **APPROVED / CLOSED** — Lead **`APPROVE HS-A`**, 2026-09-17 ET.*
