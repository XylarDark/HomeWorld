# HomeWorld – Plugin Setup

All required plugins are enabled in [HomeWorld.uproject](../HomeWorld.uproject). No Marketplace install is needed for co-op: **Steam Sockets** (in .uproject) replaces SteamCore/Steam Sessions.

| Plugin | .uproject name | Purpose |
|--------|----------------|---------|
| PCG (Procedural Content Generation) | `PCG` | Worlds/biomes |
| Gameplay Ability System (GAS) | `GameplayAbilities` | PoE-style combat |
| Steam Sockets | `SteamSockets` | Co-op (replaces SteamCore) |
| Enhanced Input | `EnhancedInput` | Better controls |
| Day Night Sequencer (UE5.5+) | `DaySequence` | Day/night cycles |

**Swarms (future):** Mass Entity is deprecated in UE 5.5+ and has been removed from this project. When implementing night swarms, enable and use whatever Mass-related plugin Epic documents as the replacement.

**Full checklist:** See [SETUP.md](SETUP.md) for developer setup steps and [SETUP_VALIDATION.md](SETUP_VALIDATION.md) to confirm setup is complete before Week 1.
