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
