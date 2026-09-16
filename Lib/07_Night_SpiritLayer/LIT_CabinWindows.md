# LIT_CabinWindows

**ID:** P3_LIT_night  
**Date:** 2026-09-16  
**Role:** LIT  
**Status:** SPEC READY — Blender MCP pending  
**Preset:** `PRESET_Homestead_Night`  
**Hard reject (canon):** dark / dead cabin windows

---

## 1. Rule

At night, **every** cabin window that faces Shot 1 or Shot 2 is warm emissive. Never dark glass. Never rely on NightMix alone — windows use **emissive instances + local warm fill**.

Kelvin target: **2700–3200K**. Art bible: cabin amber / golden.

---

## 2. Material cite

| Element | Master | Instance notes |
|---|---|---|
| Cabin body (logs, roof, door frame) | `M_WoodCabin` | Emissive **off**; NightMix cool-washes timber |
| Window panes / lantern glass | `M_WoodCabin` window instance **or** dedicated `MI_WoodCabin_WindowGlow` | **Emissive on** warm amber |
| Optional porch lantern | Same warm emissive language | PROP lantern if present |

Do **not** invent an 11th master. Window glow = instance Emissive on `M_WoodCabin` (sheet allows warm emissive on window/lantern glass only).

```json
{
  "name": "LIT_CabinWindows",
  "kelvin_min": 2700,
  "kelvin_max": 3200,
  "emissive_color_hex": "#FFB060",
  "emissive_rgb_linear_approx": [1.0, 0.69, 0.38],
  "emissive_strength_eevee": 12.0,
  "bloom": true,
  "never_dark": true,
  "master": "M_WoodCabin",
  "instance": "MI_WoodCabin_WindowGlow"
}
```

---

## 3. Light spill (`LIT_CabinWarm`)

Graybox already places `LIT_CabinWarm` volume at `(−6.0, 1.0, 1.5)`.

| Field | Value |
|---|---|
| Type | Area / point / spot soft |
| Kelvin | ~3000K |
| Color hex | `#FFB060`–`#FFC078` |
| Intensity | Enough to warm porch, nearby fence, planter faces, path start — not blow out whole island |
| Radius / soft | Falloff tight to cabin zone (~3–5 m influence) |
| Specular | Soft; avoid plastic hotspots on stylized wood |

Windows provide the **bloom hero**; `LIT_CabinWarm` provides **spill** onto garden/path so Shot 2 reads cozy.

---

## 4. Placement / coverage

Assume ENV-H modular cabin at graybox `SM_Cabin` origin `(−6.0, 1.0, 0.0)`, size ~5.5 × 4.5 × 5.5 m.

| Facing | Requirement |
|---|---|
| Shot 1 (`CAM_Hero`) — cabin left | Front / path-facing windows **lit** |
| Shot 2 (`CAM_CabinClose`) — three-quarter cabin face | All visible panes **lit**; no black rectangles |
| Side / rear not in shot | May be dimmer but prefer still warm if visible in silhouette |

**Count:** Match cabin kit window slots (ENV-H). LIT does not invent extra windows — every kit window pane gets the glow instance.

---

## 5. Bloom / post

| Setting | Target |
|---|---|
| Bloom | ON |
| Threshold | ~0.5–0.6 so windows + moon bloom; grass does not |
| Intensity | ~0.4–0.5 lookdev — “cozy bloom,” not neon sci-fi |
| Gate claim | **Windows bloom** readable in Shot 1 and Shot 2 stills |

---

## 6. NightMix interaction

| Param | Behavior |
|---|---|
| Cabin body NightMix | Cool wash / value mul per `M_WoodCabin` overlay |
| Window Emissive | Stays warm; optionally **multiply up** slightly as NightMix rises so contrast increases |
| Forbidden | Darkening window emissive with NightMix; swapping to a night texture set |

---

## 7. Acceptance / rejects

**Pass when:**  
- Visible windows read amber 2700–3200K  
- Soft bloom on panes  
- Warm spill on porch / planters / path start  
- Warm-vs-cool contrast vs moonlight  

**Fail when:**  
- Any dark / dead window in Shot 1 or 2  
- Neon cyan / sci-fi window color  
- Photoreal HDRI interior through glass  
- Bloom so extreme it washes the frame muddy  
