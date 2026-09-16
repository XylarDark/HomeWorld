# VOLUME_Haze

**ID:** P3_LIT_night  
**Date:** 2026-09-16  
**Role:** LIT  
**Status:** SPEC READY — Blender MCP pending  
**Preset:** `PRESET_Homestead_Night`

---

## 1. Intent

Soft **under-cliff haze / cloud-sea** separates the homestead plateau from the planet valley below. Sells height, depth, and the key-art “floating above a world” read. Hopeful cyan–blue-white — not horror fog, not photoreal mist.

---

## 2. Placement (relative to graybox)

| Field | Value |
|---|---|
| Name | `VOLUME_Haze` |
| Primary zone | Under `SM_Cliff_LookoutFace` and along torn underside toward cabin face |
| Cliff face ref | `SM_Cliff_LookoutFace` origin `(7.5, −5.5, −4.0)`, size `6 × 2.5 × 8` |
| Suggested volume bounds | Box/sphere cluster covering approx **X ∈ [−4, 14]**, **Y ∈ [−14, −4]**, **Z ∈ [−18, −2]** |
| Density peak | Just below lookout edge / cliff lip — thicker under right cliff, thinner toward mid-air islets |
| Clear air | Plateau top (Z ≈ 0 walkable) stays mostly clear so garden/path stay readable |

```json
{
  "name": "VOLUME_Haze",
  "bounds_hint_m": {
    "x": [-4.0, 14.0],
    "y": [-14.0, -4.0],
    "z": [-18.0, -2.0]
  },
  "density": 0.08,
  "anisotropy": 0.2,
  "color_rgb": [0.55, 0.72, 0.95],
  "color_hex": "#8CB8F2",
  "role": "under_cliff_cloud_sea"
}
```

---

## 3. Look parameters

| Param | Target |
|---|---|
| Color | Soft blue-white / cyan `(0.55, 0.72, 0.95)` — art bible horizon/haze family |
| Density | Low–medium (~0.05–0.12) — soft sea, not soup |
| Anisotropy | Low (~0.15–0.3) — gentle forward scatter from moon key |
| Lighting | Lit by `LIT_Moon_Key` / sky; may catch faint warm bounce near cabin underside — keep cool overall |
| Horizon link | Blend toward horizon glow (`#7EC8E8` feel) at curved world edge |

**Eevee:** Principled Volume or volume scatter + absorption in a bounded domain; volumetrics ON.  
**UE later:** Exponential height fog / volumetric fog tuned to same read — keep name `VOLUME_Haze`.

---

## 4. Composition duties

| Shot | Must do |
|---|---|
| Shot 1 | Visible under cliff lip between plateau and planet; does not erase pine valley / path / 2–3 rooftops |
| Shot 2 | Optional soft edge only — do not flood cabin close with haze |
| Shot 3 (later) | Haze still sells drop-off during glide departure |

Planet masses (`SM_Landing_Circle`, roofs, path, pine valley blocks) must remain **readable through or below** the haze — haze is a soft band, not a whiteout.

---

## 5. Acceptance / rejects

**Pass when:**  
- Soft cloud-sea under cliff in Shot 1  
- Height/drop feels large  
- Planet elements still gate-readable from `CAM_Hero`  

**Fail when:**  
- Grimdark black void under cliff  
- Photoreal ground fog hiding valley  
- Density so high rooftops/path disappear  
- Sci-fi neon volume  
