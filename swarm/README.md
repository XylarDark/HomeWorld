# HomeWorld Swarm Kit

The conductor reads these files. Specialists receive **only** their role card plus canon slices listed in the wave packet — not the full brief ([DevEnvTemplate](https://github.com/XylarDark/DevEnvTemplate) thin-context practice).

**Human Lead:** [START_HERE.md](../START_HERE.md) · **Process:** [SWARM_OPS.md](SWARM_OPS.md) (Human Use gates, evidence, git safety, KNOWN_ERRORS) · **On-demand agents:** [.cursor/agents/](../.cursor/agents/README.md)

```
swarm/
  README.md                          ← you are here
  CONDUCTOR_KICKOFF_PROMPT.md        ← paste into a new chat with the files attached
  SWARM_OPS.md                       ← how the swarm runs (coordination runtime)
  PHASE_BOARD.md                     ← live status; conductor updates this
  HANDOFF_TEMPLATE.md                ← copy per completed task
  agents/                            ← paste into .cursor/agents/ as-is
    conductor.md
    designer.md
    world.md
    art-director.md
    tech-artist.md
    env-homestead.md
    env-planet.md
    props.md
    creatures.md
    lighting.md
    gameplay.md
    systems.md
    integration.md
    qa.md
  packets/
    WAVE_0_CANON.md
    WAVE_1_PARALLEL.md
    WAVE_2_HOMESTEAD.md
    WAVE_3_PLANET.md
    WAVE_4_VERBS.md
    WAVE_5_SLICE.md
```

Canon (what the game is) lives in:

`../HOMEWORLD_MVP_SWARM_BRIEF.md`

Ops (how agents coordinate) lives here. Do not merge them. Workers should not rewrite canon.
