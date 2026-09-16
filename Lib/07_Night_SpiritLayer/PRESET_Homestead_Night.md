# PRESET_Homestead_Night

**ID:** P3_LIT_night  
**Date:** 2026-09-16  
**Role:** LIT  
**Status:** SPEC READY — Blender MCP not available; build when MCP connects  
**Collection:** `Lib/07_Night_SpiritLayer`  
**Preview map:** `Maps/Preview_Homestead_Night`  
**North star:** `refs/keyart_homestead_night.jpg`  
**Inputs:** `Docs/02_ART_BIBLE.md`, `Docs/02_MATERIAL_SHEET.md`, `Lib/06_Materials_Master/NIGHTMIX_DEMO.md`, `Docs/00_SHOTLIST.md` Shots 1–2, `Lib/00_Core/CAM_Hero.md`, `Docs/00_CANON.md`

---

## 1. Intent

Homestead night is **one lighting preset + NightMix overlay**, not a second map. Warm cabin amber punches against cool moonlight. Moon is a **feature** (huge warm yellow disc), never a tiny white speck. Cabin windows **never dark**. Soft volume haze under the cliff sells the drop to the planet below.

Tone: warm, readable, handmade, hopeful — not grimdark, not photoreal, not sci-fi.

---

## 2. Machine-readable preset (JSON)

```json
{
  "preset_id": "PRESET_Homestead_Night",
  "engine_targets": ["Blender_Eevee_lookdev", "UE5_Lumen_later"],
  "nightmix": 0.85,
  "world": {
    "sky_color": "#0B1630",
    "horizon_glow": "#7EC8E8",
    "stars": "dense_soft_white",
    "peach_clouds": true,
    "ambient": [0.08, 0.10, 0.18],
    "ambient_strength": 0.35
  },
  "lights": [
    {
      "name": "LIT_Moon",
      "type": "emissive_disc + directional_or_area_key",
      "color_hex": "#FFE07A",
      "color_range": ["#FFD56A", "#FFE28A"],
      "kelvin_feel": "warm_yellow_not_white",
      "disc_angular_diameter_deg": 18,
      "key_intensity_eevee": 2.2,
      "key_softness": 0.65,
      "role": "hero_sky_disc + cool-neutral rim/fill on world"
    },
    {
      "name": "LIT_CabinWindows",
      "type": "mesh_emissive + local_area_fill",
      "kelvin": [2700, 3200],
      "emissive_color_hex": "#FFB060",
      "bloom": true,
      "never_dark": true,
      "role": "warm_accent_porch_path_planters"
    },
    {
      "name": "LIT_MoonCool",
      "type": "fill_volume_standin",
      "origin_graybox": [10.0, -2.0, 12.0],
      "color": [0.55, 0.62, 0.85],
      "intensity": 0.45,
      "role": "cool_cliff_pine_grass_edge_fill"
    },
    {
      "name": "LIT_CabinWarm",
      "type": "local_fill_standin",
      "origin_graybox": [-6.0, 1.0, 1.5],
      "kelvin": 3000,
      "intensity": 1.4,
      "role": "porch_fence_planter_warm_spill"
    }
  ],
  "volume": {
    "name": "VOLUME_Haze",
    "placement": "under_cliff_lookout_face",
    "density": 0.08,
    "anisotropy": 0.2,
    "color": [0.55, 0.72, 0.95],
    "role": "cloud_sea_separating_plateau_from_planet"
  },
  "post": {
    "bloom": true,
    "bloom_threshold": 0.55,
    "bloom_intensity": 0.45,
    "ao": true,
    "volumetrics": true,
    "shadows": "soft_blue_purple_never_pure_black"
  }
}
```

---

## 3. Light stack (authoring order)

| Priority | Name | Type | Role |
|---:|---|---|---|
| 1 | `LIT_Moon` disc | Large emissive sphere/disc | Hero sky read — huge warm yellow |
| 2 | `LIT_Moon` key | Sun / directional or large area | Soft top/side cool-neutral fill + rim on cliff tops, pine crowns, grass edges |
| 3 | `LIT_CabinWindows` | Window pane emissives (`M_WoodCabin` window instances) | Amber bloom 2700–3200K; never dark |
| 4 | `LIT_CabinWarm` | Local area / point at cabin | Spill onto porch, nearby fence, planters, path start |
| 5 | `LIT_MoonCool` | Soft fill (graybox volume at `(10, −2, 12)`) | Cool forest / cliff fill; shadows stay deep **blue–purple** |
| 6 | `VOLUME_Haze` | World volume / cube under cliff | Blue-white haze sea under lookout face |
| 7 | World / sky | Background | Navy → dark purple; dense soft stars; peach clouds; horizon cyan/peach; distant snow peak readable |

**Eevee lookdev (MCP later):** Bloom ON, AO ON, volumetrics ON.  
**UE later:** Lumen + oversized warm moon (UDS or equivalent); same names.

---

## 4. Palette lock (from art bible)

| Chip | Hex / range | Use in this preset |
|---|---|---|
| Moon warm yellow | `#FFD56A`–`#FFE28A` | Disc albedo + emissive |
| Cabin amber | ~2700–3200K / `#FFB060` feel | Window + porch spill |
| Navy sky | deep navy → dark purple | World background |
| Peach clouds | peach / pale pink / cream | Mid-sky forms |
| Cool moonlight fill | soft cool / neutral | Rim on cliff, pines, grass |
| Horizon glow | soft cyan/blue → peach | Curved world edge |
| Cliff shadow | cool gray-violet | Never pure black |

**Do:** high silhouette contrast; warm windows punch; saturated but soft PBR under NightMix.  
**Don’t:** bleach moon white; kill window emissive; muddy mid-gray; grim overcast; rebuild geometry for night.

---

## 5. NightMix drive notes

| Topic | Spec |
|---|---|
| Source | Single GameState / time-of-day float → material `NightMix` on all ten masters |
| Homestead_Night default | **`NightMix = 0.85`** (spirit-capable night; not full 1.0 unless spirit layer peaks) |
| Day (not this preset) | `NightMix → 0` + this light stack off / Planet_Day on |
| Overlay | Tint + desaturate + value mul per master JSON `night_overlay` — **no** `_Night` texture sets |
| Spirit layer | `M_SpiritUnlit` peaks when NightMix high; layer visibility can track same float |
| Cabin body | NightMix cool-washes timber; **windows stay warm** via emissive instances / LIT — never rely on NightMix alone for window read |
| Nurtured crops | `M_Nurtured` emissive remains readable under NightMix |
| Demo proof | `Lib/06_Materials_Master/NIGHTMIX_DEMO.md` sphere row — LIT does not invent 11th master |

**Runtime contract (GP later):** one float drives (1) light preset blend / enable, (2) NightMix on masters, (3) optional spirit-layer visibility. Do not author per-mesh night duplicates.

---

## 6. Shot binding

| Shot | Camera | Preset use |
|---|---|---|
| **1** Homestead night lookout | `CAM_Hero` | Full stack: huge moon upper-right, warm cabin left, haze under cliff, planet readable |
| **2** Cabin + garden close | `CAM_CabinClose` (graybox) | Same preset; emphasize window bloom + planter spill; moon may be partial / out of hero framing — do **not** widen into Shot 1 |

---

## 7. Gate claims (LIT-owned for WAVE 2)

- [x] Spec: `Preview_Homestead_Night` assembly checklist targets key-art read  
- [x] Spec: windows bloom (2700–3200K emissive + bloom)  
- [x] Spec: moon huge and warm (`#FFD56A`–`#FFE28A`, ~18° disc — not white speck)  
- [ ] Live Eevee/UE frame pending Blender MCP / ENV-H + PROP dress  

---

## 8. Related files

- `Lib/07_Night_SpiritLayer/LIT_Moon.md`
- `Lib/07_Night_SpiritLayer/LIT_CabinWindows.md`
- `Lib/07_Night_SpiritLayer/VOLUME_Haze.md`
- `Lib/07_Night_SpiritLayer/CAM_Hero_LIT_NOTES.md`
- `Maps/Preview_Homestead_Night/README.md`
