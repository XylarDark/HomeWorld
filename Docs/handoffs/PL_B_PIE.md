# PL-B Human PIE Verb Pass — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-B |
| **Status** | **OPEN / READY FOR LEAD Alt+P** — map/Manny prepped on DESKTOP; Lead away 2026-09-17 ~12:54 ET |
| **Lead gate** | **`APPROVE PL-B`** before PL-C (or explicit **WAIVE** per prefix) |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-B |
| **Map** | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| **Host** | DESKTOP **DESKTOP-21CT3H0** — Conductor parent + **Lead Alt+P** |
| **Prior debt** | [VP_A_PIE.md](VP_A_PIE.md) — WAIVE record **kept intact**; PL-B files real greps |

## DESKTOP prep (Conductor, Lead away)

| Check | Result |
|-------|--------|
| MCP ping | **PASS** |
| Config / BP mesh | **PASS** — `SKM_Manny_Simple` + `ABP_Unarmed_C` (`Saved/PL_B_ready.json` `manny_ok: true`) |
| Map open attempt | Console `OpenLevel` / `LoadMap` issued for `L_VS_MVP_Markers` — confirm in Editor viewport on return |
| Automation PIE greps | **Not run as PASS** — MCP PIE path remains unreliable (see VP-A); human Alt+P required |

## Goal

Close VP-A **WAIVE** debt with real Output Log lines after PL-A character spawn.

## One-shot Alt+P checklist (Docs/12c–12e)

1. Confirm map `L_VS_MVP_Markers` + Manny pawn (not Engine cube).
2. Clear Output Log filter → show all; later filter each prefix.
3. Run steps below; paste matching lines into the results table.

| # | Action | Expect prefix |
|---|--------|---------------|
| 1 | `hw.TimeOfDay.Phase 2` then `0` | `FORM: spirit form` / `FORM: body form` |
| 2 | Day: Interact at `GP_GlideStart` / CRUMB depart | `FALLBACK: TryStartFallbackGlide` (+ segment logs) |
| 3 | Walk `GP_PortalA` ↔ `GP_PortalB` | `FALLBACK: Portal` |
| 4 | `hw.Gather.Ore 1` / Interact harvest | `GATHER: RES_*` |
| 5 | Offer food at `GP_BeastPad`; wait ~4s | `TAME:` bond / state |
| 6 | `hw.Gather.Flowers 1` ×3; Phase 2; Interact `GP_SpiritWisp_A/B/C` | `HEAL: success` |
| 7 | Night/spirit at `GP_N1_Crop` / `GP_N2_Stored` Interact | `NURTURE: success` |
| 8 | `hw.TimeOfDay.Phase 3` | `DAWN: persisted inventory=` (+ `FORM: body form`) |

## Prefix checklist

| Prefix | Runbook cue | Result | Log excerpt |
|--------|-------------|--------|-------------|
| `FORM:` | Phase 2↔0 / Dawn | **PENDING** | |
| `FALLBACK:` | Glide + portals | **PENDING** | |
| `HEAL:` | Spirit wisps | **PENDING** | |
| `NURTURE:` | N1/N2 | **PENDING** | |
| `DAWN:` | Phase 3 | **PENDING** | |
| `TAME:` | Beast pad | **PENDING** | |
| `GATHER:` | Ore / wood / herb | **PENDING** | |

## Done criteria

- [ ] All six primary prefixes + supporting `GATHER:` have PASS or documented fail with log excerpt
- [ ] Character spawn confirmed in PIE (controlled pawn — Manny mesh visible)

## Hard rules

- Docs/07 CLOSED — no reopen
- No free-flight (FALLBACK glide only)
- No invented greps — only real Output Log lines
- No `.uasset` / `.umap` commits

---

*PL-B — READY FOR LEAD Alt+P (Conductor prepped DESKTOP while Lead away).*
