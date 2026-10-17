# T0 human desktop pipeline

Lead tutorial. Taste and Test are yours. Agents measure, place-if-absent, and report. They do not set the look.

Canon stays where it is. This file does not rewrite [Docs/02_ART_BIBLE.md](../02_ART_BIBLE.md) or [swarm/PHASE_BOARD.md](../../swarm/PHASE_BOARD.md).

| Pin | Value |
| --- | --- |
| Map | `Maps/VS_MVP` / `L_VS_MVP_Markers` |
| Engine | UE 5.8 only |
| Reader | `Content/Python/graybox_spec_reader.py` — do not write a second one |
| Report | `Docs/qa/GRAYBOX_SPEC_REPORT.md` |

## 1. Diagnosis

Agents stall on feel, silhouette, and whether a space is playable. A clean report is not a stamp. The heal slot is the example: `SM_NODE_PLANT_SLOT_DAY_PLANTED` measures 0.9 × 0.9 × 0.12, flat. The heal signature wants a narrow upright column. The day soil pad is supposed to read flat until nurture. That fork is yours. An agent that retunes the signature to pass has failed.

Agent-safe labour: read `Lib/01_Homestead` and `Lib/02_Zones` JSON, measure a live Blender scene, place a missing primitive without overwriting authored mesh, write the report, grep a beat against the map.

Lead-only: which silhouette is the beat, whether twenty metres reads, whether a third-party mesh is allowed in, ship or no-ship.

Feature Acts for the fourteen MUST beats are merged and not proven. The next work is you walking a bite, not another system.

## 2. Pipeline map

| Step | Who | Output |
| --- | --- | --- |
| T0 beat from [PROTOTYPE_FEATURE_LIST_V1.md](../handoffs/PROTOTYPE_FEATURE_LIST_V1.md) | Human | One MUST, named |
| Lib spec JSON | Human owns the numbers; agent may load them | `Lib/01_Homestead` or `Lib/02_Zones` |
| Blender greybox | Human authors silhouette-critical mesh; agent may `run(place=True)` only if absent | Blend + report |
| Paid third-party or hand | Human, DEC-0015 | Sidecar with tier; free tier never reaches `Content/` |
| FBX | Human export; agent checklist | `AssetCreation/Exports/` |
| Place on VS_MVP | Human in editor | No agent commit of `Content/*.uasset` |
| Stills | Human | [Docs/33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) |
| Taste stamp | Human | One line in the session handoff |

## 3. Desktop sessions

Each session is 45–90 minutes. Stop when the evidence path exists. Do not start a second beat.

### Session A — heal slot fork

Goal: decide day pad vs nurture column. Do not retune the signature.

Preconditions: Blender 5.2.2, repo at `C:\dev\HomeWorld`, report open.

Steps:

1. Read the plant-slot row in `Docs/qa/GRAYBOX_SPEC_REPORT.md`.
2. In Blender, frame `SM_NODE_PLANT_SLOT_DAY_PLANTED`. Stand back. If you cannot tell the beat at twenty metres, it has not said it.
3. Stamp one line: day pad stays flat until nurture, or the nurture volume is a second object. Do not edit `homeworld_graybox_silhouette.py` to make the fail go away.
4. If the volume is missing, an agent may call `graybox_spec_reader.run(place=True)` once. If it exists, do not overwrite it.

Good enough: location on the homestead, size written down, distinct from kettle and path, you can walk to it on VS_MVP.

Evidence: a sentence in `Docs/handoffs/SESSION_HANDOFF_heal-slot.md` plus the report path.

Stop and ask swarm if the spec origin and the blend origin disagree by more than the report tolerance.

### Session B — one other MUST, same shape

Goal: one row from the backlog below.

Preconditions: Session A stamped.

Steps: open the Lib JSON for that beat, measure, place only if absent, play VS_MVP, write what you saw.

Good enough: you can name the verb and the volume without reading the spec.

Evidence: handoff file. No `.uasset` commit.

## 4. Backlog walk order

Do not invent beats. Fourteen MUST from the stamped list, art and layout only:

1. Wake / start day on the homestead.
2. Kettle + herbs → tea. Distinct from the plant pad.
3. Plant given herb outside. Day pad may stay flat. This is the taste fork.
4. Equip backpack.
5. Glider to the open field.
6. Collect herb seeds in the field.
7. Rune unlock before bed → spirit.
8. Day camp eject. Not lethal.
9. Homeworld night without bed: no spirit.
10. Planetside night without bed: glider boot home.
11. Bed → spirit after rune. M7/M11 shrines and bed.
12. Nurture planted herb. Upright column if you stamped that in Session A. M12.
13. Home portal → camp portal.
14. Camp night: avoid one guard, soothe two sleepers. M14.

Homestead greybox rows in the report (porch modules outside the cabin footprint, island hero short) are blocking layout, not new beats. Clear them only when they stop you placing the current MUST.

## 5. Third-party tools

DEC-0015: the pipeline fails closed on free tiers. A free Meshy or Sloyd generation must not land in `Content/`. Paid tier is recorded in a sidecar and checked at promote. Silhouette-critical props (heal column, kettle, shrine, sleeper) are authored in Blender. Generation is a reference, not the mesh. No Hunyuan or TRELLIS into `Content/`.

## 6. Install

This file is the install. Checklist: [T0_HUMAN_DESKTOP_CHECKLIST.md](T0_HUMAN_DESKTOP_CHECKLIST.md).

## 7. Do bites

Human, or one agent assist: measure, place-if-absent, report. No implement-now. No `Content/*.uasset` commit.

## 8. eggbot

No new Co seat. Defer a tutorial-runner bot.

## 9. Child research

No. DEC-0015 and the art bible already cover third-party tools.

## 10. Accept checklist

- [ ] Tutorial is `Docs/guides/T0_HUMAN_DESKTOP_PIPELINE.md`
- [ ] No second reader
- [ ] Heal signature not retuned
- [ ] No new MUST labels
- [ ] No `.uasset` in the commit
- [ ] Conductor ACCEPT is a separate stamp
