# Lib/00_Core/CAM_Hero.md

**ID:** P1_WLD_graybox  
**Date:** 2026-09-16  
**Role:** WLD  
**Shot:** Shot 1 — Homestead night lookout — key-art match (`Docs/00_SHOTLIST.md`)  
**Inputs:** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`

---

## Pose (meters, +Z up)

| Field | Value |
|---|---|
| Name | `CAM_Hero` |
| Location | (−4.0, 4.5, 3.2) |
| Aim / look-at | (7.0, −3.5, 1.0) → then continue gaze toward (0.0, −70.0, −95.0) |
| Rotation (Euler XYZ, degrees) | X = −18°, Y = 0°, Z = −145° |
| Lens | ~35 mm equiv (wide enough for homestead + valley; not fisheye) |
| Near / far | 0.1 / 500 |

**Intent (shotlist):** Slightly behind and above the cabin plateau, looking across the stone path toward the right cliff edge and down into the planet valley. Homestead left, lookout/family edge right, huge moon upper-right (sky; LIT/ENV), world below readable.

Composition anchors:
- Left frame: `SM_Cabin`, `SM_Garden_Beds`, start of `SM_Path_Homestead`
- Right cliff: `SM_Lookout_Pad` (+ silhouette markers ENV places)
- Down / mid-distance: `SM_Islet_01/02`, pine valley blocks
- Far below: `SM_Landing_Circle`, path, roofs, `SM_Shrine_Return`

---

## Sightline checklist (gate)

From this pose, the following volumes must fall inside the key-art frustum (no occlusion by island mass except intentional cliff silhouette):

| Must-see | Volume | Status |
|---|---|---|
| Landing circle | `SM_Landing_Circle` | CLAIMED PASS |
| 2–3 roofs | `SM_Roof_Hamlet_01`, `SM_Roof_Hamlet_02`, `SM_Roof_Hamlet_03` | CLAIMED PASS |
| Forest path | `SM_Path_Planet_SegA` (SegB readable) | CLAIMED PASS |
| Return shrine | `SM_Shrine_Return` | CLAIMED PASS |

Additional lookout-test points (canon §2): first harvest `SM_Gather_FirstHarvest`, way home via return shrine + cliff back-read — placed for ENV verify.

**Reject if (shotlist):** planet below missing path / rooftops / pine valley; pancake island; family edge not readable at lookout.

---

## Helper cameras (framing only — not hero-modeled)

Poses live as CAM_ volumes in `GRAYBOX_LAYOUT.md`. `CAM_Hero` is the P1 gate camera.
