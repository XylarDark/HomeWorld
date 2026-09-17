# Handoff

- **ID:** P4_LIT_day
- **Phase:** P4 / WAVE 3
- **Role:** LIT
- **Owner agent:** Executor (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend` (`LIT_Planet_*`, `LIT_LandingDay`)
- `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`
- `Docs/handoffs/P4_LIT_day.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| LIT_Planet_Sun | SUN key | — | 02_Forest |
| LIT_Planet_Fill | AREA cool fill | — | 02_Forest |
| LIT_LandingDay | AREA clearing | — | 02_Forest |
| Scene props `LIT_PRESET_Planet_Day`, `Planet_Night_Spirit_note` | meta | — | Scene |

## Phase exit boxes I claim

- [x] **Planet_Day** preset for Shot 4: warm sun key + cool fill + landing area
- [x] Optional **Planet_Night_Spirit** notes only (reuse homestead night/spirit cues at `SM_Shrine_Return`; NightMix driver; no new lights/materials invented)
- [x] Did not invent new materials — same 10 masters; NightMix=0 for day lookdev
- [x] Homestead night stack left intact for Shots 1–3 / portal

### Planet_Day (machine-readable)

```json
{
  "preset_id": "Planet_Day",
  "nightmix": 0.0,
  "lights": [
    {"name": "LIT_Planet_Sun", "type": "SUN", "energy": 3.2, "color": [1.0, 0.95, 0.85], "role": "warm_key"},
    {"name": "LIT_Planet_Fill", "type": "AREA", "energy": 80.0, "color": [0.55, 0.68, 0.95], "size": 18.0, "role": "cool_fill"},
    {"name": "LIT_LandingDay", "type": "AREA", "energy": 120.0, "color": [1.0, 0.98, 0.92], "size": 12.0, "origin": [0, -70, -88], "role": "clearing_fill"}
  ]
}
```

### Planet_Night_Spirit (notes only — not a second map)

- Drive `NightMix ≈ 0.85` on the ten masters (same as `PRESET_Homestead_Night`).
- Enable soft `M_SpiritUnlit` on `SM_Shrine_Return` glow; link to homestead shrine portal (Shot 5).
- Reuse moon/cool fill language from `Lib/07_Night_SpiritLayer/` — do not author an 11th master or sci-fi portal light.

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path / PHASE_BOARD

## Inputs I used

- `Docs/00_SHOTLIST.md` Shot 4
- `Docs/02_MATERIAL_SHEET.md`
- `Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md` (night/spirit reuse notes)
- `Lib/00_Core/GRAYBOX_LAYOUT.md` (`LIT_LandingDay` volume)
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- Blender 5.2 Eevee Next still lacks classic bloom flag (same as P3); day stills rely on sun/fill energy.
- Day/night is light hide_render toggle for stills — runtime should use one NightMix float + preset blend (GP later).

## Risks for the next owner

- Keep day and night as parameter/preset switches, not duplicate meshes.
- Portal night beauty pass should prefer shrine cameras + spirit unlit, not landing-day sun.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `blender/floating_island_homestead_LIB.blend`
  - `Docs/handoffs/P4_LIT_day.md`
  - `Maps/Preview_Lookout_To_Planet/README.md`
- Screenshot / frame / render / checklist output:
  - `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png` (Planet_Day)
  - `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png` (night stack retained for depart)
- Test or verify notes (command run + outcome):
  - CLI Eevee render with day lights on / night lights hidden for Shot 4
  - Masters cite-only; no 11th `M_*` family added
