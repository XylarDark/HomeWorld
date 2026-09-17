# PL-A Character Realization — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-A |
| **Status** | **EVIDENCE COMPLETE — PENDING LEAD `APPROVE PL-A`** |
| **Lead gate** | **`APPROVE PL-A`** before PL-B |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-A |
| **Baseline** | Main @ `93a47e7` (PR #75) + preflight follow-up — DESKTOP **DESKTOP-21CT3H0** |

## Summary

Replace VP-B mesh-only interim with Lead-accepted Epic UE 5.7 Mannequin substitute:

| Item | Value |
|------|-------|
| **Lead** | **Manny substitute APPROVED** 2026-09-17 ET |
| **Source (host)** | `UE_5.7\Templates\TemplateResources\High\Characters\Content\Mannequins` |
| **DESKTOP dest** | `Content/Characters/Mannequins/` (**local only** — **no `.uasset` commits**) |
| **Skeletal mesh** | `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` |
| **Anim BP** | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` |
| **Apply script** | `Content/Python/pl_a_apply_character.py` (do **not** re-run `vp_b_apply_character.py`) |
| **Legacy** | `/Game/Man/...`, `ABP_HomeWorldCharacter` — **deferred / unassigned** |

## Done criteria (Docs/16)

- [x] Character BP uses non-Engine project mesh (Manny substitute)
- [x] Compiling ABP (`ABP_Unarmed` compile OK) — mesh-only interim retired
- [x] `npm run preflight:ue -- --require-editor` exit **0** with `mesh_only: false` (post preflight path fix)
- [x] Safe-Build — **N/A** (no C++ touched)

## DESKTOP evidence (2026-09-17 ET)

| Check | Result |
|-------|--------|
| Copy Mannequins → `Content/Characters/Mannequins` | **PASS** — 128 files / ~125 MB |
| Key assets on disk | **PASS** — `SKM_Manny_Simple`, `SK_Mannequin`, `ABP_Unarmed` |
| Config tip | **PASS** — PR #75 @ `93a47e7` |
| `pl_a_apply_character.py` (MCP) | **PASS** — `Saved/PL_A_apply.json` `ok: true`; BP compile OK; ABP compile OK |
| BP mesh / anim_class | **PASS** — `SKM_Manny_Simple` + `ABP_Unarmed_C` (not `/Engine/...`) |
| `npm run preflight:ue -- --require-editor` | **PASS** — exit **0** after preflight honors config ABP path |
| Safe-Build | **N/A** |

### Apply JSON excerpt

```json
{
  "mesh_path": "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple",
  "anim_path": "/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed",
  "ok": true,
  "bp_compile": "ok",
  "abp_compile": "ok"
}
```

## Hard rules

- Docs/07 CLOSED — no reopen
- No free-flight
- No `.uasset` / `.umap` commits

---

*PL-A evidence filed — stop for Lead **`APPROVE PL-A`** before PL-B.*
