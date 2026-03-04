# Day 18 [3.3][3.4] Shrine POI, Treasure POI — implementation plan

**Goal:** Shrine actor (interaction/GAS); Treasure actor (loot on interact).

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 18).

## Key steps

1. **Shrine POI:** Add overlap or interaction to BP_Shrine_POI (or new BP_Shrine): Box/Sphere overlap component; on overlap or Interact trigger optional GAS ability (e.g. buff). Use existing GA_Interact or custom. Placeholder mesh OK. Document in task doc; implement in C++ (optional) or Blueprint.
2. **Treasure POI:** Add interaction to BP_Treasure_POI: on Interact grant resources (use inventory subsystem if present, or log/stub). Placeholder chest/cube OK. See [UHomeWorldInventorySubsystem] if available; otherwise stub "grant wood/ore" for Day 19+.
3. **Validation:** PIE on planetoid (or DemoMap with POI placed); approach Shrine and Treasure; trigger interact; confirm feedback (log or UI).

## Success criteria

- Shrine: overlap or Interact triggers behavior (GAS or placeholder logic).
- Treasure: Interact grants resources (or stub that logs/returns success).
- Task doc Day 18 updated with implementation notes.

## Notes

- BP_Shrine_POI and BP_Treasure_POI already exist (Day 17). Add components and logic in Blueprint or C++ helper; prefer programmatic-by-default (C++ where reusable).
- If UHomeWorldInventorySubsystem does not exist, stub "AddResource(Player, Wood, 10)" or equivalent for Treasure; implement full inventory in later day.
