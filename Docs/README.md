# Docs/ — MVP swarm canon

This directory is **Blender-first MVP swarm canon**: GDD slices, art bible, material sheet, WAVE handoffs, and QA placeholders for the multi-agent production kit.

## Do not merge with `docs/`

| Path | Purpose |
|------|---------|
| **`Docs/`** (this tree) | MVP swarm operating system — canon, handoffs, shot list, kit-facing specs linked from `Lib/` |
| **`docs/`** (lowercase) | Unreal Engine 5.7 project documentation — setup, automation, PCG, task lists, known errors |

These are **intentionally separate**. On case-insensitive filesystems (macOS/Windows defaults), Git may only check out one of the two names locally — clone on Linux CI or use a case-sensitive volume if you need both trees simultaneously.

## Entry points

- **Audit & upgrade strategy (Lead-gated):** [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md)
- **WAVE A inventory:** [08a_INVENTORY.md](08a_INVENTORY.md)
- **WAVE B harness gap:** [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) — COMPLETE (PR #12)
- **WAVE C boot health:** [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) — COMPLETE (PR #13)
- **WAVE D content canon:** [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) — COMPLETE (PR #14 merged)
- **WAVE E upgrade pass:** [08e_UPGRADE_PASS.md](08e_UPGRADE_PASS.md) — **Gate: `APPROVE WAVE E`**
- **Start swarm:** [../START_HERE.md](../START_HERE.md)
- **Master prompt:** [../HOMEWORLD_MASTER_PROMPT.md](../HOMEWORLD_MASTER_PROMPT.md)
- **Game canon brief:** [../HOMEWORLD_MVP_SWARM_BRIEF.md](../HOMEWORLD_MVP_SWARM_BRIEF.md)
- **Swarm ops:** [../swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md)
- **UE project context:** [../AGENTS.md](../AGENTS.md) and [../docs/README.md](../docs/README.md)
