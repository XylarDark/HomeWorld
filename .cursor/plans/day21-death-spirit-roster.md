# Day 21 [4.1][4.2] Death → spirit, Spirit roster — implementation plan

**Goal:** On death, character becomes spirit; spirit roster in GameState or subsystem.

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 21).

## Key steps

1. **Death → spirit:** When a family/player character dies (health 0 or custom death event), mark as spirit: e.g. add tag "Spirit", remove from playable roster if applicable, add to spirit list. Hook into existing damage/death (GAS or custom) or add minimal death detection (e.g. health attribute or event).
2. **Spirit roster:** Subsystem (e.g. UHomeWorldSpiritRosterSubsystem) or GameState holds list of spirits. Stub: TArray<FName> or struct with ID + optional name. Provide AddSpirit(id/name), GetSpirits(), optional RemoveSpirit for Day 23.
3. **Integration:** On death callback, call roster->AddSpirit(...). Log for validation. No UI required for Day 21; UI or command can be added later.
4. **Validation:** Trigger death (e.g. console or test damage), confirm spirit added to roster and log; optional: console command to list spirits.

## Success criteria

- Death (or test trigger) adds an entry to the spirit roster.
- Roster is queryable (GetSpirits or equivalent); stub storage only.
- Task doc Day 21 updated with implementation notes.

## Notes

- Family vs player: if only family members become spirits, hook family death path; if player can die and become spirit, hook player death. Clarify in task doc.
- Day 22 will consume roster for "assign spirit to node."
