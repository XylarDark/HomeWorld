# Day 19 [3.5][3.6] Cultivation, Mining — implementation plan

**Goal:** Cultivation and Mining nodes/zones; workable by spirits (Phase 4); yield resources over time.

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 19).

## Key steps

1. **Cultivation node:** Actor or zone that spirits can be assigned to (Phase 4); yields e.g. Wood/Food over time (tick or timer). Placeholder mesh. Data: resource type, yield rate (config or Blueprint).
2. **Mining node:** Same pattern; yields Ore/Stone. Data-driven (resource type, yield rate) in Blueprint or C++.
3. **Implementation:** Create C++ base (e.g. AHomeWorldYieldNode) with ResourceType, YieldRate, optional timer/tick that adds to a global or player inventory when "worked" (spirit assignment in Phase 4); or stub "when overlapping spirit, add yield every N seconds". For Day 19 minimal: placeable actors with config; actual yield logic can be tick-based stub that adds to subsystem when a "worker" is set.
4. **Validation:** Place node in level; optional: trigger yield (e.g. overlap or key) and confirm resource added; or document "spirit assignment in Day 22".

## Success criteria

- At least one Cultivation and one Mining node type (Blueprint or C++) with configurable resource type and yield rate.
- Yield can be triggered (stub: on timer or on overlap) and adds to inventory/subsystem.
- Task doc Day 19 updated.

## Notes

- Spirit assignment (Day 22) will reference these nodes; keep interface simple (e.g. SetWorker/GetWorker, or tag "CultivationNode"/"MiningNode").
- Reuse UHomeWorldInventorySubsystem::AddResource for yield output if player-collected; or separate "node inventory" for spirit-deposited yield.
