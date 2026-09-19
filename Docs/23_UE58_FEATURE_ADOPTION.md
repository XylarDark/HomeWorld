# Docs/23 — UE 5.8 Feature Adoption (U58F)

| Field | Value |
|-------|-------|
| **Status** | **U58F-A…G IMPLEMENTED** (C AD gate pending for pine commit; G sandbox-only) — Lead implement-plan 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Prior** | Docs/22 UE 5.8 Upgrade **CLOSED** — [22_UE58_UPGRADE.md](22_UE58_UPGRADE.md) |
| **Prefix** | **U58F** |
| **Engine** | Launcher UE **5.8.2** |
| **Branch** | `feat/ue58-feature-adoption` |

---

## Gate

Lead unlocked adoption via feature-adoption plan implement.

---

## Phases

| Phase | Focus | Status | Evidence |
|-------|--------|--------|----------|
| **U58F-A** | Strategy + matrix | **APPROVED** | This doc · [UE58_TECH.md](../docs/UE/UE58_TECH.md) |
| **U58F-B** | PCG 5.8 | **APPROVED** | Plugins on · `u58f_pcg_smoke.py` · PCG_BEST_PRACTICES 5.8 |
| **U58F-C** | PVE stylized pine | **PLUGIN ON / AD PENDING** | [U58F_C_PVE_PINE.md](handoffs/U58F_C_PVE_PINE.md) |
| **U58F-D** | MegaLights + Fog SSS | **APPROVED** | DefaultEngine.ini · `u58f_night_look_smoke.py` |
| **U58F-E** | Lumen Lite | **APPROVED** | DefaultScalability.ini · UE58_TECH CVars |
| **U58F-F** | MCP decision | **APPROVED** | [U58F_F_MCP_DECISION.md](handoffs/U58F_F_MCP_DECISION.md) — keep UnrealMCP |
| **U58F-G** | Mesh Terrain | **SPIKE READY** | [U58F_G_MESH_TERRAIN.md](handoffs/U58F_G_MESH_TERRAIN.md) — no VS_MVP replace |

---

## Adoption matrix

See plan stamp / table in prior revision — verdicts unchanged (Adopt / Reject / Defer).

---

## Plugins enabled (this track)

`PCGBiomeCore`, `PCGPrimitives`, `ProceduralVegetationEditor`, `MeshTerrainMode` (plus existing PCG stack). Epic `ModelContextProtocol` **not** enabled.

---

## Non-goals

MetaHuman hero/family; mobile; Mover; dual MCP; Landscape replace without AD+WLD.
