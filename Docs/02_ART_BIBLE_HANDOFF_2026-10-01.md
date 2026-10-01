# Art direction handoff — 2026-10-01

For the desktop agent. Read this with `Docs/02_ART_BIBLE.md`. That file is the look law. This file is the reasoning that produced the 2026-09-30 lock and the next build order. Do not treat this as a second bible.

Repo: `XylarDark/HomeWorld`  
Look law: `Docs/02_ART_BIBLE.md` (updated on `main`, commit `5b47b7cc`)  
Export preset only: `AssetCreation/STYLE_GUIDE.md` (Mario Galaxy rounded pillar retired)  
Key art index: `VisionBoard/KeyArt/README.md`

---

## 1. What is locked

HomeWorld is semi-polygon with detail on top. Faceted masses, not flat untextured low poly, not photoreal, not Mario-Galaxy soft clay. Surface life sits on the facets.

- Player is small. World is large. Enemies and beasts are huge and often cropped.
- Player: Zelda/Pixar, unique but non-descript. Short geometric hair, muted coat, one warm scarf. Face built from brow, lid, and mouth planes. Not a hood, not Disney, not high fantasy. Enemies share that face language.
- One living eye per important object. Player face, beast eyes, cabin's brightest window, one leaning flower plus a bug, crystal inner shard plus a moth, campfire flame. A second eye usually adds noise.
- Two cameras, same assets, never rescale. Intimate among beds or fire. Default vista about 20 ft, orbit allowed.
- Night is `NightMix` on the ten masters, not a second mesh. Emotion is climate around the same silhouette.
- Contract shot: dusk homestead, player looking back, uneven warm windows, porch lamp, herbs, lupine bee, crystal moth, cropped moss-bear with readable eyes.
- Second location test: planetside night camp. Same player, three larger enemies of different heights, club / sword / bow, starry sky, mountain, pines. Fire is the warm window.

Kept from the 2026-09-16 bible: palette, NightMix, ten masters, pine and torn-cliff rules, shot gates. Superseded: hooded player, no-beast reject, rounded-clay style. The no-beast reject is lifted only for the homestead bear and the planetside camp.

---

## 2. Image-to-3D pipeline (what to install)

Blender MCP cannot generate a mesh from an image. It imports and cleans. The UE back half already exists: `AssetCreation/Exports/<Category>/` and `Content/Python/batch_import_asset_creation.py`.

Install only:

1. Blender MCP (ahujasid/blender-mcp) if it is not connected. Cleanup hand, not generator.
2. glTF importer (ships with Blender).
3. One free generator. No GPU: Hugging Face space for Hunyuan3D-2.1 or TRELLIS. With an NVIDIA GPU (about 8–12 GB): ComfyUI plus Hunyuan3D-2.1 nodes. TRELLIS is the lighter fallback.

Do not install Tencent Cloud Hunyuan MCP (needs API keys). Do not make Meshy, Tripo, or Rodin required. Do not add a second in-viewport generator addon.

Missing script the desktop agent should add: `AssetCreation/Blender/cleanup_ai_glb.py`.

Flow:

1. Concept image, plain background, one object.
2. Generate. Save GLB to `AssetCreation/AI_Sources/`.
3. MCP runs the cleanup script: import, decimate to bible budget (kit 40–300, cabin 2k–8k, beast body 8k–25k), shade flat, mark sharp, freeze custom normals, origin at ground contact, apply scale.
4. Export FBX: forward X, up Z, face smoothing, FBX 2020.2, into `AssetCreation/Exports/<Category>/`.
5. Existing UE batch import.

Facet read comes from decimate plus flat shade, not from asking the generator for low poly. Wrong silhouette: regenerate. Wrong density: decimate. Quad remesh only for hero face, crystal, and beast head.

---

## 3. Industry read, early October 2026

Sources: 2026 State of the Game Industry survey coverage (about 2,300 professionals), Steam AI-art backlash writeups, r/IndieDev and r/Games threads, X gamedev posts 29 Sep–1 Oct 2026.

- 52% of developers say generative AI is hurting the industry, up from 30% in 2025. Artists 64% negative. Design and narrative 63%. Programmers use it most and dislike it least.
- Actual use: research 81%, code and daily tasks 47%, prototyping 35%, asset generation 19%.
- Player backlash is about unedited visible work: cutscenes, character design, key art, dialogue. The word slop means generated content that was never reviewed. Inconsistent resolution (mixels) is the same tell as an old asset flip.
- Indies get the public beating. Store pages with raw AI stills are the risk. Code help and private prototypes are not the thing being review-bombed.
- Readable space without yellow paint is being praised (Control Resonant discussion, late September 2026). Environment should point the player.

---

## 4. What makes this product shine

The dusk homestead already has the missing thing: one face language, one scale ruler, one warm light against a cool world. Keep AI behind that lock. Ship the cleaned mesh, not the GLB.

Cabin window, path, shrine, and campfire already point the player. Do not add a quest marker until the path fails.

---

## 5. What is weak

- Still two key-art stills and a bible. No playable minute where the player walks the path, the bear reads, and the fire holds the frame.
- Planetside camp reads as a generated enemy set. Three bear-brutes with different props, one body language. The homestead bear works because it is one cropped guardian. The camp needs one role each.
- Raw image-to-3D will fight the bible. Without the cleanup script, the pipeline produces the inconsistent kit forums call slop.

---

## 6. Build order

1. One playable dusk loop: path, cabin eye, shrine eye, bear eyes. Same assets at intimate and far camera.
2. `cleanup_ai_glb.py` before any more generators.
3. Split the three camp enemies by silhouette, not by weapon only.
4. Do not put raw AI stills on a store page.

Open, not locked: family face-kit, day planetside palette, dawn-after-storm homestead, enemy species beyond the bear and the three camp brutes.

Encoded stills were prepared locally (`homestead_dusk_baseline`, `player_expression_sheet`, `homestead_dusk_face_pass`) but the GitHub connector could not take the 130–350 KB base64 payloads. Planetside camp still was not on disk.
