# Repo optimization audit — 2026-10-02

Feature branch only. No moves in this commit. Numbers are from `main` at the time of the audit (4,313 tracked files).

## What the active projects actually do

The worked-on open Unreal trees are plugins and samples, not solo games with a second agent OS in the root.

| Project | What they keep in the repo | What they refuse |
| --- | --- | --- |
| Lyra (Epic sample) | `Content/` for shared assets, gameplay in `Plugins/GameFeatures/<feature>/` with its own Content, Config, optional Source | One giant game module; assets at the Content root |
| Cesium for Unreal (~7k commits, 1.2k stars) | `Source/Runtime` and `Source/Editor`, each `Public/` and `Private/`. Docs in `Documentation/`. Tests in `TestsProject/` | Editor-only code in the runtime module |
| Xist Common Game Sample, Rade | `Config`, `Content`, `Source`, `Plugins`, plus README / gitignore / gitattributes | Prompt files, session logs, and key art at the repo root |

Lyra’s lesson for a solo project is not “add Game Feature Plugins now.” It is: one namespace under `Content/HomeWorld/`, features as folders, and do not let generated actor files become the repository.

## HomeWorld, measured

| Area | Files | Share |
| --- | ---: | ---: |
| `Content/__ExternalActors__/HomeWorld` | 2,948 | 68% |
| `Content/__ExternalObjects__/HomeWorld` | 9 | — |
| Rest of `Content/` | ~377 | 9% |
| `Docs/` | 289 | 7% |
| `docs/` (same folder on Windows) | 154 | 4% |
| `Source/` | 171 | 4% |
| `Lib/` | 55 | — |
| `.cursor/` | 54 | — |
| `VisionBoard/` | 31 | — |
| `scripts/` | 30 | — |
| `swarm/` | 27 | — |

`Docs/` and `docs/` are one directory on this machine (DEC-0029). Git on a case-sensitive remote still stores both casings as separate paths. That is a real split, not only an editorial one.

Root also carries `HOMEWORLD_MASTER_PROMPT.md`, `HOMEWORLD_MVP_SWARM_BRIEF.md`, `SylizedProvencal.png`, and several `.bat` launchers next to `README.md`.

`Source/HomeWorld/` is one runtime module. Gameplay, subsystems, tests (`HomeWorldCampNightTests.cpp`), and types sit as sibling files. `Source/HomeWorldEditor/` exists, which matches Cesium’s Runtime/Editor split. The runtime module does not use `Public/` and `Private/`.

## Priority

1. **External actors.** 68% of the tree is World Partition one-actor-per-file output. Epic’s own guidance is to Git LFS those, or to stop tracking them and regenerate from the map. Until that is decided, every clone, agent scan, and diff pays for them. Do not “organize” them. Decide track-or-ignore.
2. **Doc gravity.** 443 doc files plus `VisionBoard/`, `swarm/`, `.planning/`, and root prompts. Agents already have `Docs/CANON_MAP.md` and a quarantine list. The optimization is a closed entry set: `START_HERE.md`, `AGENTS.md`, `Docs/CANON_MAP.md`. Move root prompts under `Docs/handoffs/` only after a steer confirm — moving them changes links.
3. **Source shape, not a rewrite.** New files go in `Public/` or `Private/`. Do not mass-move existing headers in this pass. Editor-only commandlets stay in `HomeWorldEditor`. Camp night tests do not belong beside the subsystem they test; a `Source/HomeWorld/Private/Tests/` folder is enough.
4. **Content namespace.** Real authored assets already sit under `Content/HomeWorld/`. A few Blueprints sit on `Content/HomeWorld/` itself (`BP_Cultivation_POI`, `BP_Mining_POI`). Lyra and the indie write-ups both say nothing loose at the feature root. Move those in the editor, not by renaming files on disk.
5. **Do not add Game Feature Plugins yet.** Lyra uses them because experiences load and unload. HomeWorld is one slice. A plugin boundary now is a new always-loaded surface, which this harness already trims.

## Out of scope

No `Source/` moves, no Content Browser renames, no LFS migration, no deletion of external actors in this branch. Those are steer decisions: track external actors or ignore them; keep both doc casings or collapse to one on a case-sensitive remote.
