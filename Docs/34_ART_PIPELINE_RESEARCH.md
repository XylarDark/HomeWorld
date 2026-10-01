# Docs/34 — Art pipeline research and decisions

| Field | Value |
|-------|-------|
| **Status** | **RESEARCHED / DECIDED** — agent-owned decisions recorded DEC-0015..DEC-0018 |
| **Date** | 2026-10-01 |
| **Scope** | Knowledge sources + tool evaluation for the asset pipeline |
| **Canon inputs** | [02_ART_BIBLE.md](02_ART_BIBLE.md) · [20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md) · [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) · [../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md](../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md) |

**Ownership note:** every decision here is agent-owned (architecture, tooling, harness) under the 2026-10-01 reset. Nothing here touches taste. The one thing reserved for the Lead is **which art books to buy with real money** — that is spend, and spend is theirs.

---

## 1. The one-line answer

**Do not build the pipeline around AI mesh generation. Build it around deterministic batch generation of kit variants from an authored master, and treat AI generation as a measured experiment gated behind real numbers.**

The reason is not scepticism about the tools. It is that the highest-leverage thing an agent can do here is *not* generation — it is the thing nobody wants to hand-model, which is thirty consistent variants of a rock.

---

## 2. Licensing — the finding that removes options

Read from license files directly, not from vendor pages.

| Tool | Verdict | Basis |
|---|---|---|
| **Hunyuan3D-2 / 2.1** | 🚫 **DO NOT USE** | License opens: *"THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY LIMITED TO THE TERRITORY."* §5.c: outputs may not be used *"outside the Territory."* Target is **PC + Steam Early Access** — EU distribution is the normal case. Shipping blocker, not a formality. |
| **TRELLIS / TRELLIS.2** | 🚫 **DO NOT USE** | `LICENSE` is MIT on the **code**; the project page states materials are *"not intended for commercial exploitation or use."* The MIT grant covers software, the non-commercial statement covers weights/materials. Genuine ambiguity, unresolved. Treat as research-only. |
| **Meshy** | ⚠️ **Pro tier only** | Free tier output is **CC BY 4.0** — commercial use permitted, **attribution mandatory**. Pro+ grants full ownership. API requires Pro+. |
| **Tripo** | ⚠️ **Paid tier only** | Free tier ToS 5.2.1: *"Tripo retains all rights to Inputs and Outputs, including all Intellectual Property rights."* No commercial rights on free. |
| **Sloyd** | ✅ Cleanest | Plus/Pro: *"you own what you generate… without royalties or attribution required."* Free = CC BY 4.0. |

**DEC-0015 — the pipeline must fail closed on free tiers.** A free-tier generation that reaches `Content/` is a policy violation that no agent will notice on its own. Tier is asserted at generation time, recorded in the sidecar, and re-checked at promote.

---

## 3. What the tools actually do

### The paradigm shift, and why it is *not* our answer

Meshy Smart Topology (`model_type: "smart-topology"`, `ai_model: "meshy-t2"`) generates **natively at a target face count** (100–15,000, default 4,000) rather than decimating. Meshy markets this as *"Built low, not crushed… the silhouette is designed for that budget instead of being decimated into it. That is the difference between a faceted asset and a smoothed blob with the polygons taken out."* ⚠️ **Vendor claim, not independently benchmarked.**

Our measured budgets are **12–1,680 tris**, which sits inside that native range — so generation is now *technically* a better fit than it was in 2025, when [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) wrote its 30-minute rule.

**This is a real change. It is also not enough to build on.** See §5.

`auto_size: true` with `origin_at: "bottom"` is genuinely useful — it solves the two failure modes we would otherwise hand-code (arbitrary scale, origin not at ground contact, which the art bible §10 requires).

Sloyd is the most interesting of the three because it is **parametric, not diffusion** — low-poly is its native form. But its visual idiom is CAD, and the art bible §8 forbids tech-gate / neon-ring reads. It would read generic-sci-fi without heavy art direction.

### The assetization bottleneck is still real

The 2026 survey (*"From Visual Synthesis to Interactive Worlds"*, arXiv 2604.23629) defines production-ready as deployable **without manual repair**: manifold topology with deformation-appropriate edge loops, PBR attributes, rigging where needed. Its central claim:

> *"converting a generated 3D object into a production-ready asset involves retopology, UV layout, material authoring, and rigging, a sequence of labor-intensive steps that collectively constitute what we term the **assetization bottleneck**."*

It also notes there is **no standardized game-readiness benchmark** — so any vendor claim about facet quality is unfalsifiable by default.

---

## 4. Knowledge sources worth your time

### Buy (Lead decision — real spend)

| Source | Why |
|---|---|
| **The Art of Octopath Traveler** — Square Enix / Dark Horse, ISBN 9781506752471 | Closest published match to our locked law. HD-2D is faceted volumes + strong surface detail + selective flat shading. That is our brief, in print, to hold next to the screen. |
| **Practical Game Design** — Brian Hoffman, O'Reilly, ISBN 9781787121799 | TOC verified: greenlight gates, **vertical slice**, full grayboxing section, level design through art implementation to final polish. Subscription. |

### Read (free, machine-readable)

**`book.leveldesignbook.com`** — Robert Yang, free, continuously updated, and **every page is available as Markdown by appending `.md`**. Index at `llms.txt`. Highest information-per-effort source found. Relevant pages: `/process/blockout`, `/process/blockout/metrics/modular`, `/process/env-art`, `/process/preproduction/scope`.

Two verified quotes that bear directly on us:

> *"You can't playtest a design document or a layout sketch, but you can playtest a blockout."*
> *"**99% of the time, your blockout will not survive a playtest.**"*

And the two case studies we should not skip — **Firewatch** skipped blockout because *"Greyboxing did not answer any of the important questions"* (pacing was narrative), and **Untitled Goose Game** where a blockout-first approach produced something subtly inauthentic and the fix was research-first location scouting.

⚠️ **Direct consequence for us:** our openworld brief is *"large planetoid, close horizon, ground bends away, deep zenith, readable constellations."* Those are **framing and feel** questions. A greybox cannot answer them. That is the Firewatch case — and it is a source-backed reason that [32_PROTOTYPE_ASSETS.md](32_PROTOTYPE_ASSETS.md) deferred our formal Shot 1/2 stills. It is not a tooling gap; it is the wrong tool for that question.

### Watch (free on GDC Vault)

| Talk | Why |
|---|---|
| **GDC 2026 — "The Modular and Expressive World Art of *Keeper*"** — Nick Maksim, Double Fine | On our exact problem. Takeaway is hiding asset repetition across a world. Instance variation, mesh morphing, painterly foliage. Within the free 2-year window. |
| **GDC 2013 + 2016 — Joel Burgess (Skyrim / Fallout 4 modular)** | The 101 and 201 of modular kit design. 2013 is 13 years old; the fundamentals have not moved. |
| **GDC 2018 — "Invisible Intuition"** (David Shaver, Naughty Dog + Robert Yang) | Called the most up-to-date industry-standard blockout talk. Composition and wayfinding. |
| **GDC 2015 — "Blending handmade detail into your game's procedural world"** (Mark Johnson) | Indie-scale handmade/algorithmic balance. Most relevant to a small team. |

### Engine-side (UE 5.8 primary docs — matches our lock)

**PCG Generation Modes**: Non-partitioned (default), **Partitioned**, **Hierarchical**, **Runtime**. Hierarchical generates at multiple scales — fine grid for hero rocks, coarse for scatter. **Hierarchical + Runtime is the pair** that gives a 20 m vista camera its detail without paying for it at 500 m.

**Foliage Mode**: default Instanced Foliage grid in World Partition is **256 m**, set separately from the WP grid.

⚠️ Read [../docs/PCG/PCG_VARIABLES_NO_ACCESS.md](../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) before building any new scatter graph — it records a real project-specific PCG constraint.

### Trim sheets — the rule, from a primary source

Roblox Creator Docs is unusually strong here because it states the *rule*:

> *"The most fundamental rule for trim sheets is to avoid contextual details that you can only apply to a single object"* — because specific details become **visible as repetition** when reused.

Square sheets, 1024×1024 practical max. **This explains a split our canon already has:** art bible §5 Layer B (moss clump, lupine sprig, fence module) is *object-scoped* — exactly what the rule forbids on a shared sheet. Our `HW_Atlas` for genuinely shared treatments (wood grain, moss, stone) plus per-object instanced kits for object-specific pieces is the correct arrangement. The canon was right; this is why.

---

## 5. Is AI generation a net win? — the position

**Conditionally yes, for volume filler and variant generation. Still no for anything in `HW_Hero`.**

### The four places it is a clear loss

1. **Anything in `HW_Hero`** — crystal, beast/enemy heads, cabin door, **player face**. Art bible §3: the face is *"built from planes that act: brows, eyelids, mouth corners"* and *"Spend triangles on the face. The coat stays cheap."* **That is an instruction about authored topology.** No generator produces deliberate deformation-zone edge flow on a face. The strongest evidence: Hunyuan3D Studio's **PolyGen** headlines *"deformation-aware edge flow"* — which implies the general state is not.
2. **Anything reused on 3+ props with a shared silhouette.** A generated rock is a *different* rock. We do not get variants of *our* silhouette, we get other people's rocks.
3. **Anything rigged.** Auto-rig works on clean humanoids and falls apart on anything unusual.
4. **Our smallest meshes** — the 12-tri lookout pad and 20–28-tri path stones are below every tool's floor. Stay hand-built.

### The compliance cost is real for a small team

Every AI-influenced asset owes a sidecar, an `AI_ASSET_LOG.md` row, and a license note ([20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md) §4). That overhead does not exist for a hand-built mesh, and it does not shrink with volume.

### The test that settles it

**DEC-0016 — one prop class, 10–35 assets, measured cleanup minutes, compared against the existing 30-minute rule.** One paid Meshy Pro month (~$20, 1,000 credits) covers it; at 20–30 credits per Smart Topology preview that is roughly 35–50 assets.

Until that test runs with real numbers, the 30-minute rule stands. **We do not rewrite a pipeline decision on an inference when an afternoon of measurement would settle it.**

---

## 6. What the pipeline actually is

The highest-leverage agent task in a Blender-based stylized pipeline is **deterministic, parameter-driven batch generation of kit variations and LOD/instance sets from a single authored master**, enforcing scale, pivot, naming, and poly budget by code.

Why this and not generation:

- Hiding asset repetition across a world is *the* central environment-art problem (the *Keeper* talk's own stated takeaway). Thirty consistent cliff-module variants is exactly the work a human will not do and a machine is better at.
- We already run the right tool — official Blender Lab MCP, connected and documented. No new MCP should be introduced.
- **It is deterministic**, which is what makes it safe to run unattended: seed the RNG, same command → same 30 variants. The Ubisoft pipeline required *"the generation needs to yield the same result given the same inputs."*
- It turns the constraints from *"good intentions"* into **code**.

⚠️ **The caveat that shapes the architecture:** LLM-authored `bpy` is still improvised code — different code each run, no grouped undo, no output schema. So:

**DEC-0017 — the generator is checked-in, human-reviewed code that the agent invokes. The agent does not improvise Blender code per run.**

This converts the task from *"agent writes Blender code"* to *"agent runs a parameterised kit generator and reports deltas"* — reproducible, diffable, reviewable.

### The split — this is the whole point

| Layer | Owner | Why |
|---|---|---|
| **A — Structure masses** | **Agent** (generator) | Facets cut on purpose, hard edges, ground-contact origin, scale applied, budget asserted |
| **B — Detail kit variants** | **Agent** (generator) | Seeded jitter, mirrored pairs, decimate-to-budget |
| **C — One living eye** | **Human** | Art bible §5: *"A second eye on the same object usually adds noise, not life."* This is taste, it is per-object, and no generator does it |
| **Master materials** | **Human tuning**, agent scaffolding | Ten masters, instance, do not invent families |
| **Provenance** | **Automatic** | Sidecar + log row is a **write-failure of the export step**, not a later memory |

That table is the answer to *"maximize what AI does while I do finishing touches."* The human's remaining work is exactly the part that requires taste and per-object judgement.

### The assertion gate — before any mesh reaches `Content/`

DEC-0018 — fail closed on every one of these:

| Check | Rule |
|---|---|
| Name | Allocated from `MVP_EXPORT_MANIFEST.md`. Never invented. One writer, serialized. |
| Scale | Measured bounding-box height within a declared per-class tolerance; pivot Z == 0; adult figure 1.7–1.8 m as the ruler |
| Poly budget | Per-class from the manifest. Pine is 472. Cabin is 1,680. Assert, do not assume. |
| Facet read | **Must still show visible planar facets under a hard-shaded master.** Non-negotiable — art bible §1: *"If a change makes the facets disappear, it is the wrong kind of beauty."* |
| Master binding | The ten masters only. Generated textures are **not admissible** — generate untextured (`should_texture: false`), skip refine for Layer A. |
| Tier | Paid tier only. Free-tier output never reaches `Content/`. |

---

## 7. Sources I could not verify — leads, not facts

1. ❌ **"Level Art for Games"** — could not confirm this title exists. No publisher page, ISBN, or retailer listing found. **Do not order on a research summary's say-so.** This was the single biggest gap: excellent sources, but no confirmed dedicated stylized-environment-art book.
2. ⚠️ **level-art.com** — substantive content surfaced repeatedly; direct fetch returned **HTTP 404**. Verify manually.
3. ⚠️ **Tim Simpson's trim sheet tutorial** — cited as canonical by two professionals; primary source never reached.
4. ⚠️ **Meshy "built low, not crushed"** — vendor marketing, quoted verbatim. Not independently benchmarked. No third-party facet-quality benchmark exists.
5. ⚠️ **Tripo vs Meshy speed/face benchmark** — sourced from `tripo3d.ai`'s own blog comparing a competitor. **Assume bias.** The face-count ranges are independently corroborated by official API docs; the timings are not.
6. ⚠️ **Hunyuan3D PolyGen / image stylization** — read from the arXiv abstract and method text. Not verified whether PolyGen ships publicly, or under what licence. Inherits the EU/UK exclusion regardless.
7. ⚠️ **`mcp-blender-agent`** (npm, MIT, *"same input, same result"*) — verified from its own README only. Cited as an architectural pattern, **not a recommendation to install.**
8. ❌ **Greebling / detail-pass primary source** — none found for stylized game environments. Nearest verified substitutes: the Gnomon moss-patch lesson, the *Keeper* talk on instance variation.
9. ⚠️ **Gnomon pricing** — catalog and workshop count verified; current individual price not. Check `thegnomonworkshop.com/pricing`.

Highest confidence in this document: the **licensing findings** (§2) and the **Meshy API parameters** (§3) — both read from license files and API reference directly. Lowest confidence: the inference in §5 that native-low-poly generation now makes cleanup cheap. **The facts are verified. The inference is untested on our assets, and one afternoon would settle it.**

---

## 8. Citations

| Source | Use |
|-------|-------|
| [book.leveldesignbook.com](https://book.leveldesignbook.com) | blockout, modular metrics, env art, slice scope — free, `.md` per page |
| arXiv 2604.23629 | production-ready definition, assetization bottleneck, vendor gap |
| arXiv 2509.12815 | PolyGen, style-first ordering |
| `docs.meshy.ai/en/api/text-to-3d` | `target_polycount`, `auto_size`, `origin_at`, `should_texture` |
| `github.com/Tencent-Hunyuan/Hunyuan3D-2.1` `LICENSE` | territorial exclusion |
| `github.com/microsoft/TRELLIS/blob/main/LICENSE` | MIT code / research-only materials |
| Roblox Creator Docs — *Develop polished assets* | trim sheet rule |
| Epic UE 5.8 docs | PCG modes, foliage grid, World Partition |
| GDC Vault — *Keeper* (2026), Burgess (2013/2016), Shaver+Yang (2018) | modular world art |