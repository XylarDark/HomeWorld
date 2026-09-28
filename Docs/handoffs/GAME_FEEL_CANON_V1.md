# GAME_FEEL_CANON_V1

**Pointers only. Seats do not ingest books. Cite EXIT `GAME_FEEL_DESIGN_LIBRARY_V1`.**  
**Status:** ACTIVE · CAP product **PARKED** · A–E untouched · juice ≠ sixth architecture layer  
**Weight / glide / path / greybox envelopes:** cite [`GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md`](GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md) — do not merge tables here.  
**Pins:** DET `0a27306` · blob `107a5118c95c1bf0b1b3d1755796632bff41b535` (cite only)

---

## 1. Core game-feel / juice — KEEP / CANDIDATE / PARK

| Status | Source | Why (≤2 lines) |
|--------|--------|----------------|
| **KEEP** | Steve Swink, *Game Feel* (2008); “Game Feel: The Secret Ingredient” (2007) | Control + space + polish triad. Shared KEEP with movement-env. Use here for polish/feedback language, not a second movement law. |
| **KEEP** | Martin Jonasson & Petri Purho, “Juice It or Lose It” (2012) | Max readable output from a dead verb. Add one channel at a time; stop when the verb already reads. |
| **KEEP** | Jan Willem Nijman, “The Art of Screenshake” (2013) | Feedback menu. Prefer land-thud / squash on glide landing over combat shake. PARK as T0 law checklist. |
| **KEEP** | Thomas & Johnston, *The Illusion of Life* — 12 principles | Squash/stretch, anticipation, follow-through, timing. Greybox can still wind-up eject / settle land. |
| **KEEP** | Kyle Gabler / Experimental Gameplay Group — “juicy” (~2005) | Generous world response to a small touch. Maps onto kettle, plant, nurture, soothe — not only hits. |
| **CANDIDATE** | GMTK motion essays (SMB satisfying motion, etc.) | Attack/sustain/release intuition when a later bite freezes curves. |
| **CANDIDATE** | Area Denial / Game Feel Field Manual cluster | Polish on lag is paint on a broken machine. Pointer only. |
| **CANDIDATE** | UE Enhanced Input / Camera / Niagara one-shot confirm | Vendor how-to when Implement later names a channel. |
| **PARK** | Fighting-game hitstop/netcode as T0 feel law | Wrong genre. Convert-not-kill + eject-not-kill. |
| **PARK** | 30-toggle juice checklists / SEO listicles | Dose without craft. |

---

## 2. Broader design that improves feel

| Status | Source | Why (≤2 lines) |
|--------|--------|----------------|
| **KEEP** | MDA (Hunicke / LeBlanc / Zubek, 2004) | Aim Sensation (gentle), Fantasy (cultivate), Discovery (field), Submission (care) — not Challenge-as-kill. |
| **KEEP** | Schell — Essential Experience / Feedback / Juiciness / Curiosity / Spaces | Thin lenses: does tea/plant/glide/nurture *confirm*? No 100-lens dump. |
| **KEEP** | Fullerton, *Game Design Workshop* — playtest scripts | Walk-script as feel instrument (`T0_GAP_INVENTORY_WALK_V1` after list stamp). |
| **CANDIDATE** | Koster *Theory of Fun* · Salen & Zimmerman meaningful play · Norman affordance | Thin cites; Norman already in movement-env. |
| **CANDIDATE** | Cultivate-feel games: Stardew / Animal Crossing / BotW care cousins | Lead taste refs for nurture/soothe. Not T0 MUST invent. |
| **PARK** | Fullerton/Schell as alwaysApply · live-ops engagement · camera-sickness as bot PASS | Pointer / Lead-only. |

---

## 3. Surface rules

| Surface | Rule |
|---------|------|
| This file | KEEP/CANDIDATE/PARK + Lead-ask map + anti-patterns. Pointer-only. |
| `READING_CANON_V1.md` | One **CANDIDATE** row → this file. A–E KEEP + blob count unchanged. |
| `GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` | Weight/glide/path live there. One-line cite only from here. |
| AGENTS / seats | ≤1 path pointer. No book lists. |
| CAP / night | **CAP PARKED**; night mood = **Lead-only**; stills confirm-only after `ready: true`. |

Harness split: movement/env DONE-WHEN → movement-env canon. Feedback/juice DONE-WHEN → this file. Soft vs closed unchanged (`ready:false` ≠ closed_fail).

---

## 4. Lead ask → practice map

Cite 1–2 rows first. **L** = Lead-only (never bot `ok: true`).

| Lead ask | Cite first | Second | L? |
|----------|------------|--------|----|
| Tighter jump / less floaty | Movement-env (Swink control+space) | GMTK motion CANDIDATE | Weight curve = L |
| Camera less sick | Movement-env camera-truth | UE follow-cam | Framing = L |
| Night mood / NightMix | — | — | **L only** |
| Verb reads (tea, plant, rune, bed) | Schell Feedback + Gabler juicy | MDA | Telegraph art = L |
| Prop readability | Movement-env Norman + greybox | Juice It (one channel) | Dress beauty = L |
| Hit feel / impact | Screenshake menu → land-thud only | — | Combat shake = PARK |
| Glide feels like a plane | Movement-env (glide = fall) | BotW GDC | Sink = L |
| Nurture / care confirm | Gabler juicy + MDA Fantasy | Cultivate-game CANDIDATE | VFX romance = L |
| Soothe / eject cartoon | Illusion of Life anticipation | Screenshake menu (gentle) | Timing beauty = L |
| Input laggy | Swink ~100 ms | UE Enhanced Input CANDIDATE | Buffer taste = L |

---

## 5. Anti-patterns

| Ruling | Pattern |
|--------|---------|
| **REJECT** | Book dump in AGENTS/personas · A–E sixth layer · CAP product revive “to prove juice” · night bot PASS · merge juice tables into movement-env · DESKTOP / `.uasset` from this canon |
| **PARK** | Fight-game / shooter juice as homestead default · Full Schell 100-lens dump · 30-toggle checklists |

---

## Example feel DONE-WHEN templates

Design may cite (grep-friendly; not Lead `APPROVE-*`):

1. `tea sprint buff readable on/off (log or UI flag)`  
2. `nurture state-change visible on same NODE_PLANT_SLOT`  
3. `soothe confirm — sleeper state flipped, no kill metric`  
4. `eject lands home not dead (EJECT_HOME)`  
5. `glide land thud / settle present — not free-flight juice`

---

*End. Cite EXIT GAME_FEEL_DESIGN_LIBRARY_V1 · Lead greenlight 2026-09-27. No Implement juice features. CAP PARKED.*
