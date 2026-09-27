# T0_GAP_INVENTORY_WALK_V1 — Gap inventory + walk-script

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Implement SCOUT (gap inventory only; no feature Act) |
| **APPROVED list** | `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` on **main** @ `9acae3b` (HW #227 MERGED) · Lead **`APPROVE-PROTOTYPE-LIST`** stamped |
| **Map canon** | `Maps/VS_MVP` → `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| **Pins** | CAP/EA **DROPPED** · DET pin HOLD `0a27306` · OpenCode ≡ Cursor (temp) |
| **Scout host** | GitHub MCP / contents API only (no clone · no CloudAgent · no `.uasset` Act) |
| **Cite** | Scope table MUST rows only · Inventory freeze labels · Architecture A–E stream/partition cite (no invented WP API) |
| **HOLD** | All other T0 mechanic implementation **DEFER** until this bite’s DONE-WHEN |

---

## Scout method (honesty)

| Source | Used |
|--------|------|
| SoT | `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` @ `9acae3b` |
| Bibles | `Docs/HOMESTEAD_BIBLE.md`, `Docs/MOVEMENT_BIBLE.md`, `Docs/DAYNIGHT_BIBLE.md`, `Docs/SPIRIT_STEALTH_BIBLE.md`, `Docs/GATHER_CRAFT_BIBLE.md` |
| Numbered | `Docs/09_FALLBACK_GLIDE.md`, `Docs/16_PLAYABLE_LOOP.md`, `Docs/21_REAP_SOW.md`, `Docs/24_MOVEMENT_IMPL.md`, `Docs/27_NIGHT_FEEL_BUILD.md`, `Docs/30_DEMO_SPINE.md`, `Docs/03_GAMEPLAY_MVP.md`, `Docs/03_SYSTEMS_MVP.md`, `Docs/06_VS_MVP_DRESS.md` |
| Transit | `Docs/handoffs/P4_WLD_transit.md`, `Lib/08_Transit/GLIDE_SPLINE.md` |
| Code | `Source/HomeWorld/*` headers + InteractAbility / Character / GoToBed / Inventory / Nurture / Stealth / FallbackGlide / TimeOfDay |
| Python | `place_vs_mvp_*.py`, `place_fallback_glide_markers.py`, `create_bp_bed.py`, `place_vs_mvp_rs_humanoid_camp.py`, `place_vs_mvp_ss_stealth.py`, `place_vs_mvp_nurture.py`, `place_vs_mvp_gp.py` |
| Maps visible | `Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap` (LFS pointer only in git); dress/markers KEEP-LOCAL on DESKTOP |
| Code search MCP | **Empty / incomplete** on both `user-GitHub-xai` and `cursor-github` — presence judged via path listing + file reads |

**Rule:** Prefer **Partial/N** when Docs claim a verb but no actor/path/impl evidence on VS_MVP. Do not invent WP contracts.

---

## Gap table (every MUST row)

| # | Beat | Present? | Actor/path | Gap note | Suggested prove label |
|---|------|----------|------------|----------|------------------------|
| 1 | Wake / start day (homestead) | **Partial** | `GP_PlayerStart` · `Content/Python/place_vs_mvp_gp.py` · `PlayerStart_VS_MVP` · `UHomeWorldTimeOfDaySubsystem` Day · `hw.Wake` / bed overlap → Dawn | Homestead spawn + day phase exist on VS_MVP marker map. No frozen `NODE_WAKE` actor label; wake-from-bed is Dawn advance, not a dedicated “start day” beat log. | `NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE` |
| 2 | Kettle + herbs → tea → sprint (~half day) | **N** | — (no `kettle`/`tea` path in tree) · Sprint is MV-A hold on same CMC (`HomeWorldTraversalComponent` / Shift · `MOVE:` logs) · Meal BPs `create_bp_meal_trigger_*.py` are breakfast/lunch/dinner, **not** kettle tea | No kettle interact, no herb→tea craft, no tea buff duration (~half day). Existing sprint is mild speed bump, not tea-gated. | `NODE_KETTLE` · `TOD_DAY` · `FORM_BODY` |
| 3 | Plant given herb nearby outside | **Partial** | Dress/kit: `SM_Planter_A/B/C` (Exports + Lib homestead) · Night target `GP_N1_Crop` (`place_vs_mvp_nurture.py` · `UHomeWorldNurtureComponent` N1) · `GA_Place` / place ability exist separately | Planters + nurture crop slot exist; **no** day “plant given herb” interact that marks a planted herb for later spirit nurture as T0 NODE_PLANT_SLOT. N1 is seed-nurture, not plant-given-herb beat. | `NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY` |
| 4 | Equip backpack → inventory | **Partial** | `UHomeWorldInventorySubsystem` + `HomeWorldInventoryTypes` (6-slot RES_*) · PL-C store-transfer UX (Docs/16) | Inventory-lite **present**; **no** backpack equip actor/path (`backpack` = 0 tree hits). Inventory not gated by equip backpack. | `NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY` |
| 5 | Glider interact → glide to open field | **Y** | `UHomeWorldFallbackGlideComponent` · `AHomeWorldCharacter::TryStartFallbackGlide` · `UHomeWorldInteractAbility` (glide first) · `GP_GlideStart` + `CRUMB_*` (`place_fallback_glide_markers.py` / `place_vs_mvp_markers.py`) · anchors `SM_Glider_Perch` / `SM_Lookout_Pad` → `CRUMB_Landing` / `SM_LandingCircle` · Docs/09 + P4_WLD_transit | FALLBACK scripted glide armed; interact near glide start; lands field/landing circle. No free-flight. DESKTOP PIE still needed to confirm KEEP-LOCAL markers present. | `NODE_GLIDER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_GLIDE` · `EJECT_HOME` *(transit reuse only — not cartoon eject)* |
| 6 | Collect herb seeds in field | **Partial** | Gather: `TryHarvestInFront` / resource piles · meshes `SM_RES_HERB_World_Mesh`, `SM_RES_SEED_World_Mesh`, `SM_Gather_FirstHarvest_Bush_*` · RS-B material sites scripts · `GATHER:` logs | Field gather **systems** + herb/seed RES exist; no frozen `NODE_FIELD_GATHER` on VS_MVP inventory labels. Open-field seed collect as T0 beat needs explicit field nodes near landing. | `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD` |
| 7 | Rune unlock before bed→spirit | **N** | — (`rune` = 0 tree hits) | No rune actor, unlock flag, or bed→spirit gate. Form currently phase-driven (see #11). | `NODE_RUNE` · `TOD_DAY` · `FORM_BODY` |
| 8 | Day camp: cartoon eject (launch→glider→home) | **N** | Camp markers only: `GP_RS_HumanoidCamp` · `_Collect` · `_Dream` (`place_vs_mvp_rs_humanoid_camp.py` · RS-D) · dream = `hw.Conversion.Test` (night convert stub) | Camp landmark exists; **no** day cartoon eject / launch→glider→home (`eject` = 0 hits). Convert stub ≠ eject-to-home. | `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY` |
| 9 | Homeworld night w/o bed: no spirit; day abilities off | **Partial** | `UHomeWorldTimeOfDaySubsystem` · `ApplyFormForPhase` (`Night` **or** `Dusk` → `bIsSpiritForm`) · `DAYNIGHT_BIBLE` (sleep-gated spirit) · gather day/night gates in SYS | **Machinery present but T0 law not met:** phase Night/Dusk auto-spirit without bed (`hw.TimeOfDay.SetPhase 2`). Bible requires no spirit until sleep. “Day abilities off” at home night w/o bed = not proven as dedicated gate. | `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` *(negative prove)* |
| 10 | Planetside night w/o bed path: glider boot home | **N** | — · Bible soft-kidnap (body no-torch → shrine → home) is **different** path · FALLBACK glide is island→planet down only | No planetside night “boot home” / reverse glider eject. Do not invent as soft-kidnap. | `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER` |
| 11 | Bed → spirit (night planetside gate) | **Partial** | `Content/HomeWorld/Building/BP_Bed.uasset` · `create_bp_bed.py` / `place_bed.py` · `UHomeWorldGoToBedTriggerComponent` (overlap → `SetPhase(Night)`) · `hw.GoToBed` · `FORM:` logs · NF2 soft form feedback | Bed→Night→spirit **works** as phase sync; **not** rune-gated; **also** spirit on Dusk/Night without bed. T0 wants bed (+ rune) as planetside night spirit gate — sleep-gate + rune missing. VS_MVP bed instance KEEP-LOCAL / may be DemoMap-oriented. | `NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE` |
| 12 | Nurture planted herb (spirit) | **Partial** | `UHomeWorldNurtureComponent` · `AHomeWorldNurtureTarget` · `GP_N1_Crop` (RES_SEED) · `GP_N2_Stored` · `NURTURE:` · InteractAbility `TryNurtureInFront` · `M_Nurtured` master | Spirit nurture on homestead N1 **present**. T0 beat wants nurture of **planted given herb** (`NODE_PLANT_SLOT`) — link to #3 plant beat still open. | `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| 13 | Home portal → camp portal (spirit) | **Partial** | `UHomeWorldShrinePortalComponent` / `AHomeWorldShrinePortalTrigger` · `GP_PortalA` ↔ `GP_PortalB` (`SM_Shrine_Homestead` ↔ `SM_Shrine_Return`) · VS_MARKER `PortalHome`/`PortalPlanet` · `bRequireNight` soft · InteractAbility portal path | Spirit/night shrine portals **home ↔ planet return shrine** present. **No** `NODE_PORTAL_CAMP` at humanoid camp; camp is separate RS markers. Home→**camp** portal pair missing. | `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| 14 | Camp night: avoid 1 guard; soothe 2 sleepers | **N** | Stealth only: `GP_SS_Lit_*` (`place_vs_mvp_ss_stealth.py`) · `UHomeWorldSpiritStealthComponent` (`STEALTH:` lit/alert/clear) · Camp dream convert stub | Avoid-light pressure exists near camp path; **no** `NODE_GUARD` / `NODE_SLEEPER`, **no** soothe verb (`soothe`/`sleeper` = 0 hits). Convert ≠ soothe. | `NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT` |

### DEFER (not MUST — listed for freeze only)

| Beat | Status | Note |
|------|--------|------|
| Other plants nurture → daytime seed collect | **DEFER** | Scope table DEFER — do not Act in this bite |

### CUT (do not reopen)

Player death · Quarantined Homestead/DemoMap as primary · CAP/EA reopen

---

## Summary counts

| Present? | Count | Beats |
|----------|------:|-------|
| **Y** | **1** | #5 Glider → field |
| **Partial** | **8** | #1 Wake · #3 Plant · #4 Backpack/inventory · #6 Field gather · #9 Night home law · #11 Bed→spirit · #12 Nurture · #13 Portals |
| **N** | **5** | #2 Kettle/tea · #7 Rune · #8 Day camp eject · #10 Planetside boot home · #14 Guard + soothe sleepers |
| **Total MUST** | **14** | — |

---

## Walk-script checklist (≤15 min · ordered · VS_MVP)

Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` · Pawn: `BP_HomeWorldCharacter` · Prefer existing cheats only (no invent).

| Step | TOD/Form | Action | Expect (readable) | Label |
|------|----------|--------|-------------------|-------|
| 1 | `TOD_DAY` / `FORM_BODY` | PIE spawn at homestead (`GP_PlayerStart`) | Body walk; cabin/garden readable | `NODE_WAKE` · `CAM_T0_WAKE` |
| 2 | Day | Seek kettle / tea / herb craft | **Expect gap** — no kettle | `NODE_KETTLE` |
| 3 | Day | Seek plant-given-herb slot outside cabin | Planters/N1 may be visible; **plant beat likely gap** | `NODE_PLANT_SLOT` |
| 4 | Day | Seek backpack equip → inventory UI | Inventory may already work; **equip gate gap** | `NODE_BACKPACK` |
| 5 | Day | Walk to lookout / `GP_GlideStart` → **E** | `FALLBACK: StartGlide` … land `CRUMB_Landing` | `NODE_GLIDER` · `CAM_T0_GLIDE` |
| 6 | Day | At field / landing — gather herb/seed nodes | `GATHER:` if piles present; else gap | `NODE_FIELD_GATHER` · `CAM_T0_FIELD` |
| 7 | Day | Seek rune unlock | **Expect gap** | `NODE_RUNE` |
| 8 | Day | Approach `GP_RS_HumanoidCamp` | Landmark only; **no cartoon eject** | `NODE_DAY_CAMP` · `CAM_T0_CAMP_DAY` · `EJECT_HOME` |
| 9 | Force `hw.TimeOfDay.SetPhase 2` **without** bed (on homestead) | Observe form | Today: likely `FORM: spirit` — **fails T0 law** `TOD_NIGHT_HOME` | `TOD_NIGHT_HOME` |
| 10 | Planetside + Night w/o bed | Seek glider boot home | **Expect gap** (kidnap≠eject) | `EJECT_HOME` |
| 11 | Day→bed: `BP_Bed` / `hw.GoToBed` | Bed / cheat → Night | `FORM: spirit` · **rune not checked** | `NODE_BED` · `CAM_T0_BED` · `TOD_NIGHT_SPIRIT` |
| 12 | Spirit | Nurture `GP_N1_Crop` | `NURTURE:` if night/spirit + RES_SEED | `NODE_PLANT_SLOT` · `FORM_SPIRIT` |
| 13 | Spirit | `GP_PortalA` ↔ `GP_PortalB` | Portal transit logs; **camp portal missing** | `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` |
| 14 | Spirit @ camp | Avoid guard; soothe 2 sleepers | Lit volumes only (`STEALTH:`); **soothe gap** | `NODE_GUARD` · `NODE_SLEEPER` · `CAM_T0_CAMP_NIGHT` |

Time box: steps 1–8 day (~8–10 min) · 9–14 night (~5 min). Skip taste polish.

---

## HOLD — mechanic DEFER

Until this inventory’s DONE-WHEN is accepted for Design/Implement follow-on packets:

- No kettle/tea/backpack/rune/eject/soothe feature PRs
- No `.uasset` / `.umap` commits
- No CAP/EA reopen
- No invent of World Partition / streaming APIs — if transit/load gaps need stream growth: **boundary unknown — Design later** (cite A–E only)
- CUT rows stay CUT

---

## DESKTOP prove steps (Test · greps only)

Host: DESKTOP-21CT3H0 · OpenCode ≡ Cursor · after KEEP-LOCAL marker scripts if needed.

### Soft_fail vs closed_fail (high-level)

| Class | Meaning | Example |
|-------|---------|---------|
| **soft_fail** | Marker/script missing or KEEP-LOCAL not saved; retry place script / re-open level | `FALLBACK: … no GP_GlideStart` after fresh clone without `place_*` |
| **closed_fail** | Code path exists but T0 law broken, or zero impl for MUST | Night phase → spirit without bed (#9); no kettle path (#2) |

### Grep / cheat menu (existing only — do not invent)

| Area | Grep / cheat | Soft_fail hint | Closed_fail hint |
|------|--------------|----------------|------------------|
| Form / TOD | `FORM:` · `hw.TimeOfDay.SetPhase` · `hw.GoToBed` · `hw.Wake` | Subsystem missing in PIE | Spirit on Night **without** bed when proving `TOD_NIGHT_HOME` |
| Glide | `FALLBACK:` · Interact E near `GP_GlideStart` | Markers not placed | Free-flight / steering (regress) |
| Portal | `FALLBACK: Portal` / shrine transit | `GP_Portal*` missing | Portal works day when T0 wants spirit/moonlight-only (policy) |
| Gather | `GATHER:` | No piles on path | Inventory reject loops |
| Nurture | `NURTURE:` · night + spirit | `GP_N1_Crop` missing | Nurture succeeds in day/body |
| Stealth | `STEALTH:` · `hw.Stealth.Status` | SS volumes missing | Kill-on-detect / crouch |
| Camp convert | `hw.Conversion.Test` | Dream marker missing | Treated as soothe/eject substitute |
| Craft (not tea) | `CRAFT:` · `hw.Craft.*` | Demo spine only | Do **not** count as kettle tea |

Docs/30: walk path preferred over cheats when proving UX; cheats OK for gap confirm.

---

## Stream / partition note (cite only — no API invent)

T0 proves on single `L_VS_MVP_Markers`. Systems owning transit / planetside load must stay **stream / world-partition-ready** for larger planetsides (PROTOTYPE_FEATURE_LIST A–E).  

**Gap if load boundaries unclear:** *boundary unknown — Design later.* Do not invent WP contracts, partition keys, or parallel stream services in this bite.

---

## Confidence notes

| Confidence | Notes |
|------------|-------|
| **High (code hit)** | FALLBACK glide · shrine portals · inventory subsystem · nurture · TimeOfDay/form · GoToBed · spirit stealth volumes · InteractAbility chain · RS humanoid camp markers · MV sprint |
| **Medium (doc + scripts; KEEP-LOCAL actors)** | VS_MVP dress/markers on DESKTOP disk; `L_VS_MVP_Markers.umap` in git is LFS pointer — PIE presence not verified this scout |
| **Doc-only / absent** | Kettle/tea · backpack equip · rune · cartoon eject · planetside boot home · guard/sleeper soothe · sleep-gated spirit law vs phase-auto form |
| **MCP search** | `search_code` returned empty/incomplete — judgments from tree paths + file reads, not search hits |

---

## DONE-WHEN (this bite)

- [x] Gap table covers every **MUST** row (14)
- [x] Suggested prove labels ⊆ Inventory freeze set
- [x] Walk-script ≤15 min ordered
- [x] Summary Y/Partial/N counts
- [x] HOLD mechanic DEFER stated
- [x] DESKTOP prove greps high-level (soft_fail vs closed_fail)
- [x] No invented WP APIs; stream gaps = Design later
- [ ] Lead/Conductor accept → unlock Design mechanic inventories per MUST

---

*Repo path: `Docs/handoffs/T0_GAP_INVENTORY_WALK_V1.md` · Bite: T0_GAP_INVENTORY_WALK_V1 only (no mechanic impl).*
