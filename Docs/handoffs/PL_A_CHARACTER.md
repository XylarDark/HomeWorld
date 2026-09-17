# PL-A Character Realization — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-A |
| **Status** | **IN PROGRESS** — Lead **Manny substitute APPROVED** 2026-09-17 ET; config paths set; DESKTOP apply / preflight evidence pending |
| **Lead gate** | **`APPROVE PL-A`** before PL-B |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-A |
| **Baseline** | Main post–PL STRATEGY (`03a3e46`) — DESKTOP **DESKTOP-21CT3H0** |

## Summary

Replace VP-B mesh-only interim (`/Engine/.../DefaultSkeletalMesh` + empty `anim_blueprint`) with a **Lead-accepted** Epic UE 5.7 Mannequin substitute:

| Item | Value |
|------|-------|
| **Source (host)** | `UE_5.7\Templates\TemplateResources\High\Characters\Content\Mannequins` |
| **DESKTOP dest** | `Content/Characters/Mannequins/` (**local only** — **no `.uasset` commits**) |
| **Skeletal mesh** | `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` |
| **Anim BP** | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` (compiling idle/walk minimal) |
| **Config** | [character_blueprint_config.json](../../Content/Python/character_blueprint_config.json) |
| **Legacy** | `/Game/Man/...` / `SK_Man_Full_01` / `ABP_HomeWorldCharacter` — **deferred** (missing skeleton; not assigned) |

## Done criteria (Docs/16)

- [ ] Character BP uses non-Engine project mesh (Manny substitute path)
- [ ] ABP compiles (ABP_Unarmed) **or** mesh-only explicitly retired with Lead note
- [ ] `npm run preflight:ue -- --require-editor` exit **0** without mesh-only as primary path
- [ ] Safe-Build green if C++ touched (N/A if scripts/config only)

## DESKTOP evidence

| Check | Result |
|-------|--------|
| Copy Mannequins → `Content/Characters/Mannequins` | **PENDING** — Conductor |
| Key assets on disk (`SKM_Manny_Simple`, `SK_Mannequin`, `ABP_Unarmed`) | **PENDING** |
| `git pull` config tip | **PENDING** |
| `setup_character_blueprint.py` (MCP) | **PENDING** |
| BP mesh / `anim_class` | **PENDING** |
| `npm run preflight:ue -- --require-editor` | **PENDING** |
| Safe-Build | **N/A** unless C++ touched |

## Hard rules

- Docs/07 CLOSED — no reopen
- No free-flight
- No `.uasset` / `.umap` commits

---

*PL-A — Lead Manny substitute APPROVED; awaiting DESKTOP apply evidence then Lead **`APPROVE PL-A`**.*
