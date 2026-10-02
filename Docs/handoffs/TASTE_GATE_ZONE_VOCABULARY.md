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

---

## Round 2 — PENDING (issued 2026-10-01 on Lead request)

Round 1 settled the *vocabulary*. It did not pick a first family, and that is
level design — Lead-owned. Three families (`heal`, `stealth`, `combat`) have no
volume anywhere in the 39-volume layout, and `gather` / `spirit` are measured
**non-conforming to their own locked signatures**, so the choice of first target
determines everything after it.

### Q7 — Which family gets the first prototype?

**RESOLVED 2026-10-01 → `spirit`.** The only family whose volumes are already placed
in the world *and* already fail its own locked signature, so the prototype has a measurable
before and after. Shrines exist on both homestead and planet-side, so it exercises "one
signature silhouette shared across sections". Clears half of the one collision finding.

### Q8 — Does the greybox author the see-through gap?

**RESOLVED 2026-10-01 → author the gap.** Four posts and a lintel, real topology,
hard-shaded, ~200 tris. The spirit signature is the only one whose defining feature is not a
proportion, so resizing boxes cannot satisfy it. The openness term in
`homeworld_graybox_silhouette.py` gets something real to measure instead of a proxy.

**What this commits the agent to:**

| # | Commitment | Why it follows |
|---|---|---|
| 1 | A spirit kit in `Lib/02_Zones/Spirit/` with real open-topology volumes | DEC-0024, one directory per family |
| 2 | The two shrines must move from `mid` band to `tall` | Measured non-conformance today |
| 3 | `SM_SpiritWound_01` must move from `flat` and lose its collision with `SM_BeastPad_01` | It is half of the one collision finding |
| 4 | **No `Content/` promote** | `Docs/20_UASSET_AI_POLICY.md` — drafts only, sidecar + `AI_ASSET_LOG` row on promote |
| 5 | Openness must be *measured from the gap*, not inferred from thickness | Q8 authorised real topology precisely so the proxy can be replaced |

⚠️ **Recorded honestly:** authoring the gap is the first time this pipeline writes geometry
that is *not* a box or a scaled box. The art bible (§5 Layer A, "cut facets on purpose, hard
edges") and DEC-0019 (never overwrite authored geometry) both apply, and the existing
`SM_Shrine_Homestead` / `SM_Shrine_Return` assemblies already exist in the blend with real
topology (base/posts/lintel/glow, per `MVP_EXPORT_MANIFEST.md`). **The prototype should
therefore *correct* those assemblies in place rather than author new ones beside them** —
otherwise the blend ends up with two rival spirit shrines and criterion 1 fails twice over.

---

Measured evidence, all from `docs/qa/GRAYBOX_SPEC_REPORT.md` and
`Lib/00_Core/GRAYBOX_LAYOUT.md`:

| Family | Volumes today | Measured conformance to its locked signature |
|---|---|---|
| `spirit` | 3 — `SM_Shrine_Homestead`, `SM_Shrine_Return`, `SM_SpiritWound_01` | **2 of 3 fail.** Both shrines read `mid`; `SM_SpiritWound_01` reads `flat`. Signature is *tall thin vertical with a see-through gap*. |
| `gather` | 1 — `SM_Gather_FirstHarvest` | 1 of 1 fails (reads `low`, signature `flat`). |
| `nurture_tame` | 1 — `SM_BeastPad_01` | conforms, but **collides** with `SM_SpiritWound_01` (both flat, aspects 0.05 / 0.17). |
| `build_place` | 14 | already prototyped — the homestead |
| `heal` / `stealth` / `combat` | **0** | nothing authored anywhere |

- **A (recommended)** — **`spirit`.** It is the only family whose volumes are *already placed in the world* and *already fail their own signature*, so the prototype has a measurable before and after, needs no new level layout invented, and exercises "one signature silhouette shared across sections" — spirit shrines exist on both homestead and planet-side. It also clears the one collision finding, since `SM_SpiritWound_01` is half of that pair.
- **B** — **`gather`.** The first family a player meets in Act 1 explore → fight → build, so the earliest teachable mechanic. Smaller delta than spirit (1 volume, not 2).
- **C** — **`combat`.** The clearest gap, and combat is placeholder-only by AGENTS.md so nothing deep is implied. But it authors a family whose mechanics are explicitly deferred, and combat placeholder art is the cheapest possible read to get wrong.
- **D** — **`heal` or `stealth`.** Also empty. Requires inventing a section from nothing, with no authored geometry to verify against.

### Q8 — If spirit: does the greybox author the *see-through gap*?

Consequence of Q7-A. The spirit signature is the only one whose defining feature is **not a proportion** — *"tall thin vertical **with a see-through gap**"*. A proportion metric cannot see a gap; the openness term in `homeworld_graybox_silhouette.py` only proxies it. So "spirit looks right at 20 m" cannot be finished by resizing boxes.

- **A (recommended)** — **Author the gap in greybox.** Four posts and a lintel, real topology, still hard-shaded and still ~200 tris. Costs more than a box, and it is the only way the "environment alone" read is honestly satisfied at the prototype tier. The openness proxy then has something real to measure.
- **B** — **Box-and-post silhouette, no authored gap.** Resize to tall-and-thin, mark openness as *deferred*, and accept that spirit is **not yet** announced correctly by shape alone. Cheapest, but the prototype then fails the rule the whole gate exists to enforce, and the report would say so.
- **C** — **Skip.** Leave spirit alone this round and author the first prototype in a family whose signature *is* pure proportion, where greybox can actually finish the job.

---

## Round log

- Round 1, 2026-10-01 — Q1 horizon lock, Q2 zone-type axis. **RESOLVED 2/2.**
- Round 2, 2026-10-01 — Q7 first family (**spirit**), Q8 the see-through gap (**author it**). **RESOLVED 2/2.**

**Gate CLOSED.** Round 3 opens only on Lead request, and only for a fork this gate did not settle.