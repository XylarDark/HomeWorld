# HR3-A Windows Agent Exec — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR3-A |
| **Status** | **APPROVED** — Lead Luke Thompson, **`APPROVE HR3-A`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE HR3-A`** — **APPROVED**; unlocks **HR3-B** |
| **Spec** | [15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) § HR3-A |
| **Date** | 2026-09-17 ET |

## Summary

Windows Shell routing to **DESKTOP-21CT3H0** is **proven for Conductor parent agents only**. Cursor **Task executor** subagents **cannot** route Shell to DESKTOP — they lack `ListMachines`, `Shell` with `machineId`, `CopyToBox`, and `CallDynamicTool`. The **canonical happy path** is: **Conductor parent** → `ListMachines` → `machineId` → Shell on **DESKTOP-21CT3H0**. Cloud agents remain Linux-only; never claim Windows Shell from cloud VM.

**Do not assign DESKTOP Shell work to Task executors.** Treat prior VP-A executor claims (Shell+machineId ran on Linux `cursor` host) as **unreliable / unsupported**.

---

## Proven facts (2026-09-17 ET) — verbatim

### Happy path (PASS)

Conductor **parent** agent (Grok Bot / HomeWorld):

- `ListMachines` → `machineId=929b6d1e-df75-4a84-b73c-a171c6eb877c` label **DESKTOP-21CT3H0** connected=true
- Shell with `machineId` in tool args → `hostname` = **DESKTOP-21CT3H0**, user `desktop-21ct3h0\user`
- UnrealMCP TCP 55557 reachable from that host; Editor Python via staging helper `C:\Users\User\HomeWorldStaging\hw_unreal_mcp_client.py`
- CopyFromBox to `C:\dev\HomeWorld\**` is **refused** (outside local-exec root); use `C:\Users\User\HomeWorldStaging\` then Shell on machine, or write via machine Shell into repo paths

### Failure mode (FAIL — executors)

Cursor **Task executor** subagents:

- Do **not** expose CallDynamicTool / Shell / ListMachines / CopyToBox for Windows routing
- HR3-A proof (2026-09-17): executor reported CallDynamicTool unavailable; hostname never run; no ListMachines/CopyToBox
- Earlier VP-A executor: claimed Shell+machineId still ran on Linux `cursor` host — treat as **unreliable / unsupported** for DESKTOP

### Cloud agents

Linux VM — no UE/MCP — unchanged. Never claim Windows Shell.

---

## Canonical machine identity

| Field | Value |
|-------|-------|
| **Hostname** | DESKTOP-21CT3H0 |
| **machineId** | `929b6d1e-df75-4a84-b73c-a171c6eb877c` |
| **Self-hosted runner labels** | `self-hosted`, `windows`, `ue58` |
| **MCP port** | TCP **55557** (UnrealMCP) |
| **Repo path (Windows)** | `C:\dev\HomeWorld\` |
| **Staging path (CopyFromBox safe)** | `C:\Users\User\HomeWorldStaging\` |
| **MCP staging helper** | `C:\Users\User\HomeWorldStaging\hw_unreal_mcp_client.py` |

---

## Proof excerpts (Conductor parent — PASS)

### ListMachines

```json
{
  "machines": [
    {
      "machineId": "929b6d1e-df75-4a84-b73c-a171c6eb877c",
      "label": "DESKTOP-21CT3H0",
      "connected": true
    }
  ]
}
```

### Shell with machineId → hostname

**Tool args:**

```json
{
  "machineId": "929b6d1e-df75-4a84-b73c-a171c6eb877c",
  "command": "hostname"
}
```

**Output:**

```
DESKTOP-21CT3H0
```

**User context (same session):** `desktop-21ct3h0\user`

### MCP reachability (DESKTOP)

- UnrealMCP TCP **55557** reachable from DESKTOP-21CT3H0 when Editor is open
- Editor Python via `C:\Users\User\HomeWorldStaging\hw_unreal_mcp_client.py` (staging helper — repo path may be outside local-exec root for CopyFromBox)

### CopyFromBox / local-exec root constraint

- **Refused:** `CopyFromBox` → `C:\dev\HomeWorld\**` (outside local-exec root)
- **Workaround (happy path):** stage to `C:\Users\User\HomeWorldStaging\`, then Shell on machine; or write directly via machine Shell into repo paths under `C:\dev\HomeWorld\`

---

## Failure mode excerpts (Task executor — FAIL)

HR3-A proof session (2026-09-17):

| Check | Executor result |
|-------|-----------------|
| `CallDynamicTool` | **Unavailable** — tool not exposed to subagent |
| `ListMachines` | **Not available** |
| `Shell` with `machineId` | **Not available** (or runs on Linux `cursor` host — unreliable) |
| `CopyToBox` / `CopyFromBox` | **Not available** |
| `hostname` on DESKTOP | **Never run** — no routing proof |

**Prior VP-A executor incident:** agent claimed Shell+machineId executed but output indicated Linux `cursor` host — **do not treat as DESKTOP evidence**.

---

## Happy path checklist (Conductor parent only)

Use this checklist before filing DESKTOP evidence or running PIE/MCP scripts. **Conductor parent agent session required** — not Task executor, not cloud agent.

| Step | Action | Pass criterion |
|------|--------|----------------|
| 1 | Confirm session is **Conductor parent** (not Task executor subagent) | Parent has `ListMachines`, `Shell`, `CopyToBox` / `CopyFromBox` |
| 2 | `ListMachines` | `DESKTOP-21CT3H0` present, `connected=true`, note `machineId` |
| 3 | `Shell` with `machineId` → `hostname` | Output **`DESKTOP-21CT3H0`** |
| 4 | Verify user context if needed | e.g. `whoami` → `desktop-21ct3h0\user` |
| 5 | Stage files if needed | Use `C:\Users\User\HomeWorldStaging\` — not CopyFromBox to `C:\dev\HomeWorld\**` |
| 6 | MCP check | TCP 55557 reachable; Editor open; helper at staging path if needed |
| 7 | Run Editor Python / PIE | Via MCP or staging helper on DESKTOP only |
| 8 | File handoff | Host, machineId, command excerpts, pass/fail table |

**DO NOT:**

- [ ] Assign DESKTOP Shell to **Task executor** subagents
- [ ] Claim Windows Shell from **cloud agent** Linux VM
- [ ] Use CopyFromBox directly to `C:\dev\HomeWorld\**` without staging workaround
- [ ] Accept executor hostname output without verifying **DESKTOP-21CT3H0**

---

## Owner matrix

| Actor | DESKTOP Shell | UE / MCP | Role |
|-------|---------------|----------|------|
| **Conductor parent** | **YES** — canonical lane | **YES** (when Editor open on DESKTOP) | DESKTOP owner for PIE/MCP evidence |
| **Task executor subagent** | **NO** — tools unavailable / unreliable | **NO** | Docs/C++ on cloud or parent-delegated paths only |
| **Cloud agent (Linux VM)** | **NO** | **NO** | Docs, C++, PRs — hand off to Conductor parent after merge |

---

## Cross-links

| Doc | Purpose |
|-----|---------|
| [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md) | § Canonical Windows agent lane; cloud → CI → DESKTOP flow |
| [CLOUD_AGENT_PACKET.md](../../swarm/CLOUD_AGENT_PACKET.md) | DESKTOP owner = Conductor parent; cloud returns after merge |
| [MCP_SETUP.md](../../docs/Setup/MCP_SETUP.md) | MCP green dot, port 55557 |
| [VP_A_PIE.md](VP_A_PIE.md) | Prior DESKTOP PIE evidence (Conductor parent path) |
| [15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) | HR3-A done criteria and gate |

---

## Done criteria (Docs/15 § HR3-A)

- [x] Runbook proves **parent** → `machineId` → hostname **DESKTOP-21CT3H0**
- [x] Known failure modes documented; happy path = **Conductor parent** (executors explicitly FAIL)
- [x] CLOUD_AGENT_PACKET / WINDOWS_BRIDGE cross-links updated
- [x] Handoff includes command output excerpts (hostname, machineId, tool availability)

---

## Gate

Lead **`APPROVE HR3-A`** — **APPROVED** (Luke Thompson, 2026-09-17 ET). HR3-A **COMPLETE**. **HR3-B UNLOCKED / IN PROGRESS** — UE preflight fails loud ([15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) § HR3-B). **VP-B remains PARKED** pending HR3.

## Prior stamp

Lead **`APPROVE HR3 STRATEGY`** (Luke Thompson, 2026-09-17 ET) — HR3 strategy **APPROVED**; HR3-A **UNLOCKED**. Evidence merge `27a1af4` (PR #58).

## Stamp

Lead **`APPROVE HR3-A`** (Luke Thompson, 2026-09-17 ET) — HR3-A **APPROVED / COMPLETE** (Conductor parent→DESKTOP lane proven; Task executors FAIL). **HR3-B UNLOCKED / IN PROGRESS** — Lead **`APPROVE HR3-B`** before implementation PR. **VP-B still PARKED**.
