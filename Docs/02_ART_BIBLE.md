# Docs/02_ART_BIBLE.md

## Status: LOCKED — supersedes P2_AD_bible (2026-09-16) — updated 2026-09-30

**Owner:** AD (art half of Track C).  
**Single source of truth:** this file. `AssetCreation/STYLE_GUIDE.md` keeps the Blender export preset only and must not restate look law. `VisionBoard/` holds prompts and encoded key art; it does not override this bible.

**North stars (2026-09-30):**

- `VisionBoard/KeyArt/homestead_dusk_baseline.jpg.b64` — dusk homestead contract. Expressive player looking back, warm cabin, lupine bee, crystal moth, cropped moss-bear with readable eyes.
- `VisionBoard/KeyArt/player_expression_sheet.jpg.b64` — face lock (calm, smile, worry, awe, determination, startle).
- `VisionBoard/KeyArt/homestead_dusk_face_pass.jpg.b64` — earlier face-pass of the same homestead, before living micro-details.
- Planetside camp is a locked location *test* (player approaching three larger armed enemies at a fire, starry pine-mountain backdrop). Encode when the still is exported; do not treat the 2026-09-16 split greybox as the current planetside contract.

Older refs `refs/keyart_homestead_night.jpg` and `refs/keyart_homestead_planetside_split.jpg` remain historical. They are not the current contract.

**Canon inputs:** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`  
**Out of scope for this file:** material parameter sheets (TA → `Docs/02_MATERIAL_SHEET.md`).

Tone lock: warm, readable, handmade, hopeful. Fantasy, not high fantasy. Cartoon, not Disney. Closest cousins: Breath of the Wild + Pixar sincerity. Not cutesy-infantile. Not grim. Not photoreal. Not sci-fi.

---

## 1. What the game looks like

HomeWorld is **semi-polygon with detail on top**.

- Big forms are faceted low-poly masses. Not flat untextured low poly. Not photoreal. Not Mario-Galaxy soft clay.
- Surface life sits on those facets: wood grain, moss clumps, flower clusters, crystal faces, leather straps.
- Most of the frame is scenery ahead of the player.
- The world is large. The player is small. Enemies and beasts are huge and often cropped.
- Planetoid read: close horizon, ground can feel like it bends away, thin air, deep zenith, readable constellations at night.

If a change makes the facets disappear, it is the wrong kind of beauty.

Rejected: flat shade, posterized color bands, chunky-toy restyle, photoreal scans, featureless hooded player.

---

## 2. Locked key art

### Homestead (primary contract)

Dusk on the floating-island hub.

- Faceted Zelda/Pixar adventurer looking back, readable face.
- Log cabin with warm uneven windows, porch lamp, hanging herbs.
- Lupine beds with one living visitor (bee).
- Shrine crystal with a moth.
- Giant cropped moss-bear with brow shelves and eyes that look.
- Warm sun left, cool forest right, thin air, planetoid moon.

### Planetside (second location test)

Night camp on the planet below.

- Same player approaching a campfire.
- Three dangerous enemies, all much larger than the player, varying height among themselves.
- Club, sword, bow and arrows. Faceted stone-and-leather brutes, readable faces.
- Starry sky with readable constellations, mountain ridge, pine forest.
- Fire is the homestead-window trick: the only warm light.

If a new biome cannot produce a shot this clear, the biome is not ready.

---

## 3. Player

Unique but non-descript. A person, not a logo.

- Young-adult adventurer, slightly androgynous.
- Short geometric hair in a few faceted clumps.
- Muted charcoal-brown coat. One warm scarf accent. No ornate armor.
- Head slightly large. Eyes graphic and clear.
- Face built from planes that act: brows, eyelids, mouth corners.
- Not a featureless hood. Not a realistic hoodie. Not a Disney princess. Not a high-fantasy chosen one.

Spend triangles on the face. The coat stays cheap.

Emotion kit to author: calm, smile, worry, awe, determination, startle.

The player is a scale ruler and an actor in close shots. The world still carries the wide frame. Family silhouettes from Shot 1 may share this face kit later (different hair and accent). That is open, not locked.

---

## 4. Creatures and enemies

Same face law as the player.

- Eyes, brow shelves, lids, a muzzle or mouth that can change.
- A snarl and a soft look are two poses of one face, not two models.
- Beasts and humanoid brutes stay faceted stone / moss / leather.
- Scale: much larger than the player. Tallest members may crop the frame.
- A group must vary in height.

Homestead guardian: giant moss-bear, often cropped, threat or quiet watcher depending on pose and light.

Planetside camp: three armed brutes around a fire. Dangerous, readable, not gore, not cute Disney animals.

The 2026-09-16 “no extra beasts / no combat staging” reject is superseded for the homestead bear and the planetside camp only. Do not add a fourth enemy species or a new combat arena until those two reads are built.

---

## 5. Two-layer build method

### Layer A — Structure

Cheap mass that holds silhouette, collision, and facet lighting. Cut facets on purpose. Shade by face. Hard edges. Do not smooth into subdivision clay. Collision uses the structure, never the flowers.

### Layer B — Detail kit

Reusable pieces snapped onto the mass. Starter kit: moss clump, lupine sprig, fence module, path stone, wood trim strip, window pane, extra crystal shard.

If a piece cannot be reused on three props, it is too unique. Hero exceptions: crystal, beast/enemy heads, cabin door, player face.

### Layer C — One living eye per important object

| Object | Cheap mass | The eye (pay here) | Cull far away |
|---|---|---|---|
| Player | Simple coat | Face | Never in intimate cam |
| Beast / enemy | Faceted body | Eyes + brows | Eyes stay |
| Cabin | Faceted logs | Brightest window + door leak + smoke + one porch item | Smoke and porch item |
| Flower bed | Instanced sprigs | One leaning hero stalk + one bug + two dew drops | Bug and dew |
| Crystal | Outer gem | Inner shard + pulse + moth | Moth |
| Campfire | Log pile | Flame + one pot or rack | Spark detail |

A second eye on the same object usually adds noise, not life.

---

## 6. Camera

Two distances. Same assets. Never rescale to cheat a lens.

| Mode | Distance | What must read | What may simplify |
|---|---|---|---|
| Intimate | Low, over-shoulder or first-person among beds / fire | Faces, grain, moss, petals, dew, moth, window leak | Far forest already impostors |
| Default / vista | About 20 ft+, orbit allowed | Silhouettes: cabin, arch, beast crop, horizon, enemy group | Sprig LOD2, no interior |

Default travel camera stays far so the world stays large.

---

## 7. Palette and lighting

Primary contrast is **warm amber vs cool night / forest**. Keep both readable. Never collapse into muddy mid-gray or pitch black.

| Chip | Role | Notes |
|---|---|---|
| Cabin amber | Window / porch / door leak | Warm golden; one window brighter than the others |
| Fire amber | Planetside key | Same job as the window |
| Crystal cyan | Shrine jewel | Tight bloom, inner shard, no lawn-wide neon |
| Navy sky | Night backdrop | Deep zenith, readable constellations |
| Warm horizon | Dusk | Thin air, close planetoid limb |
| Spring grass / lupine | Homestead ground | Quiet ground, loud flowers |
| Warm dark wood | Cabin / planters / rails | Handmade, not scan wood |
| Moss stone | Bear / brutes / shrine | Faceted, moss on upward and shaded faces |

Night is a parameter + overlay, not a second map. `NightMix` 0→1 shifts the ten masters. Do not duplicate meshes to “do night.”

Emotion is climate around the same silhouette: window color, garden health, sky, smoke, beast proximity, fire alive or dead. Do not rebuild the cabin to change mood.

One main key at a time: dusk sun, campfire, or shrine cyan, plus a cooler fill. Emissives are jewels.

---

## 8. Shape language (kept)

| Element | Rule |
|---|---|
| Cliff / island | Layered torn earth. Never a pancake disc or cylinder plug. |
| Pines | Stylized conical pines. No second tree species in MVP. |
| Cabin | Simple rustic log, gabled, stone chimney ok. Cozy, not Victorian, not sci-fi. |
| Shrine / portal | Handmade spirit cue. Not a tech gate or neon ring. |
| Planet below | Pine valley, path, mountain ridge, camp clearing. |

Readable silhouettes beat detail.

### Per-family signature silhouettes (2026-10-01)

A **zone type is a mechanic family**, not a biome. TG-ZONE-FAMILY settled that a section
*is* a family of mechanics and that geography is authored to announce it; TG-ZONE-VOCABULARY
confirmed the family is the art vocabulary and that `EBiomeType` is terrain dressing only.
The consequence is mechanical, not polish:

> A family that cannot be told apart **by shape from 20 m away** has failed its section.
> No HUD may rescue it.

Every family therefore carries one signature silhouette, and no two families may share a
scale band. This table is **locked taste** — see
[handoffs/TASTE_GATE_GRAYBOX_SILHOUETTE.md](handoffs/TASTE_GATE_GRAYBOX_SILHOUETTE.md) and
taste-profile §3. Machine form: `Content/Python/homeworld_graybox_silhouette.py`.

| Family | Signature silhouette at 20 m |
|---|---|
| `gather` | low wide soft mound, reads as a spreading patch |
| `nurture_tame` | broad low pad with a raised rim you can see over |
| `heal` | narrow upright, single soft column |
| `spirit` | tall thin vertical **with a see-through gap** |
| `stealth` | low broken horizontal, never a closed mass |
| `build_place` | flat square plate, deliberately dull |
| `combat` | jagged asymmetric wedge, tallest in frame |

**Traversal is the spine, not a family.** Paths, the lookout pad, the glide perch, islets and
the landing circle carry no silhouette of their own; they inherit the neighbouring family's
material and are excluded from the collision check. Hub volumes (cabin, garden, pines) carry
`build_place` — the cabin is that family's signature landmark.

**Current state:** only `build_place` has authored volumes. `heal`, `stealth` and `combat`
have **no volume anywhere** in the 39-volume layout, so those families are taught nowhere.
`gather`, `nurture_tame` and `spirit` are measured and **non-conforming**: they read flatter
and squarer than their signature. Authoring them is level design — Lead-owned, not invented.

**First prototype: `spirit`** (Lead, 2026-10-01, `TG-ZONE-VOCABULARY` Round 2). It is the
only family both already placed in the world *and* already failing its own signature, so the
before and after are measurable. The **gap is authored in real topology** — four posts and a
lintel — because the spirit signature is the only one whose defining feature is not a
proportion. Correct the existing shrine assemblies in place; do not author rival ones beside
them. Drafts only — nothing promotes to `Content/` without a sidecar and an
`AI_ASSET_LOG` row (Docs/20).

---

## 9. Shots — approval criteria

Approve against `Docs/00_SHOTLIST.md` plus the 2026-09-30 north stars.

| Shot | Pass when | Fail when |
|---|---|---|
| Homestead dusk contract | Expressive player, uneven warm windows, bee, moth, cropped bear eyes, facets intact | Hooded blank, dead windows, smoothed meshes, photoreal |
| Cabin close | One brighter window, door leak, one porch item, facet wood | Clutter kit, dark windows, scan wood |
| Glide | Lookout edge, islets, same pine language, world stays large | Free-flight sim, new biome, rescaled assets |
| Planet camp | Three larger enemies of different heights, fire as the warm eye, stars + mountain + pines | Same-size crowd, gore, Disney animals, grim void |
| Spirit shrine night | Crystal cyan answering cabin gold, same masters | Neon tech portal, rebuilt geometry for night |

**Still rejected:** photoreal scans, grimdark, sci-fi kits, pancake islands, tiny white moon, dead night windows, extra tree species, smoothing facets away, rescaling per camera, legendary outfits.

---

## 10. Naming and masters (unchanged)

Prefixes: `M_` `SM_` `SK_` `FX_` `PCG_` `BP_` `CAM_` `LIT_`  
Suffixes: `_Day` `_Night` `_Spirit` `_Nurtured` `_World` `_Stored`

Ten masters only (instance; do not invent families):

1. `M_StylizedGrass`
2. `M_CliffRock`
3. `M_WoodCabin`
4. `M_WoodWild`
5. `M_FoliageCard`
6. `M_PathStone`
7. `M_GatherHerb`
8. `M_BeastStylized`
9. `M_SpiritUnlit`
10. `M_Nurtured`

Each exposes BaseColor, Roughness, Variation, NightMix 0–1, optional Emissive.  
Scale: meters. Adult about 1.7–1.8 m. Enemies much larger. Origins at ground contact. Apply scale.

AD does not author the material sheet. TA owns parameter ranges.

Nanite is optional on solid static masses. Not on the player, flowers, bugs, or moths. Those use instances and LODs.

---

## 11. Pipeline

Blender library first. Unreal is assembly.

- `HW_Kit_Structure` — cabin, shrine, path, fence, player body, beast/enemy bodies
- `HW_Kit_Detail` — moss, sprigs, chips, trim, panes, shards, bugs, moths
- `HW_Atlas` — shared trim / moss / flower / rock
- `HW_Hero` — crystal, heads, door handle, player face

Profile the expensive view: flower beds, or the campfire looking up at the tallest enemy.

---

## 12. Open, not locked

- Partner / child using the same face kit
- Day-body planetside palette of the camp
- Dawn-after-storm homestead
- Enemy species beyond moss-bear and the three camp brutes

Until those lock, default to the player kit, the three-armed camp, and the moss-bear.

---

## 13. Downstream

| Role | Use this bible for |
|---|---|
| TA | Chips, NightMix, ten masters |
| ENV / PROP | Facets, kit reuse, one living eye |
| LIT | Dusk sun, fire, crystal, moon size |
| QA | Homestead baseline + camp test + shot table |

**Evidence:** 2026-09-16 P2 lock retained where it does not conflict. 2026-09-30 player, living-eye, homestead baseline, and planetside camp supersede the hooded silhouette and the no-beast reject.
