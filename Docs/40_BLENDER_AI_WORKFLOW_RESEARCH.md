# Blender and AI workflow — research

**Date:** 2026-10-07
**Status:** Locked by Lead on 2026-10-07 (interview #19, 3A). The eight LIB rules in section 4 are the lock.
**When to use:** Before an agent edits `blender/floating_island_homestead_LIB.blend`, exports a kit, or treats a collection move as "just transforms."

This note is how HomeWorld should use Mixar (the project's Blender 5.2 build, with the MCP add-on) and export to UE 5.8. It does not change PR #297.

Web claims below are cited. Project facts are marked as project docs.

## 1. Game-asset practice

### Kits and modular pieces

A kit only snaps if every piece shares one grid and one pivot rule. Published kit practice uses a base module (often 1 m, or 100 / 200 / 400 cm in Unreal units) and puts every piece's pivot on the same corner of that footprint, on the floor. One centered pivot in a corner-pivoted kit is enough to open gaps. Greybox proxies should use the final dimensions and the final pivot before the real mesh exists. [Modular Kit Workflow in UE5](https://www.strayspark.studio/blog/modular-kit-workflow-greybox-to-final-ue5), [Build Modular Levels That Actually Snap Together](https://www.strayspark.studio/learn/tutorials/build-modular-levels-that-snap-together), [Modular Prop Kits for Games](https://nastyrodent.com/modular-prop-kits-for-games/).

Epic's own FBX page says the pivot Unreal uses is the origin at export time, and that placing that origin on a corner of the mesh is what makes grid snap work in the editor. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).

HomeWorld already chose a different, also valid, rule for props: ground contact, not a shared corner. That is locked in `docs/04_EXPORT_TABLE.md` (units meters, adult 1.8 m, origins at feet / underside). Do not silently switch the cabin or the camp to corner pivots. A new *snapping* kit (walls, path tiles) needs one pivot rule written down before the first piece.

### Scale and units

Blender 5.2's scene units can be Metric, with the meter equal to scale 1.0. [Scene Properties, Blender 5.2](https://docs.blender.org/manual/en/5.2/scene_layout/scene/properties.html).

Apply **Scale** (and Rotation when the piece is an exportable module) so the object scale is 1.0 and the mesh data carries the size. Apply **Location** is a different operation: it moves the object's origin to the world origin. [Apply, Blender 5.2](https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/apply.html). Agents must not "apply all transforms" on a placed kit.

Some UE tutorials set Blender's unit scale to 0.01 and work in centimeters. [Configure Blender for Unreal Engine 5](https://propgon.com/en/configure-blender-unreal-engine-5-workflow/). HomeWorld's export table already says meters. Stay on meters. Do not adopt the 0.01 recipe in this blend.

FBX "Apply Transform" (bake space into vertex data) is marked experimental in Blender's exporter and is known to break armatures. [FBX, Blender 5.1](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_fbx.html), [bpy.ops.export_scene](https://docs.blender.org/api/current/bpy.ops.export_scene.html). Static kit meshes can bake a scale of 1. Characters and anything animated should not use that experimental bake.

### Pivots and origins

The origin is the point Blender translates, rotates, and scales. Set Origin can move geometry to the origin, move the origin to the geometry or to the 3D cursor, or move it to the center of mass. [Object Origin, Blender 5.2](https://docs.blender.org/manual/en/5.2/scene_layout/object/origin.html). Affect Only Origins edits the origin directly and can move linked duplicates together. [Tool Settings, Blender 5.2](https://docs.blender.org/manual/en/5.2/scene_layout/object/tools/tool_settings.html).

For a HomeWorld `SM_` prop, the origin stays on the ground-contact point in the export table. For a socket, Epic wants a dummy named `SOCKET_[RenderMeshName]_##`, exported in the same FBX as that one render mesh. Two render meshes with sockets cannot share one FBX. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).

### Naming and collections

A readable kit name says which kit, which connection, which variant: `SM_KitWarehouse_WallStraight_01` is the pattern one pipeline writeup uses. [Modular Prop Kits for Games](https://nastyrodent.com/modular-prop-kits-for-games/). HomeWorld already uses `SM_`, `UCX_`, `M_`, `SOCKET_`, `CAM_`, `CRUMB_` with the same string in Blender and in UE (`docs/04_EXPORT_TABLE.md`).

A collection is a bag of objects, not a single kind of object. `02_Forest` currently holds kit meshes and the planet day lights. The export table already sends `07_Night_SpiritLayer` to lighting, not to a mesh FBX. Mesh kits and light rigs should not share a collection if an agent is allowed to move "the collection."

### LODs and collision

UE 5.8 imports LODs when Import Mesh LODs is on. Each LOD must occupy the same space and share the pivot. Materials may differ per LOD. UE can also autogenerate LODs after import. The 5.8 page does not publish a `_LOD0` suffix rule; it points at the DCC tool's own LOD setup. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). Graybox does not need hand-authored LODs. When a mesh is large on screen, Lead asks for LODs. Until then, leave LOD chains to UE autogeneration.

Custom collision is named from the render mesh and exported in the same FBX:

| Prefix | Shape |
|---|---|
| `UBX_` | Rectangular box. Do not move the vertices off a box. |
| `UCP_` | Capsule. |
| `USP_` | Sphere. Rigid-body and zero-extent traces only, and not if the mesh is scaled non-uniformly. |
| `UCX_` | Closed convex hull. Prefer this. |

`UCX_Tree_01`, then `UCX_Tree_01_00`, `_01` for more hulls. Hulls should not intersect. A non-convex mesh must be split by hand; the importer's split is unpredictable. Spheres and boxes fail if the static mesh is scaled non-uniformly. Importing several meshes that each have collision in one FBX only keeps the first mesh's collision. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).

UE 5.8 still documents FBX 2020.2 as the import pipeline's version. A different exporter version can break the import. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).

HomeWorld's export table already names the simple proxies (`UCX_SM_Cabin`, shrine boxes, landing disc). Match those names. Do not turn on complex-as-simple for a whole forest.

### Materials and texel density

UE's FBX import builds materials from the file and auto-connects color and normal only. Specular may import unconnected. Other maps often do not import. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). That path fights HomeWorld's ten masters and NightMix (`Docs/02_MATERIAL_SHEET.md`): night is a parameter, not a second texture set. Export the mesh. Assign the existing `M_` / `MI_` in UE. Do not let the importer create an eleventh material.

For unique textured props, texel density matters more than packing efficiency: a 1 m patch should carry about the same number of texels on every surface. Remeshing an AI mesh throws the UVs away, so density has to be set again after the retopo. [Blender-to-Game-Engine Pipeline, 2026](https://www.strayspark.studio/blog/blender-to-game-engine-pipeline-2026). HomeWorld's stylized masters make this a UV-scale check against the master, not a unique atlas per rock.

### Export path to Unreal

1. Metric meters, unit scale 1. Object scale 1 on every `SM_`. Rotation applied only when the module's rest pose should be zero.
2. Origin per the export table (ground contact) or per that kit's one pivot rule.
3. Collision and sockets named and in the same FBX as their one render mesh.
4. Axes: HomeWorld's table says **-Y forward, Z up**. Blender's FBX operator default in the current API listing is `-Z` forward, `Y` up. [bpy.ops.export_scene](https://docs.blender.org/api/current/bpy.ops.export_scene.html). Use the table, not the operator default.
5. Selected mesh only. Do not export the whole LIB scene. Lights stay out of the mesh FBX.
6. Stage under `AssetCreation/Exports/<Category>/`, then import to the UE path in the export table. UE 5.8 can also import from the editor toolset (`import_file`, with explicit flags for materials, textures, and combine). [StaticMeshTools, UE 5.8](https://tc-imba.github.io/ue-official-mcp/references/toolsets/editor_toolset.toolsets.static_mesh.StaticMeshTools/). Combine Meshes is off when the FBX is a kit of separate pieces. [FbxStaticMeshImportData, UE 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FbxStaticMeshImportData).
7. Triangulate simple graybox in the exporter if needed. Epic says hand triangulation is the controlled option, and automatic triangulation can pick bad edges. [FBX Static Mesh Pipeline, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). Hero silhouettes wait for Lead before anyone triangulates them.

### Git and `.blend` files

Git stores a binary as a whole new file when it changes. It does not produce a useful text diff. Git LFS replaces the blob with a small pointer and stores the bytes elsewhere. [About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage), [Git LFS (GitLab)](https://docs.gitlab.com/17.5/topics/git/lfs/).

Blender Studio's version-control tests found that **uncompressed** `.blend` files delta much better in ordinary Git, because compression rewrites most of the bytes every save. Git LFS does not delta; it stores each revision whole. Compressed blends plus LFS were competitive on size with SVN, and LFS was faster to commit, at the cost of keeping every revision. [Benchmarking Version Control, Blender Studio](https://studio.blender.org/blog/benchmarking-version-control-git-lfs-svn-mercurial/).

Git LFS file locking exists so two people cannot edit an unmergeable binary. `git lfs track "*.blend" --lockable` marks the path read-only until `git lfs lock`. A push that touches someone else's lock is rejected. [git-lfs-track](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-track.adoc), [File Locking (git-lfs wiki)](https://github-wiki-see.page/m/git-lfs/git-lfs/wiki/File-Locking), [Locking API](https://github.com/git-lfs/git-lfs/blob/main/docs/api/locking.md). The GitHub LFS pages retrieved for this note document pointers and plan size limits. They do not document the lock commands. A git-lfs issue comment says GitHub's lock server will lock a path even when `.gitattributes` does not say `lockable`. [git-lfs #4168](https://github.com/git-lfs/git-lfs/issues/4168). Treat `git lfs lock` on this GitHub repo as unconfirmed until someone runs it once.

Moving a file that is already in history into LFS means rewriting history. [Moving a file to Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/moving-a-file-in-your-repository-to-git-large-file-storage). HomeWorld's `.gitattributes` tracks UE content and some art folders. It does not track `*.blend`. The LIB blend is about 280 KB, so size is not why it is hard to review.

What actually makes a blend reviewable:

- One writer at a time. Mixar closed, no second save. A lock command is the tool if the host supports it. Until then the rule is social: one branch, one editor.
- One authoring app. Project `docs/KNOWN_ERRORS.md` says a Mixar save of a Blender 5.x blend downgrades the file, and that `mixar.exe --version` reports 4.2.2 while `bpy.app.version` reports 5.2.0. This LIB file is a Mixar save (zstd magic `28 B5 2F FD`). Open and save it with Mixar only.
- A text sidecar in the same change: object counts, world bounds, names that moved, names that stayed. The blend diff will stay opaque. The sidecar is the review.
- Do not enable Blender compression to "help git" if the file is still stored as a normal blob. Studio measurements say compression hurts deltas. [Blender Studio](https://studio.blender.org/blog/benchmarking-version-control-git-lfs-svn-mercurial/). Mixar already writes zstd, so this file will not delta cleanly either way. That is another reason for the text sidecar.

## 2. Blender and AI, as people are using it

### MCP and agent scripting

Blender does not talk to an LLM by itself. The official MCP setup is three pieces: Blender 5.1 or newer, an add-on inside Blender, and an MCP server the LLM client launches. The published examples are scene questions, screenshots, and explaining a Geometry Nodes tree. The result depends on the model. [MCP Server — Blender](https://www.blender.org/lab/mcp-server/).

The official tool list people are reading in the source is: scene and object summaries, missing files, linked libraries, screenshots, viewport and render, and Python execution. Generated Python runs in Blender. The repo's own sandbox is named as a weak sandbox, not a security boundary. [Blender MCP security notes, devtalk](https://devtalk.blender.org/t/blender-mcp-server-after-claude-mcp-security-for-blender-scripting-3d-agent-notes/45131).

The widely used community add-on listens on `localhost:9876` with no authentication. `execute_blender_code` is arbitrary Python, including the disk, unless safe mode is on (`BLENDER_MCP_SAFE_MODE=1`), which blocks direct file I/O, subprocesses, and network. Only one client should connect. Save before letting an agent run code. [How MCP for Blender Works](https://www.mcp-for-blender.com/docs/concepts/how-it-works), [Configuration](https://www.mcp-for-blender.com/docs/reference/configuration).

What works: read the scene, measure bounds, rename, move objects whose class is already decided, export a named selection, render a still for a human. What does not: leaving a GUI session open while an agent also drives port 9876, treating a screenshot as art approval, or letting generated Python save the blend with no assertion. HomeWorld has already hit the port collision: a Mixar GUI and a headless MCP server both want 9876 (`docs/KNOWN_ERRORS.md`).

### Geometry Nodes

Geometry Nodes are a generator inside Blender. They are fast when instances stay instances, and they get expensive when you realize instances, boolean dense meshes, or nest node groups until the stack limit. [Geometry Nodes Performance](https://docs.blender.org/manual/en/dev/modeling/geometry_nodes/performance.html).

FBX and OBJ do not store the node graph. Export bakes the evaluated mesh. People trying to export instances hit Join Geometry duplicating meshes, and the practical answer on artist forums is: the game does not run Blender's graph; rebuild the scatter in the engine or spawn instances there. [Export geometry nodes instances](https://blenderartists.org/t/how-to-export-geometry-nodes-instances-in-a-game/1419992). A 2026 pipeline writeup says the same of USD: the file gets the baked result, not the parameters, and procedural material slots can shift on every reimport. Alembic is for baked animation, not for a live kit. [Geometry Nodes to Unreal Engine, 2026](https://www.strayspark.studio/blog/geometry-nodes-to-unreal-engine-2026-pipeline).

What works: a node group that builds one module (a pine, a fence span) which an artist then realizes and exports as an `SM_`. What does not: using Geometry Nodes as HomeWorld's zone generator. The zone generator is already C++ plus JSON specs. A Blender graph would not survive the FBX hop, and it would not be what the player runs.

### AI mesh and texture generators

Text-to-mesh and image-to-mesh tools (Tripo, Meshy, Rodin, and the same class) can produce a turntable mesh. The same writeups describe the usual result: tens or hundreds of thousands of triangles, non-manifold faces, UVs that are not packed for a texel density, and color that is not a PBR set. A game prop of the same read is often a few thousand triangles. Retopology or remesh throws the UVs out, so textures are rebaked. Decimate keeps bad flow and bad deformation. AI retopo does not place the loops a shoulder or a knee needs. [Blender-to-Game-Engine Pipeline, 2026](https://www.strayspark.studio/blog/blender-to-game-engine-pipeline-2026), [Clean up an AI model](https://triverse.ai/blog/clean-up-ai-model-in-blender-tutorial), [Tripo cleanup](https://www.tripo3d.ai/blog/how-to-clean-up-ai-generated-3d-models-in-blender), [Meshy retopology](https://www.meshy.ai/tutorials/ai-retopology-guide), [Meshy to Blender](https://help.meshy.ai/en/articles/16100257-meshy-to-blender-cleanup-workflow).

What works: a private reference for a human who is about to block out a shape, if Lead asked for that reference. What does not: dropping the generated mesh into `02_Forest` or onto a master material. It will not match the ten-master sheet, the silhouette will not be the one Lead is drawing, and the cleanup is longer than building the graybox box.

## 3. Who does what

| AI agents | Humans (Lead) |
|---|---|
| Measure a collection and print bounds, counts, parents, and types | Decide the silhouette and whether a shape is the one |
| Block out boxes to a spec envelope that already has numbers | Art direction, palette, and the ten masters |
| Placement math from a spec (offsets, shelf translations) on objects whose class is meshes | Whether a light, camera, or volume moves |
| Batch rename to `SM_` / `UCX_` / `SOCKET_` when the pattern is already the export table | New names that are not in the table |
| Export the FBX with the checklist in section 1, to the staging folder | Import approval and the in-editor read |
| Reopen the file and assert the bounds that were promised | Final sign-off, including the blend PR |
| Write the text sidecar so the review is not a binary diff | Merge |

An agent does not apply a collection move to every object in the collection. It classifies first. An agent does not call a render a pass. An agent does not invent a pivot rule.

## 4. Rules for this LIB blend

Locked by Lead on 2026-10-07 (interview #19, 3A).

1. **One blend, one app.** `blender/floating_island_homestead_LIB.blend` is edited in Mixar only. Steam Blender 5.2.2 does not resave it.
2. **One writer.** Mixar is closed before an agent opens the file. The agent saves only from a background run, and only after the assertions pass. A failed check leaves the file untouched.
3. **Meshes move. Lights, cameras, and volumes do not,** unless Lead named that light. A collection name is not a license to transform every object in it.
4. **Kit shelf is a rigid move of `SM_` meshes** (and their mesh parents), plus a text sidecar. World placement of a zone is the C++ generator, not a pile of objects at the field origin.
5. **Export from the table.** Meters, scale 1, ground-contact origin, `-Y` forward / `Z` up, one render mesh per FBX when it has collision or sockets, no importer-created materials.
6. **No AI-generated mesh in the LIB** unless Lead accepts that mesh as a reference and a human rebuilds it as an `SM_` on a master.
7. **Geometry Nodes, if used, die at export.** Realize, apply scale, export the `SM_`. The zone seed stays in C++.
8. **The reviewable diff is the sidecar and the JSON contract,** not the blend bytes. LFS stays off this file until the file is actually large or Lead has confirmed GitHub locking. Do not `git lfs migrate` this history as a side effect of a kit edit.

### Worked example: `LIT_Planet_Fill` in PR #297

Lead asked to park `02_Forest` and `06_Camp` off-world as kit and template source. The agent measured, then translated objects by +10000 m on X.

Reopened mesh bounds after the save:

- `02_Forest` meshes: x 9962.672..10046.841, y -166..-65, z -95.2..-10. Outside the field box (x -210..210, y -290..130).
- `06_Camp` meshes: x 10015.496..10021.790, y -82.2..-75.7, z -95..-93.5. The five `SM_Camp_*` pieces. Outside the field box.
- `01_Homestead` meshes stayed at about (-84.09, -50, -12) to (84.25, 50, 10.45).

Two lights at the island origin stayed: `LIT_Planet_Sun` (sun, energy 3.2) and `LIT_LandingDay` (area, energy 120, size 12 m). Those are the right kind of exception under rule 3. They light the island datum. They are not slot templates.

`LIT_Planet_Fill` did not get that exception on the first pass. It is an area light, energy 110, that sat in the forest volume at about (-13.9, -60, -85). It moved with the meshes because it was inside the forest bounds and inside the `02_Forest` collection. That is the mistake this note is for. The light's position is a lighting read. Rule 3 says it stays unless Lead names it.

Lead interview #19 (1A, 2A) named the correction: put `LIT_Planet_Fill` back at (-13.948, -60, -85), and move `LIT_Planet_Sun`, `LIT_LandingDay`, and `LIT_Planet_Fill` out of `02_Forest` into `09_Planet_Day`. Sun and LandingDay transforms stay. That correction is on PR #297, not in this docs change.

## Sources

- [Scene Properties, Blender 5.2 LTS](https://docs.blender.org/manual/en/5.2/scene_layout/scene/properties.html) (retrieved 2026-10-07)
- [Apply, Blender 5.2 LTS](https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/apply.html) (retrieved 2026-10-07)
- [Object Origin, Blender 5.2 LTS](https://docs.blender.org/manual/en/5.2/scene_layout/object/origin.html) (retrieved 2026-10-07)
- [Tool Settings, Blender 5.2 LTS](https://docs.blender.org/manual/en/5.2/scene_layout/object/tools/tool_settings.html) (retrieved 2026-10-07)
- [FBX, Blender 5.1](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_fbx.html) (retrieved 2026-10-07)
- [bpy.ops.export_scene](https://docs.blender.org/api/current/bpy.ops.export_scene.html) (retrieved 2026-10-07)
- [FBX Static Mesh Pipeline, Unreal Engine 5.8](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine) (retrieved 2026-10-07)
- [FbxStaticMeshImportData, UE 5.8 Python API](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FbxStaticMeshImportData) (retrieved 2026-10-07)
- [StaticMeshTools, UE 5.8](https://tc-imba.github.io/ue-official-mcp/references/toolsets/editor_toolset.toolsets.static_mesh.StaticMeshTools/) (retrieved 2026-10-07)
- [Modular Kit Workflow in UE5, StraySpark](https://www.strayspark.studio/blog/modular-kit-workflow-greybox-to-final-ue5) (retrieved 2026-10-07)
- [Build Modular Levels That Actually Snap Together, StraySpark](https://www.strayspark.studio/learn/tutorials/build-modular-levels-that-snap-together) (retrieved 2026-10-07)
- [Modular Prop Kits for Games](https://nastyrodent.com/modular-prop-kits-for-games/) (retrieved 2026-10-07)
- [Configure Blender for Unreal Engine 5](https://propgon.com/en/configure-blender-unreal-engine-5-workflow/) (retrieved 2026-10-07)
- [Blender-to-Game-Engine Pipeline, 2026, StraySpark](https://www.strayspark.studio/blog/blender-to-game-engine-pipeline-2026) (retrieved 2026-10-07)
- [About Git Large File Storage, GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) (retrieved 2026-10-07)
- [Moving a file to Git LFS, GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/moving-a-file-in-your-repository-to-git-large-file-storage) (retrieved 2026-10-07)
- [Git LFS, GitLab](https://docs.gitlab.com/17.5/topics/git/lfs/) (retrieved 2026-10-07)
- [Benchmarking Version Control, Blender Studio](https://studio.blender.org/blog/benchmarking-version-control-git-lfs-svn-mercurial/) (retrieved 2026-10-07)
- [git-lfs-track](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-track.adoc) (retrieved 2026-10-07)
- [File Locking, git-lfs wiki](https://github-wiki-see.page/m/git-lfs/git-lfs/wiki/File-Locking) (retrieved 2026-10-07)
- [Git LFS locking API](https://github.com/git-lfs/git-lfs/blob/main/docs/api/locking.md) (retrieved 2026-10-07)
- [git-lfs issue 4168](https://github.com/git-lfs/git-lfs/issues/4168) (retrieved 2026-10-07)
- [MCP Server — Blender](https://www.blender.org/lab/mcp-server/) (retrieved 2026-10-07)
- [Blender MCP security notes](https://devtalk.blender.org/t/blender-mcp-server-after-claude-mcp-security-for-blender-scripting-3d-agent-notes/45131) (retrieved 2026-10-07)
- [How MCP for Blender Works](https://www.mcp-for-blender.com/docs/concepts/how-it-works) (retrieved 2026-10-07)
- [MCP for Blender configuration](https://www.mcp-for-blender.com/docs/reference/configuration) (retrieved 2026-10-07)
- [Geometry Nodes Performance](https://docs.blender.org/manual/en/dev/modeling/geometry_nodes/performance.html) (retrieved 2026-10-07)
- [Export geometry nodes instances, Blender Artists](https://blenderartists.org/t/how-to-export-geometry-nodes-instances-in-a-game/1419992) (retrieved 2026-10-07)
- [Geometry Nodes to Unreal Engine, 2026, StraySpark](https://www.strayspark.studio/blog/geometry-nodes-to-unreal-engine-2026-pipeline) (retrieved 2026-10-07)
- [Clean up an AI model, Triverse](https://triverse.ai/blog/clean-up-ai-model-in-blender-tutorial) (retrieved 2026-10-07)
- [Clean up AI-generated models, Tripo](https://www.tripo3d.ai/blog/how-to-clean-up-ai-generated-3d-models-in-blender) (retrieved 2026-10-07)
- [AI retopology, Meshy](https://www.meshy.ai/tutorials/ai-retopology-guide) (retrieved 2026-10-07)
- [Meshy to Blender cleanup](https://help.meshy.ai/en/articles/16100257-meshy-to-blender-cleanup-workflow) (retrieved 2026-10-07)

Project docs used as local fact, not as web sources: `docs/04_EXPORT_TABLE.md`, `Docs/02_MATERIAL_SHEET.md`, `docs/KNOWN_ERRORS.md`, `.gitattributes`.
