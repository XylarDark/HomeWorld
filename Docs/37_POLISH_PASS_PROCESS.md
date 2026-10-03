# Docs/37 — Polish pass process

| Field | Value |
|-------|-------|
| **Status** | **ACTIVE** — agent-owned process; measurement layer only |
| **Date** | 2026-10-03 |
| **Scope** | How the three polish passes (environment size, asset pass 1, mechanics feel 1) are entered, sequenced and stopped |
| **Enforced by** | `Content/Python/polish_readiness.py` → `Docs/qa/POLISH_READINESS.json` |
| **Ownership boundary** | This doc governs *when a pass may start* and *what it is measured against*. It does not decide what the world should look like or feel like. See [docs/human-use/OWNERSHIP.md](../docs/human-use/OWNERSHIP.md) |
| **Related** | [34_ART_PIPELINE_RESEARCH.md](34_ART_PIPELINE_RESEARCH.md) (what to build) · [28_TASTE_GATES.md](28_TASTE_GATES.md) (who decides) · [IndustryStandards/](IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md) (prior scoping) · [canon/FEEL.md](canon/FEEL.md) (targets) |

---

## 1. The short answer

**All three gates are RED. One of them is RED for a reason you can fix cheaply this week, and one of them is RED because the measuring instrument does not exist yet.**

| Gate | Question | State | Blocker in one line |
|------|----------|-------|---------------------|
| **G-ENV** | May we size and block out? | **RED** | 4 open greybox blockers (of 5; 1 waived), the island circuit window is arithmetically unreachable, and nothing has timed a walk |
| **G-ASSET** | May we start asset production? | **RED** | Blocked behind G-ENV by rule, not by accident |
| **G-FEEL** | May we start feel work? | **RED** | No human has ever played the build |

**The most important finding in this document is one line of arithmetic.** FEEL.md's island circuit window is 45–90 s. The character walks at 6.0 m/s. The island as authored has a 48 m perimeter, which is an 8-second lap. So the window's *floor* needs **5.6 laps** — and a circuit that winds five times is not a circuit. Either the island is far too small, or the window is far too long, or the circuit is meant to be partly flown on FALLBACK (whose own glide window is 12–25 s) rather than walked.

This was knowable the moment the walk speed and the island size existed. The island was authored at 19.3 m a long time before anyone divided.

There is also one thing already green that is worth knowing about: **the world is assembled**. `Content/HomeWorld/Maps/MainMenu.umap` carries 1,270 placed actors and built HLOD layers. This project's docs refer to "DemoMap and Homestead"; neither name exists. The world is not missing — it is misnamed, which is a documentation fix and a cheap one.

---

## 2. The rule everything else follows from

> **A pass may not start until its measuring instrument exists and has a recorded baseline.**

This is the whole rework argument in one sentence. Rework is not caused by people making mistakes at the art stage — it is caused by making an art-stage decision before there was a number to decide it against. The number is cheap. The art is not. The cost curve is brutal in one direction and flat in the other.

The level design book's blockout page states it as: *"Keep it cheap until it is ready to become expensive. It is 'cheap' to delete or rebuild some rough blockout geometry, but throwing away finalized art passed work is 'expensive' and wasteful."*

`polish_readiness.py` exists to make this rule enforceable rather than aspirational. Its operating principle is the same one that governs `run_ue_automation.py`, turned on readiness:

> **Absence of evidence is not evidence of readiness.**

A check whose source artifact is missing reports `MISSING`, never `PASS`. A gate with any `MISSING` or `FAIL` is `RED`. Exit code `2` is reserved for "a gate could not be measured at all", which is a different and worse problem than "a gate is red" and is not collapsed into it.

---

## 3. The stage ladder

Each rung is more expensive to leave than the one below. **A gate opens the furthest rung you may enter, not the whole ladder.**

| Stage | What it is | Cost to reverse |
|-------|-----------|-----------------|
| **S0 MEASURE** | Instruments exist; numbers recorded at a named commit | Free |
| **S1 BLOCKOUT** | Cheap placeholder geometry; massing, metrics, sightlines | Free — delete and rebuild |
| **S2 ART-BLOCKOUT** | Real shapes, palette, materials by eye. **No UV, no texture.** | Cheap — still blockout underneath |
| **S3 ASSET PRODUCTION** | Unwrap, texture, final materials, LODs | Expensive |
| **S4 DRESS** | Prop placement, clutter, set dressing | Expensive, and placement is coupled to scale |
| **S5 FEEL TUNE** | Movement, camera, timing, juice | Cheap per change, expensive to re-baseline |

**S2 is the rung HomeWorld has never used, and it is the one that does the most work.** The Valorant/Icebox case in the env-art page ran a month of greybox, then playtest, then an *art blockout* — basic shapes, colour swatches, massing — before anyone unwrapped anything. The stated benefit was not speed; it was that *"prolonging the blockout stage improves the final art pass and allows for more collaboration"*, because the designers still had room to move geometry and the artists had not yet spent a day per asset.

Adding S2 costs one extra step and is the single highest-leverage change to this project's process. It is the difference between finding out the island is too small on a Tuesday and finding out after a texture pass.

---

## 4. The three gates

### G-ENV — environment size

**Opens stage:** S2 ART-BLOCKOUT

| Check | Target | Source of the target |
|-------|--------|---------------------|
| `env.world_assembled` | ≥1 placed actor | Presence, not naming |
| `env.island_sized` | 0 blocking `2_sized` bbox findings | Greybox report's own `blocking_count` |
| `env.pivot_grounded` | 0 blocking ground-contact findings | Greybox report |
| `env.master_binding` | 0 blocking findings | Art bible S10 |
| `env.family_distinct` | 0 blocking findings | Greybox report |
| `env.traversal_measured` | cabin→lookout 15–25 s, island circuit 45–90 s | **Docs/canon/FEEL.md** |
| `env.traversal_reachable` | no canon window contradicts the island size | **Docs/qa/TRAVERSAL_BUDGET.md** |

Two notes on why these are the right six.

**Coverage is asserted, not assumed.** `--selftest` compares the criteria the greybox report can raise as *blocking* against the criteria some check actually covers, and fails if any are uncovered. This is not theoretical: the first version of this gate covered four of the five blocking findings and did not say so, while presenting G-ENV as the greybox gate. A gate that reports honestly on a subset is worse than no gate, because it reads as coverage.

**`2_sized` carries two independent blockers.** The island size mismatch and the island pivot bug are both filed under that criterion for the same volume. The gate narrows by detail text to split them, because a size fix and a pivot fix have nothing to do with each other and must not be waived together.

**The pivot check is the cheap one with the expensive failure mode.** `SM_Island_Hero`'s lowest vertex sits at Z −0.450, so every module parented under the island root inherits that offset. Dressing props onto a bad root produces placements that are all subtly wrong in the same direction — which reads as "the level feels off" rather than "a pivot is wrong", and gets art-fixed instead of pivot-fixed.

**The traversal check has no timing instrument — but it does have an arithmetic one, and the arithmetic fails.**

`Docs/canon/FEEL.md` has declared cabin→lookout at 15–25 s and island circuit at 45–90 s since the GDD, and nothing times a walk. What it could do, and now does, is check whether the windows are even *reachable* on the island that exists — a window is a distance budget wearing a stopwatch, so `seconds × walk speed` gives the distance it demands.

Both quantities are now measured, not assumed:

- **Walk speed 600 cm/s (6.0 m/s)**, extracted from `BP_HomeWorldCharacter`'s movement component CDO by `probe_movement_budget.py` running in the editor. This number had never been written down anywhere, which is why the windows were unfalsifiable: they were denominated in a quantity nobody had extracted from the world.
- **Island extents 19.3 × 10.7 m authored** (spec declares 21 × 14), from the greybox report. As an ellipse that is a **48 m perimeter, or 8.0 s per lap walked**.

Against that:

| Window | Shape | Implied path | State |
|---|---|---|---|
| cabin→lookout 15–25 s | point-to-point | 90–150 m | reachable — ~5–8 crossings of the 19 m long axis |
| **island circuit 45–90 s** | **closed loop** | **270–540 m** | **NOT reachable** |

The circuit's *floor* needs 270 m of walking against a 48 m lap: **5.6 laps**. A circuit that winds five times is not a circuit, so one of three numbers is wrong — the island, the window, or the assumption that the circuit is walked at all rather than partly flown on FALLBACK, whose own glide window is 12–25 s.

**This is arithmetic on measured numbers, not taste, and it needs a human ruling on which number is wrong.** It is also exactly the finding that justifies measuring before building: the island was authored at 19.3 m and the circuit window implies roughly six times that, and nobody could have seen the gap without dividing.

The reference case for the timing instrument that is still missing is Dirty Bomb, where spawn→objective time is compared against an 8–12 s window, so "this feels long" becomes "this is 14.2 s". That needs the game running with World Partition cells streamed and a pawn driven along a drawn route — the desktop, not a commandlet. `Content/Python/traversal_budget.py` cannot do it and does not pretend to; it is a necessary-condition check, and a `REACHABLE` from it means *size does not contradict the window*, never *the walk fits the window*.

### G-ASSET — asset pass 1

**Opens stage:** S4 DRESS

| Check | Target |
|-------|--------|
| `dep.g-env` | G-ENV must be GREEN first |
| `asset.master_count` | Exactly 10 masters (art bible S10) |
| `asset.board` | One row per mesh with a declared stage and priority |
| `asset.poly_budgets` | Export manifest declares a budget per mesh |

**The dependency is the point, not a formality.** The env-art page's most consistent statement is that *"the environment artist is usually supposed to wait for a mature blockout before beginning an art pass."* Encoding it as a hard dependency rather than advice is what stops a month of production art from being spent against geometry that then moves. It is currently RED, which is correct: G-ENV is RED.

**Work iteratively, and start big.** Two practices from the same source that the board is designed to force:

- Get **many assets to 50%, then step back and evaluate them together.** The env-art page's line is *"sometimes a 50% finished art asset can actually be 100% finished enough"* — and a finished one is too late to move cheaply. The board's `stage` column exists so a batch can be reviewed at S2 rather than one asset at a time at S3.
- **Massing, palette and themes before pebbles and grunge.** Starting big is what makes a batch reviewable.

### G-FEEL — mechanics feel 1

**Opens stage:** S5 FEEL TUNE

| Check | Target |
|-------|--------|
| `dep.g-asset` | G-ASSET must be GREEN first |
| `feel.human_playtest` | A human played the build at a named commit |
| `feel.tunable_baselines` | ≥1 measured value per TODO tunable |
| `feel.verb_script` | 8 verbs, each pass or documented fail |
| `feel.binary_fresh` | Last automation run: 0 failed, `dll_stale` false |

**No human has played this build.** This is the finding that matters most in this document, and nothing in the repo substitutes for it.

- 42 green automation rows are **code assertions**. They prove the verbs fire. They say nothing about whether the island is the right size or the glide is the right shape — which are the two questions a feel pass exists to answer.
- `Docs/canon/PLAYTEST.md`'s "last known good" is a **scripted PIE probe** from 2026-09-20, not a play session.
- The only filed verb run is **all-FAIL under a WAIVE** (Docs/14 VP-A), and the track closed anyway.

FEEL.md carries six tunables as TODO proposals with rationale but no chosen number — glide gravity scale, glide lateral influence, camera arm length, camera pitch bias, night length, gather node cooldown — because nothing was ever played to choose one. Measuring each one's *current* value costs nothing and is the precondition for telling whether a change helped. Steve Swink's framing is the relevant one: measure each piece so you can separate medium from message. Tuning is only horizontal if you know where you started.

**One constant per experiment.** Record before-value, after-value, and the commit for each feel change. A feel change that cannot be evaluated against a baseline is a redesign, not a tune.

---

## 5. The rework budget

The industry numbers are worth holding onto, from the same blockout source: *Neon White* shipped 100+ levels and scrapped roughly double that, and one single level went through 50+ changes. That is not a team failing to design well. That is the cost of designing while the expensive thing is already built.

So the process tracks one number: **how much geometry changes after S2.** If that number climbs, the failure is upstream — the blockout was not mature enough — and the fix is to move the gate, not to work faster. Cheaper to instrument than to argue about.

---

## 6. Waivers

A blocker may be waived rather than fixed. Waivers live in `Docs/qa/polish_waivers.json`, keyed on the finding's full `(criterion, volume, detail)` identity.

They are deliberately loud rather than convenient:

- A waived blocker still appears in the output, with its rationale. It does not vanish.
- Waivers key on all three fields because the greybox report files **several independent blockers under one criterion for one volume** — `SM_Island_Hero` alone carries both a size mismatch and a bad pivot. A two-field key would let a waiver meant to accept a size mismatch silently accept a pivot bug.
- A waiver naming a finding that no longer exists reports **`STALE`**, because a gate whose waivers have outlived their findings has stopped describing the repo.
- Waived counts separately from passed. A gate with nine passes and one waiver is not a clean nine.

One waiver currently exists — `SM_Island_Hero`'s y-extent, 10.7 m authored against a 14.0 m spec with 1.4 m tolerance. **It is a record, not a resolution:** the spec and the geometry still disagree, and rescaling authored geometry is forbidden by AGENTS.md. Nothing downstream should read it as settled.

**A waiver is not available for the traversal finding, and should not be.** The island circuit window being unreachable is not a blocker someone can accept their way past — it means two of the three numbers involved (island size, circuit window, whether the circuit is walked) are mutually inconsistent. Waiving it would leave canon and geometry disagreeing about the shape of the game while the report said the check passed. It needs a ruling.

---

## 6a. The circuit finding, in full

Because it is the one finding here that changes what should be built next rather than what should be checked next.

| Quantity | Value | Source | Status |
|---|---|---|---|
| Walk speed | 600 cm/s = 6.0 m/s | `BP_HomeWorldCharacter` CDO | **measured** 2026-10-03, never previously written down |
| Island extents, authored | 19.3 × 10.7 m | `SM_IslandTop`, greybox report | measured |
| Island extents, spec | 21 × 14 m | `ASSEMBLY_FOOTPRINTS` | declared, and disputed (waived) |
| Ellipse perimeter, authored | 48 m | derived | model assumption, stated above |
| Seconds per lap, walked | 8.0 s | perimeter ÷ speed | derived |
| Island circuit window | 45–90 s | `Docs/canon/FEEL.md` | canon since the GDD |
| Implied path length | 270–540 m | window × speed | derived |
| **Laps needed for the floor** | **5.6** | 270 ÷ 48 | **fails** |

Three mutually exclusive readings. Only one can be true, and which one is not an engineering question:

1. **The island is much too small.** 5.6 laps implies a perimeter near 270 m, i.e. roughly 2.3× the authored long axis. That would make the circuit real — and would invalidate the spec, the footprint data, every authored module placement, and the `SM_Island_Hero` waiver together.
2. **The window is much too long.** 45–90 s was a GDD guess that has never been checked against the world. Tightening it to something like 12–20 s would fit the island comfortably. This costs nothing and is the cheapest fix available.
3. **The circuit is not fully walked.** `FEEL.md` gives FALLBACK a 12–25 s glide window in the same table. If the circuit is meant to include a glide segment, the walked portion shrinks by that much — but even a 25 s glide inside a 45 s floor leaves 20 s of walking, still 120 m against a 48 m lap.

Option 2 is the cheapest and the most likely, which is itself the finding: **a number in canon was never checked against the world it describes.** That is the argument for this entire document in one example.

Until it is ruled on, `G-ENV` cannot open, and the cheapest S2 work available is the **art blockout** — shapes and palette, no UVs, no textures — which is cheap to redo if the island grows by 2.3×.

---

## 7. What this document does not decide

Stated plainly, because the point of a process document is to know where it stops:

- **How big the island should be**, and which of the three readings above is right. FEEL.md's windows are the current answer and they contradict the island; reconciling them is a Lead decision.
- **Whether any of this is good.** 42 green rows and a green gate mean code runs and asserted laws hold. Neither is evidence that the island feels right.
- **Art direction, palette, prop choice.** Art Director's call, per [OWNERSHIP.md](../docs/human-use/OWNERSHIP.md) and [02_ART_BIBLE.md](02_ART_BIBLE.md).
- **Whether feel improved.** Measured deltas plus a human verdict, per [28_TASTE_GATES.md](28_TASTE_GATES.md).

---

## 8. Running it

```powershell
# Is the gate able to fail? Run this first, and after touching the script.
py Content\Python\polish_readiness.py --selftest

# Report readiness.
py Content\Python\polish_readiness.py

# Can the canon windows be met by the island that exists? Needs the movement
# probe below to have run at least once.
py Content\Python\traversal_budget.py --selftest
py Content\Python\traversal_budget.py

# Extract walk speed from the character CDO. MUST run inside the editor - this is
# the one step with no host-side equivalent, and it is why the walk speed sat
# unwritten in the project until 2026-10-03.
#   UnrealEditor-Cmd.exe HomeWorld.uproject -run=pythonscript `
#     -script=Content/Python/probe_movement_budget.py -unattended -nullrhi

# Prove the gate's own tests can fail (all fail-open mutations killed).
py Content\Python\tests\_mutate_polish_readiness.py

# Regression tests for the fail-open paths (host pytest only; the editor's
# automation runner imports these modules and never executes their assertions).
py -m pytest Content\Python\tests -q
```

Exit codes: `0` all gates GREEN · `1` a gate is RED · `2` a gate could not be measured.

Run it before each polish session, not after. The point is to catch a stage being entered without a baseline, which is only possible while the stage has not started yet.

---

## 9. Sources

- **Level Design Book — Blockout.** <https://book.leveldesignbook.com/process/blockout> — cheap-until-expensive; playtest in-engine rather than in the editor view; Neon White's shipped-vs-scrapped ratio; Dirty Bomb's 8–12 s traversal window; grid sizing derived from player width.
- **Level Design Book — Environment Art.** <https://book.leveldesignbook.com/process/env-art> — waiting on a mature blockout; Valorant/Icebox's art-blockout stage before production; iterative batch review at 50%; start big; readability as a property that degrades during the art pass; prop/material inventory as a verification tool.
- **Steve Swink — *Game Feel* / "Tuning Horizontal".** Measuring each component before changing it; input-to-response latency thresholds; camera as a first-class feel component rather than a settings screen.