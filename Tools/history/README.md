# Tools/history — WAVE F agent company (retired)

These scripts belonged to the pre-swarm **agent company** (Developer / Fixer / Guardian / Refiner) and its
run-until-done loop. That loop was **removed in WAVE F** — see
[../AGENT_COMPANY.md](../AGENT_COMPANY.md) and [../AUTOMATION_LOOP_UNTIL_DONE.md](../AUTOMATION_LOOP_UNTIL_DONE.md)
for the historical design.

They are kept for archaeology only. **Do not run them and do not restore them.**

| Retired script | Role |
| --- | --- |
| `Start-AutomationSession.ps1` | Launch the agent-company session (superseded by `Start-AllAgents.ps1`, also deleted) |
| `Run-AutomationWithCapture.ps1` | Run one loop round with Output-Log capture |
| `Guard-AutomationLoop.ps1` | Retry / same-failure / progress loop guards |
| `Watch-HeartbeatStall.ps1` | Watcher: detect a stalled agent heartbeat, trigger the loop-breaker |
| `Common-Automation.ps1` | Shared helpers for the above |
| `Get-AutomationStatus.ps1` | Report loop state |
| `Update-AutomationStatusLive.ps1` | Write live loop status |
| `Check-AutomationPrereqs.ps1` | Gate: UE_EDITOR, Editor, MCP port before a round |
| `Append-AgentRunRecord.ps1` | Append one NDJSON line to `Saved/Logs/agent_run_history.ndjson` |

**Active driver:** [../../swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) + **Conductor** —
[../../START_HERE.md](../../START_HERE.md).

**Live build/test tooling stays one level up** in `Tools/`: `Safe-Build.ps1` (canonical),
`RunFullBuild.ps1`, `RunTests.ps1`, `Package-AfterClose.ps1`, `CleanProject.ps1`.
