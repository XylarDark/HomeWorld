# LIT_Moon

**ID:** P3_LIT_night  
**Date:** 2026-09-16  
**Role:** LIT  
**Status:** SPEC READY — Blender MCP pending  
**Preset:** `PRESET_Homestead_Night`  
**North star:** `refs/keyart_homestead_night.jpg`

---

## 1. Rule

Moon size is a **feature**, not a decoration. Huge warm yellow soft-edged disc. **Reject** tiny white speck / cold white / hard-edged sun disc.

Art bible chip: **`#FFD56A`–`#FFE28A`**.

---

## 2. Disc geometry + color

| Field | Value |
|---|---|
| Object name | `LIT_Moon` (disc mesh) + `LIT_Moon_Key` (directional/area) |
| Disc diameter (world) | **28–36 m** (hero disc large enough to dominate upper-right of Shot 1) |
| Disc distance from `CAM_Hero` | ~55–75 m along upper-right sky ray (far enough to parallax soft; close enough to read huge) |
| Angular size in Shot 1 | **~16–20°** of vertical FOV (target **18°**) — reads as key-art moon, not speck |
| Shape | Soft circular disc (slightly soft alpha edge / glow fringe); not crescent for MVP |
| Albedo / emissive color | `#FFE07A` center → `#FFD56A` rim (within bible range) |
| Emissive strength (Eevee) | High enough to bloom; center brighter than rim |
| Roughness | N/A (unlit / emissive disc) |
| Shadow | Disc itself does not cast hard shadow; **key light** does soft shadows toward lower-left |

```json
{
  "name": "LIT_Moon",
  "disc_diameter_m": 32,
  "angular_diameter_deg_shot1": 18,
  "color_hex_center": "#FFE07A",
  "color_hex_rim": "#FFD56A",
  "kelvin_feel": "warm_yellow",
  "forbidden": ["tiny_white_speck", "cold_white", "photoreal_crater_moon"]
}
```

---

## 3. Placement relative to CAM_Hero / key art

**`CAM_Hero` pose (WLD, do not overwrite):**  
Location `(−4.0, 4.5, 3.2)`, aim toward lookout `(7.0, −3.5, 1.0)` then valley `(0.0, −70.0, −95.0)`, Euler ≈ `X −18°, Y 0°, Z −145°`, ~35 mm.

| Anchor | Spec |
|---|---|
| Screen position (Shot 1) | **Upper-right quadrant** — above / beyond family lookout silhouettes |
| World hint origin | Place disc center near **`(18.0, −28.0, 22.0)`** as starting guess; nudge so moon sits upper-right in `CAM_Hero` frustum without clipping cabin left |
| Key light direction | From upper-right toward lower-left (matches key-art soft shadows on plateau) |
| Key light color | Cool-neutral / soft lavender-blue fill on world — **disc stays warm**; key can be slightly cooler than disc so cabin amber still wins contrast |
| Key intensity (Eevee) | ~2.0–2.5; softness / angle high so cliffs get soft rim, not harsh midday |
| Graybox fill volume | `LIT_MoonCool` at `(10.0, −2.0, 12.0)` — keep as soft fill companion |

**Composition lock (key art):**  
Cabin left + warm windows → path → family at right cliff facing moon → moon upper-right → peach clouds mid → navy stars → snow peak left-distant → haze under cliff → planet below.

---

## 4. Key light companion (`LIT_Moon_Key`)

| Field | Value |
|---|---|
| Type | Sun/directional **or** large area light |
| Color | `(0.70, 0.78, 0.95)` cool-neutral (world fill/rim) |
| Energy | Tuned so grass stays lively under NightMix; cliff strata readable |
| Softness | High — soft blue–purple shadows, never pure black |
| Specular | Low on foliage cards / grass |

Disc = sky hero read. Key = lighting contribution. Both required.

---

## 5. Shot 1 vs Shot 2

| Shot | Moon behavior |
|---|---|
| Shot 1 (`CAM_Hero`) | Full disc in upper-right; must pass “huge warm” gate |
| Shot 2 (`CAM_CabinClose`) | May be out of frame or partial glow only — do not reframe camera to chase moon (that becomes Shot 1) |

---

## 6. Acceptance / rejects

**Pass when:**  
- Angular size ~16–20° in Shot 1  
- Color in `#FFD56A`–`#FFE28A`  
- Soft bloom fringe readable  
- Warm-vs-cool contrast with cabin amber survives  

**Fail when:**  
- Tiny white speck  
- Cold white / blue-white moon disc  
- Photoreal crater moon  
- Moon so dim it reads as a star  
