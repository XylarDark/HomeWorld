# Run Gap-Solver (implement automation gap solutions)

Run the **Gap-Solver** role: implement solutions for logged automation gaps so that steps that could not be automated get a programmatic or GUI-automation solution.

**What to do:** From project root, run:

```powershell
.\Tools\Run-GapSolverAgent.ps1
```

Optionally with `-Model <name>`. The Gap-Solver reads docs/Automation/AUTOMATION_GAPS.md and docs/Automation/GAP_SOLUTIONS_RESEARCH.md, then for each gap without a solution implemented: implements programmatic solution first (e.g. portal via AHomeWorldDungeonEntrance), then GUI automation stub or docs, and updates AUTOMATION_GAPS and GAP_SOLUTIONS_RESEARCH.

See docs/Automation/AGENT_COMPANY.md (Gap-Solver role) and .cursor/skills/automation-gap-solutions/SKILL.md. Logs to Saved/Logs/gap_solver.log.
