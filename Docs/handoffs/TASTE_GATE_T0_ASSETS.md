# TASTE_GATE_T0_ASSETS — the camp, the wound, and the three untaught families

| Field | Value |
|---|---|
| **Gate id** | `TG-T0-ASSETS` |
| **Status** | **PENDING** — Round 1 issued 2026-10-02 |
| **Job** | **taste** (art design + game mechanic design) |
| **Heuristic** | Docs/28 **1** — would change art bible §8 shape language or a shot; and the families that are untaught are a **product** gap (6) |
| **Owner** | human |
| **Opened by** | agent, while finishing Queue A and B of `T0_WORK_SORT` |
| **Upstream** | `TG-ZONE-FAMILY` 8/8 · `TG-GRAYBOX-SILHOUETTE` 2/2 · `TG-ZONE-VOCABULARY` 4/4 |
| **Precedence** | taste-profile §2 — max 2 questions per turn, 2 per round |

---

## Why this gate exists

The remaining work is not agent-owned. Four of the five beats that still need art need it
because **the camp does not exist**:

```
camp_named_objects: []     # measured from the live blend, 2026-10-02
```

M14 is the climax — *avoid 1 guard, soothe 2 sleepers* — and it happens on an empty plain.
M8 and M10 eject you *from* nothing. M13's destination is a void.

Everything mechanical that can be done without you has been done: **8 behaviour tests,
mutation-verified**, covering the P0 form law and all five day-gated beats.

**What is left needs your eye and, in four cases, your images.**

---

## Round 1 — PENDING

### Q1 — The camp. What is it, and does it take your images?

`combat`'s locked signature is *jagged asymmetric wedge, tallest in frame*. I can hit that
proportion with boxes. What boxes cannot invent is what makes a camp a camp.

I need from you, in this order:

1. **One reference image** of a camp you would accept as this game's — fire, shelter, the
   guard's position, the two sleeper alcoves. Any source. Nintendo/WoW/etc is fine; it is a
   shape reference, not a style target.
2. **The firing line** — where the guard looks, and where the two sleepers sit relative to
   the player's approach. This is layout, and it decides whether "avoid 1" is possible.
3. **Whether the camp reads at all without the player having been there.** Under
   "environment alone" a zone must announce its mechanic from shape — so a camp with a
   visible guard and two visible alcoves has to *look* like an encounter before you commit.

- **A (recommended)** — I author from your one image + the three answers above, at greybox
  tier, ten masters only, and you judge the silhouette at 20 m.
- **B** — No images. I author from the art bible vocabulary alone and you judge. Faster,
  and the first pass will be wrong in ways you can describe but not show.
- **C** — Defer the camp entirely. M14 ships as a component with no world, and the prototype
  is accepted as mechanics-only. Honest, and it forfeits the one beat that proves the theme.

### Q2 — The spirit wound: crater, or standing marker?

`SM_SpiritWound_01` is a 3 × 3 m crater with a flat glow plate. No posts, no lintel, no gap.
It reads `flat`.

The `spirit` signature is *tall thin vertical **with a see-through gap***. A crater cannot
satisfy that without becoming a different object. It is the one place where the art gate
and the beat's meaning actively disagree.

This is the fork I have been deferring since the taste gates, and it now blocks three beats
(3, 8, 12 in the art column) because the whole `spirit` family's read depends on whether
spirit has a consistent shape.

- **A (recommended)** — **Standing marker.** A second spirit form: a cracked standing stone
  or a broken arch, same family as the shrines, same gap. Consequence: `SM_SpiritWound_01`
  stops being a hole in the ground and becomes a thing you approach. A "wound" you stand in
  front of and a "wound" you are inside are different stories, and the vertical one reads
  spirit.
- **B** — **Keep the crater.** Consequence: the crater is the one spirit volume that does not
  read as spirit, and I record it as a documented exception so it stops being a finding.
  A wound in the ground is a real idea and I am not dismissing it — but it needs the
  exception to exist.
- **C** — **Both, as two kinds of spirit site.** A crater for the wound and a marker for
  the shrine. Consequence: the collision assertion must learn that two spirit sub-types can
  differ, which weakens the check for the whole family.

---

## Round 2 — will follow, and it is the bigger one

Held so Round 1 is answerable in two questions. Already queued:

| # | Fork | Why it is a fork and not a task |
|---|---|---|
| Q3 | **Are `heal`, `stealth` and `combat` in the prototype at all?** | All three have **no volume anywhere** in the 39-volume layout. Under "one family per section, taught in isolation" they are taught nowhere. Authoring sections for them is level design |
| Q4 | **Does the plant slot read as `heal` or as part of the garden?** | The day state is a flat soil pad and reads as neither. Measured non-conformance, currently reported rather than fixed |
| Q5 | **The rune: `stealth` or `spirit`?** | MUST #7 is a *gate flag*, not a place. I authored a low broken stone because stealth means *low broken horizontal, never a closed mass* — but a tall monolith measured 2.00 and I judged the family over the object. A gate flag may deserve a different family entirely |
| Q6 | **The island top: which document is truth?** | `SM_IslandTop.json` says 21×14×0.5 crust · `GRAYBOX_LAYOUT.md` §1 says 21×14×**4.0** · the blend is 19.3×10.7×0.45. Three answers, none matching |
| Q7 | **`M_FamilySilhouette` and `M_ValleyNight`** | In the blend, not among the ten masters. Either remap, or justify as named instances — art bible §10 allows instances and the allowed list predates these |
| Q8 | **Is the camp a *section* or a *place inside the spirit section*?** | TG-ZONE-FAMILY says one family per section. If the camp is its own section it is a `combat` section and needs ~84 m; if it sits inside the spirit path it does not |

---

## What is NOT being asked, and why

| Not asked | Why |
|---|---|
| Palette, tone, materials | Locked in art bible §1, §7, §10. Taste is not doing taste work — this gate is art and mechanic *shape*, not look |
| Whether to keep any test I wrote | 8 behaviour tests, 2 mutation-verified, asserting laws from your own inventories. Not a taste question |
| Priority or scheduling | Your call in chat, not a gate |
| Whether to build the camp at all before the other bites | Q1-C covers the skip case |

---

## Evidence behind every option

**Q1** — `docs/qa/GRAYBOX_SPEC_REPORT.md`, `T0_ROADMAP.md` §1. The camp measurement is from
the live `.blend` via Blender MCP, not from PIE. I cannot see the game.

**Q2** — `T0_WORK_SORT.md` §2, `Lib/02_Zones/`. The crater is `SM_SpiritWound_01_Crater`
3×3×0.35 with a flat `SM_SpiritWound_01_Glow` 1.8×1.8×0.2. Measured band `flat`; spirit
requires `tall`.

**Round 2** — each is cited at its entry when the round is issued.

⚠️ **One standing caveat, carried from the research:** there is no published standard for a
greybox silhouette-distinctness check, and no source shows anyone running one
programmatically. Shaver's method is a manual squint test. `ASPECT_TOLERANCE` has no measured
eye threshold behind it. A collision is a prompt to look, never proof — and that is why
these forks are yours rather than the assertion's.
