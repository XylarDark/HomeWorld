# Fork optimization plan

Implemented 2026-10-10. Three rooms: Look, Play, Prove. Session start is the production door.

## What the industry actually separates

Studios split **craft** from **production**.

Craft pillars that show up across team guides are design, engineering, art, audio, and QA. Production is not a fifth craft. It owns scope, order, and dependencies, and it walks the other crafts along one chain. [Team structure](https://kiotogaming.com/game-development-team-structure/), [Production pipeline](https://videogamedevelopmentauthority.com/game-development-production-pipeline)

“Asset” is not a peer of art. An asset is the output of the art pipeline: concept, model sheet, mesh, review, export. Splitting art and asset into two rooms makes the same work look like two projects. Feature pods still mix design, art, engineering, and QA around one player outcome, while the craft lead keeps the quality bar. [Cross-discipline teams](https://medium.com/@chris.casanova/structure-teams-to-win-15d98e65c5d7)

The critical path is the dependency chain that decides when the slice can be played. It is not the whole backlog. Work that does not sit on that chain is later, or future. Art scope for a slice is the camera path the player actually walks, counted once, not every name in a design doc. [Milestone schedule](https://www.productionalchemist.com/p/production-101-13-how-to-build-a), [Art scope](https://nastyrodent.com/vertical-slice-art-scope/)

## What we have now

| Card | Running list |
|---|---|
| Art | None. The card says there is no sitting checklist. |
| Asset | `Docs/art/ASSET_CONTEXT_TASKS.md` |
| Gameplay | None. The card follows whatever lock the chat names. |
| Testing | None. The card follows whatever prove the chat names. |

`Docs/context/SESSION_START.md` is already the one start door. It is not yet a picture of critical path, later, and future.

## Proposed rooms

Three craft rooms. Session start stays the production door. No fifth craft room. The art bible stays the look law inside the look room. It is not its own fork.

| Room | Owns | Task list |
|---|---|---|
| Look | Stills, meshes, Mixar export. Art and asset are this one room. | `Docs/art/ASSET_CONTEXT_TASKS.md` |
| Play | Beats, locks, what the player does. | A new `Docs/context/PLAY_TASKS.md`, fed from the active queue in `Docs/CANON_MAP.md`. |
| Prove | What done means. One named prove at a time. | A new `Docs/context/PROVE_TASKS.md`, fed from open proves. Not a sign-off the agent can tick. |

Audio and a standalone engineering room stay off the fork list until a critical-path beat is blocked on sound or on code alone. Until then they are co-fork tags on a Play or Look task.

## Three lanes

Every task is one of these. The sitting queue only walks the first lane.

- **Critical path.** The prototype cannot be generated or played without it. Now: player turnaround audit, cabin turnaround, partner, child, then the field and camp pieces the rescue loop stands on.
- **Later.** In this prototype, not blocking the next playable step. Edge, perch, shrine, barriers, and the lair after the mouth.
- **Future.** Dogs, cats, the rest of the animals and humanoids, and any second mesh for night. Night stays NightMix on the same mesh.

## Co-fork

A task has one owner room and zero or more blockers in other rooms. The owner does not start the blocked step. Session start, when it opens a room, reads that room’s list and says the first critical-path item whose blockers are done.

Examples:

- Partner stills are Look. The camp seated pose waits on that same mesh.
- A cabin mesh is Look. Placing it in the level is Play or engineering-tagged, and it waits on a kept mesh.
- A prove is Prove. It waits on the beat existing in a build.

## What session start would do

It stays the only start. Mode and close do not move. After the reads, if the work is the project picture or “what next,” it does not offer four rooms. It opens the three lists, names the first critical-path item that is not kept, and starts that item’s room.

A look task opens `Docs/context/ART_ASSET_DOOR.md`. A play task opens the named lock. A prove task opens the named prove. One item, then stop for a keep, a reject, or the next lock.

## Not in this proposal

Renaming the four cards before this plan is accepted. Deleting `FORK_ART.md` or `FORK_ASSET.md` before the look room exists. Generating stills or meshes. Checking track boxes.
