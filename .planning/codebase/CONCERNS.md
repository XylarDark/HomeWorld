---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Concerns

**Analysis Date:** 2026-09-28

## Active Product Horizon

- `swarm/PHASE_BOARD.md` (2026-09-27 Lead lock): **Harness / bot optimization — idle**
- CAP + EA **DROPPED** from backlog (not HELD)
- Ball: Conductor — next harness bite only when Lead names one
- **Do not invent** Co MUST Acts or product roadmap phases in GSD

## Tech Debt / Fragility

**Case-sensitive Docs vs docs:**
- `Docs/` and `docs/` collide on default Windows/macOS checkouts — CI Linux or case-sensitive volume needed for both trees simultaneously

**UnrealMCP plugin gitignored:**
- Local install required; cold clones need Setup-MCP path

**KEEP-LOCAL characters:**
- `Content/Characters/` never committed — DESKTOP must copy from UE TemplateResources (Docs/17e)

**Placeholder / stub surfaces still in Source:**
- Boss / GC / night encounter / minigame stubs (`*Placeholder*`, `*Stub*`, NFT/leaderboard subsystems) — historical product; do not expand without Lead-named Act

**START_HERE.md still mentions UE 5.7 in one header line** while `HomeWorld.uproject` and `AGENTS.md` lock **5.8** — treat 5.8 as authority

## Process Risks

- Inventing GSD phases that open product work past PHASE_BOARD would fight Co outer loop — **forbidden**
- Task/cloud agents running DESKTOP Shell/MCP/PIE — forbidden (HS-B / HR3-D)
- Silent skip of HS-D re-verify before polish — forbidden
- Auto-committing `.opencode/` — forbidden (untracked GSD install)

## Security

- MCP / `.env` configs gitignored — keep credentials off git
- No secrets belong in `.planning/codebase/*`

## Performance

- Open world + Mass/PCG — profile before large content Acts; not a current GSD host phase

## Known Tracking

- Live errors: `docs/KNOWN_ERRORS.md`
- Automation impossibilities: `docs/Automation/AUTOMATION_GATS.md` / `AUTOMATION_GAPS.md`
- Closed product tracks through Docs/30 Demo Spine — see PHASE_BOARD POST-AUDIT table

---
*Concerns analysis: 2026-09-28*
