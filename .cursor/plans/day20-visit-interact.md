# Day 20 [3.7] Visit and interact — implementation plan

**Goal:** Player can travel to planetoid, reach POIs, interact (harvest treasure, activate shrine, etc.).

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 20).

## Key steps

1. **Level streaming / portal:** Verify or document how player travels from DemoMap (homestead) to planetoid (Day 16: place_portal_placeholder, Level Streaming or Open Level). No code change if already documented; optional: add a minimal trigger Blueprint or level-streaming volume setup script.
2. **POI interaction:** Day 18 already provides E/Interact for Shrine (log) and Treasure (AddResource, destroy). Ensure the same flow works when player is on the planetoid level (same GameMode/character, GA_Interact, TryHarvestInFront).
3. **Validation:** PIE test: travel to planetoid → move to Shrine/Treasure → press E; confirm Shrine log and Treasure loot. Document any manual steps (e.g. place portal trigger, set default map for testing planetoid).

## Success criteria

- Documented path for "travel to planetoid" (portal/streaming) and confirmation that Interact works on planetoid POIs.
- Optional: minimal script or Blueprint to trigger level transition at portal placeholder; or doc-only if manual setup suffices.

## Notes

- If GameMode and character are shared across levels, no code change needed for Interact on planetoid.
- Day 16 manual steps (Level Streaming Volume or Open Level at portal) are the main dependency.
