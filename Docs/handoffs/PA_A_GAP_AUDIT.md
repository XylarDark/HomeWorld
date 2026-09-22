# PA-A — Gap audit (mesh vs plate vs VS_MVP)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE PA-A`**, 2026-09-22 ET |
| **Track** | PA-A **CLOSED / COMPLETE** → **PA-C OPEN / IN PROGRESS ready** (PA-B optional; PA-D/E locked) |
| **Host** | CLOUD (stamp) · DESKTOP (Blender/import evidence for PA-C) |
| **Impl doc** | [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) — gap audit accepted |
| **Prior** | [PA_STRATEGY.md](PA_STRATEGY.md) **APPROVED / CLOSED** — Lead **`APPROVE PA STRATEGY`**, 2026-09-22 ET |
| **Scope locked** | **Homestead kit only** (planetside out) |

**PA track is not CLOSED** — only PA-A closes here. **Do not** stamp **`APPROVE PA-C`** or whole-track CLOSED until PA-E evidence.

---

## Lead gate (record)

Lead typed in chat (2026-09-22 ET):

```text
APPROVE PA-A
```

Gap audit verdicts **accepted**. Unlocks **PA-C** (Blender upgrade/create on DESKTOP + Blender MCP).

---

## Accepted gap table (plate vs greybox vs VS_MVP)

| Piece | Verdict |
|-------|---------|
| Cabin | UPGRADE |
| IslandTop | KEEP (light rim later) |
| Cliff modules | CREATE (highest risk) |
| Pine S/M/L | UPGRADE (foliage collapsed) |
| Planters×3 | CREATE |
| Fence segs | CREATE |
| Path stones | CREATE |
| Lookout pad | KEEP |
| Glider perch | UPGRADE |
| Soft shrine | KEEP |
| Islets | KEEP optional |

---

## PA-C ordered queue (Blender)

Execute on DESKTOP in this order (highest risk / shot read first):

1. **Cliff modules** — torn-earth underside; compositing with `SM_IslandTop`
2. **Pines** — S/M/L family; stylized foliage (collapsed greybox baseline)
3. **Cabin** — modular upgrade in place
4. **Path stones** — corridor dress along homestead path
5. **Planters ×3** — garden zone beds
6. **Fence segments** — post-and-rail edges
7. **Glider perch** — departure read (Shot 3 helper)
8. **Optional island rim** — light `SM_IslandTop` edge pass (non-blocking)

**KEEP (no PA-C mesh work unless polish pass later):** IslandTop plate (rim optional), Lookout pad, Soft shrine, Islets (optional crumbs).

---

## Not in this handoff

- Blender `.blend` / FBX exports (PA-C)
- Content `.uasset` promote (PA-D)
- PIE Shot 1/2 evidence (PA-E)

---

## DESKTOP chain (PA-C → PA-D)

```text
# Blender MCP + STYLE_GUIDE per queue item
# AssetCreation/Blender/export_to_asset_creation.py
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("batch_import_asset_creation.py")
execute_python_script("place_vs_mvp_dress.py")
```

Cloud agents: propose paths only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist (PA-A)

- [x] Gap table recorded and Lead **`APPROVE PA-A`** stamped
- [x] PA-C queue locked in Docs/32 + this handoff
- [x] DECISIONS.md append row
- [ ] PA-C per-asset Blender evidence (DESKTOP — next)
