# Build policy — Safe-Build vs Build-HomeWorld.bat

**For agents:** Always use **`.\Tools\Safe-Build.ps1`** from the repo root when compiling C++.

## Relationship

```
Tools/Safe-Build.ps1
  ├─ Close Unreal Editor if running (graceful, then force if needed)
  ├─ Invoke Build-HomeWorld.bat
  └─ Retry once on Editor-related failure (Live Coding, exit code 6)
```

| Entry | Who uses it | Notes |
|-------|-------------|-------|
| **`Tools/Safe-Build.ps1`** | Agents, automation, orchestrator | **Canonical** for autonomous builds |
| **`Build-HomeWorld.bat`** | Humans with Editor already closed | Low-level wrapper; Safe-Build calls this internally |
| **`py Content/Python/run_automation_cycle.py`** | Full build → scripts → UE automation cycle | Applies same Editor-close protocol when build is enabled |

## Options

- **`-LaunchEditorAfter`** (Safe-Build): After success, relaunch Editor and wait for MCP port 55557 (requires `UE_EDITOR`).

## References

- [EDITOR_BUILD_PROTOCOL.md](../Editor/EDITOR_BUILD_PROTOCOL.md) — full protocol
- [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) — Live Coding / exit code 6
- [AGENTS.md](../../AGENTS.md) — agent command list
