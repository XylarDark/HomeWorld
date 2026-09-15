# MCP Setup – Cursor to Unreal Editor

This guide gets the **MCP (Model Context Protocol) bridge** working so Cursor can talk to the Unreal Editor. When it’s set up, the AI agent can create assets, spawn actors, configure Blueprints, and run Python scripts in the Editor from Cursor.

**You will:** Run one batch file (recommended) or follow the manual steps. Then build the project, open the Editor, and restart Cursor so the connection appears.

---

## Quick start (recommended)

From the project root, run:

```
Setup-MCP.bat
```

This installs `uv`, clones the MCP server, installs Python dependencies, copies the UE plugin, and creates `.cursor/mcp.json`. When it finishes: run **Build-HomeWorld.bat**, open the Editor, and **restart Cursor**. You should see the MCP connection (green dot) when the Editor is running.

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
| **`.cursor/mcp.json`** | Live config (gitignored). Copy from [`.cursor/mcp.json.example`](../../.cursor/mcp.json.example). Servers: **`unrealMCP`** (`uv` + `--directory` → folder with `unreal_mcp_server.py`, default `C:\tools\unreal-mcp\Python`) and **`blender`** (`cmd /c uvx blender-mcp` on Windows). |
| **Editor** | HomeWorld opens with **UnrealMCP** enabled; Output Log shows the plugin listening on **55557**. |
| **Blender** (optional) | Blender 3.0+ with BlenderMCP addon; N-panel **Start MCP Server** (default `localhost:9876`). See [Blender MCP](#blender-mcp-ahujasid) below. |
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
    "blender": {
      "command": "cmd",
      "args": ["/c", "uvx", "blender-mcp"]
    }
  }
}
```

After creating or modifying this file, **fully quit and relaunch Cursor**. Hygiene notes: [DevEnvTemplate MCP hygiene](../../DevEnvTemplate/docs/guides/mcp-hygiene.md) (never commit secrets; prefer `${env:NAME}`).

### 5. Verify

1. Open the HomeWorld project in Unreal Editor (plugin starts automatically).
2. In Cursor, go to **Settings > Tools & MCP**. Look for a green dot next to **unrealMCP**.
3. Test by asking Cursor to "list all actors in the current level" or "spawn a cube at origin".

---

## Blender MCP (official Blender Lab — Blender 5.1+)

HomeWorld targets the **official** Blender Lab MCP stack ([blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/)), not the community PyPI package `uvx blender-mcp` (ahujasid). Both default to port **9876**, but the wire protocols differ. Pointing Cursor at the PyPI package while Blender runs the Lab addon causes Cursor to stay on **Connecting** forever (TCP connects; handshake never completes).

### Prerequisites

- Blender **5.1+** (this machine: Steam Blender 5.2)
- Lab **MCP** extension enabled (`lab_blender_org/mcp`) — Preferences → Extensions
- Official MCP client binary installed once:

```powershell
uv tool install "git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp"
# resolves to: %USERPROFILE%\.local\bin\blender-mcp.exe
```

### Connect

1. In Blender: **Edit → Preferences → Add-ons → MCP** → **Start MCP Bridge Server** (leave running; default `localhost:9876`). Enable **Online Access** if Blender prompts for it.
2. Cursor `.cursor/mcp.json` `blender` entry must launch the Lab binary, e.g. `"command": "C:\\Users\\<user>\\.local\\bin\\blender-mcp.exe"` (see `.cursor/mcp.json.example`).
3. Toggle **blender** off/on in **Settings → Tools & MCP** (or fully quit Cursor from the tray) after config changes.
4. Confirm green; only one MCP client should talk to Blender at a time.

### Asset pipeline with both MCPs

1. **Blender MCP** — clean mesh, apply transforms, export FBX/GLB with the HomeWorld preset to `AssetCreation/Exports/<Category>/` (helper: `AssetCreation/Blender/export_to_asset_creation.py`).
2. **unrealMCP** — `execute_python_script("batch_import_asset_creation.py")` to import into `/Game/HomeWorld/...`.

Full preset and style: [AssetCreation/STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md). Workflow overview: [AssetCreation/README.md](../../AssetCreation/README.md).

### Troubleshooting (Blender)

| Issue | Fix |
|-------|-----|
| Cursor stuck **Connecting** | You are almost certainly running **PyPI `uvx blender-mcp`** against the **Lab addon**. Switch `command` to `blender-mcp.exe` from `uv tool install …#subdirectory=mcp`. Kill leftover `blender-mcp` / `python …blender-mcp` processes, Stop/Start the bridge in Blender, toggle the Cursor server. |
| Lab addon “Online access must be enabled” | Enable online access in Blender system preferences (required for the Lab socket server). |
| TCP 9876 listens but tools hang | Confirm you are on Lab protocol (null-byte JSON). A quick probe that returns scene objects means the addon is healthy; the Cursor-side binary was wrong. |
| `spawn … ENOENT` | Use the full path to `blender-mcp.exe` under `%USERPROFILE%\.local\bin\`. |
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

External LLMs can generate Python that is then run via MCP (`execute_python_script`) or via the Editor (Tools → Execute Python Script). Conventions, example prompts, and a sample script are in [EXTERNAL_AI_AUTOMATION.md](EXTERNAL_AI_AUTOMATION.md). Always review generated code before running.

## Troubleshooting

| Issue | Fix |
|---|---|
| MCP tools don't appear in Cursor | Restart Cursor after adding/changing `.cursor/mcp.json`; ensure `uv` is on PATH; copy from `.cursor/mcp.json.example` if the live file is missing |
| "Connection refused" | Ensure the Editor is open with the UnrealMCP plugin enabled; check Output Log for errors |
| Python version error | Requires Python 3.10+; check with `python --version` |
| Plugin compilation failure on UE 5.7 | Switch to UnrealMCPBridge fallback (see above) |
| `uv` not found | Run the install script or add `C:\Users\<user>\.local\bin` to PATH |
| Blender MCP missing / ENOENT / stuck Connecting | See [Blender MCP](#blender-mcp-official-blender-lab--blender-51); use Lab `blender-mcp.exe`, not PyPI `uvx blender-mcp` |
