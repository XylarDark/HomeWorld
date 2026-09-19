# Docs/23 — UE 5.8 Feature Adoption (U58F)

| Field | Value |
|-------|-------|
| **Status** | **U58F-A…G IMPLEMENTED** (C AD gate pending for pine commit; G sandbox-only) — Lead implement-plan 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Prior** | Docs/22 UE 5.8 Upgrade **CLOSED** — [22_UE58_UPGRADE.md](22_UE58_UPGRADE.md) |
| **Prefix** | **U58F** |
| **Engine** | Launcher UE **5.8.2** (features from 5.8.0; 5.8.2 hotfix install) |
| **Branch** | `feat/ue58-feature-adoption` |
| **PR** | [#111](https://github.com/XylarDark/HomeWorld/pull/111) |

---

## Gate

Lead unlocked adoption via the UE 5.8 Feature Adoption plan implement order (**`APPROVE U58F STRATEGY`** implied by implement-all). Horizon: Act 1 / VS_MVP + Reap-Sow ROI — not kitchen-sink Experimental enable.

---

## Phases

| Phase | Focus | Status | Evidence |
|-------|--------|--------|----------|
| **U58F-A** | Strategy + matrix | **APPROVED** | This doc · [UE58_TECH.md](../docs/UE/UE58_TECH.md) |
| **U58F-B** | PCG 5.8 | **APPROVED** | Plugins on · `u58f_pcg_smoke.py` ok · PCG_BEST_PRACTICES 5.8 |
| **U58F-C** | PVE stylized pine | **PLUGIN ON / AD PENDING** | [U58F_C_PVE_PINE.md](handoffs/U58F_C_PVE_PINE.md) |
| **U58F-D** | MegaLights + Fog SSS | **APPROVED** | DefaultEngine.ini · `u58f_night_look_smoke.py` ok |
| **U58F-E** | Lumen Lite | **APPROVED** | DefaultScalability.ini · UE58_TECH CVars |
| **U58F-F** | MCP decision | **APPROVED** | [U58F_F_MCP_DECISION.md](handoffs/U58F_F_MCP_DECISION.md) — keep UnrealMCP |
| **U58F-G** | Mesh Terrain | **SPIKE READY** | [U58F_G_MESH_TERRAIN.md](handoffs/U58F_G_MESH_TERRAIN.md) — no VS_MVP replace |

---

## Adoption matrix (decision stamp)

| 5.8 capability | Fit for HomeWorld | Verdict |
|----------------|-------------------|---------|
| **PCG** nondestructive manual edit + biome/graph workflow | Planet path / forest PCG central | **Adopt** |
| **Procedural Vegetation Editor (PVE)** | Pine masters / Nanite cards — stylized only | **Adopt with Art Director gate** |
| **MegaLights** (production-ready) | Homestead night warm windows + many dynamics | **Adopt** |
| **Fog Screen Space Scattering** | Night / spirit atmosphere | **Adopt** |
| **Lumen Lite** | Steam EA low-end / 60 FPS | **Adopt** (scalability; keep HQ for hero shots) |
| **Day Sequence** | Already enabled | **Keep / deepen** |
| **Epic MCP / ModelContextProtocol** (Experimental) | UnrealMCP already proven (55557) | **Evaluate only — keep UnrealMCP** |
| **Mesh Terrain** (Experimental) | Cliffs/overhangs/caves | **Spike only** (sandbox; Lead `APPROVE U58F-G` for Landscape replace) |
| **Toon Shader** | vs 10 Substrate masters | **Spike with AD** — no master replace without bible amendment |
| **MetaHuman / Mesh-to-MH / MH Crowds / markerless Animator** | Photoreal vs Manny KEEP-LOCAL + stylized family | **Reject for hero/family** |
| **MassCrowd / Learning Agents / Mover rewrite** | Future swarms / movement | **Defer** |
| **Dataflow / Chaos Cloth / Destruction** | Physics authoring | **Defer** |
| **Movie Render Graph / Live Link Hub / Accumulation DoF** | Cinematics / VP | **Defer** |
| **Mobile SDK / Remote / Platform Preview** | Platform lock = PC + Steam EA | **Reject** |
| **Control Rig Dynamics / Direct Mesh Controls** | Anim polish | **Defer** until character pass beyond Mannequins |

---

## Plugins enabled (this track)

`PCGBiomeCore`, `PCGPrimitives`, `ProceduralVegetationEditor`, `MeshTerrainMode` (plus existing PCG stack). Epic `ModelContextProtocol` **not** enabled.

---

## DESKTOP smoke (2026-09-19)

| Script | Result |
|--------|--------|
| `u58f_pcg_smoke.py` | **ok** — PCG + BiomeCore + Primitives + PythonInterop |
| `u58f_pve_smoke.py` | **ok** — PVE enabled; AD gate PENDING |
| `u58f_night_look_smoke.py` | **ok** — MegaLights + Fog SSS project CVars; volumetric fog on height fog |
| `u58f_mesh_terrain_smoke.py` | **ok** — MeshTerrainMode on; sandbox map not created (KEEP-LOCAL) |

Forest graph `/Game/HomeWorld/PCG/ForestIsland_PCG` absent post-WAVE F — plugins adopted; duplicate graphs when forest PCG returns.

---

## Non-goals

MetaHuman hero/family; mobile; Mover; dual MCP; Landscape replace without AD+WLD; committing Mannequins or non-allowlisted `.uasset` dumps.

---

## Success criteria

- [x] Docs/23 filed; PHASE_BOARD wired; matrix stamped
- [x] PCG 5.8 plugins + practices docs; smoke ok
- [x] PVE plugin on; pine Content commit AD-gated (handoff)
- [x] Night: MegaLights + Fog SSS in DefaultEngine.ini; smoke ok
- [x] Lumen Lite documented (Medium GI/Reflections)
- [x] MCP decision: keep UnrealMCP
- [x] Mesh Terrain spike ready (sandbox-only)
