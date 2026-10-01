# TASTE_GATE_ZONE_VOCABULARY — env-art horizon, and which "zone type" is the product

| Field | Value |
|-------|-------|
| **Gate id** | `TG-ZONE-VOCABULARY` |
| **Status** | **RESOLVED** — Round 1, 2026-10-01, 2/2 forks |
| **Job** | **taste** (product scope + game mechanic design) |
| **Heuristic** | Docs/28 **6** — next *product* track was TBD; the Lead has now named one (environment art design + zone types + mechanics), which unblocks this interview |
| **Owner** | human |
| **Opened by** | Lead request, 2026-10-01 — *"prototype the environment art design as well and establish some zone types and mesh them with game mechanics. Setup an interview to further refire our taste scope here"* |
| **Precedence** | taste-profile §2 — max **2 questions per turn**; scope-refinement R6 (Rounds 1–4 CLOSED, do not re-ask) |
| **Upstream** | [TASTE_GATE_ZONE_FAMILY.md](TASTE_GATE_ZONE_FAMILY.md) (8/8) · [TASTE_GATE_GRAYBOX_SILHOUETTE.md](TASTE_GATE_GRAYBOX_SILHOUETTE.md) (2/2) · [swarm/PHASE_BOARD.md](../../swarm/PHASE_BOARD.md) · [VisionBoard/Planetoid/PLANETOID_BIOMES.md](../../VisionBoard/Planetoid/PLANETOID_BIOMES.md) · `Source/HomeWorld/HomeWorldPlanetoidTypes.h` |

---

## Conflicting sentences, with sources

Scope-refinement step 1 requires naming the conflicts before asking anything.

| # | Sentence | File |
|---|---|---|
| 1 | *"Lead lock 2026-09-27 ET: CAP + EA DROPPED from backlog; horizon = harness/bot only"* | `swarm/PHASE_BOARD.md` (Current phase) |
| 2 | *"CAP product track and **EA/env art are off the backlog** (not shelved). No CAP Do, no EA SCOUT"* | `swarm/PHASE_BOARD.md` (CAP/EA backlog) |
| 3 | *"I also want to prototype the environment art design as well and establish some zone types"* | Lead chat, 2026-10-01 |
| 4 | *"A section **is** a family of mechanics you may use there. Geography is authored to announce the mechanic family."* | `TASTE_GATE_ZONE_FAMILY.md` (fork A) |
| 5 | *"Planetoid biome type... **four biomes** (Desert, Forest, Marsh, Canyon)"* | `HomeWorldPlanetoidTypes.h` / `PLANETOID_BIOMES.md` |
| 6 | *"Zone alignment: what the player does there (**fight, harvest, empower**)"* | `HomeWorldPlanetoidTypes.h` / `PLANETOID_BIOMES.md` |

⚠️ **1 + 2 contradict 3 directly.** The Lead's lock says env art is *off* the backlog, not
merely unstarted. That lock is the Lead's to lift, and it is the first question.

⚠️ **4, 5 and 6 are two different axes both called "zone".** The seven mechanic families
are *functional* (what you can do). The four biomes are *geographic* (where you are). Three
alignments are a third cut (Corrupted/Neutral/Positive). Nothing in the tree says which one
"zone type" means, and the code already ships a 4 × 3 = 12-combination enums pair that
TG-ZONE-FAMILY never mentioned. This is the collision that will produce three vocabularies
in one prototype if it is not settled first.

---

## Settled decisions

| Fork | Answer | Consequence |
|---|---|---|
| **Q1 — horizon** | **Lift the lock, scoped to one prototype** (2026-10-01, Lead) | `PHASE_BOARD.md` Current phase becomes **"harness idle; env-art prototype is the live ball."** One zone type, greybox tier, no new biome art. Harness work parks rather than being abandoned. The 2026-09-27 lock is **superseded, not deleted** — the history stays readable. |
| **Q2 — zone-type axis** | **Mechanic family is the zone type** (2026-10-01, Lead) | The seven TG-ZONE-FAMILY families are the art and level vocabulary. `EBiomeType` (Desert/Forest/Marsh/Canyon) drops to **terrain dressing and weather only** and leaves the art vocabulary. `EPlanetoidAlignment` is not a zone type. Art bible §8 shape language keys off family. |

### Scope of the lift — what it does and does not authorise

**Authorised:** one greybox-tier zone prototype, cut for **one** mechanic family. The
`family` field on specs. Art bible §8 gains a per-family silhouette table.

**Not authorised by this gate:** new biome art, a second family prototype, a `Docs/` track
beyond the art bible edit, changing the engine lock or the platform lock, or promoting the
prototype to `Content/`. Anything else is a fresh gate.

⚠️ **Recorded for whoever implements this:** `HomeWorldPlanetoidTypes.h` ships a
`EBiomeType` + `EPlanetoidAlignment` pair (4 × 3 = 12 combinations) and
`AHomeWorldGameMode` exposes `GetCurrentZoneBiome()` / `GetCurrentZoneAlignment()`. Per Q2
those **stay** — they are not deleted, and biome keeps working as a terrain-dressing input.
What changes is that **neither is a zone type for art or level design purposes.** Adding a
`UHomeWorldZoneType` keyed to the seven families is the implementation question, and it is
architecture — agent-owned, logged as DEC-0023, not gated here.

---

## Round 1 — RESOLVED 2026-10-01

- **Q1** — "Lift the lock, scoped to one prototype" chosen over hold-separately and over skip.
- **Q2** — "Mechanic family is the zone type" chosen over biome-as-zone-type and over both-as-levels.

---

## Rejected on the record

| Rejected | Why |
|---|---|
| Agent picking the horizon | Scope/priority is the Lead's. Reopening a documented Lead lock is not an architecture call. |
| Treating `EBiomeType` as already-settled | It predates TG-ZONE-FAMILY (2026-03 vs 2026-10-01) and was never reconciled with it. Shipped code is not a decision the Lead made *about this fork*. |
| Re-asking scope rounds 1–4 | Closed 2026-09-24. Co-op, persistence, day/night loop, look automation are settled and are not reopened here. |

## Round log

- Round 1, 2026-10-01 — Q1 horizon lock, Q2 zone-type axis. **RESOLVED 2/2.**
- Round 2 — not started. Opens only when the Lead asks, and only for a fork this gate did not settle.