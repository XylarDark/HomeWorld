# Handoff

- **ID:** P5_CHA_life
- **Phase:** P5 / WAVE 4 (Life, verbs, placeholders)
- **Role:** CHA
- **Owner agent:** CHA (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend` (collections `04_Beasts`, `05_Spirits` — homestead/planet preserved)
- `Lib/04_Beasts/KIT_README.md`
- `Lib/05_Spirits/KIT_README.md`
- `Docs/handoffs/P5_CHA_life.md`
- `Maps/Preview_Homestead_Night/shot5_portal_night.png` (optional Shot 5; `CAM_PortalNight`)

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SK_Family_Adult | SK_ blockout | M_WoodCabin | 04_Beasts |
| SK_Family_Child_A | SK_ blockout | M_WoodCabin | 04_Beasts |
| SK_Family_Child_B | SK_ blockout | M_WoodCabin | 04_Beasts |
| SK_Beast_Small (+ _Body, _TameMark) | SK_ | M_BeastStylized | 04_Beasts |
| SOCKET_TameMark / SOCKET_Saddle / SOCKET_GliderAttach / SOCKET_BeastInteract | EMPTY | — | 04_Beasts |
| SOCKET_BeastPerch | EMPTY | — | 04_Beasts (parent: SM_Glider_Perch) |
| SK_Spirit_01/02/03_Hurt | SK_ wisp | M_SpiritUnlit_Hurt (instance of M_SpiritUnlit) | 05_Spirits (+ 07_Night_SpiritLayer) |
| SK_Spirit_01/02/03_Healed | SK_ wisp | M_SpiritUnlit_Healed (instance of M_SpiritUnlit) | 05_Spirits (+ 07_Night_SpiritLayer) |
| SOCKET_Heal_SK_Spirit_* | EMPTY | — | 05_Spirits |

## Phase exit boxes I claim

- [x] Family blockouts (adult + 2 children) at lookout — readable silhouettes
- [x] One small quadruped `SK_Beast_Small` on `SM_BeastPad_01` with tame-mark socket
- [x] Spirit wisps: 3 hurt (wound) + 3 healed (shrine) via M_SpiritUnlit state instances
- [x] Optional glider/saddle socket empties on beast + perch
- [x] No extra fauna, no combat anims
- [x] Did not wipe homestead/planet; did not start WAVE 5; did not edit PHASE_BOARD / GDD / SYS code

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family (hurt/healed = M_SpiritUnlit instances only)
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path (PHASE_BOARD, GDD, gameplay SYS files)

## Inputs I used

- `Docs/00_CANON.md` (§3 verbs, §4 resources)
- `Docs/01_GDD_MVP.md` §§6–7 (beast, spirits)
- `Docs/02_MATERIAL_SHEET.md` §§2.8–2.9
- `Lib/06_Materials_Master/M_BeastStylized.json`, `M_SpiritUnlit.json`
- Existing pads: `SM_BeastPad_01`, `SM_SpiritWound_01`, `SM_Shrine_Homestead`, `SM_Glider_Perch`, `SM_Lookout_Pad`
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- None for CHA placeholders. Runtime SYS may collapse 6 lookdev wisps → 3 meshes with state swap.

## Risks for the next owner

- SYS: wire V4 tame SM on `SOCKET_BeastInteract` / `SOCKET_TameMark`; V6 heal on hurt wisps → swap to healed instance params.
- GP: night layer visibility should include `05_Spirits` / `07_Night_SpiritLayer`.
- PROP: gatherables + nurture glows in sibling handoff `P5_PROP_verbs.md`.
- Do not add a fourth spirit or second beast.

## Evidence

- Repo-relative paths:
  - `blender/floating_island_homestead_LIB.blend`
  - `Lib/04_Beasts/KIT_README.md`
  - `Lib/05_Spirits/KIT_README.md`
  - `Docs/handoffs/P5_CHA_life.md`
  - `Maps/Preview_Homestead_Night/shot5_portal_night.png`
- Object names (verify in Outliner collections `04_Beasts` / `05_Spirits`):
  - Family: `SK_Family_Adult`, `SK_Family_Child_A`, `SK_Family_Child_B`
  - Beast: `SK_Beast_Small` @ beast pad; sockets `SOCKET_TameMark`, `SOCKET_Saddle`, `SOCKET_GliderAttach`
  - Spirits: `SK_Spirit_0{1,2,3}_Hurt` @ wound; `SK_Spirit_0{1,2,3}_Healed` @ homestead shrine
- Test notes: Lab MCP `execute_blender_code` build; blend saved without clearing `01_Homestead` / `02_Forest`.
