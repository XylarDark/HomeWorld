# MCP Setup – Cursor to Unreal Editor

This guide gets the **MCP (Model Context Protocol) bridge** working so Cursor can talk to the Unreal Editor. When it’s set up, the AI agent can create assets, spawn actors, configure Blueprints, and run Python scripts in the Editor from Cursor.

**You will:** Run one batch file (recommended) or follow the manual steps. Then build the project, open the Editor, and restart Cursor so the connection appears.

---

## Quick start (recommended)

From the project root, run:

```
Setup-MCP.bat
```

This installs `uv`, clones the MCP server, installs Python dependencies, copies the UE plugin, and creates `.cursor/mcp.json`. When it finishes: run **`.\Tools\Safe-Build.ps1`** (preferred; see [BUILD_POLICY.md](BUILD_POLICY.md)), open the Editor, and **restart Cursor**. You should see the MCP connection (green dot) when the Editor is running.

---

## Installed configuration (reference)

| Component | Location |
|-----------|----------|
| Python MCP server | `C:\tools\unreal-mcp\Python\unreal_mcp_server.py` |
| UE plugin (UnrealMCP) | `Plugins\UnrealMCP\` (gitignored; copied from the cloned repo) |
| Cursor config | `.cursor\mcp.json` |
| Cursor rule | `.cursor\rules\09-mcp-workflow.mdc` |

The plugin auto-starts a TCP listener on **port 55557** when the Editor opens. Cursor launches the Python MCP server via the `uv run` command defined in `.cursor/mcp.json`.

---

## Configuration audit (HomeWorld)

Use this when onboarding a machine or after changing install paths. Full matrix: [DEV_ENV_MATRIX.md](DEV_ENV_MATRIX.md).

| Check | Expected |
|--------|----------|
| **`.cursor/mcp.json`** | Live config (gitignored). Copy from [`.cursor/mcp.json.example`](../../.cursor/mcp.json.example). Servers: **`unrealMCP`** (`uv` + `--directory` → folder with `unreal_mcp_server.py`, default `C:\tools\unreal-mcp\Python`) and **`mixar`** (`cmd /c Tools\mixar-mcp.cmd` on Windows). |
| **Editor** | HomeWorld opens with **UnrealMCP** enabled; Output Log shows the plugin listening on **55557**. |
| **Mixar** (optional) | Mixar at `C:\Program Files\Mixar\mixar.exe` (Blender 4.2.2 fork) with the Lab MCP add-on enabled and online access permitted. Start it with `.\Tools\Start-MixarMcp.ps1` (default `localhost:9876`). See [Mixar MCP](#mixar-mcp-official-blender-lab-add-on-served-by-mixar) below. |
| **Cursor** | After edits to `mcp.json`, fully quit and relaunch Cursor; **Settings → Tools & MCP** shows healthy connections. |
| **Cursor Agent CLI** (automation loop) | `agent --version` works; `agent login` or **`CURSOR_API_KEY`** set. See [AUTOMATION_READINESS.md](../Automation/AUTOMATION_READINESS.md). |

---

## Manual setup from scratch

Follow these steps if the batch script fails or you need to customize the installation.

### 1. Install prerequisites

```powershell
# Install uv (Astral package manager)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to current session PATH
$env:Path = "C:\Users\$env:USERNAME\.local\bin;$env:Path"

# Verify
uv --version        # expects 0.10+
python --version     # expects 3.10+
```

### 2. Clone and install the Python server

```powershell
git clone https://github.com/chongdashu/unreal-mcp.git C:\tools\unreal-mcp
cd C:\tools\unreal-mcp\Python
uv sync
```

Verify the module loads:

```powershell
uv --directory C:\tools\unreal-mcp\Python run python -c "import unreal_mcp_server; print('OK')"
```

### 3. Install the UE plugin

Copy the plugin into the project:

```powershell
Copy-Item -Path "C:\tools\unreal-mcp\MCPGameProject\Plugins\UnrealMCP" `
          -Destination "c:\dev\HomeWorld\Plugins\UnrealMCP" -Recurse -Force
```

The plugin is already listed in `HomeWorld.uproject`:

```json
{"Name": "UnrealMCP", "Enabled": true}
```

Restart the Editor. The plugin compiles on first launch and starts the TCP listener on port 55557. Check Output Log for `UnrealMCP: Server started`.

### 4. Cursor configuration

Live config is **gitignored**. Copy the example, then edit machine paths:

```powershell
Copy-Item .cursor\mcp.json.example .cursor\mcp.json
# Edit .cursor\mcp.json: set unrealMCP --directory to your unreal-mcp Python folder
```

Example shape (see [`.cursor/mcp.json.example`](../../.cursor/mcp.json.example)):

```json
{
  "mcpServers": {
    "unrealMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\tools\\unreal-mcp\\Python",
        "run",
        "unreal_mcp_server.py"
      ]
    },
    "mixar": {
      "command": "cmd",
      "args": ["/c", "C:\\dev\\HomeWorld\\Tools\\mixar-mcp.cmd"]
    }
  }
}
```

After creating or modifying this file, **fully quit and relaunch Cursor**. Hygiene notes: [UserHarness MCP hygiene](../../UserHarness/docs/guides/mcp-hygiene.md) (never commit secrets; prefer `${env:NAME}`).

### 5. Verify

1. Open the HomeWorld project in Unreal Editor (plugin starts automatically).
2. In Cursor, go to **Settings > Tools & MCP**. Look for a green dot next to **unrealMCP**.
3. Test by asking Cursor to "list all actors in the current level" or "spawn a cube at origin".

---

## Mixar MCP (official Blender Lab add-on, served by Mixar)

**Mixar is the default 3D tool** (developer decision 2026-10-05). Mixar is a **Blender 4.2.2 fork** from mixar.app, so existing `bpy` scripts, the FBX/GLTF exporters, and the official Blender Lab MCP add-on all work unchanged. Vanilla Blender 4.4 remains installed but is no longer the default.

**Mixar misreports its version, so confirm which app you are talking to before trusting anything:**

| Signal | Value |
|--------|-------|
| `mixar.exe --version` | **`Blender 4.2.2`** — the real base version |
| `bpy.app.binary_path` | `C:\Program Files\Mixar\mixar.exe` — the reliable identifier |
| `bpy.app.version` | `(5, 2, 0)` — **a compatibility spoof**, not the real version |
| `bpy.app.version_string` | `4.2.2` — the Mixar app version |
| Executable name | `mixar.exe`, **not** `blender.exe` |

The `(5, 2, 0)` tuple exists so extensions that require Blender ≥5.1 install and run; do not reason "Mixar is a 5.2 fork" from it. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for the full list.

> **`.blend` caveat:** Mixar writes a 4.2-era file. Opening a `.blend` authored by Blender 5.x logs `WARNING File written by newer Blender binary, expect loss of data!`. Treat `.blend` as write-once from its authoring app and export FBX/GLB from Mixar rather than open-and-resaving.

HomeWorld targets the **official** Blender Lab MCP stack ([blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/)), not the community PyPI package `uvx blender-mcp` (ahujasid). Both default to port **9876**, but the wire protocols differ. Pointing the client at the PyPI package while the Lab add-on serves the socket leaves the client on **Connecting** forever (TCP connects; handshake never completes).

### Prerequisites

- Mixar at `C:\Program Files\Mixar\mixar.exe`
- Lab **MCP** extension installed and enabled. It lives in Mixar's own config namespace — note the **doubled** `Mixar`: `%APPDATA%\Mixar\Mixar\5.2\extensions\user_default\mcp`
- **Online access** enabled in Mixar (Preferences → System). The add-on refuses to start without network permission. Already set on this machine.
- Official MCP client binary installed once:

```powershell
uv tool install "git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp"
# resolves to: %USERPROFILE%\.local\bin\blender-mcp.exe
```

### Start the server

**Two ways to serve MCP, and they share port 9876.** Because the Lab add-on is enabled persistently, **any Mixar you launch — including the GUI — auto-starts its MCP socket.** So if Mixar is already open, there is nothing to start.

| Mode | How | Notes |
|------|-----|-------|
| GUI | Just open Mixar | Serves automatically on launch. What a human drives while generating assets. |
| Headless | `.\Tools\Start-MixarMcp.ps1` | No window. What an agent should use, so work does not depend on a human session. |

```powershell
.\Tools\Start-MixarMcp.ps1            # launch, block until the port is reachable
.\Tools\Start-MixarMcp.ps1 -Status    # who is serving? GUI or headless, and which pid
.\Tools\Start-MixarMcp.ps1 -Stop      # stop the headless server only
```

Under the hood the headless path is `mixar.exe --background --command blender_mcp --host 127.0.0.1 --port 9876`.

- `-Stop` **will not kill a GUI Mixar**, even one holding unsaved work. It selects by command line (`blender_mcp`), never by socket ownership alone, because the GUI holds the same port. If only a GUI is serving, it says so and leaves it alone — close Mixar yourself.
- The add-on registers a headless CLI command named **`blender_mcp`**. Passing its module id `bl_ext.user_default.mcp` fails with `Unrecognized command`.
- **Do not use the `blender_*.cmd` files shipped in the Mixar install.** They are stock Blender launchers that invoke `"%~dp0\blender"`, and no such file exists in a Mixar install, so every one of them fails. Use `Tools\Start-MixarMcp.ps1`.
- `Start-MixarMcp.ps1` decides liveness by opening a TCP connection, not by `Get-NetTCPConnection`, which was observed flapping between two different owning pids while a stale server was present.

### Connect

1. Start the server (above).
2. The client is `Tools/mixar-mcp.cmd`, a thin wrapper that sets `BLENDER_PATH=C:\Program Files\Mixar\mixar.exe` then runs `blender-mcp.exe`. `blender-mcp` resolves the app executable from `BLENDER_PATH` and otherwise falls back to `blender` on `PATH`, which would quietly open vanilla Blender. `.cursor/mcp.json` and `opencode.json` both point at this wrapper under the server name **`mixar`** (renamed from `blender` on 2026-10-05, so the tool namespace is `mixar.*`).
3. Toggle **mixar** off/on in **Settings → Tools & MCP** (or fully quit the host from the tray) after config changes.
4. Confirm green; only one MCP client should talk to Mixar at a time.

### Asset pipeline with both MCPs

1. **Mixar MCP** — clean mesh, apply transforms, export FBX/GLB with the HomeWorld preset to `AssetCreation/Exports/<Category>/` (helper: `AssetCreation/Blender/export_to_asset_creation.py`, still valid: it is a plain `bpy` script).
2. **unrealMCP** — `execute_python_script("batch_import_asset_creation.py")` to import into `/Game/HomeWorld/...`.

Full preset and style: [AssetCreation/STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md). Workflow overview: [AssetCreation/README.md](../../AssetCreation/README.md).

### Troubleshooting (Mixar)

| Issue | Fix |
|-------|-----|
| Cursor stuck **Connecting** | You are almost certainly running **PyPI `uvx blender-mcp`** against the **Lab add-on**. Use `Tools/mixar-mcp.cmd`, which launches the Lab binary. Kill leftover `blender-mcp` processes, `.\Tools\Start-MixarMcp.ps1 -Stop`, toggle the client server. |
| `Unrecognized command: "bl_ext.user_default.mcp"` | The `--command` name is **`blender_mcp`**, not the extension module id. |
| `Error: Online access must be enabled in the system preferences` | Set **Preferences → System → Online access** in Mixar, or pass `--online-mode`. `bpy.app.online_access_override` is **not writable** from Python; use the preference or the flag. |
| A `blender_*.cmd` launcher exits immediately | Expected — the shipped launchers are broken stock Blender scripts. Use `Tools\Start-MixarMcp.ps1`. |
| Port 9876 reachable but reports the wrong pid | `Get-NetTCPConnection` is unreliable here. Use `Tools/Start-MixarMcp.ps1 -Status`, which probes with a real TCP connect. |
| TCP 9876 listens but tools hang | Confirm you are on Lab protocol (null-byte JSON). A quick probe that returns scene objects means the add-on is healthy; the client-side binary was wrong. |
| `spawn … ENOENT` | Use `Tools/mixar-mcp.cmd` (full paths to both Mixar and `blender-mcp.exe`). |
| Two clients fighting | Quit the other MCP host; only one client to port 9876 |

---

## Fallback: UnrealMCPBridge

If UnrealMCP fails to compile against UE 5.7, use `appleweed/UnrealMCPBridge` instead. It proxies to UE's built-in Python API via a socket bridge with no C++ plugin compilation required.

### Install

Available on the [Fab marketplace](https://www.fab.com/listings/0167ac03-47b5-4a08-b68f-5d54ab7b208e) or from GitHub:

```powershell
git clone https://github.com/appleweed/UnrealMCPBridge.git C:\tools\UnrealMCPBridge
pip install mcp
```

### Configure Cursor

Update `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "unrealMCP": {
      "command": "python",
      "args": ["C:\\tools\\UnrealMCPBridge\\MCPClient\\unreal_mcp_client.py"]
    }
  }
}
```

In the Editor, click **Start MCP Bridge** in the toolbar (port 9000).

---

## Capabilities

| Capability | UnrealMCP | UnrealMCPBridge |
|---|---|---|
| Actor CRUD (create, transform, delete) | Yes | Yes |
| Blueprint creation and component setup | Yes | Yes |
| Blueprint node graph wiring | Yes | No |
| Any `unreal.*` Python call | No (curated tools) | Yes |
| PCG graph manipulation | Via Python | Via Python |
| Viewport control | Yes | No |
| AnimGraph editing | No | No |

## MCP-first workflow

When connected, the AI agent follows `.cursor/rules/09-mcp-workflow.mdc`:

1. **MCP tools first** for live Editor manipulation
2. **Python scripts** for batch/repeatable operations (saved in `Content/Python/`)
3. **Manual instructions** only when MCP and Python cannot accomplish the task

## External AI / LLM-generated scripts

External LLMs can generate Python that is then run via MCP (`execute_python_script`) or via the Editor (Tools → Execute Python Script). Conventions, example prompts, and a sample script are in [EXTERNAL_AI_AUTOMATION.md](../Automation/EXTERNAL_AI_AUTOMATION.md). Always review generated code before running.

## Troubleshooting

| Issue | Fix |
|---|---|
| MCP tools don't appear in Cursor | Restart Cursor after adding/changing `.cursor/mcp.json`; ensure `uv` is on PATH; copy from `.cursor/mcp.json.example` if the live file is missing |
| "Connection refused" | Ensure the Editor is open with the UnrealMCP plugin enabled; check Output Log for errors |
| Python version error | Requires Python 3.10+; check with `python --version` |
| Plugin compilation failure on UE 5.7 | Switch to UnrealMCPBridge fallback (see above) |
| `uv` not found | Run the install script or add `C:\Users\<user>\.local\bin` to PATH |
| Mixar MCP missing / ENOENT / stuck Connecting | See [Mixar MCP](#mixar-mcp-official-blender-lab-add-on-served-by-mixar); start the server with `.\Tools\Start-MixarMcp.ps1` and use the Lab `blender-mcp.exe` via `Tools/mixar-mcp.cmd`, not PyPI `uvx blender-mcp` |
