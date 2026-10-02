# PROMPT — T0 Human Desktop Pipeline Tutorial

**ID:** `T0_HUMAN_PIPELINE_TUTORIAL`  
**Kind:** Interview EXIT — IMPLEMENTATION (human-owned taste + asset/layout labour)  
**Author:** HW Conductor  
**Date:** 2026-10-02  
**For:** Lead pastes this **entire file** into Grok (phone OK). Grok returns EXIT as a **desktop tutorial** the Lead follows in person. Conductor ACCEPT later when `EXIT_T0_HUMAN_PIPELINE_TUTORIAL.md` lands in-repo.

---

## ROLE

You are advising **Luke Thompson (Lead / human AD + mechanic owner)** on HomeWorld (UE 5.8, PC + Steam Early Access).

He has concluded (correctly per ownership) that **AI agents hit a ceiling** on: art feel, silhouette distinctness, third-party asset generation taste, and crafting playable space. Agents remain useful for **manual labour** (measure, place-if-absent, report, import checklist, prove greps) — not for **setting feel** or **authoring the look**.

Your job: design a **human-first pipeline + step-by-step desktop tutorial** that develops **already-outlined T0 prototype gameplay + greybox/env-art**, using the repo’s locked docs. Do **not** invent a new product track or new MUST beats.

---

## CONTEXT

| Pin | Value |
|-----|-------|
| Repo | `C:\dev\HomeWorld` (GitHub `XylarDark/HomeWorld`) |
| `main` tip (at prompt write) | `07c98d0` |
| Map | `Maps/VS_MVP` / `L_VS_MVP_Markers` |
| Engine | UE **5.8** only |
| Live product track | **T0 / PROTOTYPE** — 14 MUST beats, Lead `APPROVE-PROTOTYPE-LIST` stamped 2026-09-27 |
| Impl state | Feature Acts for M1–M14 largely **merged**; board says **MERGED / NOT PROVEN** (prove result sections missing) |
| Env-art | Folded **into** T0 (not a separate track). Greybox tier; silhouette distinctness is a **mechanical** requirement (zone announces by environment alone) |
| Current measured defect | `SM_NODE_PLANT_SLOT_DAY_PLANTED` reads **flat** (bbox 0.9×0.9×0.12); heal signature wants **narrow upright, single soft column**. Spec itself notes day soil pad *should* read flat until nurture — **taste fork for Lead**, not an agent retune |
| Tooling live | Blender 5.2.2 LTS (Steam); `Content/Python/graybox_spec_reader.py` measures/places-missing/never overwrites; report `Docs/qa/GRAYBOX_SPEC_REPORT.md` |
| Agent vs human | `docs/human-use/OWNERSHIP.md` — **Taste + Test = Human**; Architecture/Code/Harness = Agent |

---

## CANON

Read and **do not contradict** these (paths relative to repo root):

1. `docs/human-use/OWNERSHIP.md` — taste/test human; what agents must not invent  
2. `Docs/02_ART_BIBLE.md` — especially §5 / §7 / §8 / §10 / §11 Pipeline  
3. `Docs/34_ART_PIPELINE_RESEARCH.md` + DEC-0015..0018 — **deterministic batch from authored master**; fail-closed on free AI mesh tiers; Hunyuan/TRELLIS forbidden for ship  
4. `Docs/32_PROTOTYPE_ASSETS.md` — PA CLOSED (homestead dress precedent)  
5. `Docs/33_PLACEMENT_STILLS.md` — placement **testing** stills (UE confidence), not image→mesh center  
6. `Lib/00_Core/GRAYBOX_LAYOUT.md` — 39 volumes  
7. `Lib/01_Homestead/*.json` + `Lib/02_Zones/**/*.json` — geometry / zone specs  
8. `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` — 14 MUST + CUT/DEFER  
9. `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` — frozen labels (`NODE_*` `TOD_*` `FORM_*` `EJECT_HOME` `CAM_T0_*`)  
10. `Docs/TaskLists/T0_PROTOTYPE_TRACK.md` — art-as-column-in-T0-bites  
11. `swarm/PHASE_BOARD.md` § T0 / PROTOTYPE track  
12. `Docs/handoffs/TASTE_GATE_ZONE_FAMILY.md` — seven families; section = family; silhouette law  
13. `AssetCreation/Exports/MVP_EXPORT_MANIFEST.md` + `AssetCreation/STYLE_GUIDE.md`  
14. `Content/Python/graybox_spec_reader.py` + `homeworld_graybox_silhouette.py` — existing reader; **do not propose a second reader**  
15. `Docs/20_UASSET_AI_POLICY.md` — never commit `.uasset`/`.umap` from agent whims  

Standing OpenCode paste (optional context, may be stale):  
`%LOCALAPPDATA%\Temp\opencode\hw-art-pipeline-handoff.txt`

---

## ASK

Produce an EXIT document that is, itself, a **Lead desktop tutorial**. Structure the EXIT with the contract sections below, but make the bulk a **runbook the human follows at the desk**.

### Required EXIT contents

1. **Diagnosis** (≤15 lines) — why AI plateaued here; what remains agent-safe labour vs Lead-only taste.  
2. **Pipeline map** — one page: stages from **locked T0 beat → Lib/zone spec → Blender greybox → (optional paid 3rd-party / hand author) → FBX → UE place on VS_MVP → stills prove → Lead taste stamp**. Name tools; mark which stages are Human vs Agent-assist.  
3. **Desktop tutorial** — ordered sessions the Lead can finish in one sitting each (target 45–90 min). For **each** session include:
   - Goal (one unknown)
   - Preconditions (apps open, paths)
   - Click/command steps (Blender / UE / external tool)
   - What “good enough for T0” looks like (the 5 Lead bars: location, size, bones for refinement, rudimentary distinctness, playtestable)
   - Evidence to save (still path, report path, gate note) — **no** fake PASS
   - When to stop and ask swarm (Conductor measure / Implement PR / Test score)
4. **Backlog walk order** — walk the **14 MUST** using existing inventories/gates; for each beat that needs **art/layout**, name the volume(s) / family and the **human** action (not a new invent PR). Call out especially:
   - `heal` / `NODE_PLANT_SLOT` (M3 day flat vs M12 sprout upright) — Lead taste fork
   - `spirit` / shrines + bed (M7/M11)
   - `combat` camp night actors (M14 Present?=N historically)
   - Homestead kit already PA-dressed vs still-greybox gaps from `GRAYBOX_SPEC_REPORT.md` blocking rows
5. **Third-party tools policy** — which generators (if any) may be used under DEC-0015; what never enters `Content/`; how Lead records paid-tier + sidecar. Prefer **authored Blender** over diffusion mesh for HW_Hero / face / silhouette-critical props.  
6. **Install instructions** — exact repo path to write the tutorial as:
   - `Docs/guides/T0_HUMAN_DESKTOP_PIPELINE.md` (create `Docs/guides/` if needed)
   - Optional checklist sibling: `Docs/guides/T0_HUMAN_SESSION_CHECKLIST.md`
   - Do **not** rewrite art bible or PHASE_BOARD; link them.
7. **Do bites** — only **human** or **tiny agent-assist** bites (measure, still capture, report refresh). Each: one unknown, DONE-WHEN path grep, forbidden co-changes. **No** “implement now.”  
8. **eggbot** — one line: no new Co seat; if a “tutorial runner” bot is useful later, defer.  
9. **child Research needed?** — Y/N.  
10. **Accept checklist** — for Conductor.

### Quality bar for the tutorial

- Written for a **tired human at a desk**, not for an agent.
- Assumes UE 5.8 + Steam Blender already installed on `DESKTOP-21CT3H0`.
- Never tells Lead to have the swarm “just generate the look.”
- Never invents MUST #15 or reopens CAP/EA.
- Never commits `.uasset`/`.umap` as the success condition; success is **Lead eyeball + playtest** with optional report.

---

## NON-GOALS

- No CAP / EA / ProveOps-as-default product Do  
- No new Co seats, no AGENTS.md body dump  
- No second greybox reader; no retune of locked heal silhouette **without Lead taste stamp**  
- No Hunyuan3D / TRELLIS for shippable Content; no free-tier Meshy/Tripo into Content  
- No inventing new mechanic labels outside `T0_MECHANIC_INVENTORIES_V1`  
- No claiming T0 prove PASS / `APPROVE-T0-*` for the Lead  
- No Architecture-first redesign ahead of working greybox volumes  
- No “agent will place all art for you” narrative  

---

## DONE-WHEN

When Lead (or Grok-at-desktop) has installed the EXIT tutorial:

```text
# files exist
Test-Path Docs\guides\T0_HUMAN_DESKTOP_PIPELINE.md
# tutorial cites canon (not empty advice)
Select-String -Path Docs\guides\T0_HUMAN_DESKTOP_PIPELINE.md -Pattern 'OWNERSHIP|02_ART_BIBLE|34_ART_PIPELINE|PROTOTYPE_FEATURE_LIST|graybox_spec_reader|NODE_PLANT_SLOT'
# EXIT filed for Conductor ACCEPT
Test-Path Docs\handoffs\research\EXIT_T0_HUMAN_PIPELINE_TUTORIAL.md
```

Optional first human session DONE-WHEN (example — EXIT may refine):

```text
# after Lead finishes Session 1 (plant slot taste)
Test-Path Docs\qa\stills\plant_slot_day_planted_close.png
Select-String -Path Docs\qa\GRAYBOX_SPEC_REPORT.md -Pattern 'SM_NODE_PLANT_SLOT_DAY_PLANTED'
# Lead has written a one-line taste decision into the tutorial checklist (pass/fail is Lead’s)
```

---

## child Research needed?

**N** — unless EXIT discovers a **licensing** ambiguity on a specific paid tool Lead wants to buy (then one child Research on that ToS only).

---

## Accept checklist (Conductor)

- [ ] EXIT has Diagnosis, Pipeline map, Desktop tutorial sessions, Backlog walk, Do bites, eggbot, child Research, Accept checklist  
- [ ] Tutorial installed at `Docs/guides/T0_HUMAN_DESKTOP_PIPELINE.md`  
- [ ] No implement-now; no CAP product Do; no second reader  
- [ ] T0 MUST walk cites existing handoffs; art column does not invent new beats  
- [ ] Fitness greps A–C on `$P` / `$E`  

---

## Paste note for Lead

Copy from `# PROMPT` through the Accept checklist into Grok. After Grok answers, save the answer as:

`Docs/handoffs/research/EXIT_T0_HUMAN_PIPELINE_TUTORIAL.md`

and have it (or you) write the tutorial body to `Docs/guides/T0_HUMAN_DESKTOP_PIPELINE.md` on DESKTOP. Ping Conductor in HomeWorld Co with those two paths for ACCEPT.
