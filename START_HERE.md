# START HERE

> **Repo layout:** This tree lives inside the **HomeWorld UE 5.7** repo. MVP swarm canon is under **`Docs/`** (capital D). Unreal project docs stay in **`docs/`** (lowercase). See [Docs/README.md](Docs/README.md) — do not merge the two trees.

## Human Lead (you)

You own **steer**, **taste**, and **test** for the swarm. Agents execute and **alert + recommend** at gates — they do not invent your approvals. See [docs/human-use/OWNERSHIP.md](docs/human-use/OWNERSHIP.md).

| You type | Meaning |
|---|---|
| `APPROVE P0` … `APPROVE P7` | Close a phase gate (Test job — only after checklist + artifact paths exist) |
| `FALLBACK FLIGHT` | Arm scripted glide + portal cut (Steer) |
| `FIX {owner} {id}` | Assign a fix-only defect ticket |
| `STOP` | Halt the swarm |

## Boot the swarm

1. Use this repository root (Unreal project + swarm kit).
2. Open a **Conductor** chat (not a flat group of all specialists).
3. Attach this whole folder to the chat.
4. Paste [HOMEWORLD_MASTER_PROMPT.md](HOMEWORLD_MASTER_PROMPT.md) as the first message  
   (shorter option: [swarm/CONDUCTOR_KICKOFF_PROMPT.md](swarm/CONDUCTOR_KICKOFF_PROMPT.md)).
5. Conductor runs waves; you approve gates when evidence is on disk.

## On-demand specialists (not always loaded)

Swarm role cards live in [`.cursor/agents/`](.cursor/agents/) (copied from [swarm/agents/](swarm/agents/)). Conductor spawns **one specialist per task** with thin context (role card + wave packet inputs only). They are **not** the UE automation company (Developer / Fixer / Guardian in [docs/Automation/AGENT_COMPANY.md](docs/Automation/AGENT_COMPANY.md) unless you explicitly invoke that loop.

## Session continuity (swarm)

At **session start:** read [docs/SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md) and [swarm/PHASE_BOARD.md](swarm/PHASE_BOARD.md) — not the full [docs/SESSION_LOG.md](docs/SESSION_LOG.md) unless debugging a past incident.

At **session end:** Conductor appends SESSION_SUMMARY and updates PHASE_BOARD when status changes.

**Cloud agents:** [swarm/CLOUD_AGENT_PACKET.md](swarm/CLOUD_AGENT_PACKET.md) — no MCP / no Safe-Build on cloud VM; Windows handoff via [docs/Setup/WINDOWS_BRIDGE.md](docs/Setup/WINDOWS_BRIDGE.md).

## Key paths

| Path | Role |
|---|---|
| [refs/keyart_homestead_night.jpg](refs/keyart_homestead_night.jpg) | Key art north star |
| [HOMEWORLD_MVP_SWARM_BRIEF.md](HOMEWORLD_MVP_SWARM_BRIEF.md) | Game canon |
| [swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) | Process — Human Use, evidence gates, git safety, KNOWN_ERRORS |
| [swarm/PHASE_BOARD.md](swarm/PHASE_BOARD.md) | Live status (Conductor writes) |
| [docs/SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md) | Rolling last-30-days swarm memory |
| [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md) | Record real failures |
| [docs/Automation/AUTOMATION_GAPS.md](docs/Automation/AUTOMATION_GAPS.md) | Log automation impossibilities |
