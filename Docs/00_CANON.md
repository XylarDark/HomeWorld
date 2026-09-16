# Docs/00_CANON.md

## 1. Status: LOCKED (P0)

## 2. Map topology

```
MOON / SKY
    huge warm-yellow moon, stars, peach clouds, distant snow peak
HERO ISLAND (hub)
    cabin, garden, path, pines, lookout, shrine, glider perch
TRANSIT
    Body/day: lookout → air current / islets / glider → landing circle
    Spirit/night: homestead shrine ↔ planet shrine
PLANET SLICE (must be visible from lookout)
    forest path 2–4 min walk, gather nodes, 1 beast pad,
    1 spirit-wound site, landing circle, return shrine,
    2–3 hamlet roof silhouettes
```

Lookout test: player can point at landing, portal exit, first harvest, and way home.

## 3. Eight MVP verbs only

1. Walk homestead
2. Glide/fly island → planet (or scripted stand-in)
3. Gather 6 resources
4. Encounter / tame 1 beast
5. Portal night island ↔ planet
6. Heal 3 spirits
7. Nurture 2 homestead targets
8. Return / dawn cycle

## 4. Six resources

| ID | Resource | World | Stored |
|---|---|---|---|
| RES_WOOD | Wood | branch / choppable pine | firewood / planks |
| RES_FIBER | Fiber | fern / vine / flax | cord |
| RES_STONE | Stone | loose rock | path stone / tool head |
| RES_BERRY | Forage fruit | berry bush | bowl / rack |
| RES_HERB | Herb | herb cluster | poultice |
| RES_SEED | Spirit seed | faint day plant | nurtured night crop |

## 5. Scale and naming

- Meters. Adult 1.8 m. Cabin 5–6 m. Island 18–24 m. Pines 6–12 m.
- Prefixes: M_ SM_ SK_ FX_ PCG_ BP_ CAM_ LIT_
- Suffixes: _Day _Night _Spirit _Nurtured _World _Stored
- Origins at ground contact. Apply scale.

## 6. Ten master materials only

1. M_StylizedGrass
2. M_CliffRock
3. M_WoodCabin
4. M_WoodWild
5. M_FoliageCard
6. M_PathStone
7. M_GatherHerb
8. M_BeastStylized
9. M_SpiritUnlit
10. M_Nurtured

Each exposes: BaseColor, Roughness, Variation, NightMix 0–1, optional Emissive. Night is a parameter + overlay, not a second map.

## 7. Hard rejects

- photoreal scans
- grimdark
- sci-fi kits
- pancake/cylinder islands
- tiny white moons
- dark cabin windows
- extra biomes
- extra beasts
- combat
- free-flight sim
- crafting trees
- multiplayer netcode
- worker self-approving a phase
- two agents writing the same file

## 8. Flight fallback note

Scripted glide down + portal both ways (Conductor may arm without meeting).

## 9. Tone

Warm, readable, handmade, hopeful. Not cutesy-infantile. Not grim. Not photoreal. Not sci-fi.

## 10. Engine path

Blender first; Unreal Engine 5 after P2 masters and P3 cabin kit.
