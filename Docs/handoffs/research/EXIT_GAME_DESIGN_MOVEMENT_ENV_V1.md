# EXIT GAME_DESIGN_MOVEMENT_ENV_V1

**Kind:** RESEARCH EXIT — GAME_DESIGN_MOVEMENT_ENV_V1

**File protocol:** Lead / Conductor paste. Canonical intended path: `Docs/handoffs/research/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md`  
**Prompt:** `PROMPT_GAME_DESIGN_MOVEMENT_ENV_V1`  
**Date:** 2026-09-27  
**Pins:** DET `0a27306` · HW tip context `f72d5d8` (math-first prop schemas on main) · CAP **PARKED**  
**Scope floor:** Interview `PROTOTYPE_T0_V1` + `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` (MUST beats unchanged)  
**Parallel:** `#234` `PROMPT_GAME_FEEL_DESIGN_LIBRARY_V1` = general juice/feel. This EXIT = **movement systems + env layout/readability only**. Cross-link; do not require merge order.  
**Closed, cite-not-reopen:** Docs/24 MV-A traversal · Docs/30 DS-A · Movement bible LOCKED · FALLBACK FLIGHT armed.

---

## Diagnosis

HomeWorld T0 already locked the **verbs** (wake → kettle-sprint → plant → backpack → glider↔field → gather → rune → eject-not-kill → bed→spirit → nurture → portals → avoid/soothe). What is still thin is a **shared language** for whether those verbs *read* in greybox: weight vs float, intentional glide vs leftover flight, homestead path that invites plant-then-leave, camp that ejects instead of kills.

Industry practice for a **small UE prototype** is consistent and cheap:

1. **Control first, polish last.** Swink: real-time control + simulated space beat juice. Sub-100 ms response; predictable gravity/momentum; camera that tells the truth about speed.
2. **Glide is controlled fall, not flight.** BotW/TotK: height is a spendable resource; horizon is the affordance; fast-travel is the enemy of the verb. HomeWorld already CUT free-flight and ARMED fallback flight — keep that.
3. **Space teaches the verb.** Totten / Lynch: landmarks, paths, nodes, edges, districts. Greybox metrics from *player* run/glide/reach — not from pretty scale. Interactables need silhouette + consistent height + day-readable contrast; night mood is Lead taste.
4. **Iterate in blockout; instrument with times and reach, not stills.** Level Design Book / Shadow Complex / “greybox longer”: walk-scripts and second-counts before art. Maps onto HomeWorld Arrange-before-Act, gate JSON, files-only score. CAP stays PARKED.

This EXIT does **not** invent MUST beats, camera code, or a capture writer. It proposes a **pointer library** so Design/Test can write DONE-WHEN in movement/env language without loading books into seats.

**Unknown closed:** Which movement + env practices are KEEP for T0 vs CANDIDATE vs PARK, and which feel-goals are bot-proveable vs Lead-only.

---

## Decision

| Option | Verdict |
|--------|---------|
| **Go** this EXIT as a standalone pointer library | **Conditional Go** |
| Wait for `#234` EXIT first | **No** — either order is valid |
| New CAP / stills harness for movement | **No-Go** (CAP PARKED) |
| New MUST beats / camera Implement | **No-Go** this turn |

**Conditional:** Lead may ACCEPT this EXIT and open the docs bites **without** `#234`. If `#234` later lands a general feel table, this file **cites** it in one line; it does not duplicate juice (screenshake, hitstop, particles). If `#234` never lands, this table still covers glide/weight/path/readability.

**A–E:** Cite only. No new harness module. Movement prove = existing three-state + walk-script + NODE labels ⊆ inventory ∩ world.

---

## 1. Movement design canon

Pointer-only. Seats do not ingest books.

| Status | Source | Why for HomeWorld T0 (≤2 lines) |
|--------|--------|----------------------------------|
| **KEEP** | Steve Swink, *Game Feel* (2008); essay “Game Feel: The Secret Ingredient” (Gamasutra/Game Developer, 2007) | Control + simulated space + polish. Sub-~100 ms input→motion; ADSR on walk/glide accel. Use for “weight” and “not floaty” language in DONE-WHEN — not as a juice checklist. |
| **KEEP** | Nintendo / BotW GDC 2017 “Breaking Conventions”; TotK GDC 2024 physics/multiplicative design (Dohta, Takayama et al.) | Climb/glide as curiosity tools; paraglider as *fall cushion*, not aircraft. Multiplicative verbs (glide × field × eject) beat authored set-pieces. Matches seamless home↔planet MUST and CUT free-flight. |
| **KEEP** | HomeWorld Movement bible **LOCKED** + Docs/24 MV-A traversal + FALLBACK FLIGHT armed | In-repo law. Industry cites **interpret** this bible; they do not reopen it. Eject-home and fallback flight already own the “not lethal / not soft-lock mid-transit” degrade (A–E layer E). |
| **KEEP** | Camera-follow / weight essays clustered: Swink response+context; GDF “Building Character Feel” (predictable camera, no opposing-body dolly, FOV as accel tell) | T0 camera polish is Lead-later; harness only needs: camera tells travel direction; no free-fly prove cam (`PROTOTYPE_FEATURE_LIST` reject). |
| **CANDIDATE** | Martin Fasterholdt, “You say jump, I say how high?” (jump metrics thesis) + SMB physics writeups (Aldrich / Game Maker’s Toolkit *Satisfying Motion of SMB*) | Attack/sustain/release on ground speed. Useful if a later bite freezes numeric walk/sprint/glide rates. Do not load in seats until metrics bite exists. |
| **CANDIDATE** | Invisible Controls / third-person camera GDC cluster (keep as URL list in the Do file, not seats) | Follow-cam framing for glider and spirit portals. Lead taste until Movement bible says otherwise. |
| **CANDIDATE** | `#234` general feel/juice library (when ACCEPTED) | Cross-link only: particles, land-thud, tea-buff telegraph. Not movement law. |
| **PARK** | Competitive netcode / sub-frame fighting-game buffers | Wrong genre; T0 is pastoral prototype, not rollback. |
| **PARK** | Full flight-sim / aircraft energy-management texts | Conflicts with “glide = controlled fall” and CUT free-flight. |
| **PARK** | AAA animation-graph tomes as T0 Implement | Over-authored polish before verbs. Greybox capsule + simple blend is enough. |

**T0 mapping (glider, eject-home, spirit portals):**

- **Glider:** height is currency; player should feel *spend*, not hover. Destination (field mass / homestead roof) readable from launch (`NODE_GLIDER` → field AABB).  
- **Eject-home:** cartoon launch → glider → home is a **scripted degrade**, not combat win. Same path day-camp and planetside-night-without-bed.  
- **Spirit portals:** zone transition = deep module (A–E B): caller sees “enter portal,” not partition keys. Failed stream → eject/home, not hang (A–E E).

---

## 2. Environment design for verbs

| Status | Source | Why for HomeWorld T0 (≤2 lines) |
|--------|--------|----------------------------------|
| **KEEP** | Christopher W. Totten, *An Architectural Approach to Level Design* (+ lecture “Architectural theory for level designers”) | Prospect/refuge, arrivals, molecule spaces, weenies. Homestead = intimate/hub; field = prospect; camp edge = threat envelope. Works in greybox. |
| **KEEP** | Kevin Lynch, *The Image of the City* (via Totten’s sandbox chapter) | Landmarks, paths, nodes, edges, districts. T0 NODE_* inventory is already Lynch-nodes. Paths between them must be walkable without UI breadcrumbs. |
| **KEEP** | *The Level Design Book* — Blockout chapter (book.leveldesignbook.com/process/blockout) | Cheap geometry until flow/metrics pass. Playtest blockout, not the GDD. Matches greybox OK + math-first arrange. |
| **KEEP** | Don Norman affordance (conceptual): consistent interactable height, silhouette, highlight-by-shape not by night bloom | Kettle / plant-slot / backpack / rune / bed / portals must read at **day** contrast. Night readability = Lead taste, not bot PASS. |
| **CANDIDATE** | Jesse Schell, *The Art of Game Design* — Lens of Essential Experience, Spaces, Interest Curve, Curiosity | Question-lenses for “does this path invite plant-then-leave?” Do not dump 100 lenses into seats. |
| **CANDIDATE** | BotW “triangle” landmarking (Fujibayashi/Dohta GDC; Game Developer “5 design lessons”) | One occluding mass + a peek of destination. Useful for homestead→perch→field if VS_MVP has a weenie; do not rebuild the map this turn. |
| **CANDIDATE** | Christopher Alexander *A Pattern Language* (via Schell) | Thin cite: “entrance transition,” “garden growing wild.” PARK full book. |
| **PARK** | AAA biome bibles / Megascans dress as prove | Over-authored polish before verbs. Dress after walk-script. |
| **PARK** | Night-mood as env *proof* | Lead lock: bright/day for bot prove; night = Lead. |
| **PARK** | Lethal-combat cover metrics (pie-slice, engagement time) as T0 camp law | Camp = eject / avoid+soothe. Shooter timing docs mis-teach the space. |

**T0 envelopes (greybox language, no new actors required):**

| Envelope | Verb it sells | Greybox tell |
|----------|---------------|--------------|
| Homestead interior → stoop | Wake, kettle, backpack, bed | Intimate space; kettle/bed silhouette; door = arrival |
| Near-outside plant slot | Plant given herb, later nurture | Slot within short walk of stoop; not in the flight path |
| Perch / glider | Leave home on purpose | Height + view of field mass; weenie on horizon |
| Open field | Gather + rune | Prospect space; gather nodes along a path, rune as landmark before “go to bed” |
| Day camp edge | Eject-not-kill | Edge + one readable threat volume; no kill-zone metrics |
| Night camp (Lead) | Avoid 1 / soothe 2 | Same volume; lighting taste later |

---

## 3. Harness / prove practices → pointer rules

**Industry pattern:** metrics from the *body* first (run speed, glide sink rate, interact reach, camera distance) → blockout sized in those units → walk-script with second-counts → art last. Shadow Complex paper-played the whole map before greybox. Level Design Book: you cannot playtest a GDD; you can playtest a blockout.

**Do not build new CAP writers.** Map onto existing HomeWorld surfaces.

| Industry practice | HomeWorld pointer rule |
|-------------------|------------------------|
| Player metrics locked before geometry | Freeze walk/sprint/glide numbers in a **docs** metrics row when a later mechanic bite opens. Until then, prove **reachability** via existing NODE actors, not new capsules. |
| Greybox / blockout gates | `T0_GAP_INVENTORY_WALK_V1` (already the first Implement after `APPROVE-PROTOTYPE-LIST`) **is** the blockout gate. Beat present? Y/N/Partial on VS_MVP. |
| Time-to-objective (e.g. 8–12 s spawn→point in MP maps) | Optional **Lead/playtest** note: homestead stoop → plant slot; perch → field landing. Soft signal. Not a closed_fail number until Design freezes it. |
| Playtest script = intended verb sequence | Walk-script = T0 MUST order. Files-only checklist. |
| Soft vs hard fail in playtests | **soft_fail:** missing dress, TOD not day, labels ∉ inventory ∩ world, greybox unreadability Lead will polish. **closed_fail:** after Act, a MUST node absent that gap-inventory marked Present, or eject path dumps player with no home degrade. Arrange `ready:false` ≠ closed_fail. |
| Screenshot / VRT | Confirm-only after math/walk green. CAP product **PARKED**. No ImageGrab PASS. Bright/day if a still is ever taken. |
| Files-only score | `hw.test_score_packet/v1`: stamps bytes+mtime on walk-script / gate JSON. Exists-only ≠ PASS. |

**Proposed pointer rules (for the Do file, not a new module):**

1. Movement/env DONE-WHEN name **NODE_*** labels and a verb, not a camera path.  
2. “Feels floaty / looks pretty at night” is **Lead taste** — never `ok: true` from a bot.  
3. Transit prove = reached `NODE_FIELD_GATHER` from `NODE_GLIDER` without a load hang; stream failure degrades to `EJECT_HOME`.  
4. No stills Act to discover missing nodes (Arrange-before-Act).  
5. `#234` juice metrics (if any) stay off this harness until that EXIT is ACCEPTED.

**A–E (cite only):** B — transit/portal APIs hide WP; E — mid-transit failure → eject/home. No 15-q; no new boundary.

---

## 4. Vision alignment — feel goals for early testers

Tied to T0 MUST. **B** = bot-proveable (actors, logs, times, labels). **L** = Lead-only taste.

| # | Feel goal | Beat | B / L |
|---|-----------|------|-------|
| 1 | Wake reads as *start of a work day*, not a combat spawn | Wake | L (staging) + B (day start actor/log) |
| 2 | Tea sprint has a readable duration and a body that *runs heavier then lighter* | Kettle → sprint | B (buff on/off) · L (weight curve) |
| 3 | Homestead path **invites plant-then-leave** (slot visible from stoop; perch visible after plant) | Plant + glider | B (two nodes reachable in order) · L (invitation) |
| 4 | Backpack equip is a *load-up* beat, not a pause menu trap | Backpack | B (state) · L (UI feel) |
| 5 | **Glide reads as intentional fall, not floaty flight** — sink is visible; landing is a decision | Glider → field | B (left perch, arrived field AABB) · L (sink/weight) |
| 6 | Field gather is along a path, not a vacuum-cleaner radius | Gather | B (nodes exist on path) · L (scatter beauty) |
| 7 | Rune is a landmark you *notice before bed*, not a hidden switch | Rune | B (interact before bed-gate) · L (iconography) |
| 8 | Day camp threat **ejects you home**; you laugh, you do not die | Eject | B (eject path fired, player at home, not dead) · L (cartoon timing) |
| 9 | Night home without bed = abilities off; no accidental spirit | Night-home law | B (flags) · L (mood) |
| 10 | Bed→spirit is a threshold (Totten arrival), not a toggle | Bed + rune | B (gated) · L (ritual) |
| 11 | Spirit nurture on the planted herb feels like *care*, same slot as day plant | Nurture | B (same `NODE_PLANT_SLOT`) · L (VFX) |
| 12 | Portals are doors, not load screens; avoid+soothe replaces kill | Portals / camp night | B (portal pair; 1 guard + 2 sleepers exist) · L (stealth juice, night look) |

Early-tester script (Lead, not a bot PASS): play MUST order once on VS_MVP greybox; mark each row B-fail vs L-note.

---

## 5. Anti-patterns — PARK / REJECT

| Pattern | Ruling | Why |
|---------|--------|-----|
| Over-authored art / NightMix before verbs walk | **REJECT** for T0 prove | Greybox longer. Taste after gap-inventory. |
| Night mood as bot `ok: true` | **REJECT** | Lead lock; CAPTURE_REDUNDANCY three-state. |
| Capture-first placement / stills as inventory | **REJECT** | CAP PARKED; math-first schemas already on main (`f72d5d8`). |
| Lethal-combat defaults (HP, fail-state death, shooter cover metrics) | **REJECT** | CUT player death; eject / avoid+soothe. |
| Free-flight / aircraft energy as “better glide” | **REJECT** | CUT free-flight; glide = fall. |
| Fast-travel skipping perch→field in the *prototype feel* pass | **PARK** | OK as prove cheat if a later bite names it; not the tester feel goal. |
| New MUST beats from this library | **REJECT** | SCOPE floor frozen. |
| Loading books into AGENTS / seats | **REJECT** | Pointer-only (`READING_CANON` law). |
| Reopening Movement bible / MV-A / DS-A | **REJECT** | Cite, do not amend. |
| DESKTOP Act / `.uasset` from this EXIT | **REJECT** | Docs bites only. |

---

## 6. Do bites (max 2) — docs only

### Bite 1 — `GD-MOVENV-CANON`

**Unknown (one):** Can Design/Test cite movement+env KEEP rows without loading books?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` *(new)* — pointer tables from §1–2, harness pointer rules from §3, feel-goals table from §4, anti-patterns short list. Pointer-only. No book paste.

**Forbidden:** `Source/**` · `Content/**` · `.uasset`/`.umap` · DESKTOP Act · CAP product · AGENTS body · A–E rewrite · `#234` body duplication · Movement bible edits.

**DONE-WHEN:**

```bash
test -f Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md
grep -E 'KEEP|CANDIDATE|PARK' Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md
grep -E 'Swink|Totten|Lynch|Level Design Book|glide' Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md
grep -E 'Lead-only|bot-proveable|NODE_|EJECT_HOME|CAP PARK' Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md
grep -E 'ready:false|closed_fail: false|Arrange' Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md
```

**child Research:** N

---

### Bite 2 — `GD-MOVENV-POINTER`

**Unknown (one):** Can READING_CANON grow **one CANDIDATE cluster** without touching A–E KEEP or AGENTS?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/READING_CANON_V1.md` — **one new CANDIDATE row** (cluster) pointing at `GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` + Swink/Totten titles. No A–E table edit. No sixth architecture layer.

**Forbidden:** A–E body · pin bump · alwaysApply · AGENTS dump · feel-library paste from `#234` · CAP.

**DONE-WHEN:**

```bash
grep -n 'GAME_DESIGN_MOVEMENT_ENV_CANON_V1' Docs/handoffs/READING_CANON_V1.md
grep -E 'CANDIDATE' Docs/handoffs/READING_CANON_V1.md
# A–E KEEP block still cites blob 107a511 — unchanged count of A–E primary rows
grep -c '107a5118c95c1bf0b1b3d1755796632bff41b535' Docs/handoffs/READING_CANON_V1.md
```

**Order:** Bite 1 merge before Bite 2 (pointer needs a target). If Lead runs only Bite 1, that is enough.

**Not opened:** feel DONE-WHEN templates as a third file — fold 2–3 example DONE-WHEN lines *into* Bite 1 (e.g. “left `NODE_GLIDER`, arrived field AABB, no load hang”). Avoid a third artifact.

---

## 7. Coordination with `#234`

| This EXIT | `#234` (general feel/juice) |
|-----------|------------------------------|
| Weight, latency, glide-as-fall, camera-truth, path/landmark, greybox metrics | Hitstop, squash, particles, audio stingers, UI juice |
| May **cite** `#234` as CANDIDATE | May **cite** this canon for movement rows |
| Neither blocks the other ACCEPT | Do not merge tables into one seat-loaded doc |

---

## eggbot

N/A

---

## child Research needed?

**N** — Sources are standard books/talks with stable titles/URLs. No rights-blocked hole blocks the KEEP table.

---

## Accept checklist (Conductor)

- [ ] Prompt seven headings were present on the Research paste  
- [ ] EXIT has Diagnosis · Decision · KEEP/CANDIDATE/PARK (movement + env) · harness pointer rules · feel-goals · anti-patterns · ≤2 Do bites · eggbot · child Research · this checklist  
- [ ] No “implement now” / DESKTOP Act / CAP product Do  
- [ ] Pointer-only; T0 SCOPE not voided; CAP PARKED  
- [ ] Coordinates with `#234` without requiring merge order  
- [ ] A–E cited only; no new module / no 15-q  

### Fitness greps (EXIT)

```bash
# B-ish: required sections
grep -E 'Diagnosis|Decision|KEEP|Do bites|eggbot|child Research|Accept checklist' \
  artifacts/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md

# C fail-strings must be empty on Do-bite instruction prose
grep -nEi 'implement now|open DESKTOP Act|run the prove|CAP product Do|APPROVE TOOL SCOUT' \
  artifacts/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md && echo FAIL

# Arrange-block must not be equated with closed_fail
grep -nE 'ready:false.{0,40}closed_fail' artifacts/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md && echo FAIL
```

---

## Sources (title + author or stable URL)

- Swink, Steve. *Game Feel: A Game Designer’s Guide to Virtual Sensation* (2008). Essay: “Game Feel: The Secret Ingredient,” Game Developer / Gamasutra (2007). https://www.gamedeveloper.com/design/game-feel-the-secret-ingredient  
- Swink six-component summaries: https://gamejuice.co.uk/articles/swink-6-components-game-feel  
- Nintendo. GDC 2017 *Breaking Conventions with Breath of the Wild*; GDC 2024 TotK physics / multiplicative design. Secondary: Game Developer “5 design lessons learned from Breath of the Wild.”  
- Unwinnable / FinalBoss essays on TotK glide as controlled fall (2026) — supporting, not primary.  
- Totten, Christopher W. *An Architectural Approach to Level Design*. Lecture: “Architectural theory for level designers.”  
- Lynch, Kevin. *The Image of the City* (landmarks / paths / nodes / edges / districts).  
- *The Level Design Book* — Blockout: https://book.leveldesignbook.com/process/blockout  
- “Greybox Longer” (2026): https://pixelwolf.net/blog/greybox-longer-level-design-before-art-opinion  
- Mustard / Chair — Shadow Complex paper-then-greybox (Game Developer “Unlocking the Vault”).  
- Schell, Jesse. *The Art of Game Design: A Book of Lenses*.  
- Fasterholdt, Martin. “You say jump, I say how high?”  
- HomeWorld: `PROTOTYPE_FEATURE_LIST_V1.md` · `READING_CANON_V1.md` · `CAPTURE_REDUNDANCY.md` · `ONE_SHOT_BITES.md` · Movement bible LOCKED · Docs/24 · Docs/30  

---

*End EXIT. Conductor: ACCEPT → schedule GD-MOVENV-CANON then GD-MOVENV-POINTER. Do not open movement Implement or CAP.*
