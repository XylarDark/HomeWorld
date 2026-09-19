# Docs/23 U58F-G — Mesh Terrain sandbox

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | U58F-G |
| **Status** | **SPIKE READY** — plugin enabled; VS_MVP Landscape **not** replaced |
| **Lead gate** | Implementing plan unlocks sandbox spike; full replace needs AD + WLD |

---

## Policy

- Plugin `MeshTerrainMode` enabled for Editor experimentation.
- Reserved map: `/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain` (create KEEP-LOCAL when sculpting).
- **Do not** convert `L_VS_MVP_Markers` / production Landscape until Art Director + World Designer + Lead explicit approve.

## Smoke

`Content/Python/u58f_mesh_terrain_smoke.py` → `Saved/u58f_mesh_terrain_smoke.json`

## 5.8.2 note

If OOM during sculpt, apply Mesh Terrain memory budget CVars from the [5.8.2 hotfix notes](https://forums.unrealengine.com/t/5-8-2-hotfix-released/2746335).
