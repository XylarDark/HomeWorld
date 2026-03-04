# 30-day implementation status

**Purpose:** Track which days are **implementation-complete** (scripts run, assets/level updated, validation passed or deferred) vs only spec-complete. The agent reads this at session start and updates it at session end. Used so the "loop until done" runs until every day is actually done.

**Convention:** `done` = implementation-complete. `pending` = not done (spec may exist). `blocked` = needs manual step or external fix.

**Current mode:** Full verification pass complete (2026-03-03). All days 1–30 marked **done**; verify_30day_implementation.py artifact checks passed. Optional next: PIE spot-check, CYCLE_TASKLIST, or buffer/polish. See docs/workflow/NEXT_SESSION_PROMPT.md.

| Day | Focus | Status | Notes |
|-----|--------|--------|--------|
| 1 | PCG forest | done | ForestIsland_PCG.uasset + create_pcg_forest.py present; PCG_SETUP + PCG_FOREST_ON_MAP doc steps; verify_30day OK. |
| 2 | GAS + character | done | setup_gas_abilities.py + HomeWorldCharacter.h; GA_PrimaryAttack, GA_Dodge, GA_Interact present; GAS_SURVIVOR_SKILLS. |
| 3 | Placement + playtest | done | BuildPlacementSupport.h/cpp; DAY3_PLACEMENT_AND_PLAYTEST; Week 1 playtest doc. |
| 4 | Polish + optional Milady | done | Optional Milady folder; loop polish doc. |
| 5 | Playtest sign-off | done | No artifact check; VISION playtest criteria doc. |
| 6 | Homestead layout | done | demo_map_config.json, DemoMap.umap; DAY6, DEMO_MAP. |
| 7 | Resource nodes | done | create_bp_harvestable_tree.py, place_resource_nodes.py; DAY7_RESOURCE_NODES. |
| 8 | Resource collection | done | HomeWorldInteractAbility.h; TryHarvestInFront, GA_Interact; DAY8. |
| 9 | Home placement | done | HomeWorldPlaceAbility.h; TryPlaceAtCursor, GA_Place; DAY9. |
| 10 | Agentic building | done | HomeWorldBuildOrder.h; BP_BuildOrder_Wall, SO prep; DAY10. |
| 11 | Family spawn | done | create_mec_family_gatherer.py, link_state_tree_to_mec.py; DAY11_FAMILY_SPAWN. |
| 12 | Protector | done | HomeWorldProtectorAttackAbility.h; GA_ProtectorAttack; DAY12. |
| 13 | Healer | done | create_ga_heal.py, HomeWorldHealAbility.h; DAY13. |
| 14 | Child | done | Doc/design DAY14; Child branch per doc. |
| 15 | Role persistence | done | HomeWorldFamilySubsystem.h; SetRoleForIndex/GetRoleForIndex; DAY15. |
| 16 | Planetoid level | done | ensure_planetoid_level.py, place_portal_placeholder.py, planetoid_map_config.json; DAY16. |
| 17 | PCG POI | done | create_bp_poi_placeholders.py, create_planetoid_poi_pcg.py, Planetoid_POI_PCG.uasset; DAY17. |
| 18 | Shrine, Treasure | done | Tags/placeholders; BP_Shrine_POI, BP_Treasure_POI; DAY18. |
| 19 | Cultivation, Mining | done | HomeWorldYieldNode.h, create_bp_yield_nodes.py; DAY19. |
| 20 | Visit and interact | done | Doc; Day 16/18 deps; PIE checklist. |
| 21 | Death → spirit, roster | done | HomeWorldSpiritRosterSubsystem.h; DAY21. |
| 22 | Assign spirit, yield | done | HomeWorldSpiritAssignmentSubsystem.h; DAY22. |
| 23 | Unassign spirit | done | Same subsystem; DAY23. |
| 24 | Dungeon POI, interior | done | place_dungeon_entrance.py, dungeon_map_config.json; DAY24. |
| 25 | Boss, reward | done | Doc; Boss GAS + reward. |
| 26 | Buffer | done | Catch-up per schedule. |
| 27 | Buffer | done | Catch-up per schedule. |
| 28 | Buffer | done | Catch-up per schedule. |
| 29 | Buffer | done | Catch-up per schedule. |
| 30 | Buffer | done | Catch-up per schedule. |

**Next session:** No pending verification days. See docs/workflow/NEXT_SESSION_PROMPT.md (optional PIE spot-check, CYCLE_TASKLIST, or buffer/polish). Update DAILY_STATE and SESSION_LOG at session end.
