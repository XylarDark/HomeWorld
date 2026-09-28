# T0_M9_NIGHT_HOME_GATE_V1 — MUST #9 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M9_NIGHT_HOME_GATE_V1` |
| **MUST** | #9 — Homeworld night w/o bed: no spirit; day abilities off |
| **Present?** | **Y** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #9 — **not** stale Partial from older `T0_MECHANIC_INVENTORIES_V1`) |
| **CAP** | **CAP PARKED** (stills confirm-only; night mood = Lead-only; bots must **not** PASS night taste) |
| **Host** | **CLOUD** docs-only (Contents API; Cursor cloud may be capped) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Regression / law lock — freezes Arrange + DONE-WHEN + prove labels for **Test files-only**. **Not** a feature Act invent. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q note) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` · `PROP_INVENTORY_V1` · `GAME_FEEL_CANON_V1` · `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` · older `T0_MECHANIC_INVENTORIES_V1` #9 shape (Found updated to gap **Y**) · historical prove `T0_M9_NIGHT_HOME_GATE_PROVE.md` / Source `#230` |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #9 (`TOD_NIGHT_HOME`) for Test files-only regression / law lock when Present?=**Y** (gap SoT), without opening a feature Act or reopening CAP?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision for this bite (inventory, **not** API invent) |
|-------|--------------------------------------------------------|
| **A — Contract** | Prove contract = named labels `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` (negative). Callers see form via **named gates** (sleep + rune + location policy), not phase alone. |
| **B — Module** | Form / sleep / rune gate = **Layer B** deep module (+ **A** contract). **No second form service.** Hide phase auto-spirit behind `CanEnterSpiritForm()` / existing character TOD path (`ApplyFormForPhase`). |
| **C — Evidence** | Law prove = FORM/logs + verb reject greps. Bright/day capture defaults do **not** apply to night mood PASS. CAP product stays **PARKED**. |
| **D — Seats** | Design freezes Arrange/DONE-WHEN here; Test scores files-only (and may cite historical Source prove). Implement does **not** Act in this bite. Conductor alone opens later Acts (#11/#7). |
| **E — Stability** | Spirit without bed (or without named sleep+rune gates) = **`closed_fail`** vs T0 law — bounded fail, not invent-retry / disable-Night workaround. |

**15-q:** Do **not** invent WP/form APIs. Prefer cite existing form/TOD prove patterns (`ApplyFormForPhase`, `CanEnterSpiritForm`, `AreDayBodyAbilitiesAllowed`, `FORM:` logs). Schema before data — **no new schema** this packet.

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

Only these prove labels (exclusive freeze for this bite):

| Label | Role |
|-------|------|
| `TOD_NIGHT_HOME` | Homeworld Night/Dusk without successful bed |
| `FORM_BODY` | Must remain body; no spirit |
| `NODE_BED` | **Negative prove** — absence of successful bed (must **not** be required for this PASS) |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` inventory freeze ∩ gap walk suggested prove labels for #9. `PROP_INVENTORY_V1` cites `NODE_BED` / `ENV_T0_BED` for envelope identity; this bite uses `NODE_BED` only as **negative**.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | On homestead at Night/Dusk **without** successful bed: stay `FORM_BODY`; **no** spirit; **day abilities off**. Spirit without bed = **`closed_fail`**. |
| **Found (gap SoT = Y)** | Source `#230` / `ApplyFormForPhase`: Night/Dusk → spirit **only** if `CanEnterSpiritForm()` (`bSpiritSleepGateGranted && bRuneGateUnlocked`). `AreDayBodyAbilitiesAllowed` rejects day verbs; logs `FORM: day verb rejected … (TOD_NIGHT_HOME …)`. Historical prove packet `T0_M9_NIGHT_HOME_GATE_PROVE.md` / `t0_m9_desktop_prove.py` exist. **Present?=Y** — law already implemented; this packet locks regression Arrange/DONE-WHEN for Test. |
| **Arrange** | Homestead (`Maps/VS_MVP`) · force Night/Dusk **without** bed · **no** `GoToBed` · bright/day capture defaults do **not** apply to night mood PASS (bots must not PASS night taste; prove is FORM/logs **not** mood) · CAP **PARKED** |
| **DONE-WHEN** | See § DONE-WHEN below (Test can run files-only greps on this md; Source prove already exists historically — **no DESKTOP Act** required from this Design packet) |
| **Depends / HOLD** | Bed path still incomplete (#11) — **Depends/HOLD**, not this bite's Act. Rune unlock (#7) separate. All other T0 MUST **DEFER**. |
| **Anti** | Do not “fix” by disabling Night · soft-kidnap / shrine ≠ this law · do not require successful `NODE_BED` for this PASS · no CAP reopen · no night bot mood PASS · no Content/Python/Source · no `.uasset` · no invent form/WP APIs · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → homestead spawn (body, Day start OK).
2. **Negative bed:** do **not** interact bed / do **not** call `hw.GoToBed` for the primary prove (`NODE_BED` absence).
3. Force Night (and optionally Dusk): existing TOD cheat only (e.g. `hw.TimeOfDay.SetPhase` Night/Dusk) — **without** granting sleep+rune gates.
4. Attempt a day body verb (sprint / mantle) while Night@home body.
5. **Prove class:** FORM/logs + verb reject — **not** night mood / NightMix taste. Bright/day capture defaults do **not** apply as night mood PASS. CAP stays **PARKED** (`GAME_FEEL_CANON_V1`: night mood Lead-only).

---

## DONE-WHEN (Test files-only)

Test may score this packet files-only on this markdown (and may cite historical Source prove — this packet does **not** require DESKTOP Act).

### Law

- Night@home w/o bed → stay `FORM_BODY`
- Day abilities off (day verbs rejected / not allowed)
- Spirit without bed = **`closed_fail`** vs T0 law

### Grep strings (must appear in this packet for Test harness)

`TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` · `closed_fail` · `CAP PARKED` / `PARKED` · `Arrange` · `DONE-WHEN`

### Negative prove

`NODE_BED` must **NOT** be required for this PASS — prove is the **absence** of successful bed (no GoToBed / no sleep-gate grant). Successful bed→spirit remains #11 (after #7 rune) and is **out of scope**.

### Historical Source note (cite only)

Gap walk / `#230` already wire `ApplyFormForPhase` + gates + `FORM: day verb rejected … (TOD_NIGHT_HOME …)`. This Design packet freezes the **law lock** for Test regression; it does **not** reopen Implement Act.

---

## HOLD / DEFER / Anti (locked)

- All other T0 MUST **DEFER**
- #11 bed→spirit and #7 rune = **separate** bites (Depends/HOLD only here)
- No CAP reopen (CAP stays **PARKED**)
- No Content / Python / Source / `.uasset` / `.umap`
- No DESKTOP PASS/FAIL from Design
- No invent WP/form APIs; schema before data — prefer existing form/TOD prove patterns
- Design does **not** self-APPROVE

---

## Ball

**Test files-only** after draft PR (grep DONE-WHEN strings + law lock). Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M9_NIGHT_HOME_GATE_V1.md` · Bite: `T0_M9_NIGHT_HOME_GATE_V1` only · Present?=Y (gap SoT) · CAP PARKED · exclusive path.*
