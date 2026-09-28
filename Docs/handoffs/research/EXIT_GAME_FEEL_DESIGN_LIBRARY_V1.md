# EXIT GAME_FEEL_DESIGN_LIBRARY_V1

**Kind:** RESEARCH EXIT — GAME_FEEL_DESIGN_LIBRARY_V1

**File protocol:** Lead / Conductor paste. Canonical intended path: `Docs/handoffs/research/EXIT_GAME_FEEL_DESIGN_LIBRARY_V1.md`  
**Prompt:** `PROMPT_GAME_FEEL_DESIGN_LIBRARY_V1`  
**Draft PR:** #234  
**Date:** 2026-09-27  
**Pins:** DET `0a27306` · HW tip context `234abe6` / later `f72d5d8` (CAP-PROP-GATE schemas on main) · CAP product **PARKED**  
**Scope floor:** Interview `PROTOTYPE_T0_V1` + `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` (MUST beats unchanged)  
**Parallel:** ACCEPTED `EXIT_GAME_DESIGN_MOVEMENT_ENV_V1` + draft #237 `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` = movement + env layout. This EXIT = **juice / feedback / verbs / input / pacing / polish language**. Cross-link; do not fork A–E; do not reopen CAP.  
**Closed, cite-not-reopen:** READING_CANON A–E KEEP · blob `107a5118c95c1bf0b1b3d1755796632bff41b535` · Movement bible LOCKED · Docs/24 MV-A.

---

## Diagnosis

HomeWorld already has architecture reading canon (A–E) and a movement/env pointer library in flight (#236 EXIT ACCEPTED → #237 Do). What is still missing is a **thin, pointer-only feel/juice library** so when Lead says “make X feel good,” Conductor/Design cite **one path**, not a book dump and not a new CAP track.

Industry split that matters for a small UE 5.8 homestead prototype:

1. **Game feel ≠ juice.** Swink: real-time control + simulated space + polish. Juice talks (2012–2013) taught the third leg and a generation mistook it for the whole body. T0 must keep control/space with the movement-env canon; this library owns **feedback dose**, verb readability, and polish language.
2. **Juice is a dose, inverted-U.** Gabler/Jonasson/Purho/Nijman are KEEP as *method* (exaggerate readable output from a verb). They are PARK as a 30-toggle checklist on greybox VS_MVP.
3. **Cultivate games juice care, not impact.** Stardew / Animal Crossing / BotW shrine-care cousins: confirmation, growth state-change, gentle audio — not hitstop. HomeWorld main draw is seed / nurture / cultivate. Combat juice (screenshake-as-law) would teach the wrong verb at camp.
4. **Pointer-only or it dies.** READING_CANON law: seats cite path; AGENTS ≤1 pointer; no chapter paste. Feel books must **not** become a sixth architecture layer.

**Unknown closed:** Which feel sources are KEEP vs CANDIDATE vs PARK for Co; how Lead asks map onto 1–2 rows; which asks stay Lead-only taste; which single pointer doc to add.

---

## Decision

| Option | Verdict |
|--------|---------|
| Add a **separate** feel pointer doc + one READING_CANON CANDIDATE row | **Go** |
| Fold juice tables into `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` | **No-Go** — that file owns weight/glide/path; mixing juice invites seat dump |
| Extend A–E KEEP with Swink as layer F | **No-Go** — A–E untouched |
| Wait for `APPROVE-PROTOTYPE-LIST` or SCOPE feel Interview | **No** — library is orthogonal; either order is valid |
| Revive CAP product / night bot PASS as feel prove | **No-Go** |

**Go conditions:** Pointer-only. CAP stays PARKED. #237 movement-env canon remains the cite for glide/weight/landmarks. This library cites that file; it does not replace it.

**A–E:** Cite only. Feel is not a sixth layer.

---

## 1. Core game-feel / juice canon

Pointer-only. Seats do not ingest books. Abstracts ≤2 lines.

| Status | Source | Why for a small UE prototype (≤2 lines) |
|--------|--------|------------------------------------------|
| **KEEP** | Steve Swink, *Game Feel* (2008); “Game Feel: The Secret Ingredient” (Game Developer / Gamasutra, 2007) | Control + space + polish triad. Shared KEEP with movement-env canon. Use here for *polish/feedback* language, not a second movement law. |
| **KEEP** | Martin Jonasson & Petri Purho, “Juice It or Lose It” (2012 talk) | Live demo of maximum readable output from a dead verb. Method: add one channel at a time (scale, particles, audio) and stop when the verb already reads. |
| **KEEP** | Jan Willem Nijman (Vlambeer), “The Art of Screenshake” (2013) | Catalog of feedback tricks. KEEP as a *menu*; PARK as T0 law. Prefer land-thud / squash on glide landing over combat shake. |
| **KEEP** | Frank Thomas & Ollie Johnston, *The Illusion of Life* — 12 principles (squash/stretch, anticipation, follow-through, timing) | Animation grammar under every juice talk. Greybox can still anticipate (wind-up on eject, settle on land). |
| **KEEP** | Kyle Gabler / Experimental Gameplay Group — original “juicy” definition (~2005, *World of Goo* lineage) | Juice = generous world response to a small touch. Maps onto kettle, plant, nurture, soothe — not only hits. |
| **CANDIDATE** | Game Maker’s Toolkit — “The Satisfying Motion of Super Mario Bros” and related motion essays | Numeric attack/sustain/release intuition. Cite if a later bite freezes sprint/glide curves. Do not load in seats. |
| **CANDIDATE** | Area Denial / “Game Feel Field Manual” cluster (Swink triad + juice-as-dose) | Useful warning: polish on lag is paint on a broken machine. Pointer only. |
| **CANDIDATE** | Unreal Engine docs: Enhanced Input, Camera, Niagara “one-shot confirm” patterns | Vendor how-to when an Implement bite *later* names a channel. Not law this turn. |
| **PARK** | Fighting-game hitstop/netcode tomes as T0 feel law | Wrong genre. Convert-not-kill + eject-not-kill. |
| **PARK** | 30-toggle “juice checklists” / SEO “make your game juicy” listicles | Dose without craft. Reject as KEEP. |

---

## 2. Broader game design that improves feel

| Status | Source | Why for homestead / day-night / form-swap (≤2 lines) |
|--------|--------|--------------------------------------------------------|
| **KEEP** | Hunicke, LeBlanc, Zubek — MDA framework (2004) | Mechanics → dynamics → aesthetics. T0 aesthetics to aim: Sensation (gentle), Fantasy (cultivate), Discovery (field), Submission (care loop) — **not** Challenge-as-kill. |
| **KEEP** | Jesse Schell, *The Art of Game Design* — lenses of Essential Experience, Feedback, Juiciness, Curiosity, Spaces | Question-lenses for “does tea/plant/glide/nurture *confirm*?” Do not dump 100 lenses into seats. |
| **KEEP** | Tracy Fullerton, *Game Design Workshop* — playtest scripts + dramatic elements | Walk-script as feel instrument. Aligns with `T0_GAP_INVENTORY_WALK_V1` after Lead list stamp. |
| **CANDIDATE** | Koster, *A Theory of Fun* (chunking / pattern mastery) | Thin cite: tea-sprint and glide are skills to *feel*, not menus to read. PARK full book in seats. |
| **CANDIDATE** | Salen & Zimmerman, *Rules of Play* — meaningful play (discernible + integrated outcome) | Nurture must change a *visible* plant state by next day. Outcome = seed collect later (already DEFER on extra plants). |
| **CANDIDATE** | Norman, *The Design of Everyday Things* — affordance / feedback pair | Already KEEP-conceptual in movement-env canon. Cross-cite; do not fork. |
| **CANDIDATE** | Cultivate-feel *games* as refs (not books): *Stardew Valley* crop-stage juice; *Animal Crossing* care confirm; BotW/TotK multiplicative verbs | Lead taste refs for nurture/soothe. Not T0 MUST invent. |
| **PARK** | Fullerton/Schell as alwaysApply seat text | Pointer only. |
| **PARK** | Difficulty-curve / live-ops engagement essays | T0 has no player death and no live-ops. |
| **PARK** | Camera-sickness medical papers as bot PASS | Lead-only; movement-env already owns camera-truth. |

**Transfer note:** 3D UE homestead + form-swap feel is mostly **confirmation of state** (day body vs night spirit, buff on/off, planted vs nurtured) plus **one transit verb** (glide / portal / eject). Juice should mark those state edges, not decorate empty space.

---

## 3. How to use the library in Co

**One thin pointer doc (preferred):** new `Docs/handoffs/GAME_FEEL_CANON_V1.md`  
**Not:** rewrite A–E; not a sixth architecture layer; not a book list in personas.

Do **not** extend READING_CANON’s KEEP table. Add **one CANDIDATE row** that points at the new feel canon (same pattern as #237 row → movement-env canon).

### Surface rules

| Surface | Rule |
|---------|------|
| `GAME_FEEL_CANON_V1.md` | KEEP/CANDIDATE/PARK tables + Lead-ask map + anti-patterns. Pointer-only. |
| `READING_CANON_V1.md` | One new **CANDIDATE** row. A–E KEEP + blob count unchanged. |
| `GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` | Cite from feel canon in one line (“weight/glide/path live there”). No juice table merge. |
| Co skill / AGENTS | **One path pointer** at most (`GAME_FEEL_CANON_V1` *or* READING_CANON). No book lists. |
| Personas / seats | Cite path. Do not load Swink/Nijman bodies. |
| CAP / night | PARKED product; night mood = Lead taste; stills confirm-only after `ready: true`. |

**Harness split (do not invent a new module):**

- Movement/env DONE-WHEN → movement-env canon (`NODE_*`, glide sink, eject-home).
- Feedback/juice DONE-WHEN → this feel canon (readable buff, nurture state-change, soothe confirm).
- Soft vs closed stays existing law: Arrange unreadability = soft; missing MUST after Act = closed. `ready:false` is not a closed fail.

---

## 4. Lead ask → practice map

Cite **1–2 library rows** first. **L** = Lead-only taste (never bot `ok: true`).

| Lead ask (paraphrase) | Cite first | Second | L? |
|-----------------------|------------|--------|----|
| “Tighter jump / less floaty” | Movement-env canon (Swink control+space) | Fasterholdt / GMTK motion (CANDIDATE) | Weight curve = L |
| “Camera less sick” | Movement-env camera-truth cluster | UE follow-cam vendor docs | Framing = L |
| “Night mood / NightMix” | — | — | **L only** — not a library Do; not bot PASS |
| “Verb reads” (tea, plant, rune, bed) | Schell Feedback lens + Gabler juicy | MDA Sensation/Fantasy | Telegraph art = L |
| “Prop readability” | PROP_INVENTORY + Norman affordance (movement-env) | Math-first / bright-day schemas | Dress beauty = L |
| “Hit feel” | **Redirect:** eject-not-kill / soothe-not-kill | Nijman menu *only* for land-thud / squash | Combat hit = REJECT |
| “Tea sprint readable” | Swink polish + Schell feedback | Gabler juicy (world answers the sip) | Weight-on-sprint = L |
| “Glide feels like flying a plane” | Movement-env KEEP (glide = fall) | BotW GDC | Sink = L |
| “Nurture doesn’t feel like care” | Cultivate-game refs + Salen meaningful play | Illusion of Life anticipation/settle | VFX = L |
| “Eject should feel cartoon, not death” | Nijman *timing* + 12 principles anticipation | T0 night/combat law | Cartoon timing = L |
| “Soothe / avoid invisible” | MDA Fantasy + Fullerton walk-script | Gabler juicy on sleeper state | Stealth juice = L |
| “Input feels laggy” | Swink real-time control (~100 ms) | UE Enhanced Input CANDIDATE | Buffer taste = L |

If an ask is **L only**, seats cite the path and stop. They do not invent a prove channel.

---

## 5. Anti-patterns — PARK / REJECT

| Pattern | Ruling | Why |
|---------|--------|-----|
| Listicles / SEO “20 juice tips” | **REJECT** | No craft; seat poison. |
| Juice checklist as T0 MUST | **REJECT** | Dose, not law. Greybox verbs first. |
| Duplicating A–E as feel sources | **REJECT** | Hard Parts / Ousterhout / DDIA / Topologies / Release It! are architecture. |
| Merging this table into movement-env canon body | **REJECT** | Two pointer docs; one cite line each way. |
| Screenshake / hitstop as camp law | **REJECT** | Eject + avoid/soothe. Convert-not-kill preserved. |
| Night lookdev as feel PASS | **REJECT** | Lead taste; CAPTURE_REDUNDANCY three-state. |
| CAP product revive “to prove juice” | **REJECT** | CAP PARKED; stills confirm-only after `ready: true`. |
| Book chapters into AGENTS / skills / alwaysApply | **REJECT** | Pointer-only. |
| New MUST beats from juice talks | **REJECT** | SCOPE floor frozen. |
| Fight-game / shooter juice as homestead default | **PARK** | Wrong fantasy. |
| Full Schell 100-lens dump | **PARK** | Thin lenses only. |

---

## 6. Do bites (max 2) — docs only

Exclusive paths. One unknown each. CLOUD. No Python writer.

### Bite 1 — `GD-FEEL-CANON`

**Unknown (one):** Can seats cite feel/juice KEEP rows without loading books and without colliding with movement-env canon?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/GAME_FEEL_CANON_V1.md` *(new)* — §1–2 tables, §3 surface rules, §4 Lead-ask map, §5 anti-patterns short, 3–5 example feel DONE-WHEN *templates* (readable tea buff; nurture state-change; soothe confirm). Pointer-only. One-line cite of `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` for weight/glide/path.

**Forbidden co-changes:** `Source/**` · `Content/**` · `.uasset`/`.umap` · DESKTOP · CAP product · AGENTS body · A–E rewrite · pin bump · alwaysApply · merge-into movement-env body · `#235` SCOPE body.

**DONE-WHEN:**

```bash
test -f Docs/handoffs/GAME_FEEL_CANON_V1.md
grep -E 'KEEP|CANDIDATE|PARK' Docs/handoffs/GAME_FEEL_CANON_V1.md
grep -E 'Swink|Juice It or Lose It|Screenshake|MDA|Schell|Gabler' Docs/handoffs/GAME_FEEL_CANON_V1.md
grep -E 'Lead-only|GAME_DESIGN_MOVEMENT_ENV_CANON|CAP PARK' Docs/handoffs/GAME_FEEL_CANON_V1.md
grep -E 'nurture|tea|soothe|eject' Docs/handoffs/GAME_FEEL_CANON_V1.md
```

**child Research:** N

---

### Bite 2 — `GD-FEEL-POINTER`

**Unknown (one):** Can READING_CANON grow **one CANDIDATE row** pointing at the feel canon without touching A–E KEEP or AGENTS?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/READING_CANON_V1.md` — **one new CANDIDATE row** pointing at `GAME_FEEL_CANON_V1.md` + Swink/juice/MDA titles. No A–E table edit. No sixth architecture layer.

**Forbidden co-changes:** A–E body · blob rewrite · pin bump · alwaysApply · AGENTS dump · CAP · movement-env KEEP rows.

**DONE-WHEN:**

```bash
grep -n 'GAME_FEEL_CANON_V1' Docs/handoffs/READING_CANON_V1.md
grep -E 'CANDIDATE' Docs/handoffs/READING_CANON_V1.md
# A–E KEEP blob cite count unchanged
grep -c '107a5118c95c1bf0b1b3d1755796632bff41b535' Docs/handoffs/READING_CANON_V1.md
```

**Order:** Bite 1 before Bite 2 (pointer needs a target). If Lead runs only Bite 1, that is enough for Co cites.

**Coordination with #237:** If movement-env pointer row is not on `main` yet, Bite 2 still only adds the *feel* row. Do not edit the movement-env row in the same bite.

---

## 7. Coordination

| This EXIT (#234) | Movement-env (#236/#237) | Interview SCOPE feel (#235) |
|------------------|--------------------------|-----------------------------|
| Juice, feedback, verb confirm, polish dose | Weight, glide-as-fall, landmarks, greybox envelopes | Product overlay: feel bar vs art bar on T0 |
| May cite movement-env in one line | May cite this as CANDIDATE juice | May cite both after ACCEPT |
| Neither blocks the other ACCEPT | Do not merge tables | Does not declare list stamp |

---

## eggbot

N

---

## child Research needed?

**N** — Titles/talks are standard with stable names. No rights/edition hole blocks the pointer table. Cultivate-game refs are optional CANDIDATE, not KEEP law.

---

## Accept checklist (Conductor)

- [ ] Prompt seven headings were present on the Research paste
- [ ] EXIT has Diagnosis · Decision · KEEP/CANDIDATE/PARK (feel + broader design) · Co surface rules · Lead-ask map · anti-patterns · ≤2 Do bites · eggbot · child Research · this checklist
- [ ] Title line `EXIT GAME_FEEL_DESIGN_LIBRARY`
- [ ] Pointer-only; A–E untouched; CAP PARKED
- [ ] No DESKTOP / feature work / CAP product instruction in Do bites
- [ ] Coordinates with movement-env canon without requiring merge order
- [ ] Max 2 docs Do; exclusive paths; greppable under `Docs/handoffs/`

### Fitness greps (EXIT)

```bash
# required sections
grep -E 'Diagnosis|Do bites|eggbot|child Research|Accept checklist' \
  Docs/handoffs/research/EXIT_GAME_FEEL_DESIGN_LIBRARY_V1.md
grep -E '^#+[[:space:]]*EXIT ' \
  Docs/handoffs/research/EXIT_GAME_FEEL_DESIGN_LIBRARY_V1.md

# C fail-strings must be empty on Do-bite instruction prose
grep -nEi 'implement now|open DESKTOP Act|run the prove|CAP product Do|APPROVE TOOL SCOUT' \
  Docs/handoffs/research/EXIT_GAME_FEEL_DESIGN_LIBRARY_V1.md && echo FAIL
```

---

## Sources (title + author or stable URL)

- Swink, Steve. *Game Feel: A Game Designer’s Guide to Virtual Sensation* (Morgan Kaufmann / CRC, 2008). Essay: “Game Feel: The Secret Ingredient,” Game Developer / Gamasutra (2007).
- Jonasson, Martin & Purho, Petri. “Juice It or Lose It” (2012).
- Nijman, Jan Willem. “The Art of Screenshake” (Vlambeer, 2013).
- Thomas, Frank & Johnston, Ollie. *The Illusion of Life: Disney Animation*.
- Gabler, Kyle et al. Experimental Gameplay Group / juicy-element notes (*World of Goo* lineage, mid-2000s).
- Hunicke, Robin; LeBlanc, Marc; Zubek, Robert. “MDA: A Formal Approach to Game Design and Game Research” (2004).
- Schell, Jesse. *The Art of Game Design: A Book of Lenses*.
- Fullerton, Tracy. *Game Design Workshop*.
- Keogh, Brendan. “An Incomplete Game Feel Reader” (2017). https://brkeogh.com/2017/03/31/an-incomplete-game-feel-reader/
- In-repo: `Docs/handoffs/READING_CANON_V1.md` · `Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` (draft #237) · `Docs/handoffs/research/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md`

*End EXIT GAME_FEEL_DESIGN_LIBRARY_V1. CAP PARKED. A–E untouched. Pointer-only.*
