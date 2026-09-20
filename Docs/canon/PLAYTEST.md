# PLAYTEST.md

Living playtest log. Update when a prove lands. “Done” requires this file’s next test to pass.

## Last known good (2026-09-17 ET)

| Prove | Result | Notes |
|---|---|---|
| VP2-A + VP2-B success-path | **9/9 PASS** | `L_VS_MVP_Markers`; DESKTOP `evidence:grep -- --success-path`; Lead `APPROVE VP2-A` / `APPROVE VP2-B` |
| D19 gather piles + `hw.Gather.Seed` | Landed | Sticky piles; seed cheat; success-path filter |
| Docs/21 RS-B…E | Track CLOSED | DESKTOP PIE for RS sites often **deferred** (MCP offline at stamp) — re-prove recommended |

What worked: control-rotation-aligned interact traces; single-verb MCP scripts; Safe-Build DLL size guard.  
What broke: mega one-shot PIE scripts; soft-reject mistaken for PASS; zero-byte `UnrealEditor-HomeWorld.dll`; abstract `HomeWorldResourcePile` spawn.

## Next 2-minute test (LOCKED)

**On DESKTOP, PIE `L_VS_MVP_Markers` in day/body: walk to a `GP_Gather_*` pile, interact once, confirm inventory gains +1 matching `RES_*` (log `GATHER:` success-path). Then run `hw.Gather.Seed 1` and confirm seed grant. Stop.**

Pass = both grants visible in log/UI. Fail = no grant, wrong form gate, or editor hang — file note here, do not start a second system.
