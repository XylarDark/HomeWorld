# Docs/08d — WAVE D Content Canon (MVP slice vs legacy)

| Field | Value |
|-------|-------|
| **Board status** | WAVE D — CONTENT CANON COMPLETE (awaiting Lead gate) |
| **Date** | 2026-09-17 |
| **Author** | Audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Prior waves** | [08a_INVENTORY.md](08a_INVENTORY.md) · [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) · [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) (PR #13 merged — WAVE C APPROVED) |
| **Contracts** | [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md) · [04_UE_HANDOFF_NOTES.md](04_UE_HANDOFF_NOTES.md) · [05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md) |
| **Hard rules honored** | Docs/07 CLOSED not reopened; FALLBACK FLIGHT armed; **documentation only** — no Content binary deletes, no C++ gameplay rewrite, no new features |

**Gate:** stop for Lead **`APPROVE WAVE D`**

---

## 1. Board status — WAVE D

| Item | Status |
|------|--------|
| **WAVE A** | COMPLETE — [08a_INVENTORY.md](08a_INVENTORY.md) |
| **WAVE B** | COMPLETE — [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) |
| **WAVE C** | COMPLETE — [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) — Lead **APPROVE WAVE C** (PR #13 merged) |
| **WAVE D** | **THIS DELIVERABLE** — MVP slice vs legacy Content canon; no dual canons for transit/look |
| **WAVE E** | NOT STARTED — blocked until Lead `APPROVE WAVE D` |

WAVE D scope: decide what pre-swarm UE **Content** stays for the signed 8-verb vertical slice vs what **yields** to the Docs/04 import path. This document is **decisions only** — no asset deletes, no gameplay rewrites.

---

## 2. Canon rules

### 2.1 Authority stack (look + transit + mesh placement)

| Layer | Wins for | Notes |
|-------|----------|-------|
| **Capital `Docs/`** (00–07 CLOSED, 04–05 contracts) | Product truth for MVP slice | Subordinate trees must not contradict |
| **`AssetCreation/Exports/` MVP FBX** + manifest + crumb JSON | Portable kit source | Staging disk before UE import |
| **Root `Maps/Preview_*` + `Maps/VS_MVP/`** | Look proof + camera reel | Not UE `/Game` maps; evidence for P6/P7 |
| **`Lib/`** (10 masters, kit specs, `GLIDE_SPLINE.md`) | Look + transit geometry spec | Blender-first until UE dress wave |
| **`Content/HomeWorld/Meshes/*`** | UE mesh destination | Per [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md) — **the** import root for kit SM_ |
| **First-pass UE anchors** | Integration stubs on Windows | `L_VS_MVP_Markers` + `MPC_HomeWorld_Time` |

Lowercase **`docs/`** remains UE engineering/session ops — not game look/transit canon.

### 2.2 Content path contract

| Docs/04 category | UE content root |
|------------------|-----------------|
| Homestead kit | `/Game/HomeWorld/Meshes/Homestead/` |
| Forest / planet slice | `/Game/HomeWorld/Meshes/Forest/` |
| Gatherables / shrines / landing | `/Game/HomeWorld/Meshes/Gatherables/` |
| Transit islets | `/Game/HomeWorld/Meshes/Transit/` |
| Beasts / Spirits (pad proxies) | `/Game/HomeWorld/Meshes/Beasts/` · `.../Spirits/` |
| VS markers + crumbs + cameras | `/Game/HomeWorld/Maps/VS_MVP/` (level `L_VS_MVP_Markers`) |
| NightMix driver | `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` |
| Ten masters (later instances) | `/Game/HomeWorld/Materials/Masters/M_*` |

Legacy import folders (`Characters`, `Harvestables`, `Dungeon`, `Biomes` under `/Game/HomeWorld/`) from pre-swarm `batch_import` paths are **not** slice canon — see decision table.

### 2.3 Disposition legend (this WAVE)

| Tag | Meaning |
|-----|---------|
| **KEEP for slice** | Required substrate or first-pass anchor for 8 verbs + FALLBACK transit |
| **YIELD to Docs/04 path** | Legacy content or workflows superseded by MVP FBX import + VS_MVP assembly |
| **QUARANTINE (freeze)** | Do not extend; do not cite as canon; resolve before delete in WAVE F |
| **DEFER WAVE E/F** | Touch only in upgrade pass (E) or archive/delete pass (F) after Lead gates |

---

## 3. Decision table — major Content areas

### 3.1 `Content/HomeWorld/Maps/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`L_VS_MVP_Markers`** (`/Game/HomeWorld/Maps/VS_MVP/`) | **KEEP for slice** | First-pass anchor: 28 actors (CRUMB_*, VS_MARKER_*, ANCHOR_*, CAM_*); idempotent via `place_vs_mvp_markers.py` |
| **`/Game/HomeWorld/Maps/VS_MVP/`** (future dress level) | **YIELD to Docs/04 path** | Target assembly map for kit meshes; replaces DemoMap/Homestead as slice play space |
| **`DemoMap`** + HLOD layers | **QUARANTINE (freeze)** | Pre-swarm PCG-on-landscape demo; fights kit island look + VS_MVP dress |
| **`Homestead`**, **`Homestead_WP`** | **QUARANTINE (freeze)** | Campaign-era open-world homestead; not signed 8-verb graybox |
| **`MainMenu`** | **KEEP for slice** | Boot/menu substrate only; no look canon |
| **`docs/Maps/DEMO_MAP.md`**, **`HOMESTEAD_MAP.md`** | **QUARANTINE (freeze)** | Doc canon yields to `Maps/Preview_*` + Docs/04; banner in WAVE B — do not extend |

### 3.2 `Content/HomeWorld/Meshes/` (post Docs/05 import)

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`Meshes/Homestead/`**, **`Forest/`**, **`Gatherables/`**, **`Transit/`** | **YIELD to Docs/04 path** | Canonical kit destination; names 1:1 with Blender `SM_*` |
| **`SM_Shrine_Homestead`**, **`SM_Shrine_Return`**, **`SM_LandingCircle`** | **YIELD to Docs/04 path** | Portal + land anchors per [04_UE_HANDOFF_NOTES.md](04_UE_HANDOFF_NOTES.md) §4 |
| **`SM_Islet_*`**, transit dress | **YIELD to Docs/04 path** | Glide route visuals along CRUMB_* |
| Legacy `/Game/HomeWorld/{Harvestables,Dungeon,Biomes,Characters}/` meshes | **QUARANTINE (freeze)** | Pre-swarm batch_import side paths; not Lib kit |
| **`Meshes/Beasts/`**, **`Meshes/Spirits/`** | **DEFER WAVE E** | Pad proxies per export table; wire when verb demos need them |

*Note:* First-pass `.uasset` meshes live on Windows only (not committed). Re-run [05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md) on any fresh UE machine.

### 3.3 `Content/HomeWorld/Materials/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`MPC_HomeWorld_Time`** (NightMix stub) | **KEEP for slice** | First-pass anchor; drives ten masters later |
| **`Materials/Masters/M_*`** (ten Lib masters) | **YIELD to Docs/04 path** | Exactly ten masters per [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md) §4 · [Docs/02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) |
| **`MI_*` instances** on kit meshes | **DEFER WAVE E** | Wire NightMix + GameState after master import |
| **`Content/HomeWorld/Milady/Materials/`** | **QUARANTINE (freeze)** | Off-slice NFT/Milady experiment; not swarm kit |

### 3.4 `Content/HomeWorld/Characters/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`BP_HomeWorldCharacter`**, **`ABP_HomeWorldCharacter`** | **KEEP for slice** | Walk/glide/portal substrate (V1–V2, V5, V8) |
| Character **mesh/rig** inside BP | **DEFER WAVE E** | Placeholder until Lib/swarm body aligns; do not block slice on Man pack look |
| **`Content/Man/`** character mesh | **QUARANTINE (freeze)** | Third-party sample pack — reference only, not kit canon |

### 3.5 `Content/HomeWorld/PCG/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`ForestIsland_PCG`** graph | **QUARANTINE (freeze)** | DemoMap landscape forest; kit uses authored pines in `Meshes/Homestead` + `Meshes/Forest` |
| **`Planetoid_POI_PCG`** | **QUARANTINE (freeze)** | Planetoid sprawl beyond signed graybox |
| PCG on **`VS_MVP`** (if any) | **DEFER WAVE E** | Only after manual kit dress; never replace kit pines with procedural third-party trees |
| **`docs/PCG/*`** engineering guides | **KEEP for slice** | UE automation truth — upgrade path refs to Docs/04 where they mention DemoMap as primary |

### 3.6 `Content/HomeWorld/Mass/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`MEC_FamilyGatherer`** + Mass configs | **QUARANTINE (freeze)** | Family agent sim off 8-verb slice (Week 2+ per AGENTS.md) |
| **`place_mass_spawner_demomap.py`** | **QUARANTINE (freeze)** | Targets quarantined DemoMap |
| Mass/StateTree wiring in Source | **DEFER WAVE E** | Off-slice unless Lead reopens scope |

### 3.7 `Content/HomeWorld/Abilities/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`GA_Interact`** | **KEEP for slice** | V3 gather / interact substrate |
| **`GA_Heal`** | **KEEP for slice** | V6 heal verb substrate |
| **`GA_Place`** | **KEEP for slice** | Build-placement hook if demo needs it |
| **`GA_Dodge`**, **`GA_PrimaryAttack`**, **`GA_ProtectorAttack`** | **QUARANTINE (freeze)** | Combat placeholder only until vision pass; not slice verbs |
| **`create_ga_*.py`**, **`setup_gas_abilities.py`** | **DEFER WAVE E** | Align reparent-to-C++ policy when upgrading slice-touching abilities |

### 3.8 `Content/HomeWorld/Building/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`BP_Bed`**, meal/bed triggers (via C++ components) | **KEEP for slice** | V8 return/dawn + rest loop hooks |
| **`BP_BuildOrder_Wall`**, **`SO_WallBuilder`**, **`DA_SO_WallBuilder_Behavior`** | **QUARANTINE (freeze)** | Agentic building off signed slice |
| **`create_so_wall_builder.py`**, **`place_build_order_wall.py`** | **QUARANTINE (freeze)** | DemoMap agentic-building path |

### 3.9 `Content/HomeWorld/UI/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`WBP_MainMenu`** | **KEEP for slice** | Boot flow only |
| Inventory / HUD widgets (if any) | **DEFER WAVE E** | SYS inventory UI beyond slice markers |

### 3.10 `Content/HomeWorld/AI/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`ST_FamilyGatherer`** | **QUARANTINE (freeze)** | Family StateTree off slice |
| **`create_state_tree_family_gatherer.py`**, **`link_state_tree_to_mec.py`** | **QUARANTINE (freeze)** | Mass/family pipeline |

### 3.11 `Content/HomeWorld/Input/` + `GameMode/`

| Asset / path | Disposition | Rationale |
|--------------|-------------|-----------|
| **`IA_*`**, **`IMC_Default`** | **KEEP for slice** | Enhanced Input substrate; `init_unreal.py` applies on Editor load |
| **`BP_GameMode`** | **KEEP for slice** | Default pawn/mode; upgrade in WAVE E for NightMix + transit wiring |

### 3.12 `Content/HomeWorld/Milady/`

| Entire subtree | **QUARANTINE (freeze)** | NFT/Milady import experiment; not MVP swarm kit |

### 3.13 `Content/StylizedProvencal/`

| Entire pack | **QUARANTINE (freeze)** | Third-party stylized environment sample — **not** Lib kit; must not drive look canon |

### 3.14 `Content/Man/`

| Entire pack | **QUARANTINE (freeze)** | Third-party character sample — **not** swarm body; do not use for marketing look |

### 3.15 `Content/Python/` — importers vs map-builders

| Script / group | Disposition | Rationale |
|----------------|-------------|-----------|
| **`batch_import_asset_creation.py`** | **KEEP for slice** | Docs/04-aware FBX importer → `Meshes/*` |
| **`place_vs_mvp_markers.py`** | **KEEP for slice** | Idempotent CRUMB/CAM/VS_MARKER + MPC stub |
| **`init_unreal.py`** | **KEEP for slice** | Enhanced Input on Editor load |
| **`mcp_harness.py`**, **`pie_test_runner.py`**, **`level_loader.py`** | **KEEP for slice** | Test/validation harness |
| **`create_demo_from_scratch.py`**, **`ensure_demo_map.py`** | **QUARANTINE (freeze)** | DemoMap + PCG forest builder — dual map canon |
| **`create_homestead_from_scratch.py`**, **`ensure_homestead_map.py`**, **`place_homestead_*.py`** | **QUARANTINE (freeze)** | Homestead campaign map builder |
| **`setup_planetoid_pcg.py`**, **`assemble_planetoid_from_config.py`** | **QUARANTINE (freeze)** | Planetoid sprawl beyond VS_MVP graybox |
| **`place_mass_spawner_demomap.py`**, **`create_mec_family_gatherer.py`** | **QUARANTINE (freeze)** | Mass/family on DemoMap |
| **`gui_automation/`** (PCG manual steps, homestead UI clickers) | **QUARANTINE (freeze)** | Pre-swarm UI automation; MCP-first policy |
| **`run_automation_cycle.py`**, agent loop callers | **QUARANTINE (freeze)** | Parallel harness vs swarm Conductor (08a/08b) |
| **`bootstrap_project.py`** | **DEFER WAVE E** | Orchestrator — repoint slice tasks to VS_MVP + import path when upgraded |

### 3.16 Summary counts

| Disposition | Count (major areas) |
|-------------|---------------------|
| KEEP for slice | 8 areas (Input, GameMode, core Character BP, core GA_*, MainMenu UI, importers/markers, MPC stub, test harness) |
| YIELD to Docs/04 | 4 areas (Meshes/*, VS_MVP map target, ten masters, shrine/landing/transit SM_) |
| QUARANTINE | 12+ areas (DemoMap, Homestead, PCG forest, Mass, combat GA, building agents, sample packs, legacy map scripts, gui_automation, Milady) |
| DEFER WAVE E/F | Mesh instances, beast/spirit pads, full dress, bootstrap repoint, archive deletes |

---

## 4. Transit canon

**Single transit model — no dual canons.**

| Mechanism | Canon | Disposition of alternatives |
|-----------|-------|----------------------------|
| **Leave island (V2)** | Scripted **FALLBACK** glide along **`CRUMB_*`** in order ([Lib/08_Transit/GLIDE_SPLINE.md](../Lib/08_Transit/GLIDE_SPLINE.md)) | **QUARANTINE** any free-flight, steering sim, or alternate spline docs/code |
| **Land** | Touchdown at **`SM_LandingCircle`** | Legacy DemoMap spawn rings → **QUARANTINE** |
| **Return (V5/V8)** | Portal **both ways**: **`SM_Shrine_Homestead` ↔ `SM_Shrine_Return`** (night/spirit) | One-way portals, planetoid gates, dungeon portals → **QUARANTINE** unless Lead expands scope |
| **Evidence** | `Maps/Preview_Lookout_To_Planet/`, `Maps/VS_MVP/CAMERA_REEL.md`, `L_VS_MVP_Markers` CRUMB actors | |
| **Gameplay doc** | [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) §5–6 · [04_UE_HANDOFF_NOTES.md](04_UE_HANDOFF_NOTES.md) §4 | |
| **Board** | `swarm/PHASE_BOARD.md` — **Flight fallback armed: YES** | |

**Explicit rejects (QUARANTINE, do not reopen without Lead):**

- Free-flight / full 6DOF island transit
- Dual transit docs (e.g. `docs/` planetoid portal guides as slice primary)
- DemoMap / Homestead as glide start/end instead of lookout perch → landing circle
- Reordering `CRUMB_*` without WLD + Docs/04 contract update

---

## 5. Look canon

**Single look model — no dual canons.**

| Layer | Canon | Not canon |
|-------|-------|-----------|
| **Art direction** | [Docs/02_ART_BIBLE.md](02_ART_BIBLE.md) + [Docs/02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) | `AssetCreation/STYLE_GUIDE.md` Mario-Galaxy tone (historical — upgrade pointers only) |
| **Look proof** | `Maps/Preview_Homestead_Night/`, `Maps/Preview_Lookout_To_Planet/`, `Maps/Preview_Portal_Night/`, `refs/keyart_homestead_night.jpg` | UE DemoMap PCG forest screenshot as marketing still |
| **Materials** | Ten **`M_*`** masters in `Lib/06_Materials_Master/`; **NightMix** scalar only | `_Night` texture sets; 11th master; StylizedProvencal/Man materials |
| **Meshes** | Lib kit `SM_*` via Docs/04 paths | Sample pack meshes, Khronos placeholder GLBs, Milady assets |
| **UE dress state** | First-pass import + markers only ([05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md)) | Claiming Lumen/Nanite beauty parity as P6 gate |
| **Pines / environment** | Authored **`SM_Pine_Homestead_*`**, **`SM_Pine_Planet_*`** from kit | PCG `ForestIsland_PCG` random Engine trees on DemoMap landscape |

Sample packs (`StylizedProvencal`, `Man`) remain on disk for engineering experiments but are **frozen** — they must not appear in slice marketing, shot list, or default maps.

---

## 6. "No dual canons" — conflicts resolved

From [08a_INVENTORY.md](08a_INVENTORY.md) § Conflicts — explicit resolutions for WAVE D:

| # | Conflict | Resolution (WAVE D) |
|---|----------|---------------------|
| 1 | Duplicate vertical-slice sign-off (`VisionBoard/MVP/` vs **`Docs/07`**) | **`Docs/07` CLOSED wins** — VisionBoard/MVP remains QUARANTINE |
| 2 | Competing GDD (`VisionBoard/MVP/*`, `docs/MVP/*`, TaskLists vs **`Docs/00`–`03`**) | **`Docs/00`–`03` win** for slice verbs/systems |
| 3 | Two map canons (DemoMap/Homestead docs + Python builders vs **`Maps/Preview_*` / VS_MVP**) | **Preview + VS_MVP + Docs/04 yield** — DemoMap/Homestead maps **QUARANTINE** |
| 4 | Two agent OS (`docs/Automation/AGENT_COMPANY` vs **`swarm/SWARM_OPS`**) | Unchanged from 08b — swarm Conductor for product direction; agent loop **QUARANTINE** |
| 5 | Style drift (`AssetCreation/STYLE_GUIDE` vs **`Docs/02`**) | **`Docs/02` + Lib masters win** — sample packs not kit |
| 6 | Build entry confusion | Unchanged from 08b — **Safe-Build** preferred; both scripts **KEEP** |
| 7 | README/AGENTS gravity | Unchanged from 08b — **START_HERE + Docs/** lead |
| 8 | Obsolete Python (GUI + DemoMap builders vs **`batch_import` + `place_vs_mvp_markers`**) | **Importers + markers win** — map builders **QUARANTINE** |
| 9 | Empty DevEnvTemplate | WAVE B documented init — not WAVE D scope |
| 10 | FALLBACK vs free-flight | **FALLBACK armed wins** — free-flight docs/code **QUARANTINE** |

**New WAVE D resolution — mesh/transit/look triple:**

There is exactly **one** portable kit (`AssetCreation/Exports` → `/Game/HomeWorld/Meshes/...`), **one** transit model (CRUMB glide + dual shrine portal), and **one** look proof chain (`Docs/02` → Preview stills → Lib masters). Legacy DemoMap PCG + Homestead campaign maps do not create a parallel playable canon for the signed slice.

---

## 7. Recommended WAVE E upgrade targets (slice-touching only)

WAVE E may **upgrade** (not quarantine-delete) these paths after Lead **`APPROVE WAVE E`**:

| Target | Upgrade intent |
|--------|----------------|
| **`Source/HomeWorld/`** character, GameMode, interact/heal, TOD/NightMix wiring | Wire V1–V8 to VS_MVP markers + MPC |
| **`BP_HomeWorldCharacter`** + **`ABP_HomeWorldCharacter`** | Glide along CRUMB_* (FALLBACK spline follow); spirit/body swap at dusk |
| **`GA_Interact`**, **`GA_Heal`**, **`GA_Place`** | Reparent to C++ ability classes per project convention |
| **`BP_GameMode`** | Drive NightMix from GameState; portal/shrine triggers on Docs/04 meshes |
| **`/Game/HomeWorld/Materials/Masters/M_*`** + **`MI_*`** | Import/create ten masters; instance on kit meshes |
| **`/Game/HomeWorld/Maps/VS_MVP/`** dressed level | Place imported SM_* at ANCHOR_* / marker poses (not full biome sprawl) |
| **`init_unreal.py`** | Minimal idempotent slice setup hooks only |
| **`pie_test_runner.py`** | Add VS_MVP / marker presence checks when dress exists |
| **`docs/PCG/*`**, **`docs/Maps/*`** | Pointer updates: VS_MVP primary; DemoMap/Homestead historical banners |
| **`bootstrap_project.py`** | Repoint default orchestration from DemoMap → VS_MVP import + markers |

**Explicitly not WAVE E unless Lead names:** Mass/family, Milady, NFT, combat GA depth, planetoid dungeons, agent-company loop revival.

---

## 8. WAVE F delete candidates (names only — no deletes in WAVE D)

After Lead **SIGN OFF AUDIT** (`Docs/08_AUDIT_SIGN_OFF.md`), candidates for archive/removal:

**Maps (legacy):**

- `DemoMap`, `DemoMap_HLODLayer_*`
- `Homestead`, `Homestead_WP`, `Homestead_HLODLayer_*`, `Homestead.ini`

**PCG graphs:**

- `ForestIsland_PCG`
- `Planetoid_POI_PCG`

**Mass / AI:**

- `MEC_FamilyGatherer`
- `ST_FamilyGatherer`

**Abilities (combat placeholders):**

- `GA_Dodge`, `GA_PrimaryAttack`, `GA_ProtectorAttack`

**Building (agentic):**

- `BP_BuildOrder_Wall`, `SO_WallBuilder`, `DA_SO_WallBuilder_Behavior`

**Sample packs (entire trees):**

- `Content/StylizedProvencal/`
- `Content/Man/`

**Milady:**

- `Content/HomeWorld/Milady/`

**Python (map-builders + GUI + agent loop):**

- `create_demo_from_scratch.py`, `ensure_demo_map.py`
- `create_homestead_from_scratch.py`, `ensure_homestead_map.py`, `place_homestead_placeholders.py`, `place_homestead_spawn.py`
- `place_mass_spawner_demomap.py`, `create_mec_family_gatherer.py`, `link_state_tree_to_mec.py`, `create_state_tree_family_gatherer.py`
- `setup_planetoid_pcg.py`, `assemble_planetoid_from_config.py`
- `Content/Python/gui_automation/` (entire tree)
- `Tools/RunAutomationLoop.ps1`, `Start-AllAgents*.ps1`, `Watch-AutomationAndFix.ps1`, `Run-*-Agent.ps1`
- Root: `Start-AllAgents.bat`, `Run-DemoMapScript.bat`, `Run-PCGForestScript.bat`, `README-Automation.md`

**Docs (historical duplicates):**

- `VisionBoard/MVP/VERTICAL_SLICE_SIGNOFF.md` (superseded by Docs/07)
- `docs/Automation/AGENT_COMPANY.md` (after swarm pointer sufficient)

*No deletes until WAVE F and Lead SIGN OFF AUDIT.*

---

## 9. Gate — APPROVE WAVE D

| | |
|---|---|
| **Gate** | Lead types **`APPROVE WAVE D`** on the WAVE D PR |
| **Unlocks** | **WAVE E** — upgrade pass on slice-touching C++/BP/Python (see §7) |
| **Do not start** | WAVE E until gate granted; no Content deletes until WAVE F |

```
STOP — Lead approval required
Type: APPROVE WAVE D
```

---

## 10. Hard rules (unchanged)

| Rule | Status |
|------|--------|
| **Docs/07 vertical slice sign-off** | **CLOSED** — do not reopen |
| **FALLBACK FLIGHT** | **ARMED** — CRUMB glide + portal both ways |
| **No new features during audit WAVEs** | WAVE D is documentation only |
| **No Content binary deletes in WAVE D** | Names listed in §8 for future WAVE F only |
| **Exclusive file ownership / handoffs** | Durable notes under `Docs/handoffs/` |

---

## Board / Actions / Gate / Next (for Lead)

| | |
|---|---|
| **Board** | WAVE D deliverable ready — content canon doc; MVP vs legacy decisions; dual canon conflicts resolved |
| **Actions** | Review PR; comment **`APPROVE WAVE D`** to unlock WAVE E |
| **Gate** | `APPROVE WAVE D` — do not start WAVE E until granted |
| **Next (after gate)** | WAVE E — upgrade C++/BP/Python touching VS_MVP, NightMix, FALLBACK glide, portal shrines |
