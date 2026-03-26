# Refine rules from runs (Refiner agent)

Run the **Refiner** role from the agent company: read run history and errors, update rules and strategy so the same failures don't recur.

**What to do:** From project root, run:

```powershell
.\Tools\Run-RefinerAgent.ps1
```

Optionally with `-Model <name>` if you want a specific model. The Refiner reads Saved/Logs/agent_run_history.ndjson, Saved/Logs/automation_errors.log, and (if present) Saved/Logs/automation_loop_breaker_report.md, then updates docs/KNOWN_ERRORS.md, .cursor/rules, AGENTS.md, or workflow docs as needed.

See docs/Automation/AGENT_COMPANY.md (roles and accountability) and docs/Automation/AUTOMATION_REFINEMENT.md (how run history is used). When run history or the Guardian report mentions an automation gap (Level Streaming, State Tree, PCG), the Refiner suggests a follow-up task to implement a solution or add GUI automation; see docs/Automation/AUTOMATION_GAPS.md and .cursor/skills/automation-gap-solutions/SKILL.md.
