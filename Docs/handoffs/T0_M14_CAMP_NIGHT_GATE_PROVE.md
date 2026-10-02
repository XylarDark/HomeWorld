# T0_M14_CAMP_NIGHT_GATE — DESKTOP prove packet (Test)

> ⚠️ **Rewritten 2026-10-02.** This packet used to score the beat as *avoid 1 guard + soothe 2
> sleepers*. The Lead corrected that, so the pass bar below is a different beat. The old
> `closed_fail` for "stealth-alone" survives in stronger form — it is now **soft-latch-only**,
> which is greppable and has its own closed_fail.

| Field | Value |
|-------|-------|
| **Bite** | `T0_M14_CAMP_NIGHT_GATE_V1` (MUST #14) · #15 touch rule · #16 the gate |
| **Map** | `Maps/VS_MVP` (camp night / spirit) |
| **Labels** | `NODE_GUARD` / `NODE_SLEEPER` / `NODE_CAPTIVE` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_CAMP_NIGHT` |
| **CAP** | **PARKED** |
| **Impl** | `UHomeWorldSpiritStealthComponent::TryEaseCampActor` + `IsFreedomUnlocked` + `IsFreedomUnlockedStrict` + `TryFreeCaptive` + `EvaluateSpiritTouch`, driven by `AHomeWorldCharacter::TryCampNight` via console `hw.CampNight`. Laws in `HomeWorldCampNight` namespace (`HomeWorldCampNightTypes.{h,cpp}`) |
| **Design** | `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` #14/#15/#16 (must list is canonical) · touch table in `Lib/02_Zones/combat/CAMP.json` |
| **Gate JSON (suggest)** | `Saved/t0_m14_camp_night_gate.json` |

## The beat, as corrected

> *"A guard will be awake that you need to help ease their thoughts so that they fall asleep, the
> other two will be asleep and you can ease their thoughts too to keep them sleeping."*
> — Lead, 2026-10-02

All **three** camp actors are calmed. One guard **awake → eased → asleep**; two sleepers
**asleep → eased so they stay asleep**. Freedom opens when **all three are eased AND asleep.**

Two consequences that catch people out:

- **The guard is not "avoided".** Avoiding them and leaving them awake is the old reading, and
  under the corrected law it *never* opens the gate. There is no avoid-the-guard victory.
- **"Keep them sleeping" has to be able to fail.** If a sleeper wakes, the gate closes again, and
  re-easing them does *not* put them back to sleep — that verb is maintenance, not a sedative.

## What a spirit may touch (MUST #15)

A spirit has no hands. It may work on **what holds and carries**, and apply **care to a mind**.

| Target | Verdict |
|---|---|
| `Soil` | **ALLOWED** — tending is the night's verb (#12) |
| `Lashings` | **ALLOWED** — untying is the rescue (#16) |
| `ActorMind` | **ALLOWED** — easing thoughts is the care verb (#14) |
| `ActorBody` | **REFUSED** — ease their thoughts, do not touch them |

`ActorMind` being allowed is the exception that lets #14 and #16 exist. `ActorBody` being
refused is what stops the beat becoming about dragging bodies instead of easing minds.

## Arrange

1. PIE `Maps/VS_MVP` → homestead / body / Day if needed for rune path.
2. **Spirit prereq (#11 path):** `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` → expect `NODE_BED:` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT`. Confirm `GetIsSpiritForm`.
3. **Optional camp route (#13):** `hw.Portal.Camp` → camp arrive soft OK; not required for Source emit soft latch.
4. CAP **PARKED** — no still product / mood bot PASS.
5. Camp night: console `hw.CampNight` (primary) → ease the **guard** and **both sleepers**; expect three `CAMP: ease ok` lines.
6. **KEEP-LOCAL:** if `NODE_GUARD` / `NODE_SLEEPER` actors are absent, every count soft-latches and logs `SOFT_LATCH_ONLY`. That is **not** a pass — see the strict row below. Do **not** commit `.uasset` / `.umap` / invent PROP rows for this Act.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| All three calmed | `CAMP: ease ok (role=GUARD` **and** two `role=SLEEPER` lines | A 2nd `hw.CampNight` re-log | Fewer than three ease lines, or `CAMP: ease skipped - need FORM_SPIRIT` |
| Eased **AND** asleep | `NODE_GUARD: … CAM_T0_CAMP_NIGHT (all 3 calmed …; strict=…)` | — | Any ease line with `asleep=0` on the guard |
| **Strict = evidence** | `strict=1` in the camp-night line | `strict=0` with `world_actor=0` — soft latch, playable but unproven | Scoring a `strict=0` run as MUST #14 PASS |
| **Soft latch is visible** | `CAMP: SOFT_LATCH_ONLY - gameplay gate is open but every count came from a missing actor` | — | A run with no `SOFT_LATCH_ONLY` **and** `strict=0` — the fail-open is silent, which is the defect |
| Free is gated | `CAMP: free REFUSED - 2/3 calm, strict=0` while short | `CAMP: CAPTIVE FREED` after a second free attempt | `CAMP: CAPTIVE FREED` at 2/3 calm |
| Spirit + night | `FORM_SPIRIT` + spirit phase | Re-sync form noise | Body-form camp-night scored as #14 |
| Touch table | `TOUCH: target=ACTOR_BODY form=SPIRIT verdict=REFUSED` and `target=LASHINGS … verdict=ALLOWED` | — | `ActorBody` scoring ALLOWED, or any refusal with no `TOUCH:` log line |
| Soothe ≠ convert | Path uses `TryEaseCampActor` — **not** `ReportFoeConverted` / `hw.Conversion.Test` | Unrelated convert stub logs | Scoring a convert stub as calming |
| Stealth module | Via `UHomeWorldSpiritStealthComponent` — **no** parallel stealth service | — | New stealth service / invented API |
| GP_SS_Lit anti | Script-only `GP_SS_Lit_*` / lit-volume alone ≠ #14 PASS | Unrelated STEALTH: LIT logs | Treating lit volumes alone as the camp-night beat |

## Pass bar (team)

- After #11 spirit path: `hw.CampNight` → three `CAMP: ease ok` lines **and** a greppable `NODE_GUARD: NODE_SLEEPER TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_CAMP_NIGHT` carrying `strict=1`.
- **A `strict=0` run is playable and is still NOT a pass.** It means three counts came from actors
  that do not exist. Say so in the report; do not round it up.
- `CAMP: CAPTIVE FREED` only after 3/3.
- **closed_fail** if: script-only `GP_SS_Lit_*`, a silent soft latch, convert-as-calm, two-of-three
  freeing, `ActorBody` allowed, or a body-form camp night scored as MUST #14.
- KEEP-LOCAL soft latch OK **as a playable path only** — never commit `.uasset` / `.umap` /
  invent PROP for this prove.
- Other T0 MUST **DEFER**. Design invent left **untouched**. No PROP JSON invent.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`.
2. `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` → expect `NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT ...`.
3. **Negative:** body form without spirit → `hw.CampNight` fails (`CAMP: ease skipped - need FORM_SPIRIT`); do **not** score as #14.
4. **Negative:** `hw.Conversion.Test` / convert stub alone → **no** `CAMP: ease ok` line; convert ≠ calm; do **not** score as #14.
5. **Negative:** walk `GP_SS_Lit_*` / `hw.Stealth.ForceLit` alone → STEALTH lit/alert may log, but **no** camp-night line; stealth-alone = closed_fail.
6. `hw.CampNight` → expect three `CAMP: ease ok` lines (1 guard, 2 sleepers) and `NODE_GUARD: … CAM_T0_CAMP_NIGHT (all 3 calmed …; strict=…)`.
7. **Soft-latch check:** with no `NODE_GUARD` / `NODE_SLEEPER` in the level, `strict=0` and a `CAMP: SOFT_LATCH_ONLY` line **must** appear. If `strict=0` appears with no such line, the fail-open went silent — that is a defect, not a pass.
8. `hw.CampNight` again → already-granted soft path (still greppable).
9. **Free:** expect `CAMP: CAPTIVE FREED` at 3/3, or `CAMP: free REFUSED - n/3 calm, strict=…` below that.
10. Confirm `IsCampNightGranted`; `GetCalmedActorCount() == 3`; `IsFreedomUnlockedStrict()`.
11. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m14_camp_night_gate.json` after greps.

## World-free regression (no PIE needed)

`HomeWorld.T0.M14.*` / `M15.*` / `M16.*` run headless and cover every law above including the
ones a paste-prove cannot: asleep-but-not-eased, eased-but-awake, killed, converted, the strict
gate refusing a soft latch, and `ActorBody` refused.

```
UnrealEditor-Cmd.exe HomeWorld.uproject -ExecCmds="Automation RunTests HomeWorld.T0; Quit" -unattended -nopause -NullRHI
```

| Test | Pins |
|------|------|
| `M14.ActorStartStates` | guard starts awake, sleepers start asleep, gate is 3 wide |
| `M14.EaseDirection` | easing the guard is the act that sleeps them; easing a sleeper only maintains |
| `M14.SoftLatchContained` | gameplay gate tolerates soft latches, **strict does not** |
| `M14.RosterNotEmpty` | the empty-array fail-open cannot report the beat complete |
| `M14.CompletionRedirectsToGate` | two sleepers alone do **not** complete #14 |
| `M15.SpiritTouchTable` | the four-row table, each with a logged reason |
| `M15.TouchThroughComponent` | the table enforced and logged through the component |
| `M16.CalmGateLaw` | eased AND asleep; killed/converted never count |
| `M16.FreedomGate` | 2/3 refuses, 3/3 opens, waking closes it again, freeing follows the gate |

## Source symbols (files-only greps)

`TryCampNight` / `IsCampNightGranted` / `bCampNightGranted` / `TryEaseCampActor` / `IsFreedomUnlocked` / `IsFreedomUnlockedStrict` / `TryFreeCaptive` / `EvaluateSpiritTouch` / `GetCalmedActorCount` / `GetGatedActorCount` / `GetSpiritTouchVerdict` / `SatisfiesFreedomGate` / `SatisfiesFreedomGateStrict` / `bSoftLatch` / `SOFT_LATCH_ONLY` / `UHomeWorldSpiritStealthComponent` / `NODE_GUARD` / `NODE_SLEEPER` / `NODE_CAPTIVE` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_CAMP_NIGHT` / `hw.CampNight` / `hw.Bed.SleepSpirit` / `hw.Rune.Unlock` / `closed_fail` (this packet) / convert / `ReportFoeConverted` / `GP_SS_Lit` / stealth-alone (anti)

**Superseded, still compiled, no longer the gate:** `TryAvoidNodeGuard` / `TrySootheNodeSleeper` /
`GetGuardsAvoidedThisSession` / `GetSleepersSoothedThisSession`. Kept callable so existing
Blueprint graphs keep resolving; marked `⚠️ LEGACY` in the header. Do not score a run off them.

## Architecture Trade-Offs A–E (cite)

| Layer | Decision |
|-------|----------|
| **A — Contract** | Labels `NODE_GUARD` · `NODE_SLEEPER` · `NODE_CAPTIVE` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT`; beat = **all 3 calmed** (eased **and** asleep) |
| **B — Module** | Existing `UHomeWorldSpiritStealthComponent` — **no** second stealth service; laws as pure functions in `HomeWorldCampNight` so they are testable without a world; convert ≠ calm |
| **C — Evidence** | `IsFreedomUnlockedStrict()` is the evidence half, `IsFreedomUnlocked()` the courtesy half; world-free automation tests + this prove packet; CAP **PARKED** |
| **D — Seats** | Implement owns Act Source; Conductor owns MCP/PIE |
| **E — Stability** | Script-only `GP_SS_Lit_*` / stealth-alone / convert-as-calm / 2-of-three freeing / `ActorBody` allowed / PROP invent as #14 = `closed_fail`; no invented guard, calm or WP APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. #11
bed spirit = **prereq** (run first; do not re-Act beyond unlock/sleep). Suggest gate JSON path:
`Saved/t0_m14_camp_night_gate.json`. Never commit `.uasset` / `.umap`. Design invent untouched.
Do **not** open other MUSTs.

**Report `strict=` explicitly.** A camp night that passed on soft latches is a playable build with
an unbuilt level — a real and useful state, but writing it up as `APPROVE` would be the exact
fail-open this beat is designed to catch.