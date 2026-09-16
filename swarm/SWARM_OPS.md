# HOMEWORLD SWARM OPS

**Runtime for the conductor.** This is the coordination script.  
Canon stays in `HOMEWORLD_MVP_SWARM_BRIEF.md`. If ops and canon conflict, **canon wins on design**, **ops wins on process**.

## 1. Architecture (locked)

Two-tier only. No flat peer chat. No shared scratch file that every agent writes.

```
Human Lead
 └── CND Conductor   (assigns, gates, merges; does not model or code features)
      ├── Phase graph with exit checkboxes
      ├── Fan-out workers with exclusive file/collection ownership
      └── QA judge with no shared memory of builder chat
```

Patterns allowed:

| Pattern | When |
|---|---|
| Chain | Phase 0 → 1 → 2 |
| Fan-out | Independent owners inside one phase (ENV-H / PROP / LIT) |
| Pipeline + gate | Every phase exit |
| Supervisor | Conductor reroute on failed QA |

Forbidden:

- Group-chat design debates after Phase 0
- Two agents editing the same Blender collection or the same UE map actor
- Implementer marking its own phase complete
- Dumping the entire brief into every worker prompt

## 2. Tooling (what to actually use)

| Layer | Tool | Job |
|---|---|---|
| Human + files | This kit + git | Source of truth |
| Conductor host | Cursor Project coordinator **or** one long Conductor chat | Assign / refuse / merge |
| Workers | Cursor subagents from `swarm/agents/` + Blender MCP | Build artifacts |
| Isolation | One owner per collection / folder; worktrees if two agents might touch the same `.blend` | Prevent overwrite |
| Optional later | LangGraph around phase flags | Resume after crash |
| Optional later | CrewAI only as a role wrapper | Not required |
| Do not start on | AutoGen group chat, OpenAI Swarm, MetaGPT studio sim | Wrong pattern |

MCP: Blender for art phases. GitHub if the repo is connected. No extra SaaS required for MVP.

## 3. Shared state (the only legal shared memory)

Agents do not brief each other in chat. They read files.

| File | Who writes | Who reads |
|---|---|---|
| `HOMEWORLD_MVP_SWARM_BRIEF.md` | Human Lead only after Phase 0 | Everyone |
| `swarm/PHASE_BOARD.md` | Conductor only | Everyone |
| `Docs/**` | Role listed on the packet | Downstream roles |
| `Docs/handoffs/*.md` | Completing worker | Conductor + QA + next owner |
| `.blend` collections | Exclusive owner in the packet | Downstream, read-only until handoff |

If it is not in a file, it did not happen.

## 4. Handoff contract

Every finished task writes `Docs/handoffs/P{phase}_{ROLE}_{slug}.md` using `HANDOFF_TEMPLATE.md`.

Conductor **refuses** the next task if any of these are missing:

- Artifact path
- Object / material name list
- Owner
- Phase exit boxes the worker claims
- Blockers
- “Did not invent” checklist (no extra biome, beast, shader family, flight model)

QA may not edit kits. QA only files defects against canon + shot list + verb list.

## 5. Phase graph

```
P0 Canon freeze
    DES + AD + CND
    GATE: Docs/00_CANON.md + Docs/00_SHOTLIST.md + folders exist
P1 GDD + graybox
    DES then WLD (chain)
    GATE: lookout camera sees landing, roofs, path; walk times written
P2 Materials + bible
    AD + TA (fan-out, different files)
    GATE: 10 masters + parameter sheet + NightMix demo
P3 Homestead kit
    ENV-H + PROP + LIT (fan-out, different collections)
    GATE: Preview_Homestead_Night matches key art tests
P4 Planet + transit
    ENV-P + WLD + LIT (WLD places, ENV-P builds, LIT presets)
    GATE: Shots 3–4; same masters; glide path visible
P5 Verbs + life
    CHA + PROP leftovers + GP + SYS
    GATE: 8 verbs executable on graybox + kits
P6 Integrate
    INT + CND + TA
    GATE: leave island, reach planet, return by portal
P7 Sign-off
    QA + AD + DES + Human Lead
    GATE: Docs/07_VERTICAL_SLICE_SIGN OFF.md
```

Never start N+1 on a failed gate. Fallback if flight slips: scripted glide down + portal both ways. Conductor may apply that cut without a design meeting.

## 6. File ownership (collision map)

| Path / collection | Sole writer |
|---|---|
| `Docs/00_*` `Docs/01_*` | DES (AD on shotlist + bible) |
| `Docs/02_ART_BIBLE.md` | AD |
| `Docs/02_MATERIAL_SHEET.md` + `Lib/06_Materials_Master` | TA |
| `Lib/01_Homestead` `SM_IslandTop` `SM_Cliff` cabin modules | ENV-H |
| `Lib/02_Forest` planet meshes | ENV-P |
| `Lib/03_Gatherables` shrine, landing circle, planters, path tiles | PROP |
| `Lib/04_Beasts` `Lib/05_Spirits` family blockouts | CHA |
| `Lib/07_Night_SpiritLayer` lights, volume, moon, cameras | LIT |
| `Lib/08_Transit` glide spline crumbs after PROP circle exists | WLD + ENV-P |
| Gameplay / systems code | GP / SYS |
| Maps, export table | INT |
| `swarm/PHASE_BOARD.md` | CND |
| Defects `Docs/qa/` | QA |

If two packets name the same path, Conductor is wrong. Fix the packet. Do not let them “work it out.”

## 7. Spawn rules

1. Human pastes `WAVE_n` packet into Conductor.  
2. Conductor copies the matching `swarm/agents/{role}.md` into a new subagent (or Cursor custom agent).  
3. Worker prompt = agent file + **only** the inputs listed in the wave packet.  
4. Worker stops when outputs exist and handoff is written.  
5. Conductor updates `PHASE_BOARD.md`.  
6. QA or Conductor ticks the gate. Human Lead may override a gate; workers may not.

Max parallel in one wave: number of **non-overlapping owners**. Phase 3 max 3 (ENV-H, PROP, LIT). Phase 5 max 3 if CHA / GP / SYS own different trees.

## 8. Defect protocol

QA writes `Docs/qa/P{n}_{id}.md`:

- Canon clause violated
- Shot or verb that fails
- Expected vs found
- Owner to fix
- Blocker? (yes = phase cannot close)

Conductor assigns a **fix-only** task to the owner. No new scope on a fix ticket.

## 9. Token and context discipline

Worker context:

- Role card
- Canon slices listed in the packet (not the whole brief unless CND / DES / AD)
- Current phase board row
- Input artifact paths

Do not paste prior worker chat. Do not paste Unreal marketplace essays. Do not let workers renegotiate moon size, resource list, or map topology.

## 10. Definition of a living swarm

The swarm is running correctly when:

- PHASE_BOARD has a current phase and named owners
- Every completed task has a handoff file
- No two open tasks share a write path
- QA has not been asked to “just approve”
- Human Lead only enters at gates and cut decisions
