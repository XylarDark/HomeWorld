# VISION BOARD — the prototype

| Field | Value |
|---|---|
| **Status** | **CANON for product work** — 2026-10-02, `TG-T0-ASSETS` Round 3 |
| **Supersedes for prototype scope** | `VisionBoard/Core/PROTOTYPE_SCOPE.md` (2026-03-08) · `VisionBoard/MVP/MVP_TUTORIAL_PLAN.md` (2026-03-08) · `VisionBoard/MVP/MVP_100_PHASED_APPROACH.md` · `VisionBoard/MVP/MVP_FULL_SCOPE_10_LISTS.md` |
| **Defers to** | [`VisionBoard/Core/VISION.md`](../VisionBoard/Core/VISION.md) for **theme and long-horizon campaign** — see §2 |
| **Directs** | [`T0_MECHANIC_INVENTORIES_V1.md`](handoffs/T0_MECHANIC_INVENTORIES_V1.md) — the 13 musts |
| **Ordered by** | [`T0_ROADMAP.md`](TaskLists/T0_ROADMAP.md) · [`T0_WORK_SORT.md`](TaskLists/T0_WORK_SORT.md) |

---

## 1. The one-paragraph version

> You are **alone** and you have **lost something**, and you are building a home in a world
> that is not empty. By day you work the open field — gather, plant, cook. By night you
> **sleep, and you become something else**, and in that form you meet the things that live at
> the pine forest who are carrying their sin rather than their nature. **You do not kill them.
> You take the sin off and they become people.** The ground opens because you did the thing.
> The world announces what it wants by its shape alone, and if you cannot tell from twenty
> metres away, it has not said it.

---

## 2. What was decided, and what it cost

`TG-T0-ASSETS` Round 3, Lead 2026-10-02. Two conflicts in `VISION.md` made the board unable
to direct anything. Both are now settled.

### V1 — The game is the **Lone Wanderer** — **SUPERSEDED 2026-10-02**

> **SUPERSEDED by the Lead, 2026-10-02.** Kept below verbatim so the change is auditable.
> The "Is not" list **no longer holds.** V1's stated cost is the reason:
>
> *"The theme's engine is 'Love as Epic Quest' — and this removes the thing you love from the
> prototype. That is a real loss, not a technicality."*
>
> The Lead's answer was to put the loved one back and make the rescue a prototype beat. See
> **V1b** below and `Docs/handoffs/TASTE_GATE_T0_ASSETS.md` Round 5.

`VISION.md:11` wins. `:56` and `:79` were Act-2 text reaching toward a game this prototype is
not.

| | |
|---|---|
| **Is** | solo · a family that is **taken**, not a family to protect · a homestead you **hold** rather than repair · conversion as the answer to combat |
| **Is not** | a rescue mission · a ruined homestead · a family you keep safe at night |

**The cost, stated plainly.** The theme's engine is *"Love as Epic Quest"* — and this removes
the thing you love from the prototype. That is a real loss, not a technicality: the game is
harder to feel good about when nobody is at stake. It is accepted because the alternative is
building a rescue arc that no must names.

**Deferred, not deleted:** the family, the rescue and the ruin are **Act 2+ text**. They live
on in `VISION.md` and nothing in this prototype contradicts them.

### V1b — The **companion**, the camp, and the rescue

`TG-T0-ASSETS` Round 5, Lead 2026-10-02. **This is the Act 2 arc V1 deferred, now in the
prototype** — because the theme needed it and V1 admitted the loss.

| | |
|---|---|
| **Is** | a **loved one who travels with you** · the camp takes them · you are **sent back to the homestead** · spirit form is the only way down to the planet side · you **release the guards' grief so they sleep** · then you **take them home** |
| **Is not** | a kill quest · a rescue by force · a family you keep safe at night · a ruin you repair |

**Love as Epic Quest is now literal:** someone is at stake, they are taken, and you go into the
dark to get them back. The conversion law holds — the guards are **calmed, not killed**, which
is the same gesture as the homestead combat, pointed at the people holding your loved one.

**Most of this already exists as musts.** `M9`/`M11` (day boundary), `M11` (spirit form needs
bed **and** rune), `M13` (home → camp portal) and `M14` (avoid 1 guard, soothe 2 sleepers,
convert-not-kill) are **the story**. `M14` in particular is *"release the negative emotions
from the camp guards so they sleep"* written as a technical requirement eight weeks earlier.

**Genuinely new:** the travelling companion, the captive, the kidnapping trigger, and the
return leg home. **Blocking:** the camp does not exist, so the middle of this story is unbuilt.

### V2 — Night is **a form the player becomes**

Not a body you defend with. Not a phase that happens to you.

| | |
|---|---|
| **Is** | bed → sleep gate → with the rune → **you are spirit** → you do spirit things → dawn → you are body again |
| **Is not** | an astral body you project and defend with · a phase that grants you a form |

**Why this and not the alternatives.** Conversion is the reason. *You meet foes in spirit and
they become people* is a mechanic that only makes sense if the player is somewhere else when
it happens. "Defend with your astral body" puts the player in the same room as the thing they
are meant to change rather than in a form capable of changing it.

**Locked, tested, and not to be re-opened:** spirit requires **both** gates. Sleep alone does
not work. Rune alone does not work. Phase alone never works — that is the `closed_fail` case,
and four behaviour tests assert it.

### V2b — **Gather by day, tend by night**

`TASTE_GATE_T0_ASSETS` Round 6, Lead 2026-10-02: *"Gather by day, tend by night will be the
theme throughout the game."*

| | |
|---|---|
| **Day** | you **gather** — herbs, dung, berries, wood. You are a collector, hands full, nothing asked of you |
| **Night** | you **tend** — soil, sleeping guards, a captive, a garden. You are a caretaker, and something depends on you |

**This is the principle, not the dung.** It arrived as a question about fertilizer and turned
out to be the answer to *why night exists at all*. V2 said night is a **form you become** and
left it at that — a form for what? V2b supplies the verb.

**It is the same act in both places, and that is what makes it a theme rather than a rule.**
Easing a guard's grief until they can sleep, and spreading compost on a bed so a plant can
grow, are one gesture: *you make it possible for something to rest.* The homestead garden and
the camp rescue are not two features — they are the same verb in two places, which is why the
player needs no tutorial to understand the camp when they arrive.

**What it resolves.** Six resources that were collected and never used had a purpose. Night
gained a verb besides combat, so the loop is a **pair** rather than a sequence. And the
`M_Nurtured` master plus `RES_SEED` already existed with nothing pointing at them.

**What it costs, honestly:**

| | |
|---|---|
| **A rule nobody has written** | What may a spirit **touch**? Soil, yes. A rope, to free someone? A sleeping guard? The camp rescue needs this answer and so does the garden. It is the single most load-bearing unwritten rule in the prototype |
| **Register conflict** | Night is meant to be *calm and caretaking*. The camp night is a tense stealth rescue. Not a contradiction — different nights — but the game has to be able to be both, and that is an art-direction demand, not a mechanic |
| **Night is now mandatory for progress** | If tending only happens at night, a player who cannot reach spirit form cannot advance the homestead at all. That is a strong dependency on `M11` and needs a fallback or an explicit failure |

**The dung question this settles:** dung yields **`RES_SEED`** — compost is the seed resource's
natural sibling, so this adds **no seventh resource** and breaks nothing. Applying it moves a
garden bed's soil state, rendered with the existing `M_Nurtured` master.

### V3 — This document is the board; `VISION.md` keeps the theme

`VISION.md` is **not** rewritten or retired. It remains the long-horizon campaign and the
reason the prototype exists. This file is what the musts are steered by, and it is short
enough to actually be read.

**The March documents are superseded for prototype scope** — they are six months old, predate
every taste decision, and `MVP_TUTORIAL_PLAN.md` still names *"Claim homestead"* as the
vertical-slice moment, which is not T0's moment.

---

## 3. The feeling target, in one line

> **Stranger in ~3 s reads safe home above a living world** — locked 2026-09-19, unchanged.
> Warm, handmade, hopeful. Cartoon, not Disney. Fantasy, not high fantasy. **Never
> photoreal, never grimdark, never sci-fi.**

The prototype serves this. It does not redefine it.

---

## 4. The three laws that constrain everything

| Law | Consequence | Enforced by |
|---|---|---|
| **Environment alone.** A zone announces its mechanic by terrain, material and light. UI appears only *after* you act, and only names it. | No entry labels. No persistent markers. A family that cannot be told apart by shape at 20 m **has failed its section** | `homeworld_graybox_silhouette.py` — a report, not a gate |
| **One mechanic family per section**, ~84 m of walking, taught in isolation. | Seven families. Each needs one volume. All seven now have one | `Lib/02_Zones/<family>/` |
| **The section releases you.** Having used the family, the terrain opens. | The boundary is a consequence of play, so it can never feel arbitrary | — level design |

**The seven families and their signature silhouettes.** Locked, and the reason the art is
decidable rather than arguable:

| Family | Reads at 20 m as | Its one volume in the prototype |
|---|---|---|
| `gather` | low wide soft mound, a spreading patch | the field nodes |
| `nurture_tame` | broad low pad with a raised rim you can see over | the beast pad |
| `heal` | narrow upright, single soft column | **the plant sprout after nurture** |
| `spirit` | tall thin vertical **with a see-through gap** | **the shrine, and the wound** |
| `stealth` | low broken horizontal, never a closed mass | **the rune** |
| `build_place` | flat square plate, deliberately dull | the cabin, the garden, the kettle |
| `combat` | jagged asymmetric wedge, tallest in frame | **the camp** |

**Traversal is the spine, not a family.** Paths, the lookout, the glide perch, islets and the
landing circle carry no silhouette. They inherit the neighbouring family's material.

---

## 5. The world, as it now stands

### Zone 1 — the homestead (the hub)
A standing island home, 21 × 14 m, held not repaired. Cabin, garden, lookout, shrine, pines.
Gives the *"stranger reads safe home above a living world"* beat its only place to happen.

### Zone 2 — the open field (planet side)
**Family: `gather`.** Open, low, long sightlines, nothing tall in the middle. Landing circle,
winding path, gather nodes. Reads as *come here and collect*.

### Zone 3 — the pine forest (planet side)
**Family: `combat`.** Dense pines, close walls, a clearing with a fire. The guard watches the
approach; two sleepers rest inside his arc. Reads as *something is here and you must choose
how to pass it*.

**Zone 2 → Zone 3 is a treeline.** Pines thicken into an unbroken wall and the ground continues
out of view. It is terrain, never a wall that was placed — TG-ZONE-FAMILY fork B.

**Open, measured, and standing in a report:** `heal`, `stealth` and `combat` had **no volume
anywhere** in the 39-volume layout. All three now have exactly one. Two are placed; the camp
waits on a reference image.

---

## 6. What the prototype must *feel* like

Not a list of features. Four moments, in the order a player meets them:

| # | Moment | Why it is the test |
|---|---|---|
| 1 | **You wake, and it is morning, and you are alone in a home that is intact.** | The hook is the *feeling*, not the plot. If the homestead does not read as safe-and-won within 3 s the theme has failed before any mechanic runs |
| 2 | **You cannot get to sleep as a spirit without doing the day first.** | This is the law made physical. The gates are not a menu — they are the reason the day exists |
| 3 | **You glide down into a field that is open and bright and full of things to collect.** | Zone 2 must read as *gather* from twenty metres, before you have picked anything up |
| 4 | **You stand outside the pine wall, and you can see there is a camp, and you can see exactly where the guard is looking.** | The climax, and it is a **shape** test. No HUD. If the arc is not visible from outside, the design has failed and the fix is art, not UI |

**Number 4 is the one that cannot be faked.** It is why the camp exists as a place rather than
as a trigger volume.

---

## 7. What the musts are, in one column

Thirteen, in dependency order, canonical in
[`T0_MECHANIC_INVENTORIES_V1.md`](handoffs/T0_MECHANIC_INVENTORIES_V1.md). **This board does
not restate their DONE-WHEN rows** — a paraphrase is how the two vocabularies drifted apart
once already.

| # | Beat | Family | Art |
|---|---|---|---|
| 1 | Night without a bed stays body | — | none — a negative law |
| 2 | Rune unlock before bed→spirit | `stealth` | ✅ placed |
| 3 | Bed → spirit | `spirit` | ⚠️ shrines read `mid`, must read `tall` |
| 4 | Day-camp eject | `combat` | ⛔ **the camp does not exist** |
| 5 | Planetside boot home | — | reuses #4's ground |
| 6 | Kettle → tea → sprint | `build_place` | ✅ placed |
| 7 | Plant given herb | `build_place` | ✅ placed |
| 8 | Nurture the planted slot | `heal` | ✅ sprout placed, day state reads flat |
| 9 | Backpack gates inventory | — | none — a UI/state law |
| 10 | Field gather near landing | `gather` | ✅ exists |
| 11 | Wake label | — | none — a label |
| 12 | Home → camp portal | `spirit` | ⛔ destination is a void |
| 13 | Avoid 1 guard, soothe 2 sleepers | `combat` | ⛔ **the whole camp** |

**Accepted: 0 of 14.** All 13 implementation commits are in `main`; six beats are
merged-but-unproven, and acceptance requires the Lead to run a prove and stamp it.

---

## 8. The boundaries this board draws

| Refused | Why |
|---|---|
| Killing a foe | AGENTS.md. Combat **strips sin and converts**. Beat #14's own Anti row: *kill / convert-as-soothe = fail* |
| A rescue arc, a ruined homestead, a family to protect | V1. Act 2+ text, deferred not deleted |
| UI that names a zone before you act | Environment alone |
| A second biome | `EBiomeType` is terrain dressing and weather, not a zone type |
| Hero art, textures, UVs | Greybox tier. Art bible §5 Layer A: cheap mass holding silhouette is the *correct* state |
| Promoting art to `Content/` | `Docs/20` — drafts only, sidecar + `AI_ASSET_LOG` row on promote |
| A harness that grows | `Docs/36` §2 — three triggers, nothing else |

---

## 9. What is still undecided, and where it is parked

| Fork | Parked in | Waiting on |
|---|---|---|
| The wound in the field or the forest? | `TG-T0-ASSETS` Round 4 | Lead |
| Does the plant slot read as `heal` or as garden? | Round 4 | Lead |
| The rune: `stealth` or `spirit`? | Round 4 | Lead |
| Island top: which document is truth? | Round 4 | Lead — three answers, none matching the blend |
| `M_FamilySilhouette`, `M_ValleyNight` | Round 4 | Lead — in the blend, not among the ten masters |
| The camp's reference image + firing line | `Docs/art/GROK_IMAGINE_PROMPTS.md` | Lead |

---

## 10. How to read this board in one minute

If you read nothing else:

1. **You are alone.** Nobody is at stake. That is a cost we accepted, not an oversight.
2. **At night you become something else**, and only if you earned it by day.
3. **You do not kill. You convert.**
4. **The world tells you what it wants with its shape, and nothing else.**
5. **Fourteen beats, all code merged, none accepted.** The next work is proving them, not
   writing them.
6. **The camp does not exist yet**, and it carries four beats including the climax.

---

*Vision board for the prototype — canon for product work, 2026-10-02. Theme and long-horizon
campaign remain in `VISION.md`; this file is what the musts are steered by, and it is short
enough to read.*
