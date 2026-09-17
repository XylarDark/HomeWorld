# VP-C Playability Polish — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-C |
| **Status** | **IN PROGRESS / PENDING APPROVE VP-C** — impl landed in repo; **not COMPLETE** |
| **Lead gate** | **`APPROVE VP-C`** before VP-C implementation PR merge / COMPLETE |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-C |
| **Baseline** | Main post–VP-B stamp + VP-A re-verify STILL FAIL @ `0e4bca1` |

## Summary

Thin playability polish for the signed VS_MVP slice — no new systems, no combat, no free-flight. **Do not mark VP-C COMPLETE** until Conductor files **VP-A re-verify PASS** on DESKTOP (or Lead **WAIVE** per prefix) per [HR3_D_EVIDENCE_LANE.md](HR3_D_EVIDENCE_LANE.md). Re-verify filed **STILL FAIL** — see [VP_A_PIE.md](VP_A_PIE.md) § Re-verify (2026-09-17 post–VP-B).

## Shipped (this PR)

| Item | Residual | Implementation |
|------|----------|----------------|
| **M_Nurtured visual** | PA-04 | `UHomeWorldNurtureComponent::ApplyNurturedVisual()` — dynamic MI on owner mesh slots; sets `Emissive` + scalar `Nurtured` from master `/Game/HomeWorld/Materials/Masters/M_Nurtured`; called on success, restore, and BeginPlay when already nurtured |
| **Interact prompts** | PA-06 | `AHomeWorldCharacter::ShowInteractFeedback` — `GEngine->AddOnScreenDebugMessage` + `INTERACT:` log; gather/heal/nurture/tame success + soft-fail messages; throttled in-range `[E]` hints via forward trace |
| **Gather node dress** | PA-06 | **No dress gap** — VP-A scene inventory PASS; `GP_N1_Crop` / `GP_N2_Stored` present via `place_vs_mvp_nurture.py`; no new meshes added |

## Deferred

| Item | Residual | Reason |
|------|----------|--------|
| **Store-transfer** | PA-07 | World ↔ Stored gatherable transfer not wired — requires inventory + placement + interact routing (>~50 LOC); defer to post–VP-C or VP-D gap session per [GATHERABLES_WORLD_STORED.md](../../Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md) |

## Prerequisites (before done criteria)

| Prerequisite | Owner | Status |
|--------------|-------|--------|
| VP-B **APPROVED / CLOSED** | Lead | **DONE** — **`APPROVE VP-B`**, 2026-09-17 ET |
| VP-A **re-verify** on DESKTOP | CND parent | **STILL FAIL** — [VP_A_PIE.md](VP_A_PIE.md) § Re-verify; MCP PIE world / PlayerController blocker |

## Done criteria (Docs/14)

- [ ] VP-A re-verify greps **PASS** (or Lead **WAIVED** per prefix) after VP-B — **STILL FAIL**
- [x] Nurture success visibly distinct (M_Nurtured dynamic MI path in C++)
- [x] Interact/gather gaps from VP-A closed or logged with reason — gather markers present; prompts added

## DESKTOP evidence

| Evidence | Status |
|----------|--------|
| VP-A re-verify verb greps | **STILL FAIL** — Conductor DESKTOP run; see [VP_A_PIE.md](VP_A_PIE.md) |
| Nurture visual + interact prompts in PIE | **PENDING** — requires human Alt+P PIE or post–automation-fix MCP path |

## Hard rules

- **Docs/07 CLOSED** — no reopen
- **No free-flight**
- **No `.uasset` / `.umap` commits**
- **Exactly 10 masters** — [02_MATERIAL_SHEET.md](../02_MATERIAL_SHEET.md)

---

*VP-C handoff — **IN PROGRESS / PENDING APPROVE VP-C**. Implementation may proceed; **COMPLETE** blocked until VP-A re-verify PASS or Lead WAIVE per HR3-D.*
