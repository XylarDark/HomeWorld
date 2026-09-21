# Docs/GATHER_CRAFT_BIBLE.md

**Status:** LOCKED (Lead locks 2026-09-21 ET — A1/B1/C1/D1)  
**Pointers:** `Docs/HOMESTEAD_BIBLE.md`, `Docs/DAYNIGHT_BIBLE.md`, `Docs/MOVEMENT_BIBLE.md`, `Docs/21_REAP_SOW.md`, `Docs/canon/SCHEMA.md`, `Docs/canon/VERBS.md`, `Docs/canon/DO_NOT.md`

---

HOMEWORLD GATHER & CRAFT BIBLE — PLANET REAP, HEARTH SPEND

## One-line lock

Gather six `RES_*` on the planet (flint/grass = **display flavor** for `RES_STONE` / `RES_FIBER`), store at home, craft **named recipes** at campfire then cottage stations; demo spine is **campfire/tent → cottage**; shops and upgrade tracks are **placeholders NOW**, full investment buildings **LATER** — never a crafting skill-tree web or 7th resource.

## Taste

- **Start on the island** after collecting wood, flint-flavor stone, and grass-flavor fiber — hearth fantasy before full cottage.
- **Day/night collection loop** feeds the demo spine; bring planet gifts home → store → spend at hearth stations.
- Upgrade tracks read as **hub places + spend unlocks**, not a generic MMO crafting web.
- Foreshadow warmth: woodshop / textile / research silhouettes; cottage rooms (kitchen, bedrooms, living room cauldron) as **readable placeholders** until functional magic/cooking LATER.

## Ownership (hard)

| Owner | Rule |
|---|---|
| **SCHEMA.md** | Exactly six `RES_*`; recipe cost rows; flint/grass display aliases |
| **HOMESTEAD_BIBLE** | Named recipes only; no weapon smithing; hub safe |
| **Docs/21** | Den / camp / special sites — dream-convert & reap/sow bonuses; **not** primary RES miners |
| **DAYNIGHT_BIBLE** | Tent + campfire = valid campsite sleep path |
| **03_SYSTEMS_MVP** | Long tables unchanged — this bible **adds** craft spend rows; do not rewrite §3 wholesale |
| **This bible** | Site→RES day gather, demo progression, placeholder buildings, craft UX stations |

---

## NOW (MVP / demo spine)

### Day gather — planet sites → `RES_*`

| Site kind (Docs/21 ID) | Yields (day / body) | Display / flavor copy |
|---|---|---|
| `trees` | +1 `RES_WOOD` | Wood |
| `rocks` | +1 `RES_STONE` | **Flint** (flavor label for stone) |
| `flowers` | +1 `RES_FIBER` and/or rotate +1 `RES_HERB` | **Grass** (flavor label for fiber) |
| Berry nodes (World gather) | +1 `RES_BERRY` | Berry |
| Seed pods (World gather) | +1 `RES_SEED` | Spirit seed |
| `animal_den` / `humanoid_camp` / `special` | Per **Docs/21** (reap/sow, dream-convert) | Not primary six-RES miners |

Gather logs remain `GATHER: RES_* +N`. Fail rules: day/body only; stack max 9; six slots — per `SCHEMA.md`.

### Store → spend order

| Rule | Spec |
|---|---|
| Default spend source | **Stored count first**, then player inventory (same `RES_ID`) |
| NOTE | **Lead-swappable** — if implementation only has inventory spend today, log `CRAFT: spend inventory-only TODO` until Stored-first wired |

### Named recipes (cost rows — schema before code)

Craft at **campfire** until cottage kitchen/stations unlock (`D1`). Outputs are placeables or consumables per `HOMESTEAD_BIBLE` — not gear trees.

| Recipe ID | Output | Cost | Station (NOW) |
|---|---|---|---|
| `RECIPE_CAMPFIRE` | Campfire placeable | 1× `RES_WOOD` + 1× `RES_STONE` + 1× `RES_FIBER` | Campfire craft point (planet or hub stub) |
| `RECIPE_TENT` | Tent placeable | 3× `RES_WOOD` + 2× `RES_FIBER` | Campfire (after campfire placed) |
| `RECIPE_TORCH` | Torch consumable | 1× `RES_WOOD` + 1× `RES_FIBER` | Campfire |
| `RECIPE_TAME_BAIT` | Taming consumable | 1× `RES_BERRY` **or** 1× `RES_HERB` | Campfire |
| `RECIPE_HEAL_SALVE` | Healing consumable | 1× `RES_HERB` **or** 1× `RES_SEED` | Campfire |
| `RECIPE_FISH_GEAR` | Fish bait / gear | 1× `RES_FIBER` + 1× `RES_BERRY` | Campfire |

**Demo progression (only these spends unlock structure NOW — C1):**

1. Gather → craft **campfire** (`RECIPE_CAMPFIRE`).
2. Gather → craft / place **tent** (`RECIPE_TENT`) — valid campsite (`DAYNIGHT_BIBLE`).
3. Continue day/night loop → **cottage unlock** at campfire: set progression flag + log `PROGRESS:COTTAGE_UNLOCK` (additional RES sink beyond B1 rows = **same loop**, no shop spends).

Shops and upgrade tracks below: **enter volumes + props + logs only** — **no RES spend**, not functional craft.

### Craft UX (D1)

| Phase | Where player crafts |
|---|---|
| Early demo | **Campfire** interact — all named recipes above |
| After `PROGRESS:COTTAGE_UNLOCK` | **Cottage kitchen** (+ future station props) — same recipe IDs; re-bind interact to kitchen mesh when placed |

Iso/build camera when placing tent/campfire if already wired (`CAMERA_BIBLE`).

### Placeholder buildings & rooms (C1 — foreshadow only)

| Placeholder | NOW behavior | LATER track |
|---|---|---|
| Woodshop | Prop + enter volume → log `PLACEHOLDER:WOODSHOP enter` | Main home / buildings craft |
| Textile shop | Prop + volume → log `PLACEHOLDER:TEXTILE enter` | Textile / fiber upgrades |
| Research shop | Prop + volume → log `PLACEHOLDER:RESEARCH enter` | Research unlocks |
| Cottage — kitchen | Room volume after unlock → log `PLACEHOLDER:COTTAGE_KITCHEN` | Cooking station craft |
| Cottage — bedrooms | Room volume → log `PLACEHOLDER:COTTAGE_BEDROOM` | Spirit/body rest buffs (fantasy) |
| Cottage — living room | Cauldron prop (non-functional) → log `PLACEHOLDER:CAULDRON` | Spells / buffs / potions |

### Upgrade tracks (LATER — locations + full buildings)

Each track gets **authored locations** and spend unlocks later — **not** a shared skill-tree web:

Main home/buildings · research · magic/spells · spirit · body · combat · cooking · fishing · potions.

**COMBAT track building** still obeys `COMBAT_DREAM_BIBLE` (rare boss seal — not trash combat). **Living-room cauldron** = placeholder prop NOW; functional magic LATER.

---

## LATER (do not implement without Lead track)

- Functional woodshop / textile / research crafting loops  
- Full cottage room gameplay (buffs, spells, potions, cooking minigames)  
- Per-track investment buildings with RES sinks beyond named demo list  
- Generic crafting skill tree or recipe discovery web  
- Weapon / armor smithing  
- Seventh resource or equipment slots  

---

## Explicit do-not

- Crafting skill-tree web or infinite recipe pages  
- 7th `RES_*` or equipment grid  
- Weapon smithing / combat gear craft on hub  
- Functional shop craft spending RES in NOW (placeholders only)  
- Replacing Docs/21 den/camp/special with primary ore-miner fantasy  
- Inventing recipe costs outside `SCHEMA.md` / this bible / Lead `DECISIONS.md` append  

## Engine note (UE5)

Read existing gather (`GATHER:`), store (`STORE:`), and inventory subsystem before adding craft. Craft success logs: `CRAFT: RECIPE_* ok` (or project-standard tag). Placeables: idempotent spawn/check-before-create. Campfire-first interact; cottage kitchen rebind after `PROGRESS:COTTAGE_UNLOCK`. Stored-first spend helper shared with tame/heal/nurture spend paths when possible.

## Done-when (playable test)

- Gather `RES_WOOD` + `RES_STONE` + `RES_FIBER` with correct site mapping (flint/grass copy optional in UI only)  
- Craft campfire stub (`CRAFT:` + placed or logged prop)  
- Craft / place tent stub  
- `PROGRESS:COTTAGE_UNLOCK` flag or log after demo loop  
- Enter placeholder shop/room volumes → placeholder logs  
- Six `RES_*` only; no weapon smithing  
