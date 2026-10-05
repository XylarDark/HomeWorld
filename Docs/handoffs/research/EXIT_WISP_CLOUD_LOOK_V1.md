# EXIT WISP_CLOUD_LOOK_V1

**Kind:** RESEARCH EXIT — WISP_CLOUD_LOOK_V1

**File protocol:** Lead / Conductor paste. Canonical intended path: `Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md`<br>
**Prompt:** Lead instruction for WISP_CLOUD_LOOK_V1 (research only; chat brief, file protocol per `PROMPT_`/`EXIT_` naming)<br>
**Date:** 2026-10-04<br>
**Pins:** HW main `0177c76` (route notes after that commit are local and uncommitted in `Docs/context/HOMEWORLD_ROUTE.md`; cited, not modified)<br>
**Scope:** Research on how the sky reads on the wisp descent, with Astroneer planetoids named as the initial benchmark for the gap. No code, no build, no PR, no island/mesh/spec/plate change, no route-file change.<br>
**Closed, cite-not-reopen:** The descent stays the steered glide that ends inside the existing field; it is not a new flight. It is not a circle around the island. The 33.75 s homestead-to-field window is set and is not reopened. The night spread is a separate flight. Later zones stay later. The 260 m line is the plains edge on the old straight glide only.

---

## Diagnosis

The locked numbers from `EXIT_WISP_CLOUD_RING_V1` already fix the shape of this pass: cloud diameter stays **6–24 m**; spacing stays **top 3–4× local diameter, middle 1.5–2.5×, bottom 4–6×**; the drop stays **one and a half times the current drop**; the window stays **33.75 seconds**; the landing stays the **existing field**. Nothing in this EXIT overwrites or re-derives those figures — they are inputs, stated here so the look advice never drifts from them.

What this bite actually asks is a reading question: with those locked numbers, how should the sky read when the player looks up, and what benchmark frames the gap under the lowest cloud?

Key observations:

1. **The active pass is fixed.** It is the glide through clouds — more than one layer — then the field below. It is not a ring or a circle around the island. Any look advice that implies orbiting the island is out of scope.
2. **"Look up" reads short.** With cloud diameters of 6–24 m and the drop at one and a half times current, the clouds are near the player, not overhead scenery from a plane. The reference read is a small-world sky: closer horizon, closer cloud shapes, scenic rather than vast. Lead named **Astroneer planetoids** as the initial benchmark for this feel — small planets where the world reads near, the horizon is close, and the view is scenic. That is a benchmark for how the sky reads, **not a scale to copy**, and Astroneer systems (terraforming, platforming economy, planet selection) are not part of this bite.
3. **The gap under the lowest cloud is unset by design.** A placeholder distance between the bottom of band C and the field is allowed here as a **comparison anchor only** — it exists so the look (clearance, read of the field, landing corridor) can be described and tested. It is not a yes: no gap value, no zone distance, and no new height is decided by this EXIT, and Astroneer does not set one.
4. **No atmosphere height is invented.** The sky's top, the cloud field's extent, and any "ceiling" stay unwritten. Bands remain fractions of the drop; spacing remains a multiplier on local diameter.
5. **The look itself stays a human call.** This EXIT frames the question and names the benchmark; Lead decides the look. Research describes, it does not steer.

**Unknown closed:** how the sky should read on the look-up (shorter distances, scenic views, benchmark = Astroneer planetoids as initial reference, comparison only); gap under the lowest cloud exists only as a comparison placeholder; all locked sizes, spacings, drop ratio, window, and landing stand.

---

## Decision

| Option | Verdict |
|--------|---------|
| Name Astroneer planetoids as initial benchmark for the sky's near, scenic read | **Go** (benchmark, not scale; no Astroneer systems) |
| State the gap under the lowest cloud as a comparison-only placeholder | **Go** (explicitly not a yes, not a zone distance, not a height) |
| Restate the active pass as glide through more than one cloud layer, then the field | **Go** |
| Overwrite locked diameter (6–24 m), spacing multipliers, drop ratio, or window | **No-Go** — locked, cited, not touched |
| Write a new meter height for the drop or an atmosphere height | **No-Go** — explicitly barred |
| Treat Astroneer as setting the gap, a zone distance, or a new height | **No-Go** — it benchmarks the read only |
| Let the look get decided by research prose | **No-Go** — look stays a human call |

---

## 1. How the sky reads when you look up

**Reading:** short distances, scenic views. The clouds hang near, the eye travels a short distance to them, and each layer reads as a scenic band rather than a ceiling. This is the planetoid read Lead named: a small world where the sky is close enough to feel, not a realistic atmosphere stretching overhead. It is a benchmark for the read — a comparison target for the human test — never a scale to copy, and no Astroneer system (terrain shaping, surveying tools, planet roster, resource loops) enters this bite.

What the read implies for the descent:

- **Orientation happens up close.** Band A (top) clouds are the first scenic marks after jump-off; you steer for them rather than sighting a distant landmark.
- **The middle band carries the play.** Band B is where the eye lands repeatedly — more than one layer worth of cloud on the way down — with the field appearing below as the layers thin toward band C.
- **The bottom of the descent clears.** Band C thins (spacing 4–6× diameter) so the field below reads clean before the landing; the gap under the lowest cloud is the open air that makes that read possible.
- **It never orbits.** The active pass is a forward glide through the layers, then the field. A circle around the island would contradict the locked route facts and is not this bite.

## 2. The gap under the lowest cloud — placeholder, comparison only

A number for the space between the bottom of band C and the field top can be useful as a **comparison anchor** for the look test: it sizes the open air in which the field reads clean. It is recorded here as **placeholder, comparison only** — not a yes, not a zone distance, not a height, and not something this EXIT sets. Astroneer does not set it either; it lends the feel, not the figure. Later zones stay later, and no atmosphere height is invented to justify it.

## 3. Locked inputs (cited, not changed)

- Cloud diameter: **6–24 m** (band bias A 14–24, B 8–16, C 6–10, per `EXIT_WISP_CLOUD_RING_V1`).
- Spacing: top **3–4×** local diameter, middle **1.5–2.5×**, bottom **4–6×**.
- Drop: one and a half times the current drop; no meter height written.
- Window: **33.75 s** homestead-to-field, unchanged.
- Landing: the existing field; night spread separate; no new flight.

## 4. What this EXIT does not do

- No code, no PR, no desktop prove; docs-only handoff below.
- No island, mesh, spec, blend, uasset, umap, or `Docs/context/HOMEWORLD_ROUTE.md` change. No edit to `UserHarness/docs/human-use/route-context.md`.
- No new meter height; no atmosphere height; no gap value as a yes; no zone distance.
- No Astroneer systems; Astroneer stays an initial benchmark for the read, not a copy target.
- No ring around the island; later zones stay later; 33.75 s and the 1.5× drop stand.

---

## 5. Do bites (max 2) — docs only

### Bite 1 — `WISP-CLOUD-LOOK-NOTE`

**Unknown (one):** Can the look summary (§1), the comparison-only gap note (§2), and the locked-input cite (§3) live in one short handoff doc that Lead cites when making the look call, without touching the route file or any spec?

**Host:** CLOUD · artifact `docs`<br>
**Exclusive paths:**

- `Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md` *(new)* — the three sections above, each stamped "benchmark / comparison-only / locked input cited, not changed," plus one line that the look itself is a human call.

**Forbidden:** `Source/**` · `Content/**` · `.uasset`/`.umap` · island spec/mesh/blend · `Docs/context/HOMEWORLD_ROUTE.md` · `UserHarness/docs/human-use/route-context.md` · generator code or config · AGENTS.md · Astroneer system mechanics · a gap value stated as yes · a meter height for the drop · an atmosphere height.

**DONE-WHEN:**

```bash
test -f Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md
grep -E 'shorter distances|scenic' Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md
grep -Ei 'comparison only' Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md
grep -E '33\.75|6–24|6-24|3–4|1\.5–2\.5|4–6' Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md
grep -Ei 'atmosphere height|new meter height' Docs/handoffs/WISP_CLOUD_LOOK_NOTE_V1.md && echo FAIL
```

**child Research:** N

---

**Not opened (no second bite):** the human look test is Lead-scheduled; generator wiring is a later Implement prompt; later zones stay later; Astroneer does not spawn a content fork.

---

## eggbot

N/A

---

## child Research needed?

**N** — The look benchmark, the comparison-only gap framing, and the locked-input cite are answered above. Generator wiring, the human look test itself, and later zones stay later and do not need their own prompt yet.

---

## Accept checklist (Conductor)

- [ ] EXIT has Diagnosis · Decision · sky-read section · gap placeholder · locked inputs · Do bites · eggbot · child Research · this checklist
- [ ] Astroneer planetoids named as initial benchmark only — no scale copy, no Astroneer systems
- [ ] Sky read framed as shorter distances, scenic views; look itself stated as a human call
- [ ] Active pass stated as glide through more than one cloud layer, then the field below; not a circle around the island
- [ ] Gap under lowest cloud marked comparison-only, not a yes; no zone distance; no new height; no atmosphere height
- [ ] Locked figures cited, not overwritten: 6–24 m, top 3–4×, middle 1.5–2.5×, bottom 4–6×, 1.5× drop, 33.75 s, existing field landing
- [ ] Do bite: one unknown, grep-sized checks, docs-only, no instruction to build in this turn
- [ ] No edit to `Docs/context/HOMEWORLD_ROUTE.md` or `UserHarness/docs/human-use/route-context.md`

### Fitness greps (EXIT)

```bash
# Required sections
grep -E 'Diagnosis|Do bites|eggbot|child Research|Accept checklist' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md

# Title check
grep -E '^#+[[:space:]]*EXIT ' Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md

# Fail-strings must be empty
grep -nEi 'implement now|start coding|merge this PR|open DESKTOP Act|run the prove' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md && echo FAIL

grep -nEi 'schedule #8|do MARKETPLACE_SCOUT|install marketplace|CAP-002 readiness as this bite|CAP product Do|APPROVE TOOL SCOUT' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md && echo FAIL

grep -nEi 'bump pin|alwaysApply|AGENTS.md body|Class S slim|rewrite A–E' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md && echo FAIL
```

---

## Sources

- `Docs/handoffs/research/PROMPT_WISP_CLOUD_RING_V1.md` and `EXIT_WISP_CLOUD_RING_V1.md` (locked diameter 6–24 m, spacing multipliers, 1.5× drop, 33.75 s window, field landing)
- `Docs/context/HOMEWORLD_ROUTE.md` (route facts; cited, not modified)
- `UserHarness/docs/human-use/route-context.md` (state detection; cited, not modified)
- Astroneer wiki: five planets plus two half-size moons (Desolo, Novus) — same-size stylized bodies as the feel benchmark (cited qualitatively; no figures adopted)

---

*End EXIT. Conductor: ACCEPT → schedule `WISP-CLOUD-LOOK-NOTE`. Do not open a generator change, a new flight, an island/mesh edit, a route-file edit, or any Astroneer-system work from this EXIT.*
