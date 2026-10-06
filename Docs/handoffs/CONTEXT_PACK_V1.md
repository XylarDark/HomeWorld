# CONTEXT_PACK_V1 — pre-built context pack

**Status:** READY. Signed off Oct 5 2026 by Conductor, Design, Implement, Test, Fix, dr eggbot. Lead asked for this packet ("design a packet that implements this team's recommendations").
**Base:** main `4bae4d4`. Gate #14 of homeworld-co-ops applies to every bite.
**Order:** bites run one at a time, 1 → 3 → 4. Bite 2 is already done (see below).

## Bite 1 — World-metrics sheet (Design, docs only)

- New file `Docs/WORLD_METRICS.md`. One row per number: value, unit, axis, source.
- **Source column** names where the number was first written (file + line, or interview) and, if any, the Lead interview that kept or changed it, e.g. "route line N, kept by #3". Every cite is checked against the file at the merged SHA. A number with no findable source is marked `unsourced`, never guessed.
- **Taste placeholders** (layer heights, the layer split inside the 50 m band) appear only as `taste placeholder, no lock`, never as plain values. They wait for Lead's taste pass.
- The GDD, the route, and packets link to rows instead of copying numbers. Existing copies are left in place in this bite; a mismatch is reported, not silently edited.
- Same PR adds Fix's two lines to `docs/KNOWN_ERRORS.md`, verbatim:
  1. **Cause:** When the player is moved into the destination portal's box, a new overlap fires in the same frame and sends them straight back. **Avoid:** Start the cooldown on every portal before the move, and place the player at least 60 uu outside every portal box. This is the #281 fix at `2369a12`.
  2. **Cause:** I assumed the portal destinations were portal components, but they were TargetPoints, so the lookup came back empty. That cost one PIE round on `bdd7b4d`. **Avoid:** Read the level manifest from bite 3 before writing any Fix SHA that depends on level data. Until the manifest exists, wait for Conductor's actor scan.
- **Done (Test):** no copied number elsewhere in `Docs/` disagrees with a row; every row has a source or `unsourced`; no taste placeholder reads as a lock.
- Merge: docs only, auto-merge on Test PASS.

## Bite 2 — Runbook additions (Conductor) — DONE

- The four editor tricks are in the shared skill `homeworld-desktop-prove`, section "Editor scripting tricks". Not in any repo PR; the repo copy under `.agents/skills` picks them up on the next sync.
- Fix's `KNOWN_ERRORS` lines ride in bite 1.

## Bite 3 — Level manifest (Implement writes, Conductor runs)

- Python script under the repo. Writes `Docs/level/L_VS_MVP_Markers_manifest.json`: each actor's label, class, location, bounds, and what sits under it. Bounds only, no line traces.
- Conductor reruns it after every level merge. Gate #14 scans and Fix SHAs read it first; Test quotes positions from it.
- **Stale** means an automation test regenerates the dump from the loaded map and fails on any label, class, location, or bounds mismatch against the committed JSON. Not `.umap` mtime (LFS).
- **Done (Test):** the stale test passes on a fresh dump and fails on a hand-edited JSON row.
- Merge: touches Source, needs Lead's yes.

## Bite 4 — Commands and log-tags index (Implement)

- Generated from Source: `Docs/COMMANDS_AND_LOG_TAGS.md` lists every `hw.*` console command, every log prefix (e.g. `CLOUD_DESCENT`, `FALLBACK: Portal`), and input bindings. Header: "generated — do not hand-edit".
- Test packets name the expected log tag from this file.
- **Done (Test):** a grep of Source for `hw.` commands and log prefixes finds nothing missing from the file.
- Merge: touches Source, needs Lead's yes.

## Out of scope

No new runbook doc. No route sentence edits. No level edits. No fertilizer or barn.
