# EXIT WISP_CLOUD_RING_V1

**Kind:** RESEARCH EXIT — WISP_CLOUD_RING_V1

**File protocol:** Lead / Conductor paste. Canonical intended path: `Docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md`<br>
**Prompt:** `PROMPT_WISP_CLOUD_RING_V1`<br>
**Date:** 2026-10-04<br>
**Pins:** HW main `0177c76` (route notes after that commit are local and uncommitted in `Docs/context/HOMEWORLD_ROUTE.md`; cited, not modified)<br>
**Scope:** Spawning-layer advice only — a placeholder cloud size range and a placeholder density by height. No code, no build, no PR, no island/mesh/spec/plate change, no route-file change.<br>
**Closed, cite-not-reopen:** The descent stays the steered glide that ends inside the field; it is not a new flight. The 33.75 s window is already set and is not reopened here. The night spread is a separate flight. The 260 m line is the plains edge on the old straight glide only — it is not reused below as a ring radius, a spawn radius, or any other radius.

---

## Diagnosis

The route facts already fix everything around the two asks: clouds are generated around the homestead so any jump has more than one spirit-blue cloud to aim for; the generator owns the wisp share; the descent passes through more than one layer; clouds differ in spacing, size, and height off the ground; fall rate, height, and zone sizes are placeholders until human testing; no meter height is written for the drop. What is genuinely unset — stated plainly in the route file itself ("The generator needs a cloud size range and a density for each height. Those are not set.") — is exactly the two asks.

Sizing logic that does not depend on the drop height:

1. **A cloud is a beat, not a texture.** Passing through one should read as a short, deliberate event at neutral glide speed — long enough to notice the spirit blue and steer for the next one, short enough that a layer holds several. Scaled against the player capsule (~2 m tall), that puts useful clouds in the single-digit to low-double-digit meters, not at terrain scale.
2. **Density belongs to the band, not the map.** The descent has a natural pacing: orient at the top, play in the middle, land clean at the bottom. That argues for three bands expressed as *fractions of the drop*, so the advice survives any later height change and never needs a meter figure.
3. **Non-uniform spacing is a multiplier plus jitter, not a count.** Giving the generator a spacing multiplier (in units of local cloud diameter) with per-band jitter gives "not uniform" without inventing a cloud count that replaces the generator, and without drawing any circle around the island.

**Unknown closed:** What starting cloud size range and density by height the layer generator should use, stated as placeholders for human testing.

---

## Decision

| Option | Verdict |
|--------|---------|
| State both asks as placeholders (fractions + multipliers, no meter drop height) | **Go** |
| Leave density an explicit unknown until human testing | **No** — a placeholder is exactly what the generator needs; human testing revises it |
| Give absolute meter bands for layer heights | **No-Go** — no meter height is written for the drop; bands are fractions |
| Anchor spacing or extent to the 260 m plains edge | **No-Go** — that line belongs to the old straight glide only |

---

## 1. Ask 1 — placeholder cloud size range

**Stated placeholder.** Generator starts with cloud **diameter 6–24 m** (horizontal), vertical **thickness ~0.4–0.5× diameter** (≈3–12 m). Per-band bias (bands defined in §2):

| Band | Diameter range | Why |
|------|----------------|-----|
| A (top) | 14–24 m | Big, readable orientation marks right after jump-off; a long drift-through while the player picks a line |
| B (middle) | 8–16 m | The main wisp-play band; each pass-through is a short beat, several per band |
| C (bottom) | 6–10 m | Small accents above the field; they must not wall off the landing read |

Scale check: smallest cloud ≈3× capsule height — a pass-through is visible, not subliminal. Largest ≈ a few seconds of glide at most — a landmark, not a weather system. All figures are placeholders for placement until human testing.

---

## 2. Ask 2 — placeholder density by height

**Stated placeholder.** Three bands as fractions of the drop (no meter heights). Spacing is a multiplier on the *local* cloud diameter, with jitter, so spacing is not uniform and scales with whatever height is current.

| Band | Span of the drop | Mean center spacing | Jitter | Character |
|------|------------------|---------------------|--------|-----------|
| A (top) | jump-off → ~40% down | 3–4× local diameter | ±40% | Sparse; room to orient and pick a line |
| B (middle) | ~40% → ~75% down | 1.5–2.5× local diameter | ±50% | Densest; the collection layer |
| C (bottom) | ~75% down → just above the field | 4–6× local diameter | ±30% | Sparsest; field below reads clean, landing corridor stays clear under the last clouds |

**Reachability floor (a placement rule, not a cloud count):** from any homestead jump azimuth, a neutrally steered glide corridor should cross **≥2 clouds in each of bands A and B and ≥1 in band C**. With the generator's wisp share applied on top, that yields more than one spirit-blue cloud in reach per jump. Counts and the wisp share stay with the generator; later mechanics may change the share and are not this bite.

**Explicitly not used:** the 260 m line, any ring or circle around the island, any uniform grid.

---

## 3. What this EXIT does not do

- No code, no PR, no desktop prove; docs-only handoff below.
- No island, mesh, spec, blend, uasset, umap, or `Docs/context/HOMEWORLD_ROUTE.md` change.
- No meter height for the drop — bands are fractions; spacing is a multiplier.
- No shooting clouds, no boost, no spawn change after clouds exist; the WoW ring glide stays an example of the fall only.
- The 33.75 s window is not reopened; no cloud count is invented that replaces the generator.

---

## 4. Do bites (max 2) — docs only

### Bite 1 — `WISP-CLOUD-LAYER-PLACEHOLDERS`

**Unknown (one):** Can the two placeholder rows (size range; density by height) live in one handoff doc that a later generator prompt cites, without touching the route file or any spec?

**Host:** CLOUD · artifact `docs`<br>
**Exclusive paths:**

- `Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md` *(new)* — the size-range table from §1, the density-by-height table and reachability floor from §2, each row stamped "placeholder until human testing." Pointer-only; no generator wiring.

**Forbidden:** `Source/**` · `Content/**` · `.uasset`/`.umap` · island spec/mesh/blend · `Docs/context/HOMEWORLD_ROUTE.md` · generator code or config · AGENTS.md · shooting clouds / boost / wisp-share mechanics.

**DONE-WHEN:**

```bash
test -f Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md
grep -E 'diameter|size range' Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md
grep -E 'Band A|Band B|Band C' Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md
grep -Ei 'placeholder until human testing' Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md
grep -E '260' Docs/handoffs/WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md && echo FAIL
```

**child Research:** N

---

**Not opened (no second bite):** generator wiring is a later Implement prompt once Lead accepts these placeholders; the human test that revises them is Lead-scheduled; shooting clouds, the boost, and wisp-share mechanics stay later per canon.

---

## eggbot

N/A

---

## child Research needed?

**N** — Both asks are answered above as stated placeholders. Spawn influence and shooting clouds stay later and, per the prompt, do not need their own prompt yet.

---

## Accept checklist (Conductor)

- [ ] EXIT has Diagnosis · Decision · Ask 1 size range · Ask 2 density by height · Do bites · eggbot · child Research · this checklist
- [ ] Size range and density by height are stated placeholders, each stamped for human testing
- [ ] No meter height written for the drop — bands are fractions, spacing is a multiplier on local diameter
- [ ] The 260 m line is not reused as a ring radius (or any radius)
- [ ] Reachability floor is a placement rule, not a cloud count; wisp share stays with the generator
- [ ] No shooting clouds, no boost, no spawn change; 33.75 s window not reopened; steered glide and field landing intact
- [ ] Do bite: one unknown, grep-sized checks, docs-only, no instruction to build it in this turn

### Fitness greps (EXIT)

```bash
# Required sections
grep -E 'Diagnosis|Do bites|eggbot|child Research|Accept checklist' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md

# 260 must appear only as a non-usage note
grep -nE '260' Docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md

# Fail-strings must be empty
grep -nEi 'implement now|start coding|merge this PR|open DESKTOP Act|run the prove' \
  Docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md && echo FAIL
```

---

## Sources

- `Docs/handoffs/research/PROMPT_WISP_CLOUD_RING_V1.md` (the two asks, the set window, the non-goals)
- `Docs/context/HOMEWORLD_ROUTE.md` (route facts; cited, not modified — size range and density recorded there as "not set")
- WoW ring glide, as example of the fall only (per prompt/canon)

---

*End EXIT. Conductor: ACCEPT → schedule `WISP-CLOUD-LAYER-PLACEHOLDERS`. Do not open generator wiring, a new flight, or any island/mesh work from this EXIT.*
