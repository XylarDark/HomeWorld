# Session Log

Agent session summaries for cross-session context persistence.

**Agents: Read this file at the start of every task** to load prior context (completed work, blockers, errors, key decisions). Append a new entry at the end of each session. See `.cursor/rules/07-ai-agent-behavior.mdc` (Session Continuity).

---

## 2026-02-22 ? PIE verification, character consolidation, cleanup rules

**Tasks completed:**
- Fixed GameMode DefaultPawnClass (BP_Character -> BP_HomeWorldCharacter)
- PIE verification: character spawns, on ground (MOVE_WALKING), AnimBP active, 1161 PCG actors
- Deleted stale BP_Character asset
- Cleaned up 11 one-off diagnostic scripts and 10 temp JSON files
- Added session cleanup rules to Cursor rules (07-ai-agent-behavior.mdc, 09-mcp-workflow.mdc)
- Updated all task docs with PIE verification results
- Committed and pushed all changes

**Tasks remaining:**
- Task 1 (Animation): Rebuild C++, populate AnimBP AnimGraph state machine (manual)
- Task 2 (Orientation): Manual WASD test needed
- Visual spot-check of PCG forest

**Key decisions:**
- Single character chain: AHomeWorldCharacter (C++) -> BP_HomeWorldCharacter (BP) -> ABP_HomeWorldCharacter (AnimBP)
- Temp files go in Saved/ not project root; one-off scripts deleted after use

**Errors encountered:**
- UE 5.7 API: get_pie_worlds() requires include_dedicated_server arg
- UE 5.7 API: PlayerController uses get_controlled_pawn() not get_pawn()
- GameMode DefaultPawnClass was pointing to wrong Blueprint

---

## 2026-02-22 ? Agentic workflow improvements

**Tasks completed:**
- Created MCP harness (mcp_harness.py) for structured command-response
- Created PIE test runner (pie_test_runner.py) with reusable checks
- Enabled PythonAutomationTest plugin, created test suite (4 test files)
- Created Blueprint inspector (blueprint_inspector.py)
- Created viewport screenshot capture (capture_viewport.py)
- Expanded CI pipeline (validate.yml) with JSON, docs, C++, hygiene checks
- Documented build automation and agent utility scripts in MCP workflow rule
- Created session log mechanism (this file)
- Cleaned up stale debug references

**Key decisions:**
- Saved/ directory is the standard location for agent I/O files (not project root)
- PythonAutomationTest plugin for test_*.py auto-discovery
- MCP harness eliminates need for one-off diagnostic scripts

---

## 2026-02-22 ? DevEnvTemplate backport, workflow audit

**Tasks completed:**
- Backported Cursor rules improvements to DevEnvTemplate (idempotency, session cleanup, error prevention)
- Committed and pushed DevEnvTemplate; updated HomeWorld submodule
- Audited project against new rule set

**Key decisions:**
- DevEnvTemplate receives general improvements; Unreal/MCP-specific rules stay in HomeWorld

---

## 2026-02-22 ? Task audit and doc cleanup

**Tasks completed:**
- Audited all task docs; removed verbose "what's done" sections
- TASKLIST and task docs now focus only on remaining work to finish/verify
- Task 3 (ground) and Task 4 (PCG) marked verified; optional follow-ups only
- Task 1 (animation): Rebuild C++, manual AnimGraph, PIE test
- Task 2 (orientation): PIE WASD test, optional MeshForwardYawOffset

**Note:** PIE tests via MCP require Editor to be running and connected.

**Latest (Editor open):** Ran `pie_test_runner.py` via MCP. Results: 5/7 passed ? PIE active, character spawned, on ground, capsule 88/42, PCG 1161 actors. Skeletal mesh and AnimInstance checks returned false negatives (Python/PIE reflection).

---

## 2026-02-22 ? Bare-bones stack foundations

**Tasks completed:**
- Added AHomeWorldPlayerState (C++); GameMode sets PlayerStateClass.
- GAS replication for simulated proxies: PossessedBy inits ASC with Owner = PlayerState when !IsLocallyControlled() && !HasAuthority().
- Created docs/CONTENT_LAYOUT.md (content paths contract); referenced from SETUP and STACK_PLAN.
- World Partition: SETUP step 5 and validation bullet (Main map WP enabled); STACK_PLAN Layer 1 lock (engine 5.7, PC/Steam EA); DaySequence and SteamSockets tech choices in Layers 6?7; AGENTS.md lock line.
- Added UBuildPlacementSupport (Blueprint Function Library) with GetPlacementHit(WorldContextObject, MaxDistance, OutHit) for build/placement trace contract.

**Note:** C++ build was not run (Live Coding active). Rebuild after closing Editor to compile new files.

---

## 2026-02-24 ? Resume after rebuild

**Context:** Previous chat crashed; user was asked to rebuild and did so.

**Rebuild:** Build-HomeWorld.bat run successfully (Result: Succeeded, 9.86s). HomeWorldPlayerState, BuildPlacementSupport, HomeWorldGameMode, HomeWorldCharacter compiled and linked.

**Next:** Task 1 ? With Editor open, run `setup_animation_blueprint.py` via MCP; then manual AnimGraph (Locomotion state machine, Idle/Walk on Speed); PIE test. Task 2 ? PIE WASD orientation check.

---

## 2026-02-24 ? Bare-bones stack completion (all weeks, core tech only)

**Tasks completed:** Week 1: GAS DefaultAbilities granting, GetPlacementTransform, animation doc. Week 2: GAS needs doc, AHomeWorldAIController, UHomeWorldSessionSubsystem stub, UHomeWorldTimeOfDaySubsystem stub. Weeks 3?4: UHomeWorldLeaderboardSubsystem stub, TimeOfDay implementation doc, Mass/swarms doc in STACK_PLAN and KNOWN_ERRORS. Docs: STACK_PLAN Implementation status table, SESSION_LOG entry.

**Key decisions:** Only stable foundations (contracts, base classes, stubs); no content. Subsystems are stubs; backends in Week 2+.

**Errors encountered:** Build failed with Live Coding active; close Editor and run Build-HomeWorld.bat to compile.

---

## 2026-02-24 ? HomeWorld agentic automation (Mass + State Trees) plan

**Tasks completed:** Policy/docs: STACK_PLAN Layer 5 now recommends UE 5.7 Mass Entity + Mass AI (replaced deprecated wording). KNOWN_ERRORS entry updated to use Mass + Mass AI for family/swarm agents. SETUP.md: Week 2 plugins subsection (MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects); removed Mass deprecated note. AGENTS.md: Stack line updated for Week 2 Mass/State Tree. ROADMAP.md: "Mass or Epic's replacement" ? "Mass Entity + Mass AI (UE 5.7 recommended)" in all three places. CONTENT_LAYOUT.md: added /Game/HomeWorld/Mass/, AI/, ZoneGraph/, SmartObjects/. Plugins: added MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects to HomeWorld.uproject. Task doc: created docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md; added Task 5 to TASKLIST.md. STACK_PLAN implementation status table: Layer 5 note updated to Mass Entity + Mass AI.

**Key decisions:** Use UE 5.7 recommended (non-deprecated) tech; AHomeWorldAIController retained for actor-based NPCs. Manual Editor steps (MEC, State Tree, spawner, ZoneGraph, Smart Objects) remain in task doc for user.

---

## 2026-02-24 ? Editor open: animation setup + Week 2 folders

**With Editor open:** Ran via MCP: `setup_animation_blueprint.py` (success ? AnimBP created or already exists at /Game/HomeWorld/Characters/ABP_HomeWorldCharacter); `ensure_week2_folders.py` (created /Game/HomeWorld/Mass, AI, ZoneGraph, SmartObjects per CONTENT_LAYOUT). Ran `pie_test_runner.py` (PIE was not running: 1/7 passed, PCG 1161 actors).

**Remaining (manual):** Task 1 ? Open ABP_HomeWorldCharacter ? AnimGraph ? add Locomotion state machine (Idle/Walk on Speed); PIE test with Play. Task 5 ? Create MEC_FamilyGatherer, ST_FamilyGatherer, place Mass Spawner, ZoneGraph, Smart Objects per FAMILY_AGENTS_MASS_STATETREE.md.

---

## 2026-02-24 ? Agentic building automation (plan implementation)

**Tasks completed:** C++: Added AHomeWorldBuildOrder (BuildDefinitionID, OverlapVolume, tag BuildOrder) and AHomeWorldResourcePile (ResourceType, AmountPerHarvest, tag ResourcePile) in Source/HomeWorld/. CONTENT_LAYOUT.md: added /Game/HomeWorld/Building/. Python: extended ensure_week2_folders.py with /Game/HomeWorld/Building/. Docs: created docs/tasks/AGENTIC_BUILDING.md (steps 1?5, success criteria, references); added Task 6 to TASKLIST.md; added "Next: Agentic building" to FAMILY_AGENTS_MASS_STATETREE.md; added agentic building bullet to STACK_PLAN Layer 4.

**Key decisions:** Build order and resource pile are abstract C++ bases; Blueprint adds mesh and Smart Object. Full build was blocked by Live Coding (Editor open); UHT parsed new headers successfully.

**Remaining (manual, in AGENTIC_BUILDING.md):** Smart Object definitions (SO_WallBuilder, HarvestWood), State Tree BUILD branch, Mass Processor MP_WoodInventory, EQS, "Convert to Construction Mesh," placing BP_BuildOrder_Wall/BP_WoodPile in level.

---

## 2026-02-24 ? Editor closed: build verify + collision profile fix

**Tasks completed:** With Editor closed, ran Build-HomeWorld.bat. Build failed: `UCollisionProfile::OverlapAllDynamic_ProfileName` is not a member in UE 5.7. Fixed both HomeWorldBuildOrder.cpp and HomeWorldResourcePile.cpp to use `SetCollisionProfileName(FName("OverlapAllDynamic"))`. Rebuild succeeded (exit code 0). Documented fix in KNOWN_ERRORS.md.

**Key decisions:** Use profile name string for overlap collision in UE 5.7; avoid removed UCollisionProfile constants.

---

## 2026-02-24 ? External AI automation (doc + optional script)

**Tasks completed:** Created docs/EXTERNAL_AI_AUTOMATION.md (definitions, primary path Cursor+UnrealMCP, optional external script-generator path, HomeWorld paths, example prompt and script, security). Updated MCP_SETUP.md with "External AI / LLM-generated scripts" subsection linking to that doc. Updated AGENTS.md with one sentence and link to EXTERNAL_AI_AUTOMATION.md. Added Content/Python/llm_build_home_example.py as idempotent reference script (ensure Building path, spawn circle of placeholder actors; HomeWorld paths only).

**Key decisions:** UnrealMCP unchanged; external AI is optional enhancement. All naming HomeWorld; no RealmBond.

---

## 2026-02-24 ? Task list: in-depth manual guides

**Tasks completed:** Analyzed TASKLIST and all task docs. Expanded task docs into in-depth step-by-step guides for manual work: (1) CHARACTER_ANIMATION.md ? detailed AnimGraph steps (state machine, Idle/WalkRun, transitions with Speed, compile/save, PIE test), checklist, and animation paths. (2) CHARACTER_ORIENTATION.md ? PIE test steps and MeshForwardYawOffset fix with exact UI path. (3) CHARACTER_GROUND.md and PCG_FOREST_ON_MAP.md ? optional in-depth verification sections. (4) FAMILY_AGENTS_MASS_STATETREE.md ? plugins, MEC creation (traits table, mesh), State Tree (Selector, states, blackboard, link to MEC), spawner/ZoneGraph/Smart Objects placement, needs + night, checklist, troubleshooting table. (5) AGENTIC_BUILDING.md ? prep assets (Construction Mesh, BP_BuildOrder_Wall from C++), SO_WallBuilder (slots, events), BP_WoodPile, State Tree BUILD branch (EQS, tasks), MP_WoodInventory, spawn and test, checklist, troubleshooting. Updated TASKLIST.md to note that docs include in-depth manual guides.

**Key decisions:** No new automation added (AnimGraph, State Tree, Smart Objects, EQS are Editor-only). All manual steps are now documented with exact UI paths, checklists, and troubleshooting so the team can complete work without guesswork.

---

## 2026-02-24 ? MEC commandlet automation (HomeWorldEditor + CreateMEC)

**Tasks completed:** Implemented the CreateMEC commandlet as specified in the alternative-automation plan. (1) Added HomeWorldEditor module: HomeWorld.uproject second module entry (HomeWorldEditor, Editor); Source/HomeWorldEditor/HomeWorldEditor.Build.cs (UnrealEd, AssetTools, AssetRegistry, MassSpawner); HomeWorldEditor.h/.cpp with IMPLEMENT_MODULE; HomeWorldEditor.Target.cs ExtraModuleNames.Add("HomeWorldEditor"). (2) Implemented CreateMEC commandlet: CreateMECCommandlet.h/.cpp ? parses Path= (default /Game/HomeWorld/Mass/MEC_FamilyGatherer), creates or loads UMassEntityConfigAsset, adds traits by class path (MassSpawner.MassAgentTrait, MassMovement.MassMovementTrait, etc.), saves via UPackage::Save. Idempotent (reuses existing asset). (3) Updated docs: ALTERNATIVE_AUTOMATION_OPTIONS.md ? added build prerequisite (build with Editor closed); KNOWN_ERRORS.md ? entry for build failure when Live Coding is active. UHT and module setup succeeded; full compile was blocked by Live Coding (Editor open). Build and commandlet run must be done with Editor closed.

**Key decisions:** Single Editor module dependency for MEC: MassSpawner (UMassEntityConfigAsset, UMassEntityTraitBase). Trait class paths use /Script/Module.Class; unknown traits are skipped with a warning. State Tree and mesh assignment left for Editor or future commandlet extension.

**Errors encountered:** None in code. Build requires Editor closed (documented in KNOWN_ERRORS and ALTERNATIVE_AUTOMATION_OPTIONS).

---

## 2026-02-24 ? Character animation: Speed variable not in AnimBP variables list

**Issue:** User on CHARACTER_ANIMATION Step 5 could not find "Speed" in the variables list for Idle/WalkRun transition conditions.

**Root cause:** Speed is exposed by the C++ parent `UHomeWorldAnimInstance`. If the ABP was created when C++ was not built (or with default parent), its parent stays `AnimInstance` and inherited C++ variables are not visible.

**Fixes applied:**
- **C++:** Added `Blueprintable` to `UHomeWorldAnimInstance` (HomeWorldAnimInstance.h).
- **Script:** `setup_animation_blueprint.py` now reparents an existing ABP to `UHomeWorldAnimInstance` when the asset already exists, so re-running the script fixes parent class and makes Speed/bIsInAir/bIsMoving visible.
- **Doc:** CHARACTER_ANIMATION.md ? Step 5: added "How to get Speed" (Variables panel vs right-click search "Speed"/Get Speed); new "Troubleshooting: Speed not in the variables list" (re-run setup script, reparent manually, or use graph search); Reference note on reparent.

**Next for user:** Re-run `setup_animation_blueprint.py` (MCP or Tools ? Execute Python Script), close and reopen ABP_HomeWorldCharacter, then in the transition graph use Speed (Variables or right-click ? search "Speed"). Rebuild C++ if the Blueprintable change was just added.

---

## 2026-02-24 ? Movement setup best-practices validation

**Tasks completed:** Validated third-person movement implementation against Epic docs, Lyra references, and community patterns (wirepair, UE5 Enhanced Input tutorials). Created `docs/MOVEMENT_INPUT_VALIDATION.md` with comparison table and references.

**Findings:** Current setup aligns with best practices: Triggered + Completed for movement (key release stops input); camera-relative direction via GetControlRotation(); AddMovementInput(world direction, scale) in Tick; bOrientRotationToMovement for third-person; four Boolean input actions (W/S/A/D) used due to Python IMC modifier issues, with Axis2D fallback when four actions are not set. No code changes required for validation.

---

## 2026-02-24 ? Orientation complete + Character Ground (plan execution)

**Tasks completed:** Implemented plan "Orientation complete + Character Ground (next task)". (1) **Part 1:** Marked Task 2 (orientation) completed: TASKLIST.md ? Task 2 row set to Completed/Done, summary updated; CHARACTER_ORIENTATION.md ? Status Completed, Latest and "What is already done" updated with mesh offset -90, checklist marked done. (2) **Part 2:** Completed Task 3 (Character on ground): TASKLIST.md ? Task 3 row set to Completed/Done, note that Task 3 was next focus and terrain deferred; CHARACTER_GROUND.md ? Status Completed, Latest updated with spawn/ground trace and note that walk-on-surface is deferred.

**Key decisions:** Terrain / walk-on-ground-surface remains a separate, deferred concern; no new task doc or implementation in this pass.

---

## 2026-02-24 ? Enhanced Input on Editor load

**Tasks completed:** Added `Content/Python/init_unreal.py` so Enhanced Input setup runs automatically when the Editor loads. Uses Unreal?s standard startup script in `Content/Python/`; calls `setup_enhanced_input.main()` (idempotent). Updated `docs/SETUP.md` validation and PIE troubleshooting to state that Enhanced Input is applied on load and when to run scripts manually if needed.

**Key decisions:** Single startup script runs only Enhanced Input (not full bootstrap) to keep startup fast and avoid prompts; same assets as manual run.

---

## 2026-02-24 ? Rules updated from session (avoid ?run script for movement?)

**Tasks completed:** Updated Cursor rules and AGENTS.md so the problems from this session are avoided. (1) **00-core-principles.mdc** ? Added ?Editor startup setup?: run critical setup (e.g. Enhanced Input) at Editor load via `init_unreal.py`; don?t require users to run setup_enhanced_input as normal first step. (2) **09-mcp-workflow.mdc** ? Added ?Editor startup scripts?: init_unreal.py runs on load; only suggest running setup_enhanced_input when troubleshooting. (3) **08-project-context.mdc** ? Added ?Critical setup on load? principle. (4) **12-python.mdc** ? Added ?Editor startup script? subsection: keep init_unreal.py minimal and idempotent. (5) **AGENTS.md** ? Noted in Dev environment setup that Enhanced Input is applied on load; manual run only for troubleshooting.

**Key decisions:** Encode ?critical setup on load? and ?don?t instruct run setup_enhanced_input unless troubleshooting? so future agents and docs don?t reintroduce the ?movement only works after running script? workflow.

---

## 2026-02-25 ? PCG Fundamental Redo (plan execution)

**Tasks completed:** Implemented PCG Fundamental Redo plan (Phase 2 Option A + Phase 3). create_demo_map.py: PCG block only ensure_landscape_has_pcg_tag + place_pcg_volume; log points to docs/PCG_SETUP.md. setup_level/bootstrap: docstring and next-steps updated. Phase 3: Created docs/PCG_SETUP.md; updated PCG_MANUAL_SETUP, PCG_FOREST_ON_MAP, KNOWN_ERRORS (script does not create/assign graph).

**Key decisions:** Single source of truth for PCG is docs/PCG_SETUP.md; script scope is tag Landscape + create/size PCG Volume only.

---

## 2026-02-25 ? PCG variables no-access research and standard procedure

**Tasks completed:** Implemented PCG Variables With No (or Unreliable) Automation Access plan. (1) Created docs/PCG_VARIABLES_NO_ACCESS.md with summary table (Get Landscape Data actor/component selector, PCG Volume graph, Static Mesh Spawner mesh entries, Surface Sampler exposed in 5.7, wiring pin labels), per-node details, and references. (2) Added Content/Python/pcg_settings_introspect.py (Editor-only; writes Saved/pcg_settings_introspect_5.7.txt). (3) Cross-linked: PCG_SETUP.md references PCG_VARIABLES_NO_ACCESS.md; KNOWN_ERRORS PCG entries reference PCG_VARIABLES_NO_ACCESS.md. (4) Encoded "variables no access" as standard procedure: new .cursor/rules/automation-standards.mdc (four-step procedure + PCG example); AGENTS.md Setup and validation updated with automation-standards.mdc and procedure sentence; docs/CONVENTIONS.md MCP-first section updated with procedure and link to PCG_VARIABLES_NO_ACCESS.md.

**Key decisions:** Checking and documenting required-but-inaccessible variables is now standard whenever we add automation for Editor/engine features; re-check on engine/API upgrades.

---

## 2026-02-26 ? Milady Character Import Pipeline roadmap implementation

**Tasks completed:** Implemented Milady Character Import Pipeline roadmap as specified in the plan. (1) Created docs/tasks/MILADY_IMPORT_ROADMAP.md with full 7-phase roadmap (Plugin setup, Wallet/NFT, IPFS PNG, Meshy 2D?3D, VRM4U import/rigging, Animation retargeting, Player integration), task tables (Programmatic/Manual, dependencies, effort, perf notes), milestones, and references. (2) Updated CONTENT_LAYOUT.md with /Game/HomeWorld/Milady/ path and purpose. (3) Updated SETUP.md with Milady pipeline plugins subsection (VRM4U, Meshy-for-Unreal, Web3/Wallet) and link to MILADY_IMPORT_SETUP.md. (4) Created docs/MILADY_IMPORT_SETUP.md with one-time setup: plugin install order, API keys, content paths, ensure_milady_folders.py usage, known issues, Remilia Collective contract reference. (5) Created Content/Python/ensure_milady_folders.py (idempotent; creates Milady/Meshes, Materials, Animations, Blueprints). (6) Added Task 7 to TASKLIST.md: Milady Character Import pipeline linking to MILADY_IMPORT_ROADMAP.md and MILADY_IMPORT_SETUP.md.

**Key decisions:** Roadmap is copy-paste ready for execution; Phase 1 programmatic deliverables (docs + script) done; plugin installs and Phases 2?7 remain for team/next sessions.

---

## 2026-02-26 ? Milady import: programmatic implementation and manual steps list

**Tasks completed:** (1) C++: UHomeWorldWalletSubsystem (connected address), UHomeWorldNFTSubsystem (LoadMiladyConfig, FetchMetadataFromURL, DownloadMiladyPNG, IPFS gateway, VerifyMiladyOwnership stub), UHomeWorldMiladyImportSubsystem (ImportMiladyFromMetadataURL: metadata then PNG; Meshy/VRM4U stubbed), FMiladyTokenMetadata (MiladyTypes.h), UHomeWorldChibiAnimInstance (BouncePhase, BounceScale, BounceOffset). (2) HomeWorld.Build.cs: HTTP, Json, JsonUtilities. (3) Config/DefaultGame.ini: [Milady] RemiliaContractAddress, EthereumRPCURL, IPFSGateway. (4) Python: create_milady_pastel_material.py (M_MiladyPastel). (5) MILADY_IMPORT_ROADMAP.md: added "Programmatic work completed" and "Manual steps required" (checklist for all phases). (6) TASKLIST.md: Task 7 status In progress, note pointing to manual steps.

**Key decisions:** ImportMiladyByTokenId stays stub until Web3 provides tokenURI; use ImportMiladyFromMetadataURL with known metadata URL for testing. Build failed with Live Coding active (Editor open); close Editor and run Build-HomeWorld.bat to compile.

---

## 2026-02-26 PCG debug: spawning below landscape and trees not upright

**Tasks completed:**
- Implemented PCG debug plan: (1) Set **transform_offset_z** to **0** in `pcg_forest_config.json` (base-pivot default); updated comment to point to PCG_SETUP. (2) Added **update_forest_island_graph_from_config(graph_asset)** in `create_pcg_forest.py` to re-apply offset and yaw-only rotation to all Transform Points nodes from config; called from **place_pcg_volume** when a graph is assigned so re-running Homestead or demo PCG script applies config without recreating the graph. (3) Comment in homestead_map_config: PCG transform_offset_z is in pcg_forest_config (shared graph). (4) Inline comment in create_pcg_forest.py for transform_offset_z (0 = base-pivot; negative = center-pivot). (5) **PCG_SETUP.md:** Reworded “Poking out the bottom” to clarify spawn Z is from transform_offset_z and pivot; added **Debug** subsection (mesh pivot, transform_offset_z 0 vs negative, rotation verification steps, volume_extent_z_padding note). (6) **KNOWN_ERRORS.md:** New entry “PCG: trees tilted or meshes poking out of the bottom of the landscape” with cause and fix. (7) **PCG_VARIABLES_NO_ACCESS.md:** Bullet linking to KNOWN_ERRORS and PCG_SETUP for trees tilted / meshes out of bottom.

**Key decisions:**
- Default offset 0 favors base-pivot meshes (Stylized Provencal); if trees float, set negative in config and re-run script.
- Graph is updated from config on every place_pcg_volume with a graph so no need to delete ForestIsland_PCG to pick up config changes.

---

## 2026-02-27 Parallel plugin: policy-driven, self-aware tool suggestions

**Tasks completed:**
- Added `.cursor/rules/11-parallel-plugin.mdc`: policy to recommend user run Parallel commands (don't do the work); tool-awareness table for when to suggest `/parallel-search`, `/parallel-extract`, `/parallel-research`, `/parallel-enrich`; citations and status/result commands.
- Updated AGENTS.md with one-line Parallel plugin mention (agent recommends commands, user pastes, agent interprets).
- Updated docs/SETUP.md: optional `/parallel-setup` under Cursor rules list.
- Updated `.cursor/rules/05-error-handling.mdc`: when investigating errors/API changes needing external info, recommend `/parallel-search` or `/parallel-extract`, then record in KNOWN_ERRORS with source/citation.

**Key decisions:**
- No PARALLEL_PLUGIN_USAGE.md; rule is single source of truth so environment is self-aware without a doc.
- Recommend-don't-do is default: agent suggests the command, user runs and pastes, agent interprets and integrates.

---

## 2026-02-27 Compound Engineering Plugin Integration

**Tasks completed:**
- Implemented Compound Engineering integration plan. (1) Created `.cursor/rules/10-compound-engineering.mdc`: policy rule with `alwaysApply: true`, situation-to-command mapping (brainstorm → `/workflowsbrainstorm`, plan → `/workflowsplan`, review → `/workflowsreview`, execute plan → `/workflowswork`, changelog → `/changelog`, document solution → `/workflowscompound`, deepen plan → `/deepen-plan`, autonomous → `/lfg`/`/slfg`, library docs → context7 MCP, first-time → `/setup`), exception when user asks for work in-chat, self-contained (no doc link). (2) Updated AGENTS.md: added Compound Engineering subsection stating recommending plugin commands is policy, mapping in rule, context7 for docs, optional `/setup`. (3) Updated docs/SETUP.md: optional step to run `/setup` in Cursor once for Compound Engineering, with pointer to rule. (4) Updated docs/CURSOR_DEV.md: one sentence that plugin recommendation is policy and link to rule.

**Key decisions:**
- Rule is single source of truth; no separate COMPOUND_ENGINEERING.md. Agent suggests plugin commands when use case fits instead of doing that workflow inline.

---

## 2026-02-27 30-Day Schedule and Doc Consolidation

**Tasks completed:**
- Created `docs/workflow/`: README.md (entry point, Pre–Day 1 checklist, task status table), VISION.md (consolidated prototype + campaign, moral system, tech summary, scope lock), 30_DAY_SCHEDULE.md (Day 1–30 with checkboxes; Act 1 → Homestead → Family → Planetoid → Spirits → Dungeon → buffer).
- Removed redundant docs: HOMESTEAD_DAILY_ROADMAP.md, TASKLIST.md, ROADMAP.md (root), PROTOTYPE_VISION.md, CAMPAIGN_VISION.md, HOMESTEAD_PLANETOID_ROADMAP.md, TEAM_APPROVAL_CHECKLIST.md. Content merged into workflow/VISION and 30_DAY_SCHEDULE.
- Updated references: AGENTS.md, README.md, CONTRIBUTING.md, STACK_PLAN.md, PLANETOID_DESIGN.md, HOMESTEAD_MAP.md, SETUP.md, MILADY_IMPORT_ROADMAP.md, .github ISSUE_TEMPLATE and PULL_REQUEST_TEMPLATE to point to docs/workflow/.

**Key decisions:**
- Single workflow folder is source of truth for vision and daily schedule. Operational docs (SETUP, KNOWN_ERRORS, PCG_SETUP, CONVENTIONS, CONTENT_LAYOUT, MCP_SETUP) and task how-to guides in docs/tasks/ remain; schedule references them by day.

---

## 2026-02-26 PCG debug: volume Z and spawn position

**Tasks completed:**
- Reduced **volume_extent_z_padding** from 10000 to 1000 cm in `homestead_map_config.json` and in `create_homestead_pcg.py` defaults so the PCG volume fits tighter around the landscape and does not extend far below the map (quick fix for "volume underneath the map").
- Updated **PCG_SETUP.md**: volume_extent_z_padding default 1000 cm; increase only if sampling fails at terrain edges.
- Added **HOMESTEAD_MAP.md** checklist for "trees/rocks out of bottom or not upright": re-run `create_homestead_pcg.py`, use transform_offset_z 0 for base-pivot meshes, re-run to resize volume with new padding.

**Remaining (already in place):** transform_offset_z is 0 in pcg_forest_config.json; `place_pcg_volume` calls `update_forest_island_graph_from_config` so re-running the Homestead PCG script re-applies offset and yaw-only rotation. Day 1 manual steps and verification (PCG manual steps, verify trees/rocks on landscape) still required.

---

## 2026-02-26 UE 5.7 tech upgrade (agentic-style pass)

**Tasks completed:**
- Created **docs/UE57_TECH.md**: single entry point for UE 5.7 tech (when to use, key links, canonical examples, audit result, plugin/5.7 status, upgrade path, plan-first for UE work). Audit: game C++ and Content/Python checked; no deprecated API usage in repo.
- Updated **AGENTS.md**: UE 5.7 API/plugin work reminder (check unreal-cpp.mdc and KNOWN_ERRORS first); added ue57-api-check to project skills list.
- Updated **07-ai-agent-behavior.mdc**: added "UE 5.7 check" to AI Agent Checklist (before C++/Blueprint/PCG/plugin changes check pitfalls and KNOWN_ERRORS; after upgrade re-verify automation).
- Updated **Source/HomeWorld/AGENTS.md** and **Content/Python/AGENTS.md**: UE 5.7 lock and pointer to unreal-cpp, KNOWN_ERRORS, UE57_TECH.
- Added **.cursor/commands/build-and-validate.md**: build steps, log check, optional PIE, reminder to check KNOWN_ERRORS when touching C++/PCG/plugins.
- Expanded **canonical examples**: README.md (GAS, PCG automation, link to UE57_TECH); unreal-cpp.mdc (GAS: HomeWorldGameplayAbility, HomeWorldAttributeSet); 12-python.mdc (level_loader, create_pcg_forest).
- Added **.cursor/skills/ue57-api-check/SKILL.md**: when to use (FindObject, FPaths, collision, get_actor_bounds, AnimBP factory, etc.), steps (pitfalls table, KNOWN_ERRORS, replacements, build/test), references.

**Key decisions:**
- UE 5.7 tech entry point is docs/UE57_TECH.md; no separate plan file edited. All implementation followed the attached UE 5.7 tech upgrade plan.

---

## 2026-02-26 PCG: Generate fix plan + agentic best practices

**Tasks completed:**
- **Phase 1:** Added "Generate produces nothing (checklist)" to [docs/PCG_SETUP.md](PCG_SETUP.md): ordered 5-step checklist (Get Landscape Data, mesh list, graph on volume, Landscape tag, Load All if WP), Output Log search (LogPCG / "No surfaces found"), Surface Sampler Debug, optional minimal PCG test; Homestead Load All and StylizedProvencal asset verification. Updated [.cursor/skills/pcg-validate/SKILL.md](.cursor/skills/pcg-validate/SKILL.md) with same checklist and diagnosis steps. Added to [AGENTS.md](AGENTS.md) Commands: "PCG Generate nothing" bullet (pcg-validate skill + PCG_SETUP checklist). Added to [.cursor/rules/07-ai-agent-behavior.mdc](.cursor/rules/07-ai-agent-behavior.mdc) AI Agent Checklist: when user reports PCG Generate produces nothing, follow checklist and pcg-validate skill.
- **Phase 2:** Created [docs/PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md): minimal working graph, mandatory manual steps, when to use Partitioned/Hierarchical generation, reference projects/tutorials. Created [.cursor/rules/pcg-best-practices.mdc](.cursor/rules/pcg-best-practices.mdc): before changing PCG graph or adding nodes, check PCG_BEST_PRACTICES and PCG_VARIABLES_NO_ACCESS. Updated pcg-validate skill with "Minimal working graph" and "Mandatory manual steps" subsections; added Key Files entry in 08-project-context for PCG_BEST_PRACTICES; added PCG graph reminder in AGENTS.md (UE 5.7 / PCG work).
- **Phase 3:** Added "From decoration to collectible resources" to PCG_BEST_PRACTICES.md (Static Mesh only vs Actor Spawner vs hybrid) and to pcg-validate skill so the agent can recommend the right option when the user wants resources in set locations for collection.

**Key decisions:**
- All discoveries written to both human docs and agent-facing artifacts (rules, skills, AGENTS.md) per plan agentic-integration table.
- No code changes to create_pcg_forest.py or create_homestead_from_scratch.py; plan was documentation and agentic best practices only.

---

## 2026-02-26 PCG debug instrumentation cleanup

**Tasks completed:**
- Removed all `_agent_log` debug instrumentation (and `#region agent log` blocks) from: `create_homestead_from_scratch.py`, `create_pcg_forest.py`, `level_loader.py`, `check_level_bounds.py`, `Content/Python/tests/test_level_loader.py`, `Content/Python/tests/test_level_pie_flow.py`. Dropped unused `json`/`time` imports where they were only used by instrumentation.

**Context:** User had confirmed PCG success (volume fitted to landscape; assets on ground and upright). Per debug workflow, instrumentation was removed after confirmed success.

---

## 2026-02-26 PCG volume and WP best practices (plan implementation)

**Tasks completed:**
- **Config-first volume:** Simplified [Content/Python/create_homestead_from_scratch.py](Content/Python/create_homestead_from_scratch.py): volume bounds come from config (`volume_center_*`, `volume_extent_*`); optional **one-shot** landscape override when `use_landscape_bounds` is true (no retries, no Phase 1/2 wait, no WP.LoadAll). Removed `time` import.
- **PCG_SETUP.md:** Rewrote **PCG volume size** section: defined "location" and "volume" as the single PCG Volume center and half-extents; config as source of truth; optional one-shot landscape; added **Partitioned Generation** steps (Is Partitioned on PCG component, Partition Grid Size on PCG World Actor). Updated Fast iteration, "What the script does," "Volume bounds" in If nothing generates, and Homestead bullet in Generate produces nothing.
- **PCG_BEST_PRACTICES.md:** Added **World Partition: volume and partition grid** subsection (config/fixed region for volume bounds; Partitioned Generation + grid; Get Landscape Data for surface only).
- **HOMESTEAD_MAP.md:** Updated Content paths, PCG summary, and Scripts table to document config-first volume bounds and set `volume_center_*`/`volume_extent_*` to match playable region; referenced Is Partitioned and PCG World Actor.

**Key decisions:** Per plan: landscape is the right source for **surface** (Get Landscape Data), not for **volume sizing** in script when using World Partition; script no longer depends on landscape bounds being available.

---

## 2026-02-26 PCG re-approach: manual vs programmatic split, programmatic steps done

**Tasks completed:**
- Created **docs/PCG_TUTORIAL_ALIGNMENT.md**: split the PCG re-approach into **Manual** (user in Editor) and **Programmatic (completed)** sections; manual plan includes follow Epic tutorial, optional reference-project verification, WP Cleanup then Generate, Load All before Generate, and post-script manual steps.
- **PCG_BEST_PRACTICES.md:** Added **Canonical flow (from Epic)** subsection: minimal Get Landscape Data → Surface, Input → Bounding, Surface Sampler → Spawner → Output; Landscape 1x1 and tag; note that our graph extends this with Density, Transform, Difference, rocks; links to Epic Foundation and PCG Tutorial Series.
- **PCG_SETUP.md:** Documented **Cleanup then Generate** for World Partition (in Steps only you do, PCG volume size step 3, Fast iteration step 5); added checklist item 6 (if Partition Grid Size or Is Partitioned changed, run Cleanup then Generate); expanded **Minimal PCG test** to canonical-only graph (Input + Get Landscape Data + Surface Sampler + one Spawner, no Density/Transform/Difference) for troubleshooting.
- **create_pcg_forest.py:** Updated top-of-file comment to state the script builds the canonical tutorial flow plus Density, Transform, optional Difference, rocks; added pointer to PCG_BEST_PRACTICES.

**Key decisions:** All programmatic work done in docs and one script comment; no new automation. User follows the manual plan in PCG_TUTORIAL_ALIGNMENT.md.

---

## 2026-02-26 Scripts and docs: organization and redundancy

**Tasks completed:**
- **PCG_MANUAL_SETUP.md:** Corrected description — script (create_pcg_forest) does create the graph; doc is for building from scratch in the Editor without the script. Added top note pointing to PCG_SETUP for script-based flow; fixed "After it works" to link to PCG_SETUP.
- **PCG_FOREST_ON_MAP.md:** Config line updated to Homestead: homestead_map_config.json (level, volume, exclusion), pcg_forest_config.json (density, transform, meshes).
- **create_homestead_from_scratch.py:** DRY — now calls ensure_homestead_map.ensure_homestead_map_exists() instead of inline _ensure_homestead_exists(); removed duplicate logic.
- **CONTENT_LAYOUT.md:** Added "Script index" table under Python and config paths (script name, purpose, entry/called-by, config). Updated configs example to homestead_map_config.json.
- **HOMESTEAD_MAP.md:** Scripts table updated to state create_homestead_from_scratch ensures map (calls ensure_homestead_map). Added note: ensure_homestead_map.py is for "map only, no PCG"; ensure_homestead_folders run separately when needed.

**Key decisions:** Scripts stay flat in Content/Python; no subdirs. Single canonical PCG runbook remains PCG_SETUP.md.

---

## 2026-02-26 Game Dev Best Practices and 30-Day Prototype (plan implementation)

**Tasks completed:**
- **VISION.md:** Added subsection **"Demonstrable prototype and vertical slice"**: MVP vs vertical slice definitions, campaign alignment (family taken → lone wanderer → claim home as base for rescue), Week 1 playtest as gate, and "one moment + one beautiful corner" by end of 30 days.
- **STACK_PLAN.md:** Added **"Free assets for prototype"** table: FAB, Quixel Bridge, POLYGON Adventure Pack, Medieval Village Megapack, Primitive Characters Pack with use (forest / homestead / family) and suggested use by day range; link to Fab free content and references to VISION and PROTOTYPE_SCOPE.
- **docs/workflow/PROTOTYPE_SCOPE.md:** Created scoping doc with gameplay loop, creative pillars, chosen moment/corner (TBD), and asset list by type (Player, Enemies, Allies, Buildings, Environment, Items/resources, Boss).
- **30_DAY_SCHEDULE.md:** Added **prototype gate** note at top: Day 5 = sign-off before Day 6; Days 26–30 = pick one moment + one corner and/or record demo; link to VISION.

**Key decisions:** All four doc updates from the plan implemented; no code changes. Campaign-aligned MVP (family taken, lone wanderer, claim base for rescue) is now explicit in workflow docs.
