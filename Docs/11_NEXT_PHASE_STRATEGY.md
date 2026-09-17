# Docs/11 — Product Next-Phase Strategy

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead Luke Thompson, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Unlocked by** | Lead **`APPROVE NP STRATEGY`**, 2026-09-17 ET |
| **Harness refine** | **CLOSED** — [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) (HR-A…D + HR-B2) |

---

## Gate

Lead **`APPROVE NP STRATEGY`** — **GRANTED** (Luke Thompson, 2026-09-17 ET).

**Next gate:** Lead **`APPROVE NP-B`** → unlock NP-C form + V1 polish (after Windows lookdev evidence).

---

## NP board

| Phase | Focus | Deliverable | Status |
|-------|--------|-------------|--------|
| **NP-A** | Inventory / gap map | [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) | **APPROVED** — Lead **`APPROVE NP-A`**, 2026-09-17 ET |
| **NP-B** | Lookdev apply | [12b_NP_B_LOOKDEV.md](12b_NP_B_LOOKDEV.md) — `assign_vs_mvp_materials.py` | **COMPLETE — awaiting APPROVE NP-B** (Windows evidence pending) |
| **NP-C** | Form + V1 polish | Body↔spirit; GP_PlayerStart; soft walk bounds | **LOCKED** |
| **NP-D** | SYS V3–V4 | 6-slot inventory + gather + tame | **LOCKED** |
| **NP-E** | SYS V6–V8 | Heal ×3, nurture ×2, dawn persist | **LOCKED** |

---

## Hard rules (every NP phase)

| Rule | Source |
|------|--------|
| Docs/07 CLOSED | Do not reopen vertical-slice sign-off |
| FALLBACK FLIGHT armed | No free-flight / flight HUD |
| No combat | Placeholder only per AGENTS.md boundaries |
| No Lumen/Nanite gates | Docs/04 deferred |
| No `.uasset`/`.umap` commits | Local Windows only |
| Exactly 10 masters | Docs/02 |
| Lead APPROVE each NP-* before build | This doc |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE NP STRATEGY`** | NP-A inventory / gap map — **DONE** |
| 1 | **`APPROVE NP-A`** | NP-B lookdev apply — **DONE** |
| 2 | **`APPROVE NP-B`** | NP-C form + V1 polish — **NEXT** |
| 3 | **`APPROVE NP-C`** | NP-D SYS V3–V4 |
| 4 | **`APPROVE NP-D`** | NP-E SYS V6–V8 |
| 5 | **`APPROVE NP-E`** | Product next-phase complete |

```
Harness refine: CLOSED — Lead Luke Thompson, APPROVE HR-B2 + APPROVE HR-D, 2026-09-17 ET
Product NP strategy: APPROVED — Lead Luke Thompson, APPROVE NP STRATEGY, 2026-09-17 ET
NP-A: APPROVED — Lead APPROVE NP-A, 2026-09-17 ET
NP-B: COMPLETE (script + docs) — awaiting APPROVE NP-B after Windows run
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) | **CLOSED** — HR track complete; unlocked this doc |
| [11d_HR_D_HANDOFF.md](11d_HR_D_HANDOFF.md) | HR-D dry-run evidence + re-grade |
| [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) | HR-B2 residual harness closure |
| [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) | NP-A deliverable — gap map (APPROVED) |
| [12b_NP_B_LOOKDEV.md](12b_NP_B_LOOKDEV.md) | NP-B deliverable — lookdev apply runbook |
| [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) | Verb spec baseline |
| [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) | SYS tables baseline |
| [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) | NP-B lookdev apply target |

---

*NP-A approved and NP-B script delivered 2026-09-17 ET. Awaiting Windows evidence + APPROVE NP-B.*
