# PRODUCT SPRINT 01 — first playable content

| Field | Value |
|---|---|
| **Status** | OPEN — starts at P1 |
| **Date** | 2026-10-02 |
| **Shape** | 8 tasks, MMMSS increments, one behaviour test each |
| **Authority** | `Docs/00_CANON.md` · `Docs/03_SYSTEMS_MVP.md` · [AGENTS.md](../AGENTS.md) |
| **Machine check** | `npm run verify` — C++ build + JS suite. Each task adds one UE automation test. |

## Why this list exists

The harness is done. `Docs/36` §5 defines success as **the product moving**, and the fitness
check reports `product` **BROKEN** — 37 harness to 23 product commits. Every task below is
product, and every one of them adds a test that would fail if the product regressed.

**The gap this sprint exists to close.** Eight taste decisions are locked and none of them is
in the world. `Docs/02_ART_BIBLE.md` §8 records the measured state: `heal`, `stealth` and
`combat` have no volume anywhere in the 39-volume layout. A player would experience none of
what was decided.

**What this sprint is not.** Not a vertical slice, not a demo build. It is the behaviour
floor — the invariants that were previously only prose, now executable.

---

## The one number

**9 UE behaviour tests, 1 → 9.** Currently 7 exist across two files:

| File | Tests |
|---|---|
| `HomeWorldInventoryTests.cpp` | 3 (schema, gather/stack, save-load) |
| `HomeWorldConversionTests.cpp` | 4 (**P1, done 2026-10-02**) |

---

## Ordering, and why

Each task is chosen so it either (a) makes the next task possible, or (b) locks a canon
invariant that nothing else checks. Three of them are already-stubbed, so the work is
**wiring plus proof**, not new systems. That is deliberate: the systems exist, the evidence
doesn't.

| # | Task | Why here | Depends on |
|---|---|---|---|
| **P1** | Combat conversion behaviour test | Canon: *we do not kill foes.* Highest-value invariant in the game and the cheapest to prove — `ReportFoeConverted` already logs, counts and assigns a role. A test here stops a future combat pass from quietly becoming a kill system. | — ✅ **DONE 2026-10-02**, 4 tests |
| **P2** | Tame-state transitions test | `UHomeWorldBeastTameComponent` is 224 LOC with a state enum and four transition functions, entirely untested. Tame is a mechanic family with no test and (per art bible §8) no volume. | — |
| **P3** | Save/load across a process restart | The one most likely to break silently. Needs P1+P2 done so the save payload has real state in it to lose. | P1, P2 |
| **P4** | Spirit stealth family test | 414 LOC, the largest single component in `Source/`, zero tests. This is the `stealth` family. | — |
| **P5** | Nurture/heal paths test | `NurtureComponent` (225) and `SpiritHealComponent` (112) are the two untested inventory paths noted in the handoff. | P2 |
| **P6** | Clear the 7 blocking graybox findings | `docs/qa/GRAYBOX_SPEC_REPORT.md` FAILs. Includes `SM_IslandTop` 3.3 m short in Y and two non-canon materials in the blend. | — |
| **P7** | Spirit zone prototype — shrine proportion | `TG-ZONE-VOCABULARY` authorised this. Shrines read `mid` when spirit must read `tall`. Correct in place, no rival shrines. | P6 |
| **P8** | Spirit wound: crater or standing marker | **Blocked on the Lead.** See below. | P7 |

---

## P1 — Combat conversion behaviour test — **DONE 2026-10-02** ✅

`Source/HomeWorld/HomeWorldConversionTests.cpp`, commit `6788aab`. All four pass; 18 automation
tests now run in `verify:ue`.

**Canon:** [CONVERSION_NOT_KILL.md](../TaskLists/TaskSpecs/CONVERSION_NOT_KILL.md) ·
[VISION.md](../../VisionBoard/Core/VISION.md) § Vanquishing foes. AGENTS.md: *"We do not
kill foes — combat strips them of their sin and converts them."*

**Behaviour:** a foe reaching its defeat condition produces a **conversion**, never a death.
The counter increments, a role is assigned round-robin, and the flow is observable in the log.

**Already exists:** `AHomeWorldGameMode::ReportFoeConverted` (logs, increments
`ConvertedFoesThisNight`, assigns `EConvertedFoeRole`), reset when phase leaves Night.
`AHomeWorldNightEncounterPlaceholder` calls it on overlap at night. Console `hw.Conversion.Test`.

**Test asserts:**

1. `ReportFoeConverted` increments `ConvertedFoesThisNight` by exactly one.
2. A role is assigned, and it is one of the five enum values — never an out-of-range index.
3. `GetConvertedFoeRole` returns a safe default for an index that was never converted.
4. **The kill test:** there is no code path in the conversion flow that destroys the player, and
   no path that leaves the foe in a "dead" state. Assert the converted foe is *converted* —
   the placeholder is removed and a role is recorded, which is not the same as dying.
5. The counter resets when phase leaves Night.

**Done when:** a new file `HomeWorldConversionTests.cpp` passes under `npm run verify:ue`.
The word "kill" appears nowhere in the assertion.

**Result:** all four pass. Two seams needed explicit assertions, exactly as predicted:

- The counter and the role list are **separate members**. A bug incrementing one without
  appending to the other leaves every foe reading as `Vendor` forever. The round-robin is now
  asserted directly, wrap included.
- `TryTriggerNightEncounter` is `protected` and only reached from `Tick`. Rather than widen
  production visibility or assert the reset indirectly, the test subclasses the GameMode to
  expose the sweep — making the member public would move a canon invariant's guard from
  protected to callable by any gameplay code, which is a worse trade than one line of scaffolding.

⚠️ **Environment note, recorded because it will bite again:** `$env:UE_EDITOR` on this machine
points at **UE 5.7**, which cannot load this 5.8-locked project. `verify.js` pins 5.8 itself
for exactly this reason. Do not trust the variable in this repo — use
`$env:HW_UNREAL_EDITOR` or let `verify` choose.

**Watch for:** the round-robin role assignment. `GetConvertedFoeRole` is documented as
returning `Vendor` for an invalid index — a test that only checks the happy path will not
notice if the round-robin never advances.

---

## P2 — Tame-state transitions test

**Canon:** TG-ZONE-FAMILY family `nurture_tame`. Art bible §8: *"broad low pad with a raised
rim you can see over."*

**Behaviour:** a beast moves through its states by its own rules, and food is the only
admission path.

**Already exists:** `UHomeWorldBeastTameComponent` (224 LOC) —
`EHomeWorldBeastTameState`, `TryOfferFood`, `TryPromoteToHelper`, `UpdateProximity`,
`ResetBondProgress`, `IsDayBodyInteractionAllowed`, `ApplyPersistedState`.

**Test asserts:**

1. Only the declared transitions are legal; an illegal transition is refused, not silently applied.
2. `TryOfferFood` is refused when out of range — proximity is required, not just the call.
3. Bond progress resets rather than accumulating across attempts.
4. `IsDayBodyInteractionAllowed` honours the day-body rule from the scope-refinement R1 pick
   (*no family systems in this slice*).

**Done when:** `HomeWorldTameTests.cpp` passes; every state in the enum is reachable by some
asserted transition, and the unreachable ones are documented rather than left looking tested.

**Watch for:** `ApplyPersistedState` — a save-load path that can set any state directly can
bypass every transition rule. That is the seam P3 will stress.

---

## P3 — Save/load across a process restart

**Canon:** AGENTS.md session-continuity rules · `docs/TaskLists/README.md` *"no second store"*
(locked in scope-refinement R1).

**Behaviour:** state that must survive a restart does, and state that must not, does not.

**Already exists:** `UHomeWorldSaveGameSubsystem` (235 LOC) — `SaveGameToSlot`,
`LoadGameFromSlot`, `DoesSaveGameExist`, `CaptureNPSessionState`, `ApplyNPSessionState`,
`PersistDawnSnapshot`.

**Test asserts:**

1. Save then load in the same process round-trips the inventory, the tame state and the
   conversion counter.
2. A load into a fresh process produces the same state — **this is the part that has never
   been tested and the part that breaks silently.**
3. `DoesSaveGameExist` is false for an empty slot, so a first run is distinguishable from a
   corrupt one.
4. `ApplyNPSessionState` cannot resurrect a foe that was converted away.

**Done when:** `HomeWorldSaveLoadTests.cpp` passes, including a genuine cross-process case.

**Watch for:** `PersistDawnSnapshot` is a separate path from `SaveGameToSlot`. Testing one and
assuming the other is how a save system loses a night of play.

---

## P4 — Spirit stealth family test

**Canon:** TG-ZONE-FAMILY family `stealth`. Art bible §8: *"low broken horizontal, never a
closed mass."*

**Behaviour:** stealth is a state the player enters and leaves by rules, and the rules are not
"soothe" and not "convert".

**Already exists:** `UHomeWorldSpiritStealthComponent` (414 LOC — the largest single component
in `Source/`), plus `HomeWorldSpiritStealthTypes`.

**Test asserts:**

1. Stealth state is entered only by its declared trigger.
2. **The confused-relationship test:** `convert != soothe`. `HomeWorldCharacter.h:316` records
   this as a closed-fail condition — `ReportFoeConverted` must never fire as a stealth exit.
3. Concealment is lost when the rule says it is, not on a timer.
4. Re-entering after exit is legal and starts from a defined state.

**Done when:** `HomeWorldStealthTests.cpp` passes.

**Watch for:** 414 LOC with no test is where a "temporary" flag turns into permanent state.
Assert the exit path explicitly rather than only the entry.

---

## P5 — Nurture and heal paths

**Canon:** families `heal` and `nurture_tame`.

**Already exists:** `UHomeWorldNurtureComponent` (225 LOC), `UHomeWorldSpiritHealComponent`
(112 LOC).

**Test asserts:** the nurture slot consumes and produces the right resources; heal changes the
right state and is refused at full health; **heal never converts a foe** — it is a different
verb and conflating them is the failure the whole conversion design exists to prevent.

**Done when:** both covered in `HomeWorldNurtureHealTests.cpp`.

**Note:** the handoff recorded these as "noted, not scheduled". Scheduling them now because
`heal` is a family with no volume and no test — it exists in code only.

---

## P6 — Clear the 7 blocking graybox findings

**Report:** [`docs/qa/GRAYBOX_SPEC_REPORT.md`](../qa/GRAYBOX_SPEC_REPORT.md) — **7 blocking, FAIL.**

| Finding | Action |
|---|---|
| `SM_IslandTop` Y bbox 10.7 vs spec 14.0 | Resize or correct the spec. **Decide which is truth** — see below. |
| `SM_IslandTop` origin not at ground contact | Fix the pivot, or change `origin_is_explicit` in the spec |
| `SM_Cabin_Porch_Deck` outside cabin footprint | Move, or widen `ASSEMBLY_FOOTPRINTS` if the spec's 5.5×4.5 excludes the porch by design |
| `SM_Cabin_Porch_Post` outside footprint | as above |
| `SM_Cabin_Porch_Rail` outside footprint | as above |
| `M_FamilySilhouette` in the blend | Not one of the ten masters. Remap to a master, or justify as an instance. |
| `M_ValleyNight` in the blend | as above |

**Done when:** the report reads **PASS** and `npm run verify` is green.

⚠️ **The island-top finding is a real fork, not a bug report.** `Lib/01_Homestead/SM_IslandTop.json`
says 21 × 14 with a 0.5 m crust; `Lib/00_Core/GRAYBOX_LAYOUT.md` §1 says `SM_Island_Hero`
21 × 14 × **4.0** with the origin at the underside so the top face sits at Z 0. The blend has
19.3 × 10.7 × 0.45 — **matching neither**. Three documents, three answers. Fixing this means
deciding which is truth, and the reader should say so rather than nudging the mesh.

---

## P7 — Spirit zone prototype: shrine proportion

**Canon:** `TG-ZONE-VOCABULARY` Round 2 · art bible §8 · `DEC-0024` (new
`Lib/02_Zones/Spirit/` kit).

**Behaviour:** a spirit volume reads **tall** with a **see-through gap** at 20 m.

**Already exists and measured:** both shrines are real assemblies of five parts — base, two
posts, lintel, glow — hard-shaded on ten masters. **The gap is already there.** The defect is
proportion: 1.8 m posts on a 1.4 m base, and the wide base dominates the bounding volume, so
the measured aspect lands `mid` instead of `tall`.

**Done when:** the spirit volumes measure band `tall`, the conformance check passes, and the
shrines were corrected **in place** — no rival shrine objects in the blend.

**Not authorised:** a `Content/` promote (Docs/20 — drafts only), a second family, new biome
art.

---

## P8 — Spirit wound: crater or standing marker — **BLOCKED ON LEAD**

`SM_SpiritWound_01` is a 3 × 3 m crater with a flat glow plate. It has no posts, no lintel and
no gap, so it reads `flat` while the spirit signature is *"tall thin vertical with a
see-through gap."*

**A crater cannot satisfy that signature without becoming a different object.** Either it
stays a crater and accepts that one spirit volume is taught wrong, or it becomes a standing
marker you approach rather than a wound you stand in.

**That is level design and it is the Lead's call.** Options were queued for a taste gate and
have not been asked. P8 is written as a placeholder so the dependency is visible, not because
the answer is known.

---

## What this sprint deliberately does not do

| Not doing | Why |
|---|---|
| Fixing `SM_IslandTop` without asking | Three canon documents disagree (§P6). Picking one silently is the failure `decision-log` was deleted over. |
| Authoring `heal`, `stealth` or `combat` volumes | Level design. Art bible §8 names them as the coverage gap; inventing sections is not the agent's call. |
| Promoting anything to `Content/` | `Docs/20` — drafts only, sidecar + `AI_ASSET_LOG` row on promote. |
| A vertical slice or demo build | This is the behaviour floor. |
| Any new harness component | `Docs/36` §2: three triggers, nothing else. |

---

*Product sprint 01 — 8 tasks, 9 behaviour tests. Every task moves the product ratio in the
direction `Docs/36` §5 defines as success.*