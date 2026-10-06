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
  2. **Cause:** I assumed the portal destinations were portal components, but they were TargetPoints, so the lookup came back empty. That cost one PIE round on `bdd7b4d`. **Avoid:** Read the level manifest from bite 3 before writing any Fix SHA that depends on level data. The manifest is on main; if it is missing, scan the level actors in this session first. (The old instruction waited for Conductor's actor scan until the manifest existed.)
- **Cross-check scope:** only `Docs/01_GDD_MVP.md`, `Docs/context/HOMEWORLD_ROUTE.md`, and `Docs/handoffs/CLOUDS_WISPS_V1.md`. Wider scope needs a Lead yes.
- **Done (Test):**

| Check | Expected | Fail label |
|---|---|---|
| Copied numbers | No number in the three cross-check files disagrees with a sheet row | `closed_fail` |
| Sources | Every row has a source cite that matches the file at the merged SHA, or reads `unsourced` | `closed_fail` |
| Taste placeholders | Every taste value reads `taste placeholder, no lock`; none appears as a plain value | `closed_fail` |
| `KNOWN_ERRORS` | Fix's two lines are present word for word in `docs/KNOWN_ERRORS.md` | `closed_fail` |
| Hook | `Docs/WORLD_METRICS.md` exists at the exact path the `SESSION_START.md` read list names | `soft_fail` |
- Merge: docs only, auto-merge on Test PASS.

## Bite 2 — Runbook additions (Conductor) — DONE

- The four editor tricks are in the shared skill `homeworld-desktop-prove`, section "Editor scripting tricks". Not in any repo PR; the repo copy under `.agents/skills` picks them up on the next sync.
- Fix's `KNOWN_ERRORS` lines ride in bite 1.

## Bite 3 — Level manifest (Implement writes, Conductor runs)

- Python script under the repo. Writes `Docs/level/L_VS_MVP_Markers_manifest.json`: each actor's label, class, location, bounds, and what sits under it. Bounds only, no line traces.
- Conductor reruns it after every level merge. Gate #14 scans and Fix SHAs read it first; Test quotes positions from it.
- **Stale** means an automation test regenerates the dump from the loaded map and fails on any label, class, location, or bounds mismatch against the committed JSON. Not `.umap` mtime (LFS).
- **Done (Test):**

| Check | Expected | Fail label |
|---|---|---|
| Manifest file | `Docs/level/L_VS_MVP_Markers_manifest.json` exists with label, class, location, bounds, and what's under it for every actor | `closed_fail` |
| Stale test, fresh | The automation test passes on a fresh dump | `closed_fail` |
| Stale test, edited | The automation test fails when one JSON row is hand-edited | `closed_fail` |
| No traces | The script uses bounds only, with no line traces | `soft_fail` |
| Hook | The manifest exists at the exact path the `SESSION_START.md` read list names | `soft_fail` |
- Merge: touches Source, needs Lead's yes.

## Bite 4 — Commands and log-tags index (Implement)

- Generated from Source: `Docs/COMMANDS_AND_LOG_TAGS.md` lists every `hw.*` console command, every log prefix (e.g. `CLOUD_DESCENT`, `FALLBACK: Portal`), and input bindings. Header: "generated — do not hand-edit".
- Test packets name the expected log tag from this file.
- **Done (Test):**

| Check | Expected | Fail label |
|---|---|---|
| Coverage | A grep of Source for `hw.*` commands and log prefixes finds nothing missing from the file | `closed_fail` |
| Header | The file starts with "generated — do not hand-edit" | `soft_fail` |
| Hook | `Docs/COMMANDS_AND_LOG_TAGS.md` exists at the exact path the `SESSION_START.md` read list names | `soft_fail` |
- Merge: touches Source, needs Lead's yes.

## Deployment — how the pack reaches every session

Lead, Oct 5 2026 (interview #9, 1A 2A): one start file and one rule set for desktop agents and room seats.

- **One start door.** `Docs/context/SESSION_START.md` reads route-context, then the route, then `Docs/WORLD_METRICS.md`, and names the other pack files to open only when the task needs them (Lead interview #18, 18A). It ends by asking one question unless the opening message already names the task. `DISCOVERY_START.md` and `ROUTE_START.md` only point to it.
- **One hook for desktop IDE agents.** `AGENTS.md` gets one line pointing to `Docs/context/SESSION_START.md`, and nothing more. The pack paths are not listed in `AGENTS.md`.
- **Pack paths.** The door reads `Docs/WORLD_METRICS.md`. It names `Docs/level/L_VS_MVP_Markers_manifest.json` and `Docs/COMMANDS_AND_LOG_TAGS.md` and opens each only when the task needs it. Fix work searches `docs/KNOWN_ERRORS.md` for the symptom and reads the matching entries. Bites add no read lines anywhere.
- **Box lanes.** `homeworld-co-ops` is a sand-workflow skill, not a file in this repo. The edit that points it at `SESSION_START.md` and drops its copy of the shared rules is unverified. Do not treat it as done.
- **OpenCode bite prompts.** Conductor's paste-ready prompts for bites 3 and 4 name the paths up front, because those files don't exist on main yet when the bite starts.

## Out of scope

No new runbook doc. No route sentence edits. No level edits. No fertilizer or barn.
