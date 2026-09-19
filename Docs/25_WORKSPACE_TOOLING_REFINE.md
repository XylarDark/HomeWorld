# Docs/25 — Workspace & Tooling Refine (WTR)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED** — WTR-A…E implemented 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Prior** | Docs/24 VNP **IMPLEMENTED** — [24_VS_NIGHT_PINE_MESH.md](24_VS_NIGHT_PINE_MESH.md); Docs/23 **CLOSED** |
| **Prefix** | **WTR** |
| **Engine** | Launcher UE **5.8.2** |
| **Branch** | `feat/ue58-workspace-tooling` |
| **Mode** | NON-SWARM (engineering harness) |

---

## Gate

Lead unlocked via UE 5.8 workspace / tooling enhancement plan. Docs/23–24 stay closed as product tracks; this track refines **workspace tools** only.

---

## Workspace adopt / defer / reject matrix

| Item | Verdict | Notes |
|------|---------|-------|
| Epic `ModelContextProtocol` (Experimental) | **Evaluate sandbox only** | No dual-server with UnrealMCP; see WTR-B |
| UnrealMCP (port 55557) | **Keep primary** | Conductor / Windows bridge |
| Python `AutomationLibrary` / screenshots | **Adopt** | Evidence pipeline (WTR-C) |
| `EditorPythonScripting.set_keep_python_script_alive` | **Adopt** | UnrealEditor-Cmd batch pattern |
| Unreal Insights + shader-compile playbook | **Adopt** | Document in UE58_TECH (WTR-E) |
| Mesh Terrain tessellation / memory CVars (5.8.2) | **Document** | Sandbox path only — [U58F_G](handoffs/U58F_G_MESH_TERRAIN.md) |
| D3D12 OOM `rhi.UseSubmissionThread=0` | **Document DESKTOP-only** | Do not bake into DefaultEngine unless Lead gate + KNOWN_ERRORS |
| ModelingObjectsCreationAPI | **Defer** | Unless pine/kit import requires it |
| Live Coding vs Safe-Build | **Keep Safe-Build policy** | No change |
| MetaHuman / Mobile / Mover | **Reject / Defer** | Product lock |

---

## Phases

| Phase | Focus | Status | Evidence |
|-------|--------|--------|----------|
| **WTR-A** | Strategy matrix | **DONE** | This doc |
| **WTR-B** | MCP capability matrix | **DONE** | [U58F_F_MCP_DECISION.md](handoffs/U58F_F_MCP_DECISION.md) — UnrealMCP primary confirmed |
| **WTR-C** | Python / evidence harden | **DONE** | `vnp_p3_pine_import.py` · `vnp_night_tune_and_evidence.py` (CAM_Hero/CabinClose/PortalNight) · `vnp_editor_keep_alive.py` · `wtr_c_batch_run.py` · PCG introspect |
| **WTR-D** | Lookdev tool refine | **DONE** | PVE notes on [U58F_C](handoffs/U58F_C_PVE_PINE.md) · `wtr_pcg_nondestructive_spike.py` · Mesh CVars on [U58F_G](handoffs/U58F_G_MESH_TERRAIN.md) |
| **WTR-E** | Stability / Insights playbook | **DONE** | [UE58_TECH.md](../docs/UE/UE58_TECH.md) DESKTOP section |

---

## Non-goals

Dual MCP in Conductor sessions; MetaHuman/mobile/Mover; VS_MVP Landscape → Mesh Terrain replace; DevHarness mass rewrite.

---

## Sources (UE 5.8)

- [UE 5.8 Released (forums)](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274)
- [5.8.2 Hotfix](https://forums.unrealengine.com/t/5-8-2-hotfix-released/2746335)
- [Python API 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/introduction)
- [Scripting and Automating the Editor](https://dev.epicgames.com/documentation/unreal-engine/scripting-and-automating-the-unreal-editor)
