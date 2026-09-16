# HomeWorld Swarm Kit

Drop this folder into the project root as `swarm/` (or keep the name).  
The conductor reads these files. Specialists receive only their role packet plus canon slices.

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
