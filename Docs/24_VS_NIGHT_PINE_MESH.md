# Docs/24 — VS Night / Pine / Mesh (VNP)

| Field | Value |
|-------|-------|
| **Status** | **IMPLEMENTED** (P3 uasset import pending Editor reconnect; M2 sculpt KEEP-LOCAL) — 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Prior** | Docs/23 U58F **CLOSED** — [23_UE58_FEATURE_ADOPTION.md](23_UE58_FEATURE_ADOPTION.md) |
| **Prefix** | **VNP** |
| **Engine** | Launcher UE **5.8.2** |
| **Branch** | `feat/vs-night-pine-mesh` |
| **Mode** | N = NON-SWARM/HYBRID · P = HYBRID (AD) · M = NON-SWARM spike |

---

## Gate

Lead unlocked via Post-U58F lookdev plan implement (night → pine → mesh). Docs/23 stays **CLOSED**.

---

## Phases

| Phase | Focus | Status | Evidence |
|-------|--------|--------|----------|
| **N0** | Night plumbing smoke | **DONE** | `Saved/u58f_night_look_smoke.json` ok |
| **N1** | VS_MVP night tune | **DONE** | Fog/volumetric on VS_MVP; CVars MegaLights + Fog SSS |
| **N2** | Shots 1 / 2 / 5 evidence | **DONE** | `Saved/VNP_Evidence/*.png` + `vnp_night_evidence.json` (level `L_VS_MVP_Markers`) |
| **P1** | PVE pine KEEP-LOCAL | **DONE** | `Saved/VNP_PVE_Pine/` + stylized OBJ |
| **P2** | Art Director gate | **APPROVE** | [VNP_P2_AD_PINE_VERDICT.md](handoffs/VNP_P2_AD_PINE_VERDICT.md) |
| **P3** | Allowlist import + PCG | **PARTIAL** | OBJ staged `Content/HomeWorld/Meshes/Environment/`; uasset import pending Editor |
| **M1** | Mesh Terrain sandbox map | **DONE** | `L_U58F_MeshTerrain` created (`vnp_mesh_terrain_sandbox.json`) |
| **M2** | Cliff/overhang spike | **SPIKE STAMPED** | No Landscape replace; sculpt KEEP-LOCAL Editor Mode |

---

## Scripts

- `Content/Python/vnp_night_tune_and_evidence.py`
- `Content/Python/vnp_load_vs_mvp_and_evidence.py`
- `Content/Python/vnp_pve_pine_package.py`
- `Content/Python/vnp_p3_pine_import.py`
- `Content/Python/vnp_mesh_terrain_sandbox.py`
- `Content/Python/vnp_m2_mesh_terrain_spike.py`

---

## Non-goals

Reopen Docs/23 as ACTIVE; MetaHuman/Mover/dual MCP; Mannequins; VS_MVP Landscape replace without `APPROVE U58F-G`.

---

## Success criteria

- [x] Night shots 1/2/5 evidence with MegaLights + Fog SSS CVars
- [x] One AD-approved stylized pine path (OBJ)
- [x] Mesh Terrain sandbox without production Landscape change
- [ ] Pine `.uasset` import when Editor/MCP back (re-run `vnp_p3_pine_import.py`)
