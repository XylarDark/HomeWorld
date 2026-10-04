# CANON MAP — one lookup, so nobody reads 441 files to find one answer

**Written 2026-10-02, after a consolidation failure that was caught in the act.**

## 0. Which document is the vision

Three documents declare themselves authoritative over the same question, and the newest never
names the ones it replaces. So, explicitly:

> **For prototype scope the vision is [`Docs/VISION_BOARD.md`](VISION_BOARD.md) — V2b,
> "gather by day, tend by night".** `Docs/00_CANON.md` (LOCKED P0) and `Docs/canon/*.md`
> (12 LOCKED files, last touched 2026-09-21) describe an **earlier cut** and are superseded
> *for prototype scope only*. `Docs/01_GDD_MVP.md` likewise. All three remain valid as
> **Act 2+ background** — VISION_BOARD §2 defers that text there deliberately.
>
> Recorded as [DEC-0029](decisions/AGENT_DECISIONS.md#dec-0029). It takes no new product decision;
> it writes down the Lead's 2026-10-02 one.

The vision axis is **not** in conflict — old and new both put gathering in the day, tending in
the night, forbid kill-combat, and require convert-not-kill. What differs is *who you are*, and
there is exactly one stale line, escalated and not edited (it is Lead-LOCKED and it is product
framing):

> `Docs/canon/FANTASY.md:14` — `| Player | Family co-op caretaker (body by day, spirit by night) |`
> vs VISION_BOARD §1 — *"You are **alone** and you have **lost something**"*, plus **one**
> companion who is rescued (Q16/Q18/Q19/Q20).

**The vision was never ambiguous. It was invisible from two of its three doors.**

## Why this file exists

While implementing T0 I wrote this into the must list:

> `#17 Spirit-stealth — Found: **Nothing.** No stealth state, no awareness, no detection`

That was **false**. Spirit-stealth has been LOCKED since 2026-09-21
(`Docs/SPIRIT_STEALTH_BIBLE.md`), implemented (`HomeWorldSpiritStealthComponent.h`, 414 lines),
and **closed with a Lead stamp** (`APPROVE SS-A`, all DONE-WHEN boxes ticked,
`Docs/25_SPIRIT_STEALTH_IMPL.md`).

The reason I got it wrong is the whole problem, and it is not a documentation failure — it is
the **same failure as the broken shrine**:

> *The shrines were in no spec, so a lintel sitting on the ground survived every gate.*
> *#17 was in no index, so a closed, stamped, implemented mechanic read as absent.*

Both are "nothing pointed at it". So this file is not documentation for its own sake; it is a
pointer surface that gets **validated** (see §6) so it cannot silently rot the way the must list
did.

---

## 1. Two structural findings — read this before trusting any path

### 1.1 `Docs/` and `docs/` are the SAME DIRECTORY on this machine

`AGENTS.md` and `Docs/README.md` both assert a canon split:

> "`Docs/` (capital D) = signed MVP product canon · `docs/` (lowercase) = UE 5.8 engineering"

**On disk that split does not exist.** Verified this session:

```
(Get-FileHash Docs\VISION_BOARD.md).Hash -eq (Get-FileHash docs\VISION_BOARD.md).Hash  →  True
Docs  →  441 md, 3999 KB
docs  →  441 md, 3999 KB   (identical listing, identical count)
```

Windows is case-insensitive, so `Docs` and `docs` are one tree of **441 markdown files, ~4 MB**.
Everything named in this map lives in that single directory tree.

`Docs/README.md` even anticipates the collision ("Git may only check out one of the two names
locally — clone on Linux CI or use a case-sensitive volume"). It is right about the hazard and
then treats the separation as real. **Consequence for CI:** on a case-sensitive checkout the two
trees would genuinely diverge and any doc I filed under `docs/Setup/` would be invisible to the
canon side. **Decision needed from the Lead** — see §7.

### 1.2 `Docs/README.md` is a wave log, not a topic index

It is chronological — `08a_INVENTORY`, `11c_HR_C_HANDOFF`, `17d_HS_EVIDENCE`, … — so it answers
*"what did WAVE B do?"* but not *"where is the camp-night rescue spec?"*. Finding a topic means
knowing its wave number. That is the "look everywhere" cost. This file replaces that use; the
README is left intact as history.

---

## 2. If you need X, read Y

| You need | Authoritative file | Status |
|---|---|---|
| Pillars, verbs, do-nots, feel | `Docs/canon/` — 12 small files, start at `README.md` | canon |
| **Theme, the game, T0 scope** | `Docs/VISION_BOARD.md` | canon, newest (V1 **SUPERSEDED**, V1b rescue, V2 spirit, **V2b gather-by-day tend-by-night**) |
| GDD slice | `Docs/01_GDD_MVP.md` | canon |
| Art direction | `Docs/02_ART_BIBLE.md` | canon |
| Ten master materials | `Docs/02_MATERIAL_SHEET.md` | **LOCKED** |
| Per-domain locked bibles | `Docs/DAYNIGHT_BIBLE.md` · `Docs/MOVEMENT_BIBLE.md` · `Docs/HOMESTEAD_BIBLE.md` · `Docs/COMBAT_DREAM_BIBLE.md` · `Docs/GATHER_CRAFT_BIBLE.md` · `Docs/SPIRIT_STEALTH_BIBLE.md` · `Docs/CAMERA_BIBLE.md` | **LOCKED** — all seven |
| Blender→UE export contract | `Docs/04_EXPORT_TABLE.md` | **LOCKED** contract |
| Never promote art to `Content/` | `Docs/20_UASSET_AI_POLICY.md` | policy (DEC-0019) |
| Zone/asset placement specs | `Lib/02_Zones/**/*.json` | **the machine-readable truth** |
| Image prompts (Grok) | `Docs/art/GROK_IMAGINE_PROMPTS.md` | in flight |
| **The 13+4 T0 MUSTs** | `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` | **canonical for T0** |
| The work queue | `Docs/TaskLists/T0_EXECUTION_PHASES.md` | active |
| Taste decisions Rounds 1–7 | `Docs/handoffs/TASTE_GATE_T0_ASSETS.md` | R1–6 RESOLVED, R7+ parked |
| Agent-owned decisions | `Docs/decisions/AGENT_DECISIONS.md` | DEC-0001…**0035** — all 35 ids present; file *order* is 0001-0026, 0033-0035, 0027-0031, so search by id not by position |
| UE 5.8 engineering | `Docs/SETUP.md`, `KNOWN_ERRORS.md`, `CONVENTIONS.md` | canon |
| Greybox measurement report | `docs/qa/GRAYBOX_SPEC_REPORT.md` | 4 blocking (regenerated 2026-10-03) |
| **Polish pass entry gates** | `Docs/37_POLISH_PASS_PROCESS.md` | active — enforces via `Content/Python/polish_readiness.py` |
| **Are we ready to polish?** | `Docs/qa/POLISH_READINESS.md` | generated; G-ENV / G-ASSET / G-FEEL all RED |
| **What is waiting on whom?** | same file, "Where everything is waiting" | generated; every blocked row declares agent / decide / do / env |
| **Decisions the Lead owes that no gate row can express** | `Docs/qa/POLISH_QUEUE.json` | 3 open, 1 deferred (Early Access paused 2026-10-04) |
| **Where the world actually lives** | `Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap` | the homestead, crumbs and field. NOT `MainMenu` — see KNOWN_ERRORS 2026-10-03 |
| **AI-agent practice, researched** | `Docs/38_AI_AGENT_PRACTICE.md` | research; read-only, gates no code |
| **What the human owns, and when to ask** | `docs/human-use/OWNERSHIP.md` | canon - Steer / Taste / Test |
| **Is the island really 180x100 in the engine?** | `Content/Python/measure_ue_island.py` -> `Docs/qa/UE_ISLAND_MEASUREMENT.json` | in-editor, read-only; gate row `env.ue_island_measured` |
| **Can we ship AI-assisted work on Steam?** | `Docs/20_UASSET_AI_POLICY.md` §4A | policy - Valve Jan 2026 disclosure rule |
| Map layout | `Maps/VS_MVP/README.md` | primary slice |

---

## 3. ⭐ The table that would have prevented the #17 error

**Why the must list drifts:** the must list answers *"what must be true"*, but *"is it built?"*
is answered in the **track docs** — one per subsystem, each with a Lead stamp. Nobody cross-links
them, so the must list's `Found` column goes stale silently.

**The rule this establishes: the `Found` column may only say `N` if no `APPROVE`-stamped track
doc claims the mechanic. This table is that cross-link, and §6 makes it machine-checked.**

| # | Must | Found — verified against `Source/` | Evidence |
|---|---|---|---|
| #1 | Wake / start day | Partial | `HomeWorldTimeOfDaySubsystem` |
| #2 | Kettle + herbs + sprint | **Logic done** | `TryBrewNodeKettleTea` + `TryNodeKettleInteractInFront`; `HomeWorld.T0.M2.TeaGateOffWithoutBrew`. **Level unbuilt** — no `NODE_KETTLE` actor |
| #3 | Plant given herb | Partial | — |
| #4 | Backpack → inventory | Partial | `HomeWorldInventorySubsystem` |
| #5 | *(full Y — excluded from bite order)* | **Y** | — |
| #6 | Collect herb seeds in field | Partial | `RES_HERB`, 55 refs |
| #7 | Rune unlock before bed→spirit | **Logic done** | `SetRuneGateUnlocked`; two-gate form in `HomeWorldFormGateTests.cpp`. **Level unbuilt** — no `NODE_RUNE` actor |
| #8 | Day camp eject | **Logic done** | `TryCampDayEject` emits `NODE_DAY_CAMP`/`EJECT_HOME`/`TOD_DAY`/`FORM_BODY`/`CAM_T0_CAMP_DAY` (`HomeWorldCharacter.cpp:1915`). **Level unbuilt** — no `NODE_DAY_CAMP` actor, no M8 test |
| #9 | Night w/o bed stays body | Partial | `bSpiritFormGate` + `bSpiritSleepGate`; `HomeWorldFormGateTests.cpp`, 4 tests |
| #10 | Planetside night boot home | **Logic done** | `StartGlideHome(bAllowNightPhase)` reusing the FALLBACK glide component — `NODE_GLIDER`/`EJECT_HOME`/`TOD_NIGHT_HOME`/`FORM_BODY` (`HomeWorldCharacter.cpp:2010`). **Level unbuilt** — no M10 test |
| #11 | Bed → spirit | Partial | `bSpiritSleepGateGranted` |
| #12 | Nurture planted herb | Partial | `HomeWorldNurtureComponent` |
| #13 | Home portal → camp portal | Partial | `HomeWorldShrinePortalComponent` |
| **#14** | **Camp night: 3 calmed** | **Logic done + tested; level unbuilt** | `TryEaseCampActor` / `IsFreedomUnlocked` / `…Strict`; 6 tests in `HomeWorldCampNightTests.cpp`. **Soft-latches** — no camp actors in any `.umap`, see §4 |
| #15 | What a spirit may touch | **Logic done + tested** | `HomeWorldCampNight::GetSpiritTouchVerdict`; `EvaluateSpiritTouch` logs every verdict; 2 tests |
| #16 | Free the captive, gated | **Logic done + tested; level unbuilt** | `FHomeWorldCampActorCalm::SatisfiesFreedomGate(Strict)`; `TryFreeCaptive`; 2 tests |
| **#17** | **Spirit-stealth** | **CLOSED — `APPROVE SS-A` 2026-09-21** ✅ | `Docs/25_SPIRIT_STEALTH_IMPL.md`; `HomeWorldSpiritStealthComponent.{h,cpp}`; `HomeWorldSpiritLitVolume.h`; `Docs/31_SPIRIT_STEALTH_FEEL.md` |

**A second false negative was found and fixed the same day.** #14's row read *"Lit stealth
volumes only; no guard/sleeper/soothe"* while `TryAvoidNodeGuard` and `TrySootheNodeSleeper` sat
in the same component, uncredited.

**A third, larger batch: four more `N`s that were all false.** #2 read *"No kettle/tea path"*,
#7 read *"`rune` = 0 hits"*, #8 read *"`eject` = 0"*, #10 read *"No reverse boot"*. Every one of
those was a **grep miss, not an absence** — `AHomeWorldCharacter` declares a named `T0 #n` hook
for each (`TryBrewNodeKettleTea`, `SetRuneGateUnlocked`, `TryCampDayEject`, `StartGlideHome`), and
#2/#7/#8's absence claims were contradicted by *passing tests*. The rows were written before the
code landed and never revisited, because revisiting them required opening `HomeWorldCharacter.h`
— a file no must-list row pointed at. **The lesson generalises: a `Found` column is a snapshot of
whatever you happened to have open.** So the `Found` state is now machine-compared against the
must list's own headings (§6, item 2) — two documents that must agree, checked rather than
remembered.

**Also already built, and previously uncredited to T0:** `HomeWorldBeastPad` +
`HomeWorldBeastTameComponent` (Wild→Cautious→Tamed→Helper, with transition logging);
six-resource inventory; `RES_HERB`.

---

## 4. The one real code defect the consolidation surfaced

`UHomeWorldSpiritStealthComponent` **soft-latches** #14 when the camp actor is absent:

```cpp
GuardsAvoidedCount = 1;   // reached even when Present?=N
UE_LOG(..., TEXT("...soft latch (KEEP-LOCAL actor missing; Present?=N...)"));
```

Defensible as gameplay (a reviewer is never hard-blocked by missing content) and **indefensible
as evidence** — #14 could report itself complete with **zero actors in the world**.

Resolution: keep both behaviours, keep them **distinguishable**. New
`FHomeWorldCampActorCalm::bSoftLatch` marks counts granted without a real actor;
`SatisfiesFreedomGateStrict()` excludes them and is what tests and prove scripts read;
`SatisfiesFreedomGate()` stays the gameplay path and logs `SOFT_LATCH_ONLY` so the difference is
visible in the log rather than hidden in a return value.

---

## 5. Quarantine — do not treat as canon

| Path | Why |
|---|---|
| `VisionBoard/MVP/**` | **Superseded for prototype scope** by `Docs/VISION_BOARD.md`. Holds theme + long-horizon campaign. |
| `Docs/Automation/AGENT_COMPANY.md` | Pre-swarm agent loop, **removed WAVE F**. Stub only. |
| `docs/TaskLists/DAILY_STATE.md`, `docs/SESSION_LOG.md` | Legacy task lists. Continuity is now handoffs + `SESSION_SUMMARY` + `swarm/PHASE_BOARD.md`. |
| `Docs/00_CANON.md` | **LOCKED P0 but pre-T0 topology** — its map tree predates the planet slice. Flagged, not quarantined; the Lead owns that call. |
| `Docs/TaskLists/**` (legacy, non-T0) | 55 files of wave-era lists. `T0_EXECUTION_PHASES.md` is the only active one. |
| `Docs/handoffs/**` (legacy, non-T0) | 158 files. Authority is the newest `SESSION_HANDOFF_*.md` only. |

---

## 6. This map is validated, and that is the point

`Content/Python/tests/test_canon_map.py` asserts:

1. every path named in §2 exists on disk;
2. **the §3 `Found` value for each must equals the state in that must's own heading in
   `T0_MECHANIC_INVENTORIES_V1.md`** — the two documents that both record built-ness are
   compared, so neither can drift alone;
3. §3 names `APPROVE` for #17 (the anti-regression: it may never read `N` again);
4. the ten masters and six resources named in §2 are the canon sets.

**Item 2 was previously claimed and not tested.** The original suite asserted only that must
*numbers* appeared in both files, so two documents could disagree on every state and still pass —
the overclaim was the same failure class as the stale rows it was meant to catch. It is now a
real comparison, normalised to one vocabulary (`N` / `Y` / `Partial` / `Logic done` / `CLOSED`),
and mutation-checked: flipping a state in either file has to fail the suite.

A map nobody checks is a map that goes stale — which is how #17 got misread in the first place.
**Deliberately over-specified rather than convenient:** a doc that fails its own test is cheaper
than a doc that is quietly wrong.

---

## 7. Open for the Lead

1. **`Docs` vs `docs`.** Keep one tree and delete the fiction from `AGENTS.md` + `Docs/README.md`,
   or genuinely split on a case-sensitive volume and keep the split. Today the instruction file
   describes a structure the working tree does not have — that is six lines of the most-read
   instructions in the repo being wrong. *(agent-recommended: one tree; the split costs more than
   it returns, and every cross-reference already ignores it)*
2. **Quarantine the 158 legacy handoffs and 55 legacy task lists**, or mark them read-only in
   place. They are the reason "look everywhere" is expensive today.
3. **`Docs/00_CANON.md`** — LOCKED P0 but pre-T0. Confirm supersession by `VISION_BOARD`.