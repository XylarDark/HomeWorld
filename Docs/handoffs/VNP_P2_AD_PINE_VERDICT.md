# VNP-P2 — AD pine gate verdict

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Gate** | VNP-P2 AD pine |
| **Role** | AD |
| **Package** | `Saved/VNP_PVE_Pine/` |
| **Inputs** | `Docs/02_ART_BIBLE.md` §2 pines / §5 hard rejects; `Docs/handoffs/U58F_C_PVE_PINE.md`; `README_AD_GATE.md`; `SM_Pine_Stylized_VNP.obj` |
| **Verdict** | **APPROVE** |
| **Lead approval** | Not claimed (AD style gate only) |

---

## Verdict

**APPROVE**

## Reason

Against `Docs/02_ART_BIBLE.md` pine lock, `SM_Pine_Stylized_VNP.obj` passes the silhouette gate: one species only; overall **conical** mass (~6 m Z, bible 6–12 m low end); **four clear tiered foliage cones** (radii stepping down toward the tip) over a short conical trunk — stylized solid card-cones, not photoreal needles, Quixel bark, muddy canopy, grimdark, or a second tree species. Thumbnail read is on-model for homestead/planet pine language; FBX deferral does not block style approval when the OBJ geometry already shows the required conical + tiered-card structure.

## Import (APPROVE)

- **OBJ → UE import OK** into `Content/HomeWorld/Meshes/` or `Biomes/` (Docs/20 allowlist still applies).
- **Pending FBX polish** when Blender is available — re-export `SM_Pine_Stylized_VNP.fbx` preferred for pipeline; silhouette/style already cleared.
- On import: instance **M_WoodWild** (trunk) + **M_FoliageCard** (tiers) only — no new master shaders.
- Scale: meters; origin at ground contact (Z=0 base as authored).

## Explicit non-claims

- No Lead `APPROVE` invented or implied.
- Kits / Content not edited by AD this turn.
- `Docs/02_ART_BIBLE.md` unchanged.
- Does not approve Epic PVE biological defaults if later substituted — this APPROVE is for the submitted stylized OBJ silhouette only.
