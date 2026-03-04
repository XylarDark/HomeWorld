# Day 16 [3.1] Planetoid level — implementation plan

**Goal:** One planetoid level; travel from homestead (DemoMap) via portal or sublevel.

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 16 section), [PLANETOID_DESIGN.md](../docs/PLANETOID_DESIGN.md).

## Key steps

1. **Create planetoid level:** New level (e.g. Planetoid_Pride) or sublevel; save under `/Game/HomeWorld/Maps/` or as sublevel of DemoMap.
2. **Portal/trigger on DemoMap:** Add portal or trigger actor that streams/loads the planetoid level (Level Streaming or Open Level). Use placeholder mesh for portal if needed.
3. **Validation:** PIE on DemoMap; trigger portal; planetoid level loads.

## Success criteria

- Planetoid level exists and can be loaded.
- From DemoMap, player can trigger travel to planetoid (streaming or open level).

## Notes

- Use placeholder assets per DAYS_16_TO_30. Manual Editor steps for level creation and level streaming setup.
