# PLAYTEST.md

Living playtest log. Update when a prove lands. “Done” requires this file’s next test to pass.

## Last known good (2026-09-20 ET)

| Prove | Result | Notes |
|---|---|---|
| Canon locked test: day gather + `hw.Gather.Seed 1` | **PASS** | DESKTOP UE **5.8**; PIE `L_VS_MVP_Markers`; placed `GP_Gather_*` via `place_vs_mvp_resource_piles.py` (KEEP-LOCAL); `try_harvest_in_front` → `GATHER: RES_WOOD +1` / `harvest ok`; `hw.Gather.Seed 1` → `GATHER: RES_SEED +1` + inventory dump |
| VP2-A + VP2-B success-path | **9/9 PASS** (2026-09-17) | Prior Lead `APPROVE VP2-A` / `APPROVE VP2-B` |
| Docs/21 RS-B…E | Track CLOSED | DESKTOP PIE for RS sites often deferred |

What worked: UE **5.8** launch (uproject `EngineAssociation` 5.8 — do not launch 5.7 against 5.8-built DLL); wait for PIE login before gather script; place piles if `GP_Gather_*` missing; control-rotation aim in `d19_gather_only.py`.  
What broke this session: launching UE **5.7** → BuildId skip of `UnrealEditor-HomeWorld.dll` (editor hung ~320 MB, no MCP); running gather before PIE world ready (`pawn=None`).

Evidence: `Saved/canon_playtest_evidence.json` (local DESKTOP); log lines `GATHER: RES_WOOD +1`, `GATHER: harvest ok`, `GATHER: RES_SEED +1`.

## Next test (LOCKED, 2026-10-16)

Replaces the gather-and-seed test on `L_VS_MVP_Markers`. That gather passed on 2026-09-20 and stays in the log above. The rule is [`Docs/context/PRINCIPLE_FIT_LOCK.md`](../context/PRINCIPLE_FIT_LOCK.md) pick 9.

**One session on DESKTOP (UE 5.8), then stop.** Luke has not played this session. PIE `L_SizeTest` with no objective: walk, stop, and hop for about five seconds. Then, on `L_EasePad` (`/Game/HomeWorld/Maps/EasePad/L_EasePad`, [`Docs/level/L_EasePad_CONTEXT.md`](../level/L_EasePad_CONTEXT.md)), play one ease that can match, weak-hit, and bonk. Luke says what felt wrong. Write that note here. Do not add a system in that session. The stroke stays off `L_SizeTest` until the walk and hop have been played. The placer has saved the pad map. This session has not been played.

Pass = both checks were played, and the note of what felt wrong is in this file. Fail = a system was added in the session, or the stroke was placed on `L_SizeTest` before the walk and hop.
