# Docs/02_ART_BIBLE.md

## Status: LOCKED (P2) — ID P2_AD_bible — 2026-09-16

**Owner:** AD (art half of Track C).  
**North stars:**
- `refs/keyart_homestead_night.jpg` — single-frame night homestead (look + Shot 1 composition).
- `refs/keyart_homestead_planetside_split.jpg` — diagonal split greybox: night floating homestead (top-left) + day planetside camp with tents, portal, campfire (bottom-right); dual-zone layout north star for demo greybox.
**Canon inputs:** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`  
**Out of scope:** material parameter sheets (TA → `Docs/02_MATERIAL_SHEET.md`); no new locations, props, biomes, or master shader families.

Tone lock: warm, readable, handmade, hopeful. Not cutesy-infantile. Not grim. Not photoreal. Not sci-fi.

---

## 1. Palette (from key art)

Primary contrast is **warm cabin amber vs cool moonlight**. Keep both readable in the same frame; never collapse into muddy mid-gray or pitch black.

| Chip | Role | Target range / notes |
|---|---|---|
| Moon warm yellow | Hero sky disc | `#FFD56A`–`#FFE28A`; huge soft-edged disc, never tiny white |
| Cabin amber | Window / porch emissive | Warm amber / golden; ~2700–3200K feel; always lit at night |
| Navy sky | Night backdrop | Deep navy → dark purple; dense soft stars |
| Peach clouds | Horizon / mid-sky | Peach, pale pink, cream highlights on voluminous soft forms |
| Cool moonlight fill | Night key on world | Soft cool / neutral rim on cliff tops, pine crowns, grass edges |
| Spring grass | Homestead + planet ground | Saturated spring greens; keep lively under NightMix |
| Warm dark wood | Cabin / planters / rails | Handmade warm brown; not scan wood |
| Cool gray-violet cliff | Layered torn rock | Cool purple-gray / charcoal in shadow; readable strata |
| Horizon glow | Distant atmosphere | Soft cyan/blue into peach at curved world edge |
| Spirit hurt | Spirit overlay (hurt) | Cooler, thinner unlit cue — readable wound, not horror gore |
| Spirit healed | Spirit overlay (healed) | Softer warmer / clearer unlit resolve — hopeful, handmade |

**Do:** high silhouette contrast; warm windows punch against cool night; saturated but soft PBR.  
**Don’t:** desaturate into grimdark; bleach moon to white; kill window emissive; muddy day grade.

---

## 2. Shape language

| Element | Rule |
|---|---|
| Cliff / island | **Layered torn earth** — blocky staggered strata, jagged underside. Separate top plate from cliff face in kit thinking. |
| Island silhouette | Never pancake disc or cylinder plug. Edge must read as broken earth. |
| Pines | **Stylized pines only** — conical, slightly fluffy, clear tiered foliage cards. No second tree species. |
| Cabin | Simple rustic log / gabled handmade form; stone foundation ok; cozy, not ornate Victorian or sci-fi prefab. |
| Family / figures | Clean dark **readable silhouettes** (adult + two children at lookout edge in Shot 1). |
| Floating islets | Small jagged rock crumbs with same pine language; transit crumbs, not new biomes. |
| Planet below | Curved livable world: pine valley, winding path, 2–3 hamlet roof silhouettes, distant snow peak. |
| Shrine / portal | Soft handmade spirit cue; not tech gate, neon ring, or dungeon mouth. |

Readable silhouettes beat detail. If a mass fails the thumbnail test, fix the mass before adding props.

---

## 3. Lighting rules — Day vs Night / NightMix

Night is a **parameter + overlay**, not a second map or rebuilt geometry.

### Night (Homestead_Night / spirit-capable)

- **Key:** huge warm moon — soft top/side cool-neutral fill and rim.
- **Accent:** cabin window emissive (amber) lighting porch / nearby fence / planters.
- **Fill:** cool forest / cliff; shadows stay deep **blue–purple**, never pure black.
- **Sky:** navy + stars + peach clouds + distant snow peak readable.
- **Spirit layer:** soft unlit / emissive cue via `M_SpiritUnlit` (+ NightMix). Hopeful, not horror.
- **NightMix intent:** `NightMix` 0→1 shifts masters toward cool night overlay while preserving base identity. Driven later by GameState time float; do not invent per-mesh night duplicates.

### Day (Planet_Day / landing clearing)

- Hopeful clear daylight; readable open ground at landing circle.
- Same pine / grass / rock / path language as homestead.
- Optional homestead cliff/sky hint above to keep “same world below the lookout.”
- Reject grim overcast that kills hopeful day read; reject muddy day grade.

### Shared

- Two MVP lighting presets: **Homestead_Night**, **Planet_Day** (optional Planet_Night_Spirit).
- Warm-vs-cool contrast must survive on night shots (1, 2, 5) and remain coherent on glide (3).
- Moon size is a **feature**, not a decoration.

---

## 4. Shots 1–5 — approval criteria

Approve only against `Docs/00_SHOTLIST.md` + key art. Exactly five shots; do not invent a sixth framing as a new location.

| Shot | Pass when | Fail when |
|---|---|---|
| **1 Homestead night lookout** | Key-art match: cabin left warm windows; garden + path; adult + two kids at right cliff; huge warm moon; navy sky; peach clouds; snow peak; layered torn cliff; planet pine valley + path + 2–3 rooftops; islets; warm vs cool | Photoreal/muddy/grim/sci-fi; extra tree species; tiny white moon; dark windows; pancake/cylinder; family unreadable; planet missing path/rooftops/valley |
| **2 Cabin + garden close** | Warm glowing windows; raised planters with colorful plant read; stone/dirt path; night cool fill vs warm emissive | Dark/dead windows; muddy/grim light; photoreal wood; extra biome props; drift into Shot 1 moon-hero wide |
| **3 Glide departure** | Lookout edge as departure; glide/scripted path toward planet; islets along transit; valley still readable; same pine language | Free-flight sim/HUD; new transit biome or sci-fi vehicle; pancake edge; loss of warm-vs-cool if night; extra trees |
| **4 Planet landing clearing, day** | Day landing circle; matching pines; path continuity into slice; open hopeful ground | Different biome; photoreal/muddy day; sci-fi pad; grimdark overcast; extra beast/combat staging |
| **5 Spirit portal arrival, night** | Night + spirit layer; shrine link island ↔ planet; same masters/pines; soft emissive spirit cue | Sci-fi portal/hard neon; grimdark void; photoreal/muddy night; new location/biome; combat/free-flight framing |

**Global style rejects (all shots):** photoreal scans; muddy palettes; grimdark; sci-fi; extra tree species; tiny white moon; dark cabin windows; pancake/cylinder islands.

---

## 5. Hard rejects (art)

From canon + shot lock — AD rejects on sight:

- Photoreal scans / Quixel-style bark and rock
- Grimdark, horror void, muddy desaturated grades
- Sci-fi kits, neon tech portals, free-flight sim framing
- Pancake or cylinder islands
- Tiny white moons
- Dark / dead cabin windows at night
- Extra biomes or tree species beyond stylized pines
- Extra beasts, combat staging, crafting spectacle sets
- New locations or flavor props not in homestead / planet canon kit
- One-off shader families outside the ten masters
- Rebuild geometry just to “do night”

---

## 6. Naming reminders (meshes / materials)

Prefixes: `M_` `SM_` `SK_` `FX_` `PCG_` `BP_` `CAM_` `LIT_`  
Suffixes: `_Day` `_Night` `_Spirit` `_Nurtured` `_World` `_Stored`

**Ten masters only** (instance; do not invent families):

1. `M_StylizedGrass`  
2. `M_CliffRock`  
3. `M_WoodCabin`  
4. `M_WoodWild`  
5. `M_FoliageCard`  
6. `M_PathStone`  
7. `M_GatherHerb`  
8. `M_BeastStylized`  
9. `M_SpiritUnlit`  
10. `M_Nurtured`

Each exposes: BaseColor, Roughness, Variation, NightMix 0–1, optional Emissive.  
Scale: meters; adult 1.8 m; cabin 5–6 m; island 18–24 m; pines 6–12 m. Origins at ground contact; apply scale.

AD does not author the material sheet — TA owns parameter ranges and NightMix demo notes.

---

## 7. Scope fence — no new locations or props

Allowed masses and props are those already implied by canon topology and kit lists only:

- Hero island: cabin, garden/planters, path, pines, lookout, shrine, glider perch, fence  
- Transit: air current / islets / glide line (scripted stand-in ok)  
- Planet slice: forest path, gather nodes, one beast pad, one spirit-wound site, landing circle, return shrine, 2–3 hamlet roof silhouettes  

Do **not** add: extra rooms, new biomes, alien flora, sci-fi vehicles, combat sets, dungeon portals, or flavor props outside the kit. If it is not required by the eight MVP verbs or Shots 1–5, it is out.

---

## 8. Downstream consumers

| Role | Use this bible for |
|---|---|
| TA | Chip targets + NightMix intent while authoring 10 masters (sheet is theirs) |
| ENV-H / ENV-P / PROP | Silhouette + pine + cliff rules; cite a master per mesh |
| LIT | Day/night presets; moon size; warm windows vs cool fill |
| QA | Shot 1–5 pass/fail against this doc + shotlist + key art |

**Evidence / lock:** Palette, shape, lighting, shot gates, rejects, and naming frozen for WAVE 1 Track C art half. Date 2026-09-16. ID `P2_AD_bible`.
