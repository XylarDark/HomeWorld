# Development environment matrix

**When to use this:** Pin what a healthy HomeWorld machine looks like before onboarding or when debugging “works on my machine.” For step-by-step first setup, start with [SETUP.md](../SETUP.md).

**Related:** [CI_SETUP.md](CI_SETUP.md) (runner parity), [MCP_SETUP.md](MCP_SETUP.md), [AUTOMATION_READINESS.md](../Automation/AUTOMATION_READINESS.md), [EDITOR_BUILD_PROTOCOL.md](../Editor/EDITOR_BUILD_PROTOCOL.md).

---

## Pinned toolchain (local Windows)

| Component | Expected | Notes |
|-----------|----------|--------|
| **OS** | Windows 10/11 x64 | Primary dev platform per AGENTS.md |
| **Unreal Engine** | **5.7.x** only | Install via Epic Launcher; e.g. `C:\Program Files\Epic Games\UE_5.7`. Stay on a **team-agreed 5.7.x patch** (e.g. 5.7.3); do not move to 5.8+ without a project decision. |
| **Visual Studio** | 2022 (2019 acceptable) | Workload: **Desktop development with C++**. Include **Windows 10/11 SDK** matching UE’s requirements. Same baseline as [CI_SETUP.md](CI_SETUP.md) self-hosted runner. |
| **Git** | Current | **Git LFS** installed; run `git lfs install` after clone. |
| **Python (host)** | 3.10+ | Used by `uv` / Unreal MCP server per [MCP_SETUP.md](MCP_SETUP.md). On Windows, use the same `py` / `python` you use for `Content/Python` scripts and automation. |
| **uv** | 0.10+ | Installed by `Setup-MCP.bat` for the MCP Python server. |

**Verify after setup**

1. Generate Visual Studio project files from `HomeWorld.uproject` (right-click → Generate Visual Studio project files, or equivalent).
2. From repo root: `.\Tools\Safe-Build.ps1` (closes Editor if needed; see EDITOR_BUILD_PROTOCOL).
3. If you use the automation loop: `.\Tools\Check-AutomationPrereqs.ps1`.

---

## Environment variables

| Variable | Required for | Example / note |
|----------|----------------|----------------|
| **`UE_EDITOR`** | Automation loop, `run_automation_cycle.py` launch/wait, optional CI tests | Full path to `UnrealEditor.exe`, e.g. `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe`. See [AUTOMATION_READINESS.md](../Automation/AUTOMATION_READINESS.md). |
| **`CURSOR_API_KEY`** | Headless Cursor Agent CLI | Alternative to `agent login` for scripted runs. |
| **`UE_ENGINE`** | CI build script default | [ci.yml](../../.github/workflows/ci.yml) defaults to `C:\Program Files\Epic Games\UE_5.7` if unset on the runner. |

Never use `Test-Path` on `UE_EDITOR` without a null check; see [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

---

## C++ language service (Cursor / VS Code family)

**Primary (recommended):** **MSVC** toolchain + **Microsoft C/C++** extension (`ms-vscode.cpptools`) for IntelliSense and debugging on Windows, aligned with Unreal’s Windows build.

**Optional trial:** [Unreal Clangd](https://github.com/boocs/unreal-clangd) — clangd-based completion/navigation for UE 5.2+. Try it if MSVC IntelliSense is slow or inaccurate for `Source/HomeWorld`; uninstall or disable duplicate providers to avoid conflicts.

**Marketplace friction:** Some Cursor users install Microsoft’s C/C++ extension via a downloaded **.vsix** or [Open VSX](https://open-vsx.org/) if the default marketplace flow fails. See also third-party writeups on VS Code marketplace terms for non-Microsoft editors.

**Team decision log:** Default stance — **MSVC + C/C++ extension**; document here if the team standardizes on clangd for all UE work.

---

## Python and CI

- **GitHub validate.yml** runs `python3` on Ubuntu (`ruff check Content/Python/`). Local Windows developers should keep Editor scripts and automation behavior consistent with Ruff-clean Python where possible.
- Optional repo root **`.python-version`** (e.g. `3.11`) can align local `pyenv`/similar; not required if everyone uses the same documented minimum (3.10+).

---

## Cursor Marketplace and plugins (decision log)

Repo policy already uses:

| Item | Status | Note |
|------|--------|------|
| **Parallel** | Adopted | Web search / extract / research; see SETUP.md and `.cursor/rules/11-parallel-plugin.mdc` |
| **Compound Engineering** | Adopted | Workflows, review, skills; see `.cursor/rules/10-compound-engineering.mdc` |

**Optional — install only if the product is already in your stack:**

| Item | Status | When to adopt |
|------|--------|----------------|
| **Sourcegraph** | Not required | Large-repo code search and agent integration beyond local tools |
| **Runlayer** | Not required | Many MCP servers; governance / audit / secrets posture |
| **Linear / ClickUp** | Not required | Issues live outside markdown task lists |
| **Figma** | Not required | Frequent design ↔ implementation sync in Cursor |
| **Cursor hosted automations** (CI fix, Slack digests, etc.) | Not required | Supplement to [Tools/](../../Tools/) PowerShell automation, not a replacement |

Update this table when the team adopts or drops a plugin.

---

## MCP and Cursor Agent CLI (audit checklist)

Use this when onboarding a machine or after moving the repo.

### `.cursor/mcp.json`

- **Expected:** Single server **`unrealMCP`** with command `uv`, args `--directory` → `C:\tools\unreal-mcp\Python`, `run`, `unreal_mcp_server.py` (path may differ if tools live elsewhere; keep it in sync with [MCP_SETUP.md](MCP_SETUP.md)).
- **Editor:** UnrealMCP plugin enabled; TCP **55557** when Editor runs.
- **Cursor:** Restart Cursor after changing `mcp.json` or after first MCP install.

### Cursor Agent CLI (automation loop)

- `agent --version` works; PATH updated after install.
- Auth: `agent login` **or** `CURSOR_API_KEY` for headless use.
- Full checklist: [AUTOMATION_READINESS.md](../Automation/AUTOMATION_READINESS.md).

### Unattended automation

If more MCP servers are added later, consider documenting which are safe for unattended loops vs. interactive-only (optional: external governance tools mentioned in the marketplace table above).

---

## Reference links

- [SETUP.md](../SETUP.md) — Onboarding steps  
- [CURSOR_DEV.md](CURSOR_DEV.md) — Rules and Cursor workflow  
- [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) — Build, MCP, and Python pitfalls  
