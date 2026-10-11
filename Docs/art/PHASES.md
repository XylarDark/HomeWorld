# Art phases

Now: Concept → Greybox
Previous: Concept, kept 2026-10-10

Say the Now line at the start of agent work, in the session header, before acting. The five names below are states. The work is the transition into the next state. Do the open transition. Leave the other four closed. A picture filed early does not open its transition.

The open context is `Docs/art/transitions/CONCEPT_TO_GREYBOX.md`. Open that file and `Docs/art/SCALE.md`. Leave the other transition files closed. Scale applies from Concept on.

## The five states

| State | What is true when it is kept |
|---|---|
| **Concept** | The card, the meters, and a mood still are kept. |
| **Greybox** | Texture-off mass at the written size is kept. Silhouette holds. A plan is kept if the asset has rooms. |
| **Prototype** | Faceted materials are kept. Front, then side, then back, one ground line, one design. Readable at about 20 feet. |
| **Polish** | A refinement of a kept prototype is kept. The player only. |
| **Final** | Mixar has cleaned the mesh from the kept stills, the FBX is exported, and that step’s pass bar has been called true. |

## The five transitions

Each transition is its own work. It has one entry, one job, and one keep. It does not borrow the next transition’s job.

### 1. Concept

| | |
|---|---|
| Entry | Kept 2026-10-10. |
| Context | `Docs/art/transitions/CONCEPT.md` |
| Job | Write or confirm the card and the meters. Keep a mood still. No build view. |
| Keep | The human keeps Concept. |
| Closed | Texture-off mass, orthographic sheets, materials as a build view, meshes. |

### 2. Concept → Greybox

| | |
|---|---|
| Entry | Concept is kept. |
| Context | `Docs/art/transitions/CONCEPT_TO_GREYBOX.md` |
| Job | Turn that kept mood into texture-off mass at the written size. Draw the plan if the asset has rooms. No story lighting. |
| Keep | The human keeps the mass, and the plan where there is one. |
| Closed | Faceted material sheets. Front, side, and back as a set. Meshes. |

### 3. Greybox → Prototype

| | |
|---|---|
| Entry | Greybox is kept. |
| Context | `Docs/art/transitions/GREYBOX_TO_PROTOTYPE.md` — closed. |
| Job | Faceted materials on that mass. Front first. Side is 90 degrees. Back is 180. One ground line. Readable at about 20 feet. |
| Keep | The human keeps that set. |
| Closed | UVs, LODs, a game-ready texture, a file in `Content/`. Polish. |

### 4. Prototype → Polish

| | |
|---|---|
| Entry | Prototype is kept, and the asset is the player. |
| Context | `Docs/art/transitions/PROTOTYPE_TO_POLISH.md` — closed. |
| Job | Refine the kept player prototype. Do not redesign it. |
| Keep | The human keeps the refinement. |
| Closed | Every asset that is not the player. Feel tuning. A mesh. |

### 5. Polish → Final

| | |
|---|---|
| Entry | Polish is kept for the player. For every other asset, Prototype is kept and Polish does not apply. |
| Context | `Docs/art/transitions/POLISH_TO_FINAL.md` — closed. |
| Job | Image-to-3D from the kept front and back. Mixar cleans and exports the FBX. The pass bar is called true. |
| Keep | That pass bar is true. |
| Closed | A mesh invented from text. A promoted `Content/` asset. |

Image-to-3D runs only inside Polish → Final, after the stills on that card are kept. Front and back are the same design. Mixar does not invent the design.

## How the longer lists fit

| Industry step | State it arrives at | Transition that does the work |
|---|---|---|
| Brief, mood, concept | Concept | Concept |
| Blockout, whitebox, greybox | Greybox | Concept → Greybox |
| Art blockout, no unwrap | Prototype | Greybox → Prototype |
| Unwrap, texture, LODs, export | Final | Polish → Final |
| In-engine dress and feel | After Final | Not one of these five. `Docs/37_POLISH_PASS_PROCESS.md` |

A level-design prototype pass is blockout. That work is Concept → Greybox. Our Prototype state is the faceted set.

S5 in the polish-process doc is feel tuning after a mesh is in the engine. Prototype → Polish is a still refinement of the player. It is not S5.

| Rung there | State here | Transition |
|---|---|---|
| S1 BLOCKOUT | Greybox | Concept → Greybox |
| S2 ART-BLOCKOUT | Prototype | Greybox → Prototype |
| S3 ASSET PRODUCTION | Final | Polish → Final |
| S4 DRESS and S5 FEEL TUNE | After Final | Not a still transition |

## Where a file lives

A still stays in its place folder. The transition is a line on the card. Do not move a picture into a transition folder.

| Place | Folder |
|---|---|
| Player | `Docs/art/player/` |
| Homestead stills | `Docs/art/homestead/` |
| Cabin plan | `Docs/art/cabin/` |
| Filed pictures | `Docs/art/STILLS_LIBRARY.md` |
| Which file is which job | `Docs/art/README.md` |
