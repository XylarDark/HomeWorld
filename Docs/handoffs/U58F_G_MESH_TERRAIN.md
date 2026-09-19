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

## 5.8.2 tessellation / memory (WTR-D)

Source: [5.8.2 Hotfix](https://forums.unrealengine.com/t/5-8-2-hotfix-released/2746335) — Mesh Terrain crash on extreme tessellation.

| Guard | Behavior |
|-------|----------|
| Soft budget | Console variable caps **newly created elements per tessellation (Remesh) modifier** — **default 100,000,000** |
| Hard cap | Attempts exceeding **MAX_int32** elements are always blocked |
| On hit | Tessellation / Remesh modifier **does nothing** (no crash) |

**Discover exact CVar name on DESKTOP** (name not published in forum prose; may ship under MeshPartition / Remesh):

```text
DumpConsoleVariables MeshPartition
DumpConsoleVariables Remesh
DumpConsoleVariables Tessellat
```

Or Epic MCP EditorAppToolset `SearchCVars` in a throwaway sandbox (never dual-server with UnrealMCP on Conductor).

**Sandbox policy:** KEEP-LOCAL sculpt only on `/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain`. Do **not** bake memory CVars into `DefaultEngine.ini` unless Lead gate + KNOWN_ERRORS entry.

**Optional cliff sculpt:** small Remesh/tessellate pass on sandbox only; if Editor OOM, stop — see UE58_TECH DESKTOP stability (D3D12 residency).
