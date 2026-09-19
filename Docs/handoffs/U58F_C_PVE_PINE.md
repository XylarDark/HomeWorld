# Docs/23 U58F-C — PVE stylized pine (Art Director gate)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | U58F-C |
| **Plugin** | `ProceduralVegetationEditor` enabled in `.uproject` |
| **AD gate** | **PENDING** — Art Director must approve first export |

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

After AD approve: import allowlisted mesh under `Content/HomeWorld/Meshes/` or `Biomes/`, wire into PCG duplicate graph (`ForestIsland_PCG_U58F_Edit`), evidence screenshot.
