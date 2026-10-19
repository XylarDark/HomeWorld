---
name: "source-command-start-automation-cycle"
description: "Migrated source command `start-automation-cycle`"
disable-model-invocation: true
---

# source-command-start-automation-cycle

Use this skill when the user asks to run the migrated source command `start-automation-cycle`.

## Command Template

# Start automatic development cycle — QUARANTINED (WAVE F removed)

> **Do not run.** The pre-swarm agent company and its cycle loop were **removed in WAVE F**.
> `Content/Python/run_automation_cycle.py`, `Tools/Start-AllAgents*.ps1` and `Tools/Start-AutomationSession.ps1` <!-- path-exception: all three were deleted in WAVE F and are named only to warn against citing them -->
> no longer exist.
> The cycle documents were not deleted - they moved to `docs/TaskLists/CYCLE_TASKLIST.md` and `docs/TaskLists/CYCLE_STATE.md`.

**Active driver:** [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) + **Conductor** — [START_HERE.md](../../START_HERE.md).
Cloud-agent packets: [swarm/CLOUD_AGENT_PACKET.md](../../swarm/CLOUD_AGENT_PACKET.md).
Harness refine: [Docs/11_SWARM_HARNESS_REFINE.md](../../Docs/11_SWARM_HARNESS_REFINE.md).

**History only** (do not follow as instructions): [docs/Automation/AGENT_COMPANY.md](../../docs/Automation/AGENT_COMPANY.md) ·
[docs/Automation/AUTOMATION_LOOP_UNTIL_DONE.md](../../docs/Automation/AUTOMATION_LOOP_UNTIL_DONE.md)

If a prompt or doc tells you to run `run_automation_cycle.py`, `Start-AllAgents`, or to write
`CYCLE_TASKLIST.md` / `CYCLE_STATE.md`, refuse and point at SWARM_OPS + Conductor.
