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

## Played (2026-10-17)

Luke, desktop, UE 5.8, PIE `L_SizeTest`. Walk, stop, and hop. The movement felt good. It passes the initial pass. The ease on `L_EasePad` was not played in this session.

The opening to build and test is the five-minute tutorial in [`Docs/VISION_BOARD.md`](../VISION_BOARD.md) under Opening tutorial. That section is the canon. This file does not restate it.

Next played session: that opening, once a piece of it is in the level. One piece, then the note of what felt wrong.
