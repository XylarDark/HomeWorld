# Docs/23 U58F-C — PVE stylized pine (Art Director gate)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | U58F-C |
| **Plugin** | `ProceduralVegetationEditor` enabled in `.uproject` |
| **AD gate** | **APPROVE** — see [VNP_P2_AD_PINE_VERDICT.md](VNP_P2_AD_PINE_VERDICT.md) (OBJ; FBX polish later) |

---

## Intent

Use PVE to author **one** on-model pine: conical, slightly fluffy, **tiered foliage cards** ([02_ART_BIBLE.md](../02_ART_BIBLE.md)). Reject Epic “biological accuracy” defaults if they read photoreal/muddy.

## Automation

- Smoke: `Content/Python/u58f_pve_smoke.py` → `Saved/u58f_pve_smoke.json`
- Do not commit PVE output until AD approve + Docs/20 allowlist path

## Reject criteria (AD)

- Photoreal bark/needles, second tree species, grim/muddy canopy
- Breaking the 10-master material sheet without bible amendment

## Next

AD **APPROVE** 2026-09-19 — [VNP_P2_AD_PINE_VERDICT.md](VNP_P2_AD_PINE_VERDICT.md).  
OBJ staged at `Content/HomeWorld/Meshes/Environment/SM_Pine_Stylized_VNP.obj`.  
Re-run `vnp_p3_pine_import.py` when Editor/MCP is up for `.uasset`; then optional PCG wire.

---

## WTR-D — PVE / external mesh import (stylized only)

Epic path (UE 5.8 Procedural Vegetation Editor): import **AD-approved** OBJ/FBX → Static Mesh on allowlisted `/Game/HomeWorld/Meshes/Environment/` → open **Modes → Procedural Vegetation** (or PVE Editor) → create/assign vegetation asset using that mesh as the stylized pine base. **Do not** pull Megaplants / photoreal sample packs.

| Step | Automation |
|------|------------|
| OBJ → StaticMesh `.uasset` | `Content/Python/vnp_p3_pine_import.py` (Editor/MCP or Cmd) |
| PVE authoring UI | GUI-heavy — log gaps; no dual Epic MCP |
| Material | Bind to Docs/02 masters only (`M_Foliage` / sheet) |

Reject: photoreal bark atlases, second species, grim muddy canopy (AD criteria above).
