# Prototype pipeline

One asset, inside Polish → Final, after its stills are kept. The transitions are in `PHASES.md`. This file stays closed until Polish → Final. Image work before that follows `Docs/art/STILL_GENERATION_STANDARD.md`: sheet, then turnaround, then a scene. The agent names the tool and the reject list. You accept or reject. Nobody checks a track box until you say that step's pass bar is true.

Law stays in `Docs/02_ART_BIBLE.md`. Prompts stay in `Docs/art/PROTOTYPE_ASSET_BRIEFS.md`. Order and pass bars stay in `Docs/art/PROTOTYPE_ASSET_TRACK.md`. Paste block stays in `Docs/art/VISUAL_NOTES_FOR_GENERATION.md`. Export rules stay in `Docs/04_EXPORT_TABLE.md`.

Do not promote a mesh into `Content/`. Drafts shelf under `AssetCreation/Exports/<Category>/`. Night is NightMix on the same mesh.

## 1. Brief

| | |
|---|---|
| Tool | The image tool you already use. |
| Agent | Copy one prompt from the briefs. Append the paste block. Stop. |
| You | Generate the still. Keep it or reject it. |
| Reject | Thumbnail fails, or a priority note fails: size, planetoid, calm, text, or a rune. |

## 2. Mesh

Only after you keep the still. Image-to-3D from that still. Do not start a fresh text-to-3D.

| | |
|---|---|
| Tool | Tripo for a draft prop. Meshy when the set must match the last accepted mesh. Rodin only for a close hero still, and only if the facets survive. |
| Agent | Name which of those three, and the poly cap. Stop. |
| You | Generate the mesh. Keep the silhouette or go back to the still. |
| Reject | Silhouette fails with texture off. Facets gone. Photoreal texture on a faceted set. Over the cap: prop 4,000, bull or guard 8,000, giant 15,000 after decimate. |

A rigid prop may be decimated. Partner, child, guards, and the bull are a shape reference, then a hand mesh. Do not keep an AI retopo on a face or a limb that bends.

## 3. Blender hand pass

| | |
|---|---|
| Tool | Blender. |
| Agent | Name the checklist. Stop if `blender.exe` is missing. Do not invent another exporter. |
| You | Texture off. Facets stay. Pivot at the contact. Scale applied. No baked light. Box collision. Name from the briefs. |
| Reject | Smoothed clay, a floating pivot, a non-1 scale, a baked light, a name that is not in the briefs. |

## 4. Two looks

| | |
|---|---|
| Tool | The same mesh, two distances. |
| Agent | Ask for the two shots. Do not grade them. |
| You | Look from the play camera, near the 1.8 m body, and from the scenic camera. Wild size is `Docs/art/SCALE.md`. |
| Reject | It only reads at one distance, or the mesh was rescaled to cheat the lens. |

## 5. Shelf

| | |
|---|---|
| Tool | FBX. Meters. Apply scale. Origin at ground contact. `-Y` forward, `Z` up. |
| Agent | Name the export-table folder. Do not copy the file into `Content/`. |
| You | Say the pass bar is true. Then the track box may be checked. |
| Reject | A file under `Content/`, a second night model, or a box checked before you say so. |

Unreal assembly is a later sitting, after a mesh has survived the two looks.

## First step

The track's first unchecked step is `SM_Home_Cabin`. Prepare that prompt only when the sitting starts. Do not check PA-1.1 in this file.
