# Maps/Preview_Homestead_Night

**Preview assembly — P3 LIT night preset**  
**Date:** 2026-09-16  
**ID:** P3_LIT_night  
**Role:** LIT (checklist owner); ENV-H + PROP supply meshes  
**Status:** SPEC / CHECKLIST — Blender MCP not available; assemble when MCP + kits land  
**North star:** `refs/keyart_homestead_night.jpg`

Sources: `Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md`, `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`, `Docs/00_SHOTLIST.md` Shots 1–2, `Docs/02_ART_BIBLE.md`.

---

## 1. Purpose

Single night lookdev preview proving **Homestead_Night** reads as key art for Shot 1 and cozy warm windows for Shot 2. Night = lights + NightMix + spirit-capable overlay — **not** a rebuilt map.

---

## 2. Assembly checklist — dependencies

### 2.1 From ENV-H (Lib/01)

- [ ] `SM_Island_Hero` / island top + layered `SM_Cliff_*` (torn earth, not pancake/cylinder)  
- [ ] Modular cabin kit dressed at `SM_Cabin`  
- [ ] Homestead pines (stylized only) at pine cluster volumes  
- [ ] Lookout pad / cliff edge readable  

### 2.2 From PROP

- [ ] Planters / garden beds at `SM_Garden_Beds`  
- [ ] Path stones along `SM_Path_Homestead`  
- [ ] Lantern / rack / workbench if in P3 kit  
- [ ] `SM_Shrine_Homestead` (socket ok as stub)  
- [ ] Landing-circle / planet proxies only as needed for Shot 1 background read (shared graybox OK)  

### 2.3 From LIT (`Lib/07_Night_SpiritLayer`)

- [ ] Apply `PRESET_Homestead_Night`  
- [ ] `LIT_Moon` disc + key (huge warm yellow)  
- [ ] `LIT_CabinWindows` emissives + `LIT_CabinWarm` spill  
- [ ] `VOLUME_Haze` under cliff  
- [ ] World/sky: navy, stars, peach clouds, horizon glow  
- [ ] Drive **NightMix = 0.85** on all ten masters (no `_Night` maps)  
- [ ] Cameras: `CAM_Hero` (Shot 1), `CAM_CabinClose` (Shot 2)  

### 2.4 Graybox lights already named

| Name | Origin | Role in preview |
|---|---|---|
| `LIT_CabinWarm` | (−6.0, 1.0, 1.5) | Warm spill stand-in → refine to area light |
| `LIT_MoonCool` | (10.0, −2.0, 12.0) | Cool fill stand-in → refine with moon key |

---

## 3. Shot 1 — key-art match tests

**Camera:** `CAM_Hero` — pose from `Lib/00_Core/CAM_Hero.md` (do not invent a new hero cam).

| # | Must-see / test | Pass criteria |
|---:|---|---|
| 1 | Cabin left | Warm glowing windows; bloom on |
| 2 | Garden + stone path | Readable on plateau |
| 3 | Family silhouettes | Adult + two children at right cliff / `SM_Lookout_Pad`, facing moon |
| 4 | Moon | Huge warm yellow (`#FFD56A`–`#FFE28A`), ~16–20° angular, upper-right — **not** tiny white |
| 5 | Sky | Starry navy; peach clouds; distant snow peak readable |
| 6 | Cliff | Layered torn earth under lookout |
| 7 | Haze | Soft under-cliff volume; height sold |
| 8 | Planet below | Pine valley + winding path + 2–3 rooftops in frustum |
| 9 | Islets | Extra small floating islets mid-distance |
| 10 | Contrast | Warm cabin amber vs cool moonlight survives |

**Shot 1 rejects:** photoreal/muddy/grim/sci-fi; extra tree species; tiny white moon; dark windows; pancake/cylinder; unreadable family; planet missing path/rooftops/valley.

---

## 4. Shot 2 — cabin + garden close tests

**Camera:** `CAM_CabinClose` `(−4.0, −2.5, 1.6)` (graybox).

| # | Must-see / test | Pass criteria |
|---:|---|---|
| 1 | Windows | Warm 2700–3200K emissive; **bloom**; never dark |
| 2 | Planters | Raised beds with colorful plant read |
| 3 | Path | Stone/dirt at homestead scale |
| 4 | Contrast | Night cool fill vs warm emissive |
| 5 | Framing | Does **not** widen into Shot 1 moon-hero wide |

**Shot 2 rejects:** dark/dead windows; muddy/grim; photoreal wood; extra biome props; drift into Shot 1 framing.

---

## 5. NightMix + spirit layer

| Setting | Value |
|---|---|
| NightMix | **0.85** on all masters in this preview |
| Spirit layer | Optional soft `M_SpiritUnlit` at shrine only if present — hopeful, not horror |
| Toggle contract | Later GP: one float flips lights + NightMix + spirit visibility |

---

## 6. Gate claims (WAVE 2 / P3 LIT)

- [x] Checklist written so `Preview_Homestead_Night` **targets** key-art read  
- [x] Windows bloom specified  
- [x] Moon huge and warm specified  
- [ ] Live stills pending ENV-H + PROP + Blender MCP  

When live: drop Shot 1 / Shot 2 frames under `Docs/qa/` (e.g. `Preview_Homestead_Night_Shot1.png`, `…_Shot2.png`) and cite in handoff evidence.

---

## 7. Out of scope for this map note

- New maps beyond this preview  
- New materials / 11th master  
- Gameplay, island hero modeling (ENV-H), PHASE_BOARD edits  
- Planet_Day preset (WAVE 3+)  
