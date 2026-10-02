# HOMEWORLD MVP — AGENT SWARM KICKOFF BRIEF

**Document type:** Master canon (what we are building)  
**Runtime:** `homeworld_swarm/SWARM_OPS.md` (how the swarm runs)  
**Owner:** Lead (human) + Swarm Conductor agent  
**Quality bar:** Senior specialists only. No junior filler. No “nice to have” scope.

Conductor: this file is canon. Do not run a free-for-all chat. Execute waves from `homeworld_swarm/packets/`. Copy `homeworld_swarm/agents/*.md` into `.cursor/agents/`. Update `homeworld_swarm/PHASE_BOARD.md`. Require `HANDOFF_TEMPLATE.md` on every task.  
**Art north star:** Cozy stylized floating-island homestead at night (key art: cabin, garden beds, pines, family lookout, huge warm moon, cliff drop revealing a livable planet below).  
**Engine path:** Blender first (lookdev, modular kits, material library, Cursor MCP). Unreal Engine 5 is the intended realtime target after the vertical slice art language is locked.  
**Product:** Wholesome family-friendly co-op ARPG survival. Homestead hub in the sky. Planet below is the explorable world.

---

## 0. CONDUCTOR INSTRUCTIONS (READ FIRST)

You are the **Swarm Conductor / Staff Engineer**. You do not do all the work. You:

1. Lock canon (this document).  
2. Spawn **one specialist per role** with a sliced brief.  
3. Forbid a specialist from inventing systems outside their role.  
4. Require artifacts, naming, and Done Criteria before a phase can close.  
5. Merge work in the order of phases. Never start Phase N+1 if Phase N exit criteria failed.  
6. Reject photoreal scans, generic sci-fi kits, grimdark tone, and open-world bloat.  
7. Prefer reusable library assets over one-off hero meshes.  
8. If flight is too large, ship **scripted glide down + shrine portal both ways** rather than slip the date.

Every spawned agent must receive:

- This canon section  
- Their role card  
- Their phase  
- Inputs they may read  
- Outputs they must write  
- Explicit **out of scope**

Tone of world: warm, readable, handmade, hopeful. Not cutesy-infantile. Not grim. Family can stand at the lookout and the world still feels safe enough to return to.

---

## 1. CANON — DO NOT RENEGOTIATE MID-SWARM

### 1.1 Fantasy loop

| Time | Form | Where | Verbs |
|---|---|---|---|
| Day | Body | Planet slice + travel off island | Walk, gather, tame, scout, glide/fly down |
| Night | Spirit | Homestead first, then planet via portal | Heal spirits, nurture materials/crops, shrine-travel |

Homestead is the hub. The planet below is a **playable slice of the same world**, not a different game.

### 1.2 Map topology (MVP)

```
MOON / SKY
    HUGE warm-yellow moon, stars, soft peach clouds, distant snow peak
HERO ISLAND (hub)
    Cabin, garden, path, pines, lookout, shrine, glider perch
    Family-scale space, walkable, night-readable
TRANSIT LAYER
    Physical: constrained flight / air-current / islet stepping from lookout → landing circle
    Spirit: shrine portal homestead ↔ planet shrine
PLANET SLICE (visible from lookout)
    Pine forest path, gather nodes, one beast habitat,
    one spirit-wound site, landing circle, return shrine,
    2–3 rooftops / hamlet silhouette so the key art remains true
```

The cliff in the key art **is the level diagram**. If a player cannot stand at the lookout and point to landing, portal exit, first harvest, and way home, the map has failed.

### 1.3 Traversal rules (MVP)

- **Body / day:** flying is a *route*, not an open flight sim. Preferred: tamed glider-beast **or** lookout air-current along visible floating islets to a marked clearing.  
- **Spirit / night:** shrine-to-shrine portal only. Same two places. No third map.  
- Flight at night is OUT of MVP.  
- Acceptable fallback: one-way scripted glide down + portal both ways.

### 1.4 MVP verbs only

1. Walk homestead  
2. Glide/fly island → planet (or scripted stand-in)  
3. Gather 6 resources  
4. Encounter / tame 1 beast  
5. Portal night island ↔ planet  
6. Heal 3 spirits  
7. Nurture 2 things at home (crop + stored material)  
8. Return, sleep / dawn cycle

If a task does not serve one of those verbs, it is not MVP.

### 1.5 Resource set (locked)

Each gatherable has **World** and **Stored** meshes.

| ID | Resource | World | Stored / nurtured |
|---|---|---|---|
| RES_WOOD | Wood | branch, choppable pine interaction | firewood / plank bundle |
| RES_FIBER | Fiber | fern / vine / flax | cord |
| RES_STONE | Stone | loose rock | path stone / tool head |
| RES_BERRY | Forage fruit | berry bush | bowl / drying rack |
| RES_HERB | Herb | herb cluster | poultice bundle |
| RES_SEED | Spirit seed | faint plant (rare by day) | nurtured night crop |

### 1.6 Scale, units, naming

- Units: meters. Adult 1.8 m. Cabin ~5–6 m wide. Hero island 18–24 m across. Pines 6–12 m.  
- Origins at ground contact or snap point. Apply scale.  
- Prefixes: `M_` material, `SM_` static, `SK_` skeletal, `FX_` vfx, `PCG_` scatter, `BP_` / `ACT_` gameplay, `CAM_`, `LIT_`  
- Suffixes: `_Day` `_Night` `_Spirit` `_Nurtured` `_World` `_Stored`  
- Collections / folders:

```
Lib/00_Core
Lib/01_Homestead
Lib/02_Forest
Lib/03_Gatherables
Lib/04_Beasts
Lib/05_Spirits
Lib/06_Materials_Master
Lib/07_Night_SpiritLayer
Lib/08_Transit
Maps/Preview_Homestead_Night
Maps/Preview_Forest_Day
Maps/Preview_Lookout_To_Planet
Docs/
```

### 1.7 Art language (locked)

- Stylized soft PBR. Saturated spring greens. Warm dark wood. Cool gray-violet cliff.  
- Huge warm moon `#FFD56A`–`#FFE28A`. Cabin windows emissive 2700–3200K.  
- Pines conical and slightly fluffy, not photoreal Quixel.  
- Island is layered torn earth, not a pancake or cylinder.  
- Night = cool forest + warm cabin + spirit overlay. Do not rebuild geometry for night.  
- Same masters on island and planet. New shader families are a defect.

### 1.8 Master materials (locked list)

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

Each master exposes: BaseColor, Roughness, Variation, `NightMix` 0–1, optional Emissive. Variants are instances.

### 1.9 Quality bar

A deliverable is rejected if:

- Moon is small or cold white  
- Cabin windows are dark  
- Island silhouette is a disc  
- Pines look scanned or lollipop  
- Planet slice not readable from lookout  
- Unique one-off shaders appear  
- Photoreal / grim / sci-fi drift  
- Flight is unbounded  
- Scope includes extra biomes, extra beasts, combat systems, multiplayer netcode, or inventory-crafting trees beyond the 6 resources  

---

## 2. TEAM ROSTER

Spawn these agents. Do not collapse roles unless a human explicitly cuts staff.

| ID | Role | Senior specialty | Primary phases |
|---|---|---|---|
| CND | Swarm Conductor | Staff eng, integration, no-scope-creep | All |
| DES | Game Designer | Systems, loop, player verbs | 0–1, 5, 7 |
| WLD | World / Level Designer | Blockout, traversal, composition | 1–2, 4, 6 |
| AD | Art Director | Style lock, reviews, shot list | 0–2, 6–7 |
| TA | Technical Artist | Master materials, naming, export | 2, 6 |
| ENV-H | Environment Artist — Homestead | Modular cabin, island, garden | 3 |
| ENV-P | Environment Artist — Planet | Forest slice, hamlet silhouette | 4 |
| PROP | Prop / Kit Artist | Gatherables, shrine, path, planters | 3–5 |
| CHA | Creature / Spirit Artist | Beast placeholder, wisps, family blockouts | 5 |
| LIT | Lighting / Atmosphere | Day/night presets, moon, volumes | 3–4, 6 |
| GP | Gameplay Programmer | Move, glide, portal, day/night form | 5–6 |
| SYS | Systems Programmer | Gather, inventory-lite, tame, heal, nurture | 5–6 |
| INT | Integration Engineer | Blender↔UE path, scenes, packaging | 6–7 |
| QA | Playtest / QA Lead | Criteria, shot tests, verb checklist | 6–7 |

**Human Lead** approves phase exits. Conductor may not close a phase without the artifact list below.

---

## 3. PHASES

### PHASE 0 — Canon freeze (half day)

**Who:** CND, DES, AD  
**Goal:** Everyone builds the same game.

**Work**
- Confirm this brief as source of truth.  
- Write `Docs/00_CANON.md` (copy of locked lists only, no essays).  
- Write `Docs/00_SHOTLIST.md`:  
  1. Homestead night lookout (key-art match)  
  2. Cabin garden close  
  3. Glide departure  
  4. Planet landing clearing day  
  5. Spirit portal arrival night  
- Folder skeleton created in the Blender file and/or repo.

**Exit**
- [ ] Naming, scale, materials, verbs, map topology agreed in writing  
- [ ] Shot list exists  
- [ ] No open “what if we also…” items inside MVP

---

### PHASE 1 — GDD slice + graybox map (1 day)

**Who:** DES, WLD, CND  
**Goal:** Playable space exists as primitives before pretty art.

**DES outputs**
- `Docs/01_GDD_MVP.md`  
  - Day loop (leave, gather, encounter beast, return)  
  - Night loop (spirit form, portal, heal 3, nurture 2, return)  
  - Form swap rules  
  - Fail states: none lethal for MVP; get lost / miss landing / miss shrine only  
- Interaction list per object (use, hold, store, nurture, heal)

**WLD outputs**
- Graybox in Blender (or UE blockout if engine already chosen):  
  - Island top + cliff massing  
  - Cabin footprint  
  - Lookout + perch  
  - Two shrine volumes  
  - Two landing circles  
  - Glide spline / islet crumbs  
  - Planet path ~2–4 minutes walk  
  - Beast pad, spirit-wound pad, hamlet cards  
- `CAM_Hero` framed to Shot 1 from the lookout

**Exit**
- [ ] From lookout camera, landing + roofs + path are visible  
- [ ] Walk distances written (seconds)  
- [ ] Glide path does not require full flight controller  

---

### PHASE 2 — Material library + art bible (1 day)

**Who:** AD, TA  
**Goal:** Ten masters exist. Nobody makes random shaders after this.

**AD outputs**
- `Docs/02_ART_BIBLE.md`: palette, silhouette rules, do/don’t refs from key art  
- Approved color chips for grass, wood, cliff, moon, spirit hurt/healed

**TA outputs**
- Node-group masters for all 10 materials  
- Instances: grass dry/lush, wood painted/raw, spirit hurt/healed, nurtured on/off  
- `Docs/02_MATERIAL_SHEET.md` — parameter names and intended ranges  
- Export notes: meters, -Y forward / Z up or UE FBX preset

**Exit**
- [ ] Every later mesh must cite a master on the sheet  
- [ ] NightMix demonstrated on a sphere row  

---

### PHASE 3 — Homestead kit + night preview (2 days)

**Who:** ENV-H, PROP, LIT, TA  
**Goal:** The key-art hub is a reusable kit, not a diorama.

**ENV-H**
- `SM_IslandTop`, `SM_Cliff` (separate)  
- Modular cabin: wall, roof, chimney, door, window, porch rail  
- Lookout + glider perch  
- 5–8 pine instances using library foliage  

**PROP**
- Planter box ×2–3, dirt, crop proxies  
- Path stone 3-pack  
- Lantern, drying rack, workbench  
- `SM_Shrine_Homestead` with portal socket  
- `SM_LandingCircle` (shared mesh)

**LIT**
- Night preset: huge moon disc + `LIT_Moon` + window emissives + volume haze  
- `CAM_Hero` matches Shot 1

**Exit**
- [ ] Preview_Homestead_Night reads as the key art  
- [ ] Cabin windows bloom  
- [ ] Cliff is layered  
- [ ] All objects named and collected under Lib/01 and Lib/08  

---

### PHASE 4 — Planet slice + transit (2 days)

**Who:** ENV-P, WLD, PROP, LIT  
**Goal:** The world below is playable and recognizable from the island.

**ENV-P**
- Reuse pine / rock / grass / path masters only  
- Forest corridor, stump, log, moss, fern  
- Hamlet silhouette 2–3 roofs  
- `SM_Shrine_Planet`, second `SM_LandingCircle`  
- `SM_SpiritWound` placeholder site  

**WLD**
- Place gather nodes, beast pad, wound site  
- Glide spline + 3–5 crumb islets  
- Keep the lower world in the lookout frustum  

**LIT**
- Day preset for planet (clearer, greener, less bloom)  
- Night spirit wash for planet (cooler, shrine glow)  
- Haze so the drop-off still feels high  

**Exit**
- [ ] Shot 3 and Shot 4 exist  
- [ ] Same materials as homestead  
- [ ] Player can mentally fly the route from still frames  

---

### PHASE 5 — Life, verbs, placeholders (2 days)

**Who:** CHA, PROP, DES, GP, SYS  
**Goal:** The loop can be acted, even if art is blocky.

**CHA**
- Family blockouts (adult + 2 children) at lookout — silhouettes only  
- One small quadruped `SK_Beast_Small` with tame-mark slot  
- Spirit wisps: hurt, healed  
- Optional glider mesh or saddle socket on beast  

**PROP**
- All 6 gatherables World + Stored  
- Nurture glow card for planters and stored goods  

**DES**
- Tune interact distances, gather counts, tame steps (max 3 actions), heal steps (max 2 actions)

**GP (prototype in Blender logic notes + later UE/Godot/whatever the stack is)**
- Body walk  
- Form swap at shrine or dusk  
- Scripted glide along spline  
- Portal trigger shrine A ↔ shrine B  
- Day/night toggle that only flips lights + NightMix + spirit layer visibility  

**SYS**
- Inventory-lite: 6 slots, stack numbers  
- Gather → Stored at homestead  
- Tame state machine: wild / cautious / tamed / helper  
- Heal: hurt wisp → healed  
- Nurture: two homestead targets gain `M_Nurtured`  

**Exit**
- [ ] Verb checklist can be executed on graybox + kits  
- [ ] No crafting tree, no combat system, no extra fauna  

---

### PHASE 6 — Vertical slice integration (2 days)

**Who:** INT, CND, LIT, TA, QA  
**Goal:** One continuous experience.

**Path A (Blender-first lookdev):** animated camera reel through Shots 1–5 + object library file.  
**Path B (if UE project exists):** import kits, Landscape or static island, spline glide, shrine portals, Lumen night, foliage paint.

**INT**
- Export table: mesh → collection → target folder  
- Collision proxies  
- Two levels or one streamed two-elevation level  
- Save `Maps/VS_MVP`  

**QA first pass**
- Run Section 5 checklist on the integrated build  

**Exit**
- [ ] Player (or camera) can leave island, reach planet, return by portal  
- [ ] Night homestead still matches key art  
- [ ] Library remains instance-based  

---

### PHASE 7 — Playtest polish gate (1 day)

**Who:** QA, AD, DES, CND  
**Goal:** Ship or cut.

**QA script**
1. Stand lookout. Name the four points (land, portal, harvest, home).  
2. Day: glide down, gather each resource once, meet beast, portal or climb-via-portal home.  
3. Night: spirit form, portal down, heal 3, portal up, nurture 2.  
4. Screenshot Shots 1–5. Compare to key art.  

**Cut list if over time**
- Free flight → spline only  
- Tame → encounter + “friend” flag  
- Hamlet interiors → silhouettes only  
- Extra islets → 3 crumbs max  

**Exit**
- [ ] Lead signs `Docs/07_VERTICAL_SLICE_SIGN OFF.md`  
- [ ] Known issues list only; no new features  

---

## 4. ROLE CARDS (PASTE INTO EACH AGENT)

### CND — Swarm Conductor
You assign work, review diffs against canon, and block scope. You merge collections and keep the file clean. You never add a biome. You write the daily integration note.

### DES — Game Designer
You own verbs, timing, and player teaching. You do not model. You write tables other agents implement. You cut features that do not serve the 8 MVP verbs.

### WLD — World Designer
You own massing, sightlines, and travel time. The lookout composition is your religion. You place volumes, not hero sculptures.

### AD — Art Director
You reject photoreal, muddy palettes, and off-model pines. You approve shots. You do not add props for flavor if they are not in the kit list.

### TA — Technical Artist
You own the 10 masters, naming, LODs, and export sanity. If someone makes a unique shader, you delete it and instance a master.

### ENV-H — Homestead Environment
You build the island, cliff, cabin kit, garden blocking, pines around the cabin. Beauty is secondary to modular reuse.

### ENV-P — Planet Environment
You build only what is visible from the lookout plus a 2–4 minute path. Same kit language. No new tree species.

### PROP — Props
You build kits that gameplay hooks onto: shrine sockets, landing circles, World/Stored gatherables, planters.

### CHA — Creatures / Spirits
Placeholders first. Readable silhouettes. Tame-mark slot. Hurt vs healed spirit is a material state, not a new mesh family if avoidable.

### LIT — Lighting
Two presets only for MVP: Homestead_Night, Planet_Day. Optional Planet_Night_Spirit. Moon size is a feature, not a decoration.

### GP — Gameplay Programmer
Movement, form, spline glide, portal, time-of-day toggle. No combat. No animation graph perfection.

### SYS — Systems Programmer
Six resources, four beast states, heal, nurture. Data-driven tables. No crafting web.

### INT — Integration
You make the slice runnable and the library portable to UE5. You document the export.

### QA — Quality
You are not a cheerleader. You run the script and file defects against canon.

---

## 5. PER-AGENT TASK PROMPT TEMPLATE

Copy this when spawning an agent:

```text
You are {ROLE} on HOMEWORLD MVP. Senior bar only.

CANON is attached. Do not renegotiate map topology, verbs, materials, or tone.

PHASE: {N NAME}
YOUR ONLY OUTPUTS: {list}
OUT OF SCOPE: anything not in that list. Especially extra biomes, extra beasts, free flight, combat, photoreal materials.

CONSTRAINTS
- Meters, applied scale, named using the prefix table
- Instance the 10 masters; no one-off shaders
- Stylized cozy PBR matching the floating-island night key art
- Planet below is the same world; keep it visible from the lookout

PROCESS
1. Read canon + any input artifacts listed
2. Build only your outputs
3. Write a short changelog: files, object names, material used
4. List blockers. Do not silently invent a solution that changes design

DONE when every output exists and the phase exit boxes you own can be checked.
```

---

## 6. HOW TO START THE SWARM

Do not paste this whole brief into every agent.

1. Copy `homeworld_swarm/` into the project as `swarm/`.
2. Copy `swarm/agents/*.md` into `.cursor/agents/`.
3. Open a Conductor chat with `swarm/agents/conductor.md` + `swarm/SWARM_OPS.md`.
4. Paste **one wave packet at a time**, starting with `swarm/packets/WAVE_0_CANON.md`.
5. Conductor updates `swarm/PHASE_BOARD.md` and collects `Docs/handoffs/`.

Wave map:

| Packet | After gate | Spawns |
|---|---|---|
| WAVE_0_CANON | — | DES, AD, CND folders |
| WAVE_1_PARALLEL | P0 | DES, WLD, AD+TA |
| WAVE_2_HOMESTEAD | P1+P2 | ENV-H, PROP, LIT |
| WAVE_3_PLANET | P3 | ENV-P, WLD, LIT |
| WAVE_4_VERBS | P4 | CHA, PROP, GP, SYS |
| WAVE_5_SLICE | P5 | INT, QA |

Role cards in §4 stay as canon summaries. Executable prompts are the files in `swarm/agents/`.  

---

## 7. BLENDER MCP ADDENDUM (FOR ART AGENTS)

When an agent is driving Blender via Cursor MCP:

- Eevee lookdev. Bloom, AO, volumetrics on.  
- Collections exactly as in §1.6.  
- Separate `SM_IslandTop` and `SM_Cliff`.  
- Moon is a large emissive disc plus a directional/area key.  
- Preview cameras: `CAM_Hero`, `CAM_CabinGarden`, `CAM_GlideStart`, `CAM_LandingDay`, `CAM_PortalNight`.  
- Save `floating_island_homestead_LIB.blend`.  
- Do not install paid add-ons.

---

## 8. UNREAL HANDOFF (PHASE 6 PATH B)

If / when UE5 is the runtime:

- Lumen + Nanite + VSM  
- Ultra Dynamic Sky or equivalent for oversized warm moon  
- Foliage tool for pines on planet slice  
- Landing circles and shrines as Blueprints with overlap  
- Glide = spline component + simple launch, not full flight movement  
- NightMix driven by a GameState time float  
- Same names as Blender

Do not start UE environment dressing until Phase 2 masters and Phase 3 cabin kit exist.

---

## 9. DEFINITION OF MVP DONE

The swarm is finished when a player or a camera reel can:

1. Wake on the island that looks like the key art.  
2. See the planet below and understand both routes.  
3. Travel down by body (glide/fly route).  
4. Gather the six materials and meet one beast.  
5. Return / go down at night as spirit through the shrine.  
6. Heal three spirits and nurture two homestead things.  
7. Stand at the lookout again. The house is still home.

Anything past that is a later season.

---

## 10. CONDUCTOR CLOSING LINE TO THE SWARM

Build a library and a loop, not a trailer that cannot be played. The island is the sentence. The planet is the paragraph. Do not write the book in MVP.
