# Handoff

- **ID:** P5_SYS_data
- **Phase:** P5 / WAVE 4
- **Role:** SYS
- **Owner agent:** Executor (docs only; no UE C++)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Docs/03_SYSTEMS_MVP.md`
- `Docs/handoffs/P5_SYS_data.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| RES_WOOD / RES_FIBER / RES_STONE / RES_BERRY / RES_HERB / RES_SEED | RES_ data IDs | — (PROP meshes) | Docs tables |
| Inventory slots 0–5 (stack max 9) | SYS schema | — | Docs/03_SYSTEMS_MVP.md |
| Beast states wild / cautious / tamed / helper | SYS SM | M_BeastStylized (CHA) | Docs tables |
| Spirit hurt → healed (×3) | SYS state | M_SpiritUnlit | Docs tables |
| N1_Crop / N2_Stored → M_Nurtured | SYS flags | M_Nurtured | Docs tables |

## Phase exit boxes I claim

- [x] 6-slot inventory-lite specified (exactly 6; stack max 9; one stack per RES_ID)
- [x] RES_* table (six only) with gather / store / spend sinks from GDD
- [x] Beast states: wild → cautious → tamed → helper (no combat)
- [x] Heal: hurt → healed for three spirits
- [x] Nurture: two homestead targets onto `M_Nurtured`
- [x] Spend mapping: tame (berry/herb), heal (herb/seed), nurture (seed + stored)
- [x] No crafting tree, no combat, no extra resources

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path / PHASE_BOARD
- [x] No UE C++ / no crafting tree

## Inputs I used

- `Docs/00_CANON.md` §§3–4, §7
- `Docs/01_GDD_MVP.md` §§4–8, §10, Appendix A
- `swarm/agents/systems.md`
- `swarm/packets/WAVE_4_VERBS.md`
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- None for docs. Runtime binding waits on PROP World/Stored props + CHA beast/wisps + GP form flag.

## Risks for the next owner

- GP must gate spend attempts by day/body vs night/spirit; SYS tables assume a form flag from GP.
- Default heal cost is `RES_HERB`; `RES_SEED` is alternate — pick one per spirit at implement time, do not invent a seventh RES.
- N2 default Stored pile is `RES_WOOD`; PROP must expose one nurturable stored prop.
- Do not start WAVE 5 from this handoff; Conductor owns phase close.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `Docs/03_SYSTEMS_MVP.md`
  - `Docs/handoffs/P5_SYS_data.md`
- Screenshot / frame / render / checklist output:
  - N/A (data tables only this wave)
- Test or verify notes (command run + outcome):
  - Verified six RES_* IDs match canon/GDD; no 7th resource; spend sinks only tame/heal/nurture + visual store
