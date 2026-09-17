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

**Next gate:** Lead **`APPROVE NP-E`** → product NP track complete.

---

## NP board

| Phase | Focus | Deliverable | Status |
|-------|--------|-------------|--------|
| **NP-A** | Inventory / gap map | [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) | **APPROVED** — Lead **`APPROVE NP-A`**, 2026-09-17 ET |
| **NP-B** | Lookdev apply | [12b_NP_B_LOOKDEV.md](12b_NP_B_LOOKDEV.md) | **APPROVED** — Lead **`APPROVE NP-B`**, 2026-09-17 ET |
| **NP-C** | Form + V1 polish | [12c_NP_C_FORM_V1.md](12c_NP_C_FORM_V1.md) | **APPROVED** — Lead **`APPROVE NP-C`**, 2026-09-17 ET |
| **NP-D** | SYS V3–V4 | [12d_NP_D_SYS_V3_V4.md](12d_NP_D_SYS_V3_V4.md) | **APPROVED** — Lead **`APPROVE NP-D`**, 2026-09-17 ET |
| **NP-E** | SYS V6–V8 | [12e_NP_E_SYS_V6_V8.md](12e_NP_E_SYS_V6_V8.md) | **COMPLETE — awaiting APPROVE NP-E** |

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
| 2 | **`APPROVE NP-B`** | NP-C form + V1 polish — **DONE** |
| 3 | **`APPROVE NP-C`** | NP-D SYS V3–V4 — **DONE** |
| 4 | **`APPROVE NP-D`** | NP-E SYS V6–V8 — **DONE** |
| 5 | **`APPROVE NP-E`** | Product next-phase complete — **NEXT** |

```
Harness refine: CLOSED — Lead Luke Thompson, APPROVE HR-B2 + APPROVE HR-D, 2026-09-17 ET
Product NP strategy: APPROVED — Lead Luke Thompson, APPROVE NP STRATEGY, 2026-09-17 ET
NP-A: APPROVED — NP-B: APPROVED — NP-C: APPROVED — NP-D: APPROVED (2026-09-17 ET)
NP-E: COMPLETE awaiting APPROVE NP-E
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) | **CLOSED** — HR track complete; unlocked this doc |
| [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) | NP-A deliverable — gap map (APPROVED) |
| [12b_NP_B_LOOKDEV.md](12b_NP_B_LOOKDEV.md) | NP-B deliverable — lookdev apply (APPROVED) |
| [12c_NP_C_FORM_V1.md](12c_NP_C_FORM_V1.md) | NP-C deliverable — form + V1 polish (APPROVED) |
| [12d_NP_D_SYS_V3_V4.md](12d_NP_D_SYS_V3_V4.md) | NP-D deliverable — gather + tame (APPROVED) |
| [12e_NP_E_SYS_V6_V8.md](12e_NP_E_SYS_V6_V8.md) | NP-E deliverable — heal + nurture + dawn persist |
| [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) | SYS tables baseline |
| [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md) | NP-B lookdev apply target |

---

*NP-E SYS V6–V8 complete 2026-09-17 ET. Awaiting Lead APPROVE NP-E (final NP gate).*
