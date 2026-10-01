# TASTE_GATE_ZONE_FAMILY — world sections, mechanic families, and diegetic boundaries

| Field | Value |
|---|---|
| **Gate id** | `TG-ZONE-FAMILY` |
| **Status** | **RESOLVED** — Rounds 1–4 complete 2026-10-01. Answers are durable taste; see §Settled |
| **Job** | **taste** (game mechanic design) |
| **Heuristic** | Docs/28 #6 — *next product track undefined and a design fork blocks it* |
| **Owner** | human |
| **Opened by** | Lead request, 2026-10-01 — "interviewed on game feel … distance, movement, scale, interaction … invisible walls explained by environmental limits … large world made in sections with each section related to a family of gameplay mechanics" |
| **Precedence** | taste-profile §2 — max **2 questions per turn**; §4 — next *product* track is a gap, and this interview is the sanctioned way to fill it |
| **Adjacent** | [00_CANON.md](../../Docs/00_CANON.md) · [26_TASTE_NEXT.md](../../Docs/26_TASTE_NEXT.md) (Night Feel, CLOSED) · [09_FALLBACK_GLIDE.md](../../Docs/09_FALLBACK_GLIDE.md) |

---

## Why this gate exists

Three of the Lead's asks are **mechanic design**, which the 2026-10-01 ownership reset reserves for the human:

1. Invisible walls must be **explained by environmental limits** (diegetic, never arbitrary).
2. A large world **made in sections**, each section bound to a **family of gameplay mechanics**.
3. The player should **know what is happening** by virtue of being in a zone.

These are not architecture and not a test bar, so they are not mine to invent or to gate
away. They also gate downstream work: distances, sightlines, walk times, section volume,
and therefore the greybox asset pipeline and the PCG scatter design. **Nothing about
world sectioning can be laid out until this fork is answered.**

## What is already locked and must not be re-opened

| Locked | Source |
|---|---|
| Feeling target: *stranger in ~3 s reads safe home above a living world* | Docs/26 |
| Shot list is five shots | [00_SHOTLIST.md](../../Docs/00_SHOTLIST.md) |
| Player is the scale ruler; adult 1.7–1.8 m; enemies much larger | art bible §10 |
| No free-flight sim; glide is a committed traversal verb with a fallback | canon / Docs/09 |
| Combat is placeholder — strips sin, converts foes; no deep combat system | AGENTS.md |
| Homestead is the hub; planetside is a locked location test | art bible §2 |

## The open forks, in dependency order

| # | Fork | Blocks | Round |
|---|---|---|---|
| A | Are sections **geographic** (places that happen to host a mechanic family) or **functional** (defined by what you can do there, geography follows)? | section volume, boundary placement, everything downstream | **1** |
| B | What physical thing is the boundary — the "environmental limit"? | diegetic walls, cliff/water/void/thorn vocabulary | **1** |
| C | How is the mechanic family **communicated** — environment alone, or environment + restrained UI? | readability budget, art bible §6 camera, no-UI-vs-UI | 2 |
| D | What is the unit of travel — walk / glide / portal — between sections? | distance, walk-time targets in [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) §6 | 3 |
| E | What are the mechanic **families** themselves? | section count, section identity | 4 |

Ordering is deliberate: **A and B first** because section volume and boundary type are
load-bearing for every distance and scale decision. C follows the communication budget.
D depends on A. E is last because the families can be named once the section model exists.

## Settled decisions

| Fork | Answer | Consequence |
|---|---|---|
| **A — section model** | **Functional** (2026-10-01, Lead chat) | A section **is** a family of mechanics you may use there. Geography is **authored to announce** the mechanic family, not the other way round. So "am I in a gathering zone" must be legible from shape, material and lighting *before* any UI fires. Terrain, scale and sightline work now serve a specific mechanic signal each. |
| **B — boundary** | **Terrain** (2026-10-01, Lead chat) | Boundaries are **cliff face, ravine, treeline, or water**. No velocity barrier, no UI wall, no invisible trigger the fiction cannot account for. Cheapest to build at greybox tier and diegetic by default. Note this couples the boundary to the planetoid read (close horizon, ground bends away) — a boundary must be readable as *terrain that continues out of view*, not as a wall that was placed. |
| **C — announcement** | **Environment alone** (2026-10-01, Lead chat) | Terrain, material, creature and light changes tell the player what they can do here. **UI appears only after the player acts, and only names it.** No entry label, no persistent marker. Consequence: every mechanic family must be taught by *shape, material and light alone*, and the read has to be strong enough to do that work unaided. This is the most expensive of the three options and is now a hard requirement on the asset pipeline. |
| **D — section size** | **≈1 minute on foot** (2026-10-01, Lead chat) | One section ≈ 60 s of walking, matching the planet-path pacing already specified in [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) §6. At the assumed 1.4 m/s stroll that is **≈84 m of travel per section**. Sections are sized to be *learned*, not traversed: a mechanic family must be understood before attention moves on. |
| **E — traversal** | **Walk between adjacent sections; glide only for real gaps** (2026-10-01, Lead chat) | Glide is a **place-to-place traversal with a visible launch and a visible landing** — the existing lookout pad / glider perch / landing circle, not a convenience hop. Preserves the canon's rejection of a free-flight sim and keeps glide special. The ~84 m figure therefore describes *the section*, not the gap between sections: a glide gap is a deliberate distance event, and both ends of it must read as terrain (per decision **B**). |
| **F — scale read** | **Lookout dominance** (2026-10-01, Lead chat) | From any high point the player can see **the next two sections** and recognise their silhouette families. Scale is learned by *looking*, not by walking. This reuses the existing `CAM_Hero` sightline checklist in [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) §7 and the 20 m+ vista camera locked in art bible §6. |
| **G — family mapping** | **One mechanic family per section, taught in isolation** (2026-10-01, Lead chat) | A gathering zone looks like a gathering zone and nothing else. This is the decision that makes **environment-alone** actually buildable: the read is legible by construction rather than by luck. Cost accepted: more distinct silhouette families to model and more sections to author. Each family gets its own **shape language, material pairing, and light signature**. |
| **H — leaving** | **The section releases you** (2026-10-01, Lead chat) | Having used the mechanic family, the terrain opens — a ravine becomes fordable, a treeline thins, a cliff reveals a descent. **The boundary is a consequence of play**, so it can never feel arbitrary, and it satisfies the Lead's original requirement that invisible walls be explained by environmental limits. |

---

## The settled feel, as one statement

> A **section** is one mechanic family, ~84 m of walking, taught entirely by terrain, material and light.
> You **leave** it by having used it — the ground opens because you did the thing.
> Boundaries are always **terrain that continues out of view**: cliff, ravine, treeline, water.
> You **see** the next two sections from any high point, and learn the world's shape by looking rather than walking.
> **Glide** crosses real gaps only, from a visible launch to a visible landing.

**The single hardest consequence:** *"environment alone"* + *"one family per section"* means **silhouette distinctness is a mechanical requirement, not art polish.** A mechanic family that cannot be told apart by shape from 20 m away has failed its section. No HUD is permitted to rescue it.

That converts the greybox finding into a hard gate: 14 of 39 volumes in [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) are ≤0.5 m thin, and cabin / shrine / pine stand / forest mass all resolve to aspect ratio 1.00. Under these decisions that is a **blocking defect**, not tidiness.

**What this now fixes in the pipeline:** each family needs a signature silhouette, so the `kit/*.json` spec gains a `family` field, and the greybox builder gains a **silhouette-collision assertion** — two volumes from different families may not share an aspect ratio at the same scale band. That assertion is an architecture decision, not a taste question, and is logged in [AGENT_DECISIONS.md](../../Docs/decisions/AGENT_DECISIONS.md).

## Rejected on the record

| Rejected | Why |
|---|---|
| Hard UI / velocity barrier | Fails the Lead's original requirement that walls be explained by environmental limits. |
| Persistent per-zone marker (R2 Q3-B) | Under "environment alone" a persistent marker is UI-adjacent; rejected in favour of form. |
| UI label on entry (R2 Q3-C) | Turns a place into a menu; explicitly rejected. |
| Journey-time dominance (R3 Q6-B) | Sense of distance strong, but it works against learning mechanic families by looking. |
| Vertical dominance (R3 Q6-C) | Best image, highest cost; the planetoid read is preserved inside lookout dominance instead. |
| Portal traversal (R3 Q5-C) | Already in canon, but compresses distance and makes "large world" a claim rather than a felt experience. |
| Two paired families per section (R4 Q7-B) | Contradicts "environment alone" — the environment would have to announce two things at once. |
| Player-chosen exit / both (R4 Q8-B, Q8-C) | Makes the world read as pre-built rather than responsive; C additionally risks a family never being taught. |

---

### Consequence chain from Rounds 1–2 (this is the load-bearing output)

These four answers interlock, and the chain below is what downstream work must satisfy:

1. **Functional + terrain boundaries** ⇒ a boundary is a *change of mechanic family*, and it is expressed as terrain that continues out of view. Therefore a section edge is a **material and silhouette change** as much as a height change — a treeline or a ravine reads as terrain, so the mechanic family has to change *at* it.
2. **Environment alone** ⇒ the read is carried by **shape language, master material, and lighting** — exactly the three levers in art bible §7 (palette/lighting) and §8 (shape language). No HUD is permitted to rescue a weak read, so **a mechanic family that cannot be told apart by silhouette is not finished.**
3. **Environment alone + functional** ⇒ **silhouette distinctness stops being art polish and becomes a mechanical requirement.** The earlier greybox finding — 14 of 39 volumes are 0.5 m thin or less, and a cabin / shrine / pine stand / forest mass all collapse to aspect ratio 1.00 — is now a *blocking defect against this decision*, not a tidiness issue. Distinct primitive and proportion per mechanic family is required to make the zone announce itself.
4. **≈84 m per section** ⇒ at greybox tier a section is roughly **20–40 volumes**. That is the real asset budget per zone, and it is the number the `kit/*.json` spec should be sized against.

**Open sub-problem for the agent (not a taste question):** given ~84 m sections and terrain boundaries, PCG scatter density and the foliage families that carry "which family is this" are an architecture call. Logged in [AGENT_DECISIONS.md](../../Docs/decisions/AGENT_DECISIONS.md); no gate needed.

---

## Round log

### Round 1 — RESOLVED 2026-10-01

**Q1 — What makes a section a section?**
- **A (recommended)** — **Functional.** A section is *a family of mechanics you may use here*; geography is then designed to announce it. Directly serves "the player knows what is happening."
- **B** — **Geographic.** Sections are places (valley, ridge, hollow); each happens to host a mechanic family. Diegetic boundaries come free, but "what is happening here" is weaker.
- **C** — **Both, deliberately layered.** A geographic region contains one or more functional sections; boundary is geographic, content is functional. More authored work, strongest result.

**Q2 — What is the wall made of?**
- **A (recommended)** — **Terrain that cannot be crossed** — cliff face, ravine, treeline, water. Cheapest to build at greybox tier, diesgetic by default, and matches the art bible's planetoid read (close horizon, ground bends away).
- **B** — **Thin air / altitude** — the planetoid edge, atmosphere thinning, cold. Fits "large world" and the 20 m vista camera; strongest sense of a small figure on a large thing.
- **C** — **Living limit** — bramble, spirit ward, beast territory. Fits *Love as Epic Quest* and the "combat strips sin" frame; riskiest to read at a glance.
- **D** — **A hard UI/velocity barrier** — explicitly *not* diegetic. Listed so it can be rejected on the record rather than drifted into.

### Round 2 — RESOLVED 2026-10-01

**Q3 — How does the player know which mechanic family a zone offers?**
- **A (recommended)** — **Environment alone; UI only confirms.** → **CHOSEN**
- **B** — Environment plus a restrained persistent marker.
- **C** — Environment plus explicit UI label on entry.

**Q4 — How large is one section?**
- **A (recommended)** — **One section ≈ one minute of travel on foot.** → **CHOSEN**
- **B** — One section ≈ 3–5 minutes.
- **C** — One section ≈ 20–30 seconds.

---

### Round 3 — RESOLVED 2026-10-01

**Q5 — What is the unit of travel between sections?**
- **A (recommended)** — Walk adjacent, glide for gaps. → **CHOSEN**
- **B** — Glide is the connective tissue.
- **C** — Portal / shrine traversal.

**Q6 — What is the strongest distance read?**
- **A (recommended)** — Lookout dominance. → **CHOSEN**
- **B** — Journey-time dominance.
- **C** — Vertical dominance.

---

### Round 4 — issued 2026-10-01

**Q7 — What is a mechanic family, concretely?**
Decisions **A** and **C** only become buildable once the families are named. The families the canon already implies are: **gather**, **nurture/tame**, **heal**, **spirit stewardship**, **stealth**, **build/place**, **combat (placeholder)**. The question is whether a section maps to one family or to a pairing.

- **A (recommended)** — **One family per section, taught in isolation.** The clearest possible read for "environment alone": a gathering zone looks like a gathering zone and nothing else. Produces more distinct silhouette families to model, and more sections to author, but each is legible by construction. Fits ~84 m sections and 20–40 volumes per section exactly.
- **B** — **Two paired families per section.** Halves the number of sections and lets a zone deepen rather than repeat; costs the clarity of the read, because the environment now has to announce two things at once.
- **C** — **One family per section, but one *signature silhouette* per family shared across all its sections.** A gathering zone anywhere in the world is recognisable by the same shape language, so the player learns the vocabulary once. Best long-term teachability and cheapest to author; requires the shape language to be strict enough that it never leaks between families.

**Q8 — When does the player leave a section?**
This is the last feel question, and it sets whether a boundary is a *consequence* or a *gate*.

- **A (recommended)** — **The section releases you.** Having learned/used the mechanic family, the terrain opens — a ravine becomes fordable, a treeline thins, a cliff reveals a descent. The boundary is a *result* of your play, so it is always diegetic and never feels arbitrary.
- **B** — **The player chooses to go.** Boundaries are fixed and always available once you can see them; the section ends when you leave. Simplest to build and to playtest; the world reads as pre-built rather than responsive.
- **C** — **Both.** Sections open on completion, but the world also has always-open terrain boundaries elsewhere, so the player can leave early if they choose. Most freedom; risks the mechanic family being skipped, which under "environment alone" means it may never be taught.

**Q5 — What is the unit of travel between sections?**
A functional section is ~84 m. That raises the question of how sections are *joined*, which sets both the distance question and the glide question.

- **A (recommended)** — **Walk between adjacent sections; glide only for large gaps.** Glide stays a special traversal with a visible launch and landing (lookout pad / landing circle / glider perch already exist in the greybox layout), never a convenience hop. Keeps the ~1 min figure honest and preserves glide as a *place*, matching the canon's rejection of a free-flight sim.
- **B** — **Glide is the connective tissue.** Sections are islands of walking separated by glide gaps; walking only happens inside a section. Strong sense of a large world and of "the world is beneath me", but makes glide ubiquitous and weakens its specialness.
- **C** — **Portal / shrine traversal.** Sections joined by spirit-shrine portals; distance is compressed deliberately. Fastest to build and to playtest across, and it is already in canon (homestead shrine + return shrine). Cost: reduces the felt size of the world and makes "large world" a claim rather than an experience.

**Q6 — What is the strongest distance read the player should get?**
This is the "large world, small player" claim in art bible §1. It has to be felt, not stated.

- **A (recommended)** — **Lookout dominance.** From any high point you can see the *next two sections* and recognise their silhouette families, so the player learns the world's structure by looking rather than by walking. Directly serves the 20 m+ vista camera already locked, and reuses the existing `CAM_Hero` sightline checklist.
- **B** — **Journey-time dominance.** The player's sense of scale comes from how long the journey *takes* — long stretches of travel with the next landmark never arriving. Strongest sense of distance, weakest for legibility of mechanic families.
- **C** — **Vertical dominance.** The planetoid read: looking *down* from the homestead at the planet below, ground bending away, deep zenith. Most striking image, most expensive to build and to light.

**Q3 — How does the player know which mechanic family a zone offers?**
Chosen model is functional, so the environment must *announce* itself. The question is how far that announcement is allowed to go.

- **A (recommended)** — **Environment alone; UI only confirms.** Terrain, material, creature and light changes tell you what you can do here; UI appears *after* you act and names it. Keeps the fantasy intact and makes the world carry the frame (art bible §6: the world stays large, default camera stays far). Cost: the read has to be strong enough to teach, and that is the hard part.
- **B** — **Environment plus a restrained persistent marker.** One subtle per-zone cue — a distinct foliage family, a light temperature, a sound bed — that is always present but never a banner. Middle path; slight risk of a cue being mistaken for decoration.
- **C** — **Environment plus explicit UI label on entry.** A short line naming the mechanic family as you cross a terrain boundary. Fastest to ship and unambiguous; costs immersion and risks turning a place into a menu.

**Q4 — How large is one section?**
With a functional model, section size *is* the pacing decision, and it sets asset counts.

- **A (recommended)** — **One section ≈ one minute of travel on foot.** Roughly the planet path already specified in [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) §6 (180–240 s core). Tight enough that a mechanic family can be learned before attention moves on; large enough that it is not a corridor.
- **B** — **One section ≈ 3–5 minutes.** More room to layer secondary mechanics inside a zone; higher risk the player has forgotten what the zone is for.
- **C** — **One section ≈ 20–30 seconds.** Reads as a beat rather than a place; best if you want the world to feel like a chain of moments.