# VP-C Playability Polish — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-C |
| **Status** | **DRAFT IN PROGRESS** — planning/impl unlocked after Lead **`APPROVE VP-B`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE VP-C`** before VP-C implementation PR merge |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-C |
| **Baseline** | Main post–VP-B stamp (PR #67 @ `e00c542`) |

## Summary

Thin playability polish for the signed VS_MVP slice — no new systems, no combat, no free-flight. **Do not mark VP-C COMPLETE** until Conductor files **VP-A re-verify** on DESKTOP (or Lead **WAIVE** per prefix) per [HR3_D_EVIDENCE_LANE.md](HR3_D_EVIDENCE_LANE.md).

## Scope (from Docs/14 § VP-C)

| Item | Residual | Spec |
|------|----------|------|
| **Interact prompts** | PA-06 | Gather/heal/nurture/tame targets show readable interact feedback (widget or debug overlay — minimal) |
| **Gather node dress** | PA-06 | `place_vs_mvp_*` / dress scripts — close placement gaps noted in VP-A evidence |
| **M_Nurtured visual** | PA-04 | On `NURTURE: success`, apply **M_Nurtured** emissive read (MI swap or material parameter) matching `bNurtured` — [Lib/03_Gatherables/PLANTERS_PATH.md](../../Lib/03_Gatherables/PLANTERS_PATH.md) |
| **Store-transfer (optional)** | PA-07 | World ↔ Stored gatherable transfer per [GATHERABLES_WORLD_STORED.md](../../Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md) — **only if cheap**; else log defer in handoff |

## Prerequisites (before done criteria)

| Prerequisite | Owner | Status |
|--------------|-------|--------|
| VP-B **APPROVED / CLOSED** | Lead | **DONE** — **`APPROVE VP-B`**, 2026-09-17 ET |
| VP-A **re-verify** on DESKTOP | CND parent | **PENDING** — append § Re-verify to [VP_A_PIE.md](VP_A_PIE.md); checklist in [HR3_D_EVIDENCE_LANE.md](HR3_D_EVIDENCE_LANE.md) |

## Done criteria (Docs/14)

- [ ] VP-A re-verify greps **PASS** (or Lead **WAIVED** per prefix) after VP-B
- [ ] Nurture success visibly distinct (M_Nurtured or documented MI path)
- [ ] Interact/gather gaps from VP-A closed or logged with reason

## DESKTOP evidence

_Not filed — Conductor owns DESKTOP PIE/log greps. No invented evidence in this stub._

## Hard rules

- **Docs/07 CLOSED** — no reopen
- **No free-flight**
- **No `.uasset` / `.umap` commits**
- **Exactly 10 masters** — [02_MATERIAL_SHEET.md](../02_MATERIAL_SHEET.md)

---

*VP-C handoff stub — DRAFT IN PROGRESS. Implementation may proceed; **COMPLETE** blocked until VP-A re-verify per HR3-D.*
