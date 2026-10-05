# PROMPT WISP_CLOUD_RING_V1

> **Historical research prompt:** This prompt was written against HW `0177c76`
> and a route working copy that was not on that pin. For present route facts,
> read [`Docs/context/HOMEWORLD_ROUTE.md`](../../context/HOMEWORLD_ROUTE.md) from
> current `main`. Any difference here is not current canon or implementation
> authorization.

## ROLE

Advise Lead on a starting cloud size range and a density by height for the cloud layer on the glide down. You are not writing code and you are not opening a build.

## CONTEXT

- HomeWorld main is 0177c76. Route notes after that commit are local and uncommitted in Docs/context/HOMEWORLD_ROUTE.md.
- The first flight is still a steered glide off the homestead that ends inside the field. It is not a new flight.
- The 75 m figure is how high the island sits above the plains, so every jump drops that. It is not owned by the old straight glide.
- The 260 m line is the plains edge on that straight glide only. Other directions have no edge. A cloud ring does not draw that line around the island.
- Fall rate, that height, and zone sizes are placeholders for placement until human testing.
- Clouds are generated around the homestead, so any jump has more than one spirit-blue cloud to aim for.
- The name ring means a glide through clouds, in the manner of a WoW ring glide, as an example only. It is not a circle around the island.
- On the way down you pass through more than one layer. Clouds differ in spacing, size, and height off the ground. You collect as many wisps as you can in that layer, then the field is below.
- The homestead-to-field window is 15 seconds now. Height is one and a half times the current drop. Neutral glide speed is two thirds. The target window is 33.75 seconds, the 15 second window times those two ratios, if the glide keeps the same shape. Do not write a meter height. A later boost can add a short burst of speed. That boost is not this bite.
- A spirit-blue cloud gives one wisp. The generator sets the share of wisp clouds to clouds that are not wisps. Later mechanics may change that share. They are not this bite.
- The wisp stays with you until it is mixed with dung at the homestead. You can hold as many wisps as you collect, one per dung.
- The night spread is a separate flight.

## CANON

- Docs/context/HOMEWORLD_ROUTE.md (local notes; do not contradict the facts in CONTEXT)
- Do not contradict the steered glide, the field landing, or the split between this descent and the night spread
- Do not treat the 260 m line as a radius around the island
- Island spec, mesh, blend, uasset, and umap are out of this prompt

## ASK

1. What placeholder cloud size range should the layer generator start with?
2. What placeholder density by height should that layer use across more than one layer, with spacing that is not uniform, so any jump off the homestead has more than one spirit-blue cloud in reach?

## NON-GOALS

- No implement, no pull request, and no desktop prove
- No shooting clouds and no changing spawn after they exist. The WoW ring glide is an example of the fall only. Do not copy that game, and do not add later interactions.
- No new flight that replaces the glide
- No island mesh, spec, or plate change
- No CAP product work
- No rewrite of AGENTS.md
- Do not invent a cloud count that replaces the generator

## DONE-WHEN

- EXIT file is Docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md
- It has Diagnosis, Do bites, eggbot, child Research, and Accept checklist
- Do bites name at most one unknown each, with a grep-sized check, and they do not say to implement now
- Size range and density by height are either a stated placeholder or an explicit unknown
- The 260 m line is not reused as a ring radius

## child Research needed?

N. This ask is cloud size range and density by height for the spawning layer only. Spawn influence and shooting clouds stay later and do not need their own prompt yet.
