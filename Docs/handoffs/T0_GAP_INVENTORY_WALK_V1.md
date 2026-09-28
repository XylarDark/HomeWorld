# T0_GAP_INVENTORY_WALK_V1 — Gap inventory + walk-script

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Implement SCOUT (gap inventory only; no feature Act) |
| **Bite** | `T0_GAP_INVENTORY_WALK_V1` |
| **Map** | `Maps/VS_MVP` → `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| **CAP** | **PARKED** (stills confirm-only; bright/day; no night PASS) |
| **DET** | pin HOLD `0a27306` |
| **APPROVED list** | `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` · Lead **`APPROVE-PROTOTYPE-LIST`** stamped **2026-09-27** |
| **Cite** | `PROTOTYPE_FEATURE_LIST_V1` · `PROP_INVENTORY_V1` · `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` · `GAME_FEEL_CANON_V1` · `EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1` |
| **Scout host** | OpenCode ≡ Cursor on **DESKTOP-21CT3H0** (`C:\dev\HomeWorld`) — files/dir/umap-string SCOUT only · **no** unrealMCP · **no** Editor/PIE · **no** `.uasset` Act |
| **HOLD** | All other T0 mechanic implementation **DEFER** until this bite’s DONE-WHEN |

---

## Scout method (DESKTOP)

| Source | Used |
|--------|------|
| Map binary (names only) | `Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap` — ASCII string scrape for `GP_*` / `CRUMB_*` / `ANCHOR_*` / `DRESS_*` / `VS_MARKER_*` / class refs (no asset edit) |
| Map folders | `VS_MVP/Markers`, `Cameras`, `Transit` — **empty of loose files**; actors live inside the umap |
| External actors | `Content/__ExternalActors__/HomeWorld/Maps/` has DemoMap · Homestead · MainMenu — **no VS_MVP** external-actor tree |
| Assets on disk | `BP_Bed.uasset`, `SM_Glider_Perch`, `SM_Planter_*`, shrine/herb gather meshes — **no** `Content/Props/Greybox` · **no** `SM_Proxy*` |
| Python | `place_vs_mvp_*.py`, `place_fallback_glide_markers.py`, `place_bed.py` (script labels; KEEP-LOCAL may differ from umap) |
| Source | `HomeWorldFallbackGlideComponent`, `HomeWorldCharacter` (glide + form gates), `GoToBedTrigger`, `Inventory*`, `Nurture*`, `ShrinePortal*`, `TimeOfDay*`, `SpiritStealth*` |
| Design SoT | origin/main: `PROTOTYPE_FEATURE_LIST_V1` · `PROP_INVENTORY_V1` (PROXY freeze) · feel/movement canons |

### PROXY vs OBSERVED (normative)

`PROP_INVENTORY_V1` T0 MUST-ENV-GREYBOX rows use mesh paths `/Game/Props/Greybox/SM_Proxy*` — **Design PROXY freeze only**. Those meshes are **absent** on DESKTOP disk. PROXY rows are **not** observed VS_MVP world actors. Score:

| Present? | Meaning |
|----------|---------|
| **Y** | Documented/implemented interact or actor on VS_MVP with concrete path/name in Source/Config/Docs **and** DESKTOP umap/disk prove history |
| **Partial** | PROXY inventory row/envelope only **or** partial system (code/script without matching VS_MVP beat actor / missing gate wire) |
| **N** | No evidence for the beat verb |

**PROP_INVENTORY JSON gap:** feature-list freeze includes `NODE_PORTAL_HOME`, `NODE_PORTAL_CAMP`, `NODE_GUARD`, `NODE_SLEEPER`, but those labels are **not** in the T0 MUST-ENV-GREYBOX `props[]` JSON — gap them honestly.

**Anti:** no CAP reopen · no `.uasset` / `.umap` commits · no invent WP APIs · no feature Act in this bite.

---

## Gap table (every MUST row)

| # | Beat | Present? | Actor/path | Gap note | Suggested prove label |
|---|------|----------|------------|----------|------------------------|
| 1 | Wake / start day (homestead) | **Partial** | umap: `GP_PlayerStart`, `PlayerStart_VS_MVP` · script `place_vs_mvp_gp.py` · TOD Day via `UHomeWorldTimeOfDaySubsystem` · PROXY `NODE_WAKE` → `SM_ProxyWakeMarker` (**not on disk**) | Homestead spawn present on VS_MVP. No frozen `NODE_WAKE` actor label; wake-from-bed is Dawn advance, not a dedicated start-day beat log. | `NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE` |
| 2 | Kettle + herbs → tea → sprint (~half day) | **Partial** | PROXY only: `NODE_KETTLE` / `SM_ProxyKettle` in `PROP_INVENTORY_V1` · **0** kettle/tea path on DESKTOP umap/Source/Python · sprint = ungated MV (`HomeWorldTraversalComponent` / day-verb gate) · meal BPs ≠ tea | PROXY envelope only (CAP PARKED). No kettle interact, no herb→tea craft, no tea-gated sprint duration. | `NODE_KETTLE` · `TOD_DAY` · `FORM_BODY` |
| 3 | Plant given herb nearby outside | **Partial** | Disk/meshes: `SM_Planter_A/B/C` · umap nurture: `GP_N1_Crop` (`HomeWorldNurtureTarget`) · PROXY `NODE_PLANT_SLOT` | Planters + N1 nurture slot exist; **no** day “plant given herb” interact marking T0 `NODE_PLANT_SLOT` for later spirit nurture. N1 ≠ plant-given-herb beat. | `NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY` |
| 4 | Equip backpack → inventory | **Partial** | `UHomeWorldInventorySubsystem` (6-slot RES_*) · PROXY `NODE_BACKPACK` / `SM_ProxyBackpack` (**not on disk**) · **0** backpack equip path | Inventory-lite present; not gated by equip-backpack actor. | `NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY` |
| 5 | Glider interact → glide to open field | **Y** | umap: `GP_GlideStart`, `CRUMB_Depart_Lookout`…`CRUMB_Landing`, `ANCHOR_SM_Glider_Perch`, `DRESS_SM_Glider_Perch`, `SM_Glider_Perch`, `VS_MARKER_LeaveIsland_FALLBACK` · Source: `UHomeWorldFallbackGlideComponent`, `TryStartFallbackGlide` · `UHomeWorldInteractAbility` (glide first) · scripts `place_fallback_glide_markers.py` | FALLBACK scripted glide armed on VS_MVP; interact near glide start; lands field/landing. No free-flight. | `NODE_GLIDER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_GLIDE` |
| 6 | Collect herb seeds in field | **Partial** | umap: `DRESS_SM_Gather_FirstHarvest_Bush_*`, `GP_Store_HERB`/`SEED`, `RES_HERB`/`RES_SEED` · meshes `SM_RES_HERB_World_Mesh`, `SM_RES_SEED_World_Mesh` · gather scripts · PROXY `NODE_FIELD_GATHER` | Field gather dress + RES systems exist; no frozen `NODE_FIELD_GATHER` field node near landing as T0 beat label. | `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD` |
| 7 | Rune unlock before bed→spirit | **Partial** | Source API: `SetRuneGateUnlocked` / `bRuneGateUnlocked` (default locked) · PROXY `NODE_RUNE` / `SM_ProxyRune` (**not on disk**) · **0** rune actor in umap | Gate hook present for T0_M9 form law; **no** world unlock interact / `NODE_RUNE` on VS_MVP. | `NODE_RUNE` · `TOD_DAY` · `FORM_BODY` |
| 8 | Day camp: cartoon eject (launch→glider→home) | **N** | Scripts only: `GP_RS_HumanoidCamp` / `_Collect` / `_Dream` in `place_vs_mvp_rs_humanoid_camp.py` — **not** in DESKTOP umap scrape · PROXY `NODE_DAY_CAMP` · **0** eject/`EJECT_HOME` impl | Camp landmark not in current KEEP-LOCAL umap; no cartoon eject path. Convert stub ≠ eject-to-home. | `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY` |
| 9 | Homeworld night w/o bed: no spirit; day abilities off | **Y** | Source `#230` / `ApplyFormForPhase`: Night/Dusk → spirit **only** if `CanEnterSpiritForm()` (`bSpiritSleepGateGranted && bRuneGateUnlocked`) · `AreDayBodyAbilitiesAllowed` rejects sprint/mantle · logs `FORM: day verb rejected … (TOD_NIGHT_HOME …)` · prove packet `T0_M9_NIGHT_HOME_GATE_PROVE.md` · `t0_m9_desktop_prove.py` | T0 night-home law implemented in character/TOD; DESKTOP Source present. Negative prove = no bed. (Bed path still incomplete — see #11.) | `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` *(negative)* |
| 10 | Planetside night w/o bed: glider boot home | **N** | — · FALLBACK glide is island→planet **down** only · soft-kidnap ≠ eject · **0** `EJECT_HOME` | No planetside night boot-home / reverse glider eject. | `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER` |
| 11 | Bed → spirit (after rune) | **Partial** | Disk: `Content/HomeWorld/Building/BP_Bed.uasset` · `UHomeWorldGoToBedTriggerComponent` / bed tag interact → `SetPhase(Night)` only · `GrantSpiritSleepGate` API exists but **not** called from GoToBed/Interact · **no** `BP_Bed` instance string in VS_MVP umap scrape · needs `#7` rune | Phase advance works; sleep-gate + rune not wired for T0 bed→spirit. Bed may be DemoMap-oriented / not placed on VS_MVP KEEP-LOCAL. | `NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE` |
| 12 | Nurture planted herb (spirit) | **Partial** | umap: `GP_N1_Crop`, `GP_N2_Stored` · classes `HomeWorldNurtureTarget` / `HomeWorldNurtureComponent` · Interact `TryNurtureInFront` · same-slot identity should be `NODE_PLANT_SLOT` | Spirit nurture on N1 **present**. Link to day plant-given-herb (#3) still open. | `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| 13 | Home portal → camp portal (spirit) | **Partial** | umap: `GP_PortalA`↔`GP_PortalB`, `VS_MARKER_PortalHome`/`PortalPlanet`, shrine dress, `HomeWorldShrinePortal*` · **no** camp portal · `NODE_PORTAL_HOME`/`NODE_PORTAL_CAMP` **∉** PROP_INVENTORY JSON props | Home↔planet return shrine pair present. Home→**camp** pair missing. Feature-list portal labels not in MUST-ENV-GREYBOX JSON. | `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| 14 | Camp night: avoid 1 guard; soothe 2 sleepers | **N** | Scripts: `GP_SS_Lit_*` (`place_vs_mvp_ss_stealth.py`) + `UHomeWorldSpiritStealthComponent` — **not** in DESKTOP umap scrape · **0** soothe/guard/sleeper · `NODE_GUARD`/`NODE_SLEEPER` **∉** PROP_INVENTORY JSON | No guard/sleeper actors; no soothe verb; stealth volumes not in current umap. Convert ≠ soothe. | `NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT` |

### DEFER (not MUST)

| Beat | Status | Note |
|------|--------|------|
| Other plants nurture → daytime seed collect | **DEFER** | Scope table DEFER — do not Act in this bite |

### CUT (do not reopen)

Player death · Quarantined Homestead/DemoMap as primary · CAP/EA reopen

---

## Summary counts

| Present? | Count | Beats |
|----------|------:|-------|
| **Y** | **2** | #5 Glider→field · #9 TOD_NIGHT_HOME law |
| **Partial** | **9** | #1 Wake · #2 Kettle (PROXY only) · #3 Plant · #4 Backpack · #6 Field gather · #7 Rune (API+PROXY) · #11 Bed→spirit · #12 Nurture · #13 Portals |
| **N** | **3** | #8 Day camp eject · #10 Planetside boot home · #14 Guard + soothe |
| **Total MUST** | **14** | — |

---

## DESKTOP umap actor inventory (observed names)

From ASCII scrape of `L_VS_MVP_Markers.umap` on DESKTOP-21CT3H0 (not PROXY):

**GP_:** `GP_PlayerStart` · `GP_GlideStart` · `GP_PortalA` · `GP_PortalB` · `GP_N1_Crop` · `GP_N2_Stored` · `GP_BeastPad` · `GP_SpiritWisp_A/B/C` · `GP_Store_{BERRY,FIBER,HERB,SEED,STONE,WOOD}`

**Transit:** `CRUMB_Depart_Lookout` · `CRUMB_Air_01..03` · `CRUMB_Islet_01..03` · `CRUMB_Approach` · `CRUMB_Landing` · `CRUMB_GlideSpline` · `ANCHOR_SM_Glider_Perch` · `ANCHOR_SM_Lookout_Pad` · `ANCHOR_SM_LandingCircle` · `ANCHOR_SM_Shrine_Homestead` · `ANCHOR_SM_Shrine_Return`

**Markers:** `PlayerStart_VS_MVP` · `VS_MARKER_PortalHome` · `VS_MARKER_PortalPlanet` · `VS_MARKER_LeaveIsland_FALLBACK` · `VS_MARKER_LandPlanet` · `CAM_GlideDepart` · `CAM_PortalNight` · cabin/landing cams

**Absent from umap (scripts may place KEEP-LOCAL later):** `GP_RS_HumanoidCamp*` · `GP_SS_Lit_*` · `NODE_*` · kettle/backpack/rune/guard/sleeper/eject · `BP_Bed` instance

**Maps paths (repo):** `Content/HomeWorld/Maps/VS_MVP/` · `Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap` · (also MainMenu* under Maps/)

---

## Walk-script checklist (ordered · day→night · ≤15 min)

Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` · Prefer existing cheats only · CAP PARKED (no night mood PASS).

1. **Day / body** — PIE spawn `GP_PlayerStart` / `PlayerStart_VS_MVP` → readable homestead cabin/garden (`NODE_WAKE` / `CAM_T0_WAKE`).
2. **Kettle** — seek kettle/herbs→tea→sprint buff — **expect gap** (`NODE_KETTLE`).
3. **Plant** — plant given herb outside near planters — **expect gap** vs `GP_N1_Crop` nurture-only (`NODE_PLANT_SLOT`).
4. **Backpack** — equip backpack → inventory UI — inventory may exist ungated; **equip gap** (`NODE_BACKPACK`).
5. **Glider** — Interact near `GP_GlideStart` / perch → FALLBACK crumbs → `CRUMB_Landing` / landing circle (`NODE_GLIDER` / `CAM_T0_GLIDE`).
6. **Field gather** — collect herb/seed near field dress/stores (`NODE_FIELD_GATHER` / `CAM_T0_FIELD`).
7. **Rune** — unlock rune before bed — **expect gap** (`NODE_RUNE`).
8. **Day camp eject** — approach day camp → cartoon eject home — **expect gap** (`NODE_DAY_CAMP` / `EJECT_HOME`).
9. **Night home w/o bed** — force Night **without** bed → stay `FORM_BODY`; day verbs rejected (`TOD_NIGHT_HOME`).
10. **Planetside night boot** — night on planet w/o bed → glider boot home — **expect gap** (`EJECT_HOME`).
11. **Bed → spirit** — after rune, bed grants spirit — sleep-gate wire + rune + VS_MVP bed instance **gaps** (`NODE_BED`).
12. **Nurture** — spirit nurture `GP_N1_Crop` (same slot identity as plant) (`NODE_PLANT_SLOT`).
13. **Portals** — spirit `GP_PortalA`↔`B` (home↔return); camp portal **missing** (`NODE_PORTAL_HOME` / `NODE_PORTAL_CAMP`).
14. **Camp night** — avoid 1 guard; soothe 2 sleepers — **expect gap** (`NODE_GUARD` / `NODE_SLEEPER` / `CAM_T0_CAMP_NIGHT`).

---

## DONE-WHEN self-check

- [x] Gap table covers all **14** MUST Scope rows
- [x] Present? scored Y / Partial / N with DESKTOP umap + Source + PROXY honesty
- [x] Suggested prove labels ⊆ feature-list inventory freeze
- [x] Walk-script ordered day→night
- [x] PROP_INVENTORY PROXY ≠ observed called out; portal/guard/sleeper JSON gap noted
- [x] CAP **PARKED** · DET `0a27306` · no `.uasset` Act
- [x] HOLD: all other T0 mechanic **DEFER**
- [ ] Lead/Conductor accept → unlock Design mechanic inventories / Test files-only follow-ons

---

## HOLD — mechanic DEFER

Until DONE-WHEN accepted:

- No kettle/tea/backpack/rune/eject/soothe/camp-portal feature PRs from this bite
- No `.uasset` / `.umap` commits
- No CAP/EA reopen (CAP stays **PARKED**)
- No invent World Partition / streaming APIs (A–E cite only)
- CUT rows stay CUT

---

*Repo path: `Docs/handoffs/T0_GAP_INVENTORY_WALK_V1.md` · Scout: DESKTOP-21CT3H0 OpenCode≡Cursor files-only · Bite: T0_GAP_INVENTORY_WALK_V1 only.*
