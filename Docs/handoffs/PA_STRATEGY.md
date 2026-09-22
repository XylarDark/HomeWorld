# PA STRATEGY — Prototype Assets (Homestead dress)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE PA STRATEGY`**, 2026-09-22 ET |
| **Track** | PA-0 **CLOSED** → **PA-A OPEN** (PA-B…E locked) |
| **Host** | CLOUD (stamp) · DESKTOP (Blender/import evidence) |
| **Impl doc** | [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) — **PA STRATEGY APPROVED** · **PA-A OPEN** |
| **Scope locked** | **Homestead kit only** — Lead **`APPROVE PA STRATEGY — homestead kit only`**, 2026-09-22 ET (planetside out) |
| **Close gate** | Lead **`APPROVE PA STRATEGY`** — **GRANTED** 2026-09-22 ET (chat) |

---

## Deliverable (PA-0)

| Item | Path |
|------|------|
| Strategy doc | [Docs/32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| Kit plate (AssetCreation) | [AssetCreation/RefImages/homestead_kit_plate_labeled.jpg](../../AssetCreation/RefImages/homestead_kit_plate_labeled.jpg) |
| Kit plate (AI ref) | [Docs/refs/ai/homestead_kit_plate_labeled.jpg](../refs/ai/homestead_kit_plate_labeled.jpg) |
| Sidecar | [Docs/refs/ai/homestead_kit_plate_labeled.sidecar.json](../refs/ai/homestead_kit_plate_labeled.sidecar.json) |
| DECISIONS note | [canon/DECISIONS.md](../canon/DECISIONS.md) — **PA STRATEGY APPROVED** |

**Not in this handoff:** Content `.uasset`, Blender `.blend`, gameplay code.

---

## Lead gate (record)

Lead typed in chat (2026-09-22 ET):

```text
APPROVE PA STRATEGY — homestead kit only
```

Unlocks **PA-A** (gap audit: plate vs [MVP_EXPORT_MANIFEST.md](../../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md) vs VS_MVP dress actors).

**PA track is not CLOSED** — only the strategy stamp closes here.

---

## Scope summary (locked)

**IN:** Upgrade `SM_Cabin`, `SM_IslandTop`, `SM_Pine_Homestead`, `SM_Lookout_Pad`, `SM_Glider_Perch`; polish `SM_Shrine_Homestead`; **create** cliff modules, 3 planters, fence segs, path dress; optional islet crumbs.

**OUT:** Planetside camp dress, character heroes, combat props, Quixel photoreal, new biomes, Substance hero maps.

**Quality:** Demo-readable low-poly (STYLE_GUIDE / SMG-like); no engine boxes on locked kit; not ship-final.

**Pipeline:** plate → optional AI_Sources draft → Blender MCP → `export_to_asset_creation.py` → `batch_import_asset_creation.py` → allowlisted Content + `AI_ASSET_LOG`.

**DONE-WHEN (track):** Shot 1 + Shot 2 readable in PIE without primitive homestead shapes.

---

## Next (PA-A)

Gap audit only — **not started** in this PR. No Blender/mesh work until PA-A filed.

---

## DESKTOP chain (PA-C/D — after gap audit)

```text
# Blender MCP + STYLE_GUIDE export
# AssetCreation/Blender/export_to_asset_creation.py
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("batch_import_asset_creation.py")
execute_python_script("place_vs_mvp_dress.py")
# PIE — Shot 1 / 2 cameras (VS_MVP)
```

Cloud agents: propose paths only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist (PA-0)

- [x] Kit plate copied to `AssetCreation/RefImages/` and `Docs/refs/ai/`
- [x] Sidecar JSON per Docs/20
- [x] Docs/32 strategy stamped
- [x] Lead **`APPROVE PA STRATEGY`**, 2026-09-22 ET
- [ ] **PA-A** gap audit (unlocked — pending)

---

*PA STRATEGY handoff — **APPROVED / CLOSED** — Lead **`APPROVE PA STRATEGY`**, 2026-09-22 ET. Next: **PA-A**.*
